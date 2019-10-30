###########################################################################
#
#  Copyright 2019 Google Inc.
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

    A. Specify credentials on command line ( highest priority if given )
       --user / -u = user credentials path
       --client / -c = client credentials path ( requires user credentials path )
       --service / -s = service credentials path

    B. Define credentials paths in JSON ( overruled by command line )
       In each json file create the following entry ( client, or user, or service )

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
       If neither the json not the command line provides a path, the environmental 
       variable GOOGLE_APPLICATION_CREDENTIALS will be used for service accounts.  
       It is created by google cloud utilities.
"""


import os
import re
import json
import pytz
import uuid
import argparse

from datetime import datetime 
from importlib import import_module

from starthinker.util.debug import starthinker_trace_start

RE_UUID = re.compile(r'(\s*)("setup"\s*:\s*{)')


def get_project(filepath, debug=False):
  """Loads json for Project Class.  Intended for this module only. Available as helper.

     Able to load JSON with newlines ( strips all newlines before load ).

     Args:
      - filepath: (string) The local file path to the recipe json file to load.
      - debug: (boolean) If true, newlines are not stripped to correctly identify error line numbers.

     Returns:
      Json of recipe file.
  """

  with open(filepath) as data_file:
    data = data_file.read()
    if not debug: data = data.replace('\n', ' ')
    return json.loads(data)


def utc_to_timezone(timestamp, timezone):
  if timestamp: return timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
  else: return None


def is_scheduled(recipe, task = {}):
  """Wrapper for day_hour_scheduled that returns True if current time zone safe hour is in recipe schedule.

     Used as a helper for any cron job running projects.  Keeping this logic in project
     helps avoid time zone detection issues and scheduling discrepencies between machines.

    Args:
      - recipe: (Recipe JSON) The JSON of a recipe.
      - task: ( dictionary / JSON ) The specific task being considered for execution.

    Returns:
      - True if task is scheduled to run current hour, else False.
  """

  tz = pytz.timezone(recipe.get('setup', {}).get('timezone', 'America/Los_Angeles'))
  now_tz = datetime.now(tz)
  day_tz = now_tz.strftime('%a')
  hour_tz = now_tz.hour

  days = recipe.get('setup', {}).get('day', [])
  hours = [int(h) for h in task.get('hour', recipe.get('setup', {}).get('hour', []))]

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
      parser.add_argument('custom', help='custom parameter to be added to standard project set.')

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

      project.initialize(_recipe=var_recipe, _user=var_user, _service=var_service, _verbose=True)
    ```

  Attributes:
    
    Dealing with authentication...
      - project: (string) The Google Cloud project id.
      - user: (string) Path to the user credentials json file.  It can also be a Google Cloud Bucket path when passed to the class directly.
      - service: (string) Path to the service credentials json file.  It can also be a json object when passed to the project class directly.
      - client: (string) Path to the client credentials json file.  It can only be a local path.

    Dealing with execution data...
      - instance: (integer) When executing all tasks, it is the one based index offset of the task to run.
      - date: (date) A specific date or 'TODAY', which is changed to today's date, passed to python scripts for reference.
      - hour: (integer) When executing all tasks, it is the hour if spefified for a task to execute.

    Dealing with debugging...
      - verbose: (boolean) Prints all debug information in StarThinker code.  See: if project.verbose: print '...'.
      - force: (boolean) For recipes with specific task hours, forces all tasks to run regardless of hour specified.
  """

  args = None
  verbose = False
  filepath = None
  task = None
  date = None

  @classmethod
  def from_commandline(cls, _task = None, parser = None):
    """Used in StarThinker scripts as entry point for command line calls. Loads json for execution.

    Usage example:

    ```
    import argparse
    from starthinker.util.project import project

    if __name__ == "__main__":

      # custom parameters
      parser = argparse.ArgumentParser()
      parser.add_argument('custom', help='custom parameter to be added to standard project set.')

      # initialize project
      project.from_commandline(parser=parser)

      # access arguments
      auth = 'service' if project.args.service else 'user'
      print(project.args.custom)
    ```

    Args:
      - parser: (ArgumentParser) optional custom argument parser ( json argument becomes optional if not None )

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.* result in the same object.

    """

    if parser is None:
      parser = argparse.ArgumentParser()
      parser.add_argument('json', help='path to recipe json file to load')
    else:
      parser.add_argument('--json', '-j', help='path to recipe json file to load')

    parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
    parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
    parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
    parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

    parser.add_argument('--instance', '-i', help='the instance of the task to run ( for tasks with same name ), default is 1.', default=1, type=int)
    parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
    parser.add_argument('--hour', '-t', help='0 - 23 hour for which tasks will be executed', default='NOW')

    parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
    parser.add_argument('--force', '-force', help='no-op for compatibility with all.', action='store_true')

    parser.add_argument('--trace_print', '-tp', help='Simplified execution trace of the program written to stdout.', action='store_true')
    parser.add_argument('--trace_file', '-tf', help='Simplified execution trace of the program written to file.', action='store_true')

    cls.args = parser.parse_args()

    # initialize the project singleton with passed in parameters
    cls.initialize(
      get_project(cls.args.json) if cls.args.json else {},
      _task,
      cls.args.instance,
      cls.args.project,
      cls.args.user,
      cls.args.service,
      cls.args.client,
      cls.args.json,
      cls.args.date,
      cls.args.hour,
      cls.args.verbose,
      cls.args.force,
      cls.args.trace_print,
      cls.args.trace_file
    )

  recipe = None
  verbose = None
  filepath = None
  instance = None
  function = None
  task = None

  
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
    cls.task = None if i is None else next(iter(cls.recipe['tasks'][i].values()))
    return cls.task


  @classmethod
  def set_task(cls, function, parameters):
    if cls.task is None: 
      cls.recipe['tasks'].append({ function:parameters })
      cls.function = function
      cls.task = parameters
      cls.instance = 1
    else: 
      i = cls.get_task_index()
      cls.recipe['tasks'][i] = { function:parameters }
      cls.function = function
      cls.task = parameters
      cls.instance = sum([1 for c, t in enumerate(cls.recipe['tasks']) if t == function and c <= i])


  @staticmethod
  def from_parameters(func):
    """Initializes a project singleton for execution by a task.
    
    Either loads parameters (recipe, instance) passed to task programatically,
    or if no parameters passed attmepts to load them from the command line. 
    Uses decorator pattern, task name is inferred from function ebing decorated.

    Args:
      - recipe: (dict) JSON object representing the project ( setup plus at least one task )
      - instance: (integer) numeric offset of task to run if multiple calls to thsi task exist
 
    """

    def from_parameters_wrapper(recipe=None, instance=1):
      if recipe: project.initialize(_recipe=recipe, _task=func.__name__, _instance=instance)
      else: project.from_commandline(func.__name__)
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
    _date='TODAY',
    _hour='NOW',
    _verbose=False,
    _force=False,
    _trace_print=False,
    _trace_file=False
  ):
    """Used in StarThinker scripts as programmatic entry point. 

    Set up the project singleton for execution of a task, be sure to mimic defaults in helper
    this function loads credentials from various source ( command line argument, json, default credentials )
    it also sets up time zone aware date and various helper flags such as force and verbose.

    Usage example:
    ```
       from starthinker.util.project import project

       if __name__ == "__main__":
         user = 'user.json'
         service = 'service.json' 
         recipe = {'setup':..., 'tasks':.... }
         project.initialize(_recipe=recipe, _user=user, _service=service, _verbose=True)
    ```

    Args:
      - _recipe: (dict) JSON object representing the project ( setup plus at least one task )
      - _task: (string) Task name form recipe json task list to execute.
      - _instance: (integer) See module description.
      - _project: (string) See module description.
      - _user: (string) See module description.
      - _service: (string) See module description.
      - _client: (string) See module description.
      - _date: (date) See module description.
      - _hour: (integer) See module description.
      - _verbose: (boolean) See module description.
      - _force: (boolean) See module description.
      - _trace_print: (boolean) True if writing execution trace to stdout.
      - _trace_file: (boolean) True if writing execution trace to file ( see config.py ).

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.* result in the same object.
    """

    starthinker_trace_start(_trace_print, _trace_file)

    cls.recipe = _recipe
    cls.function = _task
    cls.instance = _instance

    # populates the task variable based on function and instance
    cls.get_task()

    cls.verbose = _verbose
    cls.filepath = _filepath

    # add setup to json if not provided and loads command line credentials if given
    if 'setup' not in cls.recipe: cls.recipe['setup'] = {}
    if 'auth' not in cls.recipe['setup']: cls.recipe['setup']['auth'] = {}
    if _project: cls.recipe['setup']['id'] = _project
    if _service: cls.recipe['setup']['auth']['service'] = _service
    if _client: cls.recipe['setup']['auth']['client'] = _client
    # if user explicity specified by command line
    if _user: 
      cls.recipe['setup']['auth']['user'] = _user
    # or if user not give, then try default credentials ( disabled security risk to assume on behalf of recipe )
    #elif not cls.recipe['setup']['auth'].get('user'): 
    #  cls.recipe['setup']['auth']['user'] = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

    cls.id = cls.recipe['setup'].get('id')
    cls.uuid = cls.recipe['setup'].get('uuid')

    # find date based on timezone
    if _date == 'TODAY':
      tz = pytz.timezone(cls.recipe['setup'].get('timezone', 'America/Los_Angeles'))
      tz_datetime = datetime.now(tz)
      cls.date = tz_datetime.date()
      cls.hour = tz_datetime.hour if _hour == 'NOW' else int(_hour)

    # or if provided use local time
    else:
      cls.date = datetime.strptime(_date.replace('/', '-').replace('_', '-'), '%Y-%m-%d').date()
      cls.hour = datetime.now().hour if _hour == 'NOW' else int(_hour)

    if cls.verbose:
      print('TASK:', _task) 
      print('DATE:', cls.date) 
      print('HOUR:', cls.hour) 


  @classmethod
  def get_uuid(cls):
    """Helper for deploying to pub/sub.  Injects a UUID into the current project's json file.

    The project's underlying recipe json file is modified by this call and needs to be read / write.

    Returns:
      UUID, and changes underlying json recipe file.
    """

    # set uid
    if not cls.uuid: 
      cls.uuid = str(uuid.uuid4())

      # write to file if path defined
      if cls.filepath:
        with open(cls.filepath, 'r') as json_file: filedata = json_file.read()
        filedata = RE_UUID.sub(r'\1\2\1  "uuid":"%s",' % cls.uuid, filedata)
        with open(cls.filepath, 'w') as json_file: json_file.write(filedata)
        cls.recipe = get_project(cls.filepath)

    return cls.uuid 


  @classmethod
  def execute(cls):
    '''Run all the tasks in a project in one sequence.

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

      project.initialize(_recipe=var_recipe, _user=var_user, _service=var_service, _verbose=True)
      project.execute()
    ```

    For a full list of tasks see: starthinker/gtech/script_*.json

    '''

    instances = {}
    for task in cls.recipe['tasks']:
      function = next(iter(task.keys()))
      #function = task.items()[0][0]

      # count instance per task
      instances.setdefault(function, 0)
      instances[function] += 1

      print('Running:', '%s %d' % (function, instances[function]))

      python_callable = getattr(import_module('starthinker.task.%s.run' % function), function)
      python_callable(cls.recipe, instances[function])
