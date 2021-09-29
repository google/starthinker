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
import json
import pytz
import argparse
import textwrap

from datetime import datetime
from importlib import import_module

from starthinker.util.debug import starthinker_trace_start

class Configuration:

  def __init__(
    self,
    recipe={},
    project=None,
    user=None,
    service=None,
    client=None,
    filepath=None,
    key=None,
    verbose=False,
    trace_print=False,
    trace_file=False,
  ):
    """Used in StarThinker scripts as programmatic entry point.

    Args:
      * recipe: (dict) JSON object representing the recipe
      * project: (string) See module description.
      * user: (string) See module description.
      * service: (string) See module description.
      * client: (string) See module description.
      * key: (string) See module description.
      * verbose: (boolean) See module description.
      * trace_print: (boolean) True if writing execution trace to stdout.
      * trace_file: (boolean) True if writing execution trace to file.
      * args: (dict) dictionary of arguments (used with argParse).

    Returns:
      Nothing.
    """

    starthinker_trace_start(trace_print, trace_file)

    self.recipe = recipe
    self.verbose = verbose
    self.filepath = filepath

    # add setup to json if not provided and loads command line credentials if given
    if 'setup' not in self.recipe:
      self.recipe['setup'] = {}
    if 'auth' not in self.recipe['setup']:
      self.recipe['setup']['auth'] = {}

    if service:
      self.recipe['setup']['auth']['service'] = service
    if client:
      self.recipe['setup']['auth']['client'] = client
    if user:
      self.recipe['setup']['auth']['user'] = user
    if project:
      self.recipe['setup']['id'] = project
    if key:
      self.recipe['setup']['key'] = key

    # TBD: if project id not given, use service credentials
    #elif not self.recipe['setup'].get('id') and self.recipe['setup']['auth'].get('service'):
    # TBD: if project id not given, use client credentials
    #elif not self.recipe['setup'].get('id') and self.recipe['setup']['auth'].get('client'):

    self.project = self.recipe['setup'].get('project', self.recipe['setup'].get('id'))
    self.key = self.recipe['setup'].get('key')

    # find date based on timezone
    self.timezone = pytz.timezone(
      self.recipe['setup'].get(
        'timezone',
        'America/Los_Angeles'
      )
    )
    self.now = datetime.now(self.timezone)
    self.date = self.now.date()
    self.hour = self.now.hour

    if self.verbose:
      print('DATE:', self.now.date())
      print('HOUR:', self.now.hour)


def commandline_parser(parser=None, arguments=None):
  """Used in StarThinker scripts as entry point for command line calls.

  Defines standard parameters used by almost every entry point.

  Usage example:

  ```
  import argparse
  from starthinker.util.configuration import commandline_parser

  if __name__ == "__main__":

    # custom parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('custom', help='custom parameter to be added.')

    # initialize project
    commandline_parser(parser=parser, ['-c', '-u'])

    # access arguments
    print(args.client)
  ```

  Args:
    * parser: (ArgumentParser) optional custom argument parser
    * arguments: (String) optional list of parameters to use when invoking, all set if None

  Returns:
    ArgumentParser - parser with added parameters

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

        Example: python run.py [path to recipe file]
        Caution: This script does NOT check if the last job finished, potentially causing overruns.
        Notes:
          - To avoid running the entire script when debugging a single task, the command line
            can easily replace "all" with the name of any "task" in the json.  For example
            python tool/recipe.py scripts/say_hello.json

          - Can be easily replaced with the following to run only the "hello" task:
            python task/hello/run.py scripts/say_hello.json

          - Or specified further to run only the second hello task:
            python task/hello/run.py scripts/say_hello.json -i 2

    """))

  if arguments is None:
    parser.add_argument('json', help='Path to recipe json file to load.')
  elif '-j' in arguments:
    parser.add_argument(
      '--json',
      '-j',
      help='Path to recipe json file to load.'
    )

  if arguments is None or '-p' in arguments:
    parser.add_argument(
      '--project',
      '-p',
      help='Cloud ID of Google Cloud Project.',
      default=None
    )

  if arguments is None or '-k' in arguments:
    parser.add_argument(
      '--key',
      '-k',
      help='API Key of Google Cloud Project.',
      default=None
    )

  if arguments is None or '-u' in arguments:
    parser.add_argument(
      '--user',
      '-u',
      help='Path to USER credentials json file.',
      default=None
    )

  if arguments is None or '-s' in arguments:
    parser.add_argument(
      '--service',
      '-s',
      help='Path to SERVICE credentials json file.',
      default=None
    )

  if arguments is None or '-c' in arguments:
    parser.add_argument(
      '--client',
      '-c',
      help='Path to CLIENT credentials json file.',
      default=None
    )

  if arguments is None or '-t' in arguments:
    parser.add_argument(
      '--task',
      '-t',
      help='Task number of the task to run starting at 1.',
      default=None,
      type=int
    )

  if arguments is None or '-v' in arguments:
    parser.add_argument(
      '--verbose',
      '-v',
      help='Print all the steps as they happen.',
      action='store_true'
    )

  if arguments is None or '-f' in arguments:
    parser.add_argument(
      '--force',
      '-force',
      help='Not used but included for compatiblity with another script.',
      action='store_true'
    )

  if arguments is None or '-tp' in arguments:
    parser.add_argument(
      '--trace_print',
      '-tp',
      help='Execution trace written to stdout.',
      action='store_true'
    )

  if arguments is None or '-tf' in arguments:
    parser.add_argument(
      '--trace_file',
      '-tf',
      help='Execution trace written to file.',
      action='store_true'
    )

  if arguments is None or '-ni' in arguments:
    parser.add_argument(
      '--no_input',
      '-ni',
      help='Raise exception if fields requiring input are in recipe.',
      action='store_true'
  )

  return parser


def is_scheduled(configuration, task={}):
  """Wrapper for day_hour_scheduled that returns True if current time zone safe hour is in recipe schedule.

     Used as a helper for any cron job running projects.  Keeping this logic in
     project
     helps avoid time zone detection issues and scheduling discrepencies between
     machines.

    Args:
      * recipe: (Recipe JSON) The JSON of a recipe.
      * task: ( dictionary / JSON ) The specific task being considered for execution.

    Returns:
      - True if task is scheduled to run current hour, else False.
  """

  days = configuration.recipe.get('setup', {}).get('day', [])
  hours = [
    int(h) for h in task.get(
      'hour', configuration.recipe.get('setup', {}).get('hour', [])
    )
  ]

  if days == [] or configuration.date.strftime('%a') in days:
    if hours == [] or configuration.hour in hours:
      return True

  return False


def execute(configuration, tasks, force=False, instance=None):
  """Run all the tasks in a project in one sequence.

  Imports and calls each task handler specified in the recpie.
  Passes the Configuration and task JSON to each handler.
  For a full list of tasks see: scripts/*.json

  Example:
  ```
    from starthinker.util.onfiguration import execute, Configuration

    if __name__ == "__main__":
      TASKS = [
        { "hello":{
          "auth":"user",
          "say":"Hello World"
        }},
        { "dataset":{
          "auth":"service",
          "dataset":"Test_Dataset"
        }}
      ]

      execute(
        config=Configuration(
          client='[CLIENT CREDENTIALS JSON STRING OR PATH]',
          user='[USER CREDENTIALS JSON STRING OR PATH]',
          service='[SERVICE CREDENTIALS JSON STRING OR PATH]',
          project='[GOOGLE CLOUD PROJECT ID]',
          verbose=True
        ),
        tasks=TASKS,
        force=True
      )
  ```

  Args:
    * configuration: (class) Crednetials wrapper.
    * tasks: (dict) JSON definition of each handler and its parameters.
    * force: (bool) Ignore any schedule settings if true, false by default.
    * instance (int) Sequential index of task to execute (one based index).

  Returns:
    None

  Raises:
    All possible exceptions that may occur in a recipe.
  """

  for sequence, task in enumerate(tasks):
    script, task = next(iter(task.items()))

    if instance and instance != sequence + 1:
      print('SKIPPING TASK #%d: %s - %s' % (sequence + 1, script, task.get('description', '')))
      continue
    else:
      print('RUNNING TASK #%d: %s - %s' % (sequence + 1, script, task.get('description', '')))

    if force or is_scheduled(configuration, task):
      python_callable = getattr(
        import_module('starthinker.task.%s.run' % script),
        script
      )
      python_callable(configuration, task)
    else:
      print(
        'Schedule Skipping: add --force to ignore schedule'
      )
