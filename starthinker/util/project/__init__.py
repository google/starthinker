###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

"""The core singleton class of StarThinker that translates json to python.

Project loads JSON and parameters and combines them for execturion.  It handles
three important concepts:

  1. Load the JSON and make all task parameters available to python scripts.
  2. Load authentication, all three parameters are optional if scripts do not
     use them.  The following parameters can be passed for authentication.

    user.json - user credentials json ( generated from client ), is refreshed
                by StarThinker as required.  Can be provided as a local path
                or a Cloud Bucket Storage path for distributed jobs.

    service.json - service credentials json ( generated from cloud project ).
                   Passed as a local path or an embedded json object for
                   distributed jobs.

    client.json - client credentials json ( generated from cloud project ).
                  Also require a user json path which will be written to after
                  client authnetication.  Once authenticated this client is not
                  required.

    Credentials can be specified in one of three ways for maximum flexibility:

    A. Specify credentials on command line (highest priority if given)
       --user / -u = user credentials path
       --client / -c = client credentials path (requires user credentials path)
       --service / -s = service credentials path

    B. Define credentials paths in JSON (overruled by command line)
       In each json file create the following entry (client, or user, or
       service)

         ```
         {
           "setup":{
             "id":"[cloud project id]",
             "auth":{
               "client":"[/home/.credentials/hello-world_client.json]",
               "service":"[/home/.credentials/hello-world_service.json]",
               "user":"[/home/.credentials/hello-world_user.json]"
             }
          },
         }
         ```

    C. Use default credentials ( lowest priority, last resort )
       If neither the json not the command line provides a path, the
       environmental variable GOOGLE_APPLICATION_CREDENTIALS will be
       used for service accounts.  It is created by google cloud
       utilities.
"""

import os
import re
import json
import pytz
import argparse
import textwrap

from datetime import datetime
from importlib import import_module

from starthinker.util.debug import starthinker_trace_start


EXIT_ERROR = 1
EXIT_SUCCESS = 0
RE_UUID = re.compile(r'(\s*)("setup"\s*:\s*{)')


def get_project(filepath=None, stringcontent=None):
  """Loads json for Project Class.  Available as helper.

    Able to load JSON with newlines ( strips all newlines before load ).

    Args:
     - filepath: (string) The local file path to the recipe json file to load.

    Returns:
     Json of recipe file.
  """

  if filepath:
    with open(filepath) as recipe_file:
      stringcontent = recipe_file.read()

  try:
    # allow the json to contain newlines for formatting queries and such
    return json.loads(stringcontent.replace('\n', ' '))
  except ValueError as e:
    pos = 0
    for count, line in enumerate(stringcontent.splitlines(), 1):
      # do not add newlines, e.pos was run on a version where newlines were removed
      pos += len(line)
      if pos >= e.pos:
        e.lineno = count
        e.pos = pos
        e.args = (
          'JSON ERROR: %s LINE: %s CHARACTER: %s ERROR: %s LINE: %s' %
          (filepath, count, pos - e.pos, str(e.msg), line.strip()),
        )
        raise


def utc_to_timezone(timestamp, timezone):
  if timestamp:
    return timestamp.replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone(timezone))
  else:
    return None


def is_scheduled(recipe, task={}):
  """Wrapper for day_hour_scheduled that returns True if current time zone safe hour is in recipe schedule.

     Used as a helper for any cron job running projects.  Keeping this logic in
     project
     helps avoid time zone detection issues and scheduling discrepencies between
     machines.

    Args:
      - recipe: (Recipe JSON) The JSON of a recipe.
      - task: ( dictionary / JSON ) The specific task being considered for
        execution.

    Returns:
      - True if task is scheduled to run current hour, else False.
  """

  tz = pytz.timezone(
    recipe.get('setup', {}).get('timezone', 'America/Los_Angeles')
  )
  now_tz = datetime.now(tz)
  day_tz = now_tz.strftime('%a')
  hour_tz = now_tz.hour

  days = recipe.get('setup', {}).get('day', [])
  hours = [
    int(h) for h in task.get(
      'hour', recipe.get('setup', {}).get('hour', [])
    )
  ]

  if days == [] or day_tz in days:
    if hours == [] or hour_tz in hours:
      return True

  return False


class project:
  """A singleton that represents the loaded recipe within python scripts.

  All access to json scripts within StarThinker must pass through the project
  class.  It handles parameters, time zones, permissions management, and
  scheduling overhead. Task function name must match JSON task name.

  Project is meant as the entry point into all StarThinker scripts as follows:

    ```
    from starthinker.util.project import project

    @project.from_parameters
    def task():
      pass # execute work using project.* as data from json

    if __name__ == "__main__":
      task()
    ```

  Project is meant to be used by a helper.

    ```
    import argparse
    from starthinker.util.project import project

    if __name__ == "__main__":

      # custom parameters
      parser = argparse.ArgumentParser()
      parser.add_argument('custom', help='custom parameter to be added to
      standard project set.')

      # initialize project
      project.from_commandline(parser=parser)

      # access arguments
      auth = 'service' if project.args.service else 'user'
      print(project.args.custom)
    ```

  Project can also be initialized directly for non-json tasks:

    ```
    from starthinker.util.project import project

    if __name__ == "__main__":
      var_recipe = '/somepath/recipe.json'
      var_user = '/somepath/user.json'
      var_service = '/somepath/service.json'

      project.initialize(_recipe=var_recipe, _user=var_user,
      _service=var_service, _verbose=True)
    ```

  Attributes:  Dealing with authentication...
      - project: (string) The Google Cloud project id.
      - user: (string) Path to the user credentials json file.  It can also be a
      Google Cloud Bucket path when passed to the class directly.
      - service: (string) Path to the service credentials json file.  It can
      also be a json object when passed to the project class directly.
      - client: (string) Path to the client credentials json file.  It can only
      be a local path.  Dealing with execution data...
      - instance: (integer) When executing all tasks, it is the one based index
      offset of the task to run.
      - date: (date) A specific date or 'TODAY', which is changed to today's
      date, passed to python scripts for reference.
      - hour: (integer) When executing all tasks, it is the hour if spefified
      for a task to execute.  Dealing with debugging...
      - verbose: (boolean) Prints all debug information in StarThinker code.
      See: if project.verbose: print '...'.
      - force: (boolean) For recipes with specific task hours, forces all tasks
      to run regardless of hour specified.
  """

  args = None
  recipe = None
  task = None
  instance = None
  filepath = None
  verbose = False
  force = False
  function = None
  timezone = None
  now = None
  date = None
  hour = None


  @classmethod
  def from_commandline(cls, _task=None, parser=None, arguments=None):
    """Used in StarThinker scripts as entry point for command line calls.

    Loads json for execution.

    Usage example:

    ```
    import argparse
    from starthinker.util.project import project

    if __name__ == "__main__":

      # custom parameters
      parser = argparse.ArgumentParser()
      parser.add_argument('custom', help='custom parameter to be added to
      standard project set.')

      # initialize project
      project.from_commandline(parser=parser)

      # access arguments
      auth = 'service' if project.args.service else 'user'
      print(project.args.custom)
    ```

    Args:
      - parser: (ArgumentParser) optional custom argument parser ( json argument
        becomes optional if not None )
      - arguments: (String) optional list of parameters to use when invoking
        project ( defaults to ALL if set to None )

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.*
      result in the same object.

    """

    if parser is None:
      parser = argparse.ArgumentParser(
          formatter_class=argparse.RawDescriptionHelpFormatter,
          description=textwrap.dedent("""\
          Command line to execute all tasks in a recipe once. ( Common Entry Point )

          This script dispatches all the tasks in a JSON recipe to handlers in sequence.
          For each task, it calls a subprocess to execute the JSON instructions, waits
          for the process to complete and dispatches the next task, until all tasks are
          complete or a critical failure ( exception ) is raised.

          If an exception is raised in any task, all following tasks are not executed by design.

          Example: python run.py [path to recipe file] --force
          Caution: This script does NOT check if the last job finished, potentially causing overruns.
          Notes:
            - To avoid running the entire script when debugging a single task, the command line
              can easily replace "all" with the name of any "task" in the json.  For example
              python all/run.py project/sample/say_hello.json

            - Can be easily replaced with the following to run only the "hello" task:
              python task/hello/run.py project/sample/say_hello.json

            - Or specified further to run only the second hello task:
              python task/hello/run.py project/sample/say_hello.json -i 2

      """))
      if arguments is None or '-j' in arguments:
        parser.add_argument('json', help='Path to recipe json file to load.')
    else:
      if arguments is None or '-j' in arguments:
        parser.add_argument(
            '--json', '-j', help='Path to recipe json file to load.')

    if arguments is None or '-p' in arguments:
      parser.add_argument(
          '--project',
          '-p',
          help='Cloud ID of Google Cloud Project.',
          default=None)
    if arguments is None or '-k' in arguments:
      parser.add_argument(
          '--key',
          '-k',
          help='API Key of Google Cloud Project.',
          default=None)
    if arguments is None or '-u' in arguments:
      parser.add_argument(
          '--user',
          '-u',
          help='Path to USER credentials json file.',
          default=None)
    if arguments is None or '-s' in arguments:
      parser.add_argument(
          '--service',
          '-s',
          help='Path to SERVICE credentials json file.',
          default=None)
    if arguments is None or '-c' in arguments:
      parser.add_argument(
          '--client',
          '-c',
          help='Path to CLIENT credentials json file.',
          default=None)

    if arguments is None or '-i' in arguments:
      parser.add_argument(
          '--instance',
          '-i',
          help='Instance number of the task to run ( for tasks with same name ) starting at 1.',
          default=1,
          type=int)

    if arguments is None or '-v' in arguments:
      parser.add_argument(
          '--verbose',
          '-v',
          help='Print all the steps as they happen.',
          action='store_true')
    if arguments is None or '-f' in arguments:
      parser.add_argument(
          '--force',
          '-force',
          help='Not used but included for compatiblity with another script.',
          action='store_true')

    if arguments is None or '-tp' in arguments:
      parser.add_argument(
          '--trace_print',
          '-tp',
          help='Execution trace written to stdout.',
          action='store_true')
    if arguments is None or '-tf' in arguments:
      parser.add_argument(
          '--trace_file',
          '-tf',
          help='Execution trace written to file.',
          action='store_true')

    cls.args = parser.parse_args()

    # initialize the project singleton with passed in parameters
    cls.initialize(
        get_project(cls.args.json) if hasattr(cls.args, 'json') else {},
        _task,
        getattr(cls.args, 'instance', None),
        getattr(cls.args, 'project', None),
        getattr(cls.args, 'user', None),
        getattr(cls.args, 'service', None),
        getattr(cls.args, 'client', None),
        getattr(cls.args, 'json', None),
        getattr(cls.args, 'key', None),
        getattr(cls.args, 'verbose', None),
        getattr(cls.args, 'force', None),
        getattr(cls.args, 'trace_print', None),
        getattr(cls.args, 'trace_file', None)
    )


  @classmethod
  def get_task_index(cls):
    i = 0
    for c, t in enumerate(cls.recipe.get('tasks', [])):
      if next(iter(t.keys())) == cls.function:
        i += 1
        if i == cls.instance:
          return c
    return None


  @classmethod
  def get_task(cls):
    #if cls.task is None:
    i = cls.get_task_index()
    cls.task = None if i is None else next(
        iter(cls.recipe['tasks'][i].values()))
    return cls.task


  @classmethod
  def set_task(cls, function, parameters):
    if cls.task is None:
      cls.recipe['tasks'].append({function: parameters})
      cls.function = function
      cls.task = parameters
      cls.instance = 1
    else:
      i = cls.get_task_index()
      cls.recipe['tasks'][i] = {function: parameters}
      cls.function = function
      cls.task = parameters
      cls.instance = sum([
          1 for c, t in enumerate(cls.recipe['tasks'])
          if t == function and c <= i
      ])

  @staticmethod
  def from_parameters(func):
    """Initializes a project singleton for execution by a task.

    Either loads parameters (recipe, instance) passed to task programatically,
    or if no parameters passed attmepts to load them from the command line.
    Uses decorator pattern, task name is inferred from function ebing decorated.

    Args:
      - recipe: (dict) JSON object representing the project ( setup plus at
        least one task )
      - instance: (integer) numeric offset of task to run if multiple calls to
        thsi task exist
    """

    def from_parameters_wrapper(recipe=None, instance=1):
      if recipe:
        project.initialize(
            _recipe=recipe, _task=func.__name__, _instance=instance)
      else:
        project.from_commandline(func.__name__)
      func()

    return from_parameters_wrapper


  @classmethod
  def initialize(cls,
                 _recipe={},
                 _task=None,
                 _instance=1,
                 _project=None,
                 _user=None,
                 _service=None,
                 _client=None,
                 _filepath=None,
                 _key=None,
                 _verbose=False,
                 _force=False,
                 _trace_print=False,
                 _trace_file=False):
    """Used in StarThinker scripts as programmatic entry point.

    Set up the project singleton for execution of a task, be sure to mimic
    defaults in helper
    this function loads credentials from various source ( command line argument,
    json, default credentials )
    it also sets up time zone aware date and various helper flags such as force
    and verbose.

    Usage example:
    ```
       from starthinker.util.project import project

       if __name__ == "__main__":
         user = 'user.json'
         service = 'service.json'
         recipe = {'setup':..., 'tasks':.... }
         project.initialize(
           _recipe=recipe,
           _user=user,
           _service=service,
           _verbose=True
         )
    ```

    Args:
      - _recipe: (dict) JSON object representing the project ( setup plus at
        least one task )
      - _task: (string) Task name form recipe json task list to execute.
      - _instance: (integer) See module description.
      - _project: (string) See module description.
      - _user: (string) See module description.
      - _service: (string) See module description.
      - _client: (string) See module description.
      - _key: (string) See module description.
      - _verbose: (boolean) See module description.
      - _force: (boolean) See module description.
      - _trace_print: (boolean) True if writing execution trace to stdout.
      - _trace_file: (boolean) True if writing execution trace to file ( see
        config.py ).

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.*
      result in the same object.
    """

    starthinker_trace_start(_trace_print, _trace_file)

    cls.recipe = _recipe
    cls.function = _task
    cls.instance = _instance
    cls.force = _force

    # populates the task variable based on function and instance
    cls.get_task()

    cls.verbose = _verbose
    cls.filepath = _filepath

    # add setup to json if not provided and loads command line credentials if given
    if 'setup' not in cls.recipe:
      cls.recipe['setup'] = {}
    if 'auth' not in cls.recipe['setup']:
      cls.recipe['setup']['auth'] = {}
    if _service:
      cls.recipe['setup']['auth']['service'] = _service
    if _client:
      cls.recipe['setup']['auth']['client'] = _client
    # if user explicity specified by command line
    if _user:
      cls.recipe['setup']['auth']['user'] = _user
    # or if user not given, then try default credentials ( disabled security risk to assume on behalf of recipe )
    #elif not cls.recipe['setup']['auth'].get('user'):
    #  cls.recipe['setup']['auth']['user'] = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

    # if project id given, use it
    if _project:
      cls.recipe['setup']['id'] = _project

    if _key:
      cls.recipe['setup']['key'] = _key

    # TBD: if project id not given, use service credentials
    #elif not cls.recipe['setup'].get('id') and cls.recipe['setup']['auth'].get('service'):
    # TBD: if project id not given, use client credentials
    #elif not cls.recipe['setup'].get('id') and cls.recipe['setup']['auth'].get('client'):

    cls.id = cls.recipe['setup'].get('id')
    cls.key = cls.recipe['setup'].get('key')

    # find date based on timezone
    cls.timezone = pytz.timezone(
      cls.recipe['setup'].get(
        'timezone',
        'America/Los_Angeles'
      )
    )
    cls.now = datetime.now(cls.timezone)
    cls.date = cls.now.date()
    cls.hour = cls.now.hour

    if cls.verbose:
      print('TASK:', _task or 'all')
      print('DATE:', cls.now.date())
      print('HOUR:', cls.now.hour)


  @classmethod
  def execute(cls, _force=False):
    """Run all the tasks in a project in one sequence.

    ```
    from starthinker.util.project import project

    if __name__ == "__main__":
      var_user = '[USER CREDENTIALS JSON STRING OR PATH]'
      var_service = '[SERVICE CREDENTIALS JSON STRING OR PATH]'
      var_recipe = {
        "tasks":[
          { "dataset":{
            "auth":"service",
            "dataset":"Test_Dataset"
          }}
        ]
      }

      project.initialize(
        _recipe=var_recipe,
        _user=var_user,
        _service=var_service,
        _verbose=True
      )
      project.execute()
    ```

    For a full list of tasks see: scripts/*.json

    """

    returncode = EXIT_SUCCESS
    instances = {}
    for task in cls.recipe['tasks']:
      script, task = next(iter(task.items()))

      # count instance per task
      instances.setdefault(script, 0)
      instances[script] += 1

      print('RUNNING TASK:', '%s %d' % (script, instances[script]))

      if _force or cls.force or is_scheduled(cls.recipe, task):
        try:
          python_callable = getattr(
            import_module('starthinker.task.%s.run' % script),
            script
          )
          python_callable(cls.recipe, instances[script])
        except Exception as e:
          print(str(e))
          returncode = EXIT_ERROR
      else:
        print(
          'Schedule Skipping: add --force to ignore schedule or run specific task handler'
        )

    return returncode
