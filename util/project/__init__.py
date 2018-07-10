###########################################################################
#
#  Copyright 2017 Google Inc.
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


RE_UUID = re.compile(r'(\s*)("setup"\s*:\s*{)')


def get_project(filepath):
  """Loads json for Project Class.  Intended for this module only. Available as helper.

    Args:
      filepath: (string) The local file path to the recipe json file to load.

    Returns:
      Json of recipe file.
    """

  with open(filepath) as data_file:
    return json.load(data_file)


def is_scheduled(project, task = None):
  """Determines if given tasks is executing this hour in a time zone safe way. 

     Used as a helper for any cron job running projects.  Keeping this logic in project
     helps avoid time zone detection issues and scheduling discrepencies between machines.

    Args:
      project: (Project Class) The instance of the project being evaluated ( not sure this is required ).
      task: ( dictionary / JSON ) The specific task being considered for execution.

    Returns:
      Task is scheduled for exection this hour ias True / False. 
    """

  if not 'hour' in project.get('setup', {}):
    return True

  tz = pytz.timezone(project['setup'].get('timezone', 'America/Los_Angeles'))
  tz_datetime = datetime.now(tz)
  tz_day, tz_hour =  tz_datetime.strftime('%a'), tz_datetime.hour
  if task:
    hours = [int(i) for i in task.get('hour', project['setup']['hour'])]
    return tz_day in project['setup'].get('day', project['setup'].get('week', [])) and tz_hour in hours
  else:
    return tz_day in project['setup'].get('day', project['setup'].get('week', [])) and tz_hour in project['setup']['hour']


class project:
  """A singleton that represents the loaded recipe within python scripts.

  All access to json scripts within StarThinker must pass through the project
  class.  It handles parameters, time zones, permissions management, and 
  scheduling overhead.

  Project is meant as the entry point into all StarThinker scripts as follows:

    from util.project import project

    def task():
      pass # execute work using project.* as data from json

    if __name__ == "__main__":
      project.load('task')
      task()

  Project is meant to be used by a helper.

    import argparse
    from util.project import project

    if __name__ == "__main__":

      # custom parameters
      parser = argparse.ArgumentParser()
      parser.add_argument('custom', help='custom parameter to be added to standard project set.')

      # initialize project
      project.load(parser=parser)

      # access arguments
      auth = 'service' if project.args.service else 'user'
      print project.args.custom

  Project can also be initialized directly for non-json tasks:

    from util.project import project

    if __name__ == "__main__":
      var_json = '/somepath/recipe.json'
      var_user = '/somepath/user.json'
      var_service = '/somepath/service.json'

      project.initialize(_json=var_json, _user=var_user, _service=var_service, _verbose=True)

  Attributes:
    
    Dealing with authentication...
      project: (string) The Google Cloud project id.
      user: (string) Path to the user credentials json file.  It can also be a Google Cloud Bucket path when passed to the class directly.
      service: (string) Path to the service credentials json file.  It can also be a json object when passed to the project class directly.
      client: (string) Path to the client credentials json file.  It can only be a local path.

    Dealing with execution data...
      instance: (integer) When executing all tasks, it is the one based index offset of the task to run.
      date: (date) A specific date or 'TODAY', which is changed to today's date, passed to python scripts for reference.
      hour: (integer) When executing all tasks, it is the hour if spefified for a task to execute.

    Dealing with debugging...
      verbose: (boolean) Prints all debug information in StarThinker code.  See: if project.verbose: print '...'.
      force: (boolean) For recipes with specific task hours, forces all tasks to run regardless of hour specified.
  """

  args = None
  verbose = False
  filepath = None
  task = None
  date = None

  @classmethod
  def load(cls, _task = None, parser = None):
    """Used in StarThinker scripts as entry point for command line calls. Loads json for execution.

       Usage example:

         from util.project import project

         def task():
           pass # execute work using project.* as data from json

         if __name__ == "__main__":
           project.load('task')
           task()
    
    Args:
      task: (string) Name of task to execute, matching task in json, hard coded by calling script.
      parser: (ArgumentParser) optional custom argument parser ( json argument becomes optional if not None )

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.* result in the same object.

    """

    if parser is None:
      parser = argparse.ArgumentParser()
      parser.add_argument('json', help='path to tasks json file')
    else:
      parser.add_argument('--json', '-j', help='path to tasks json file')

    parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
    parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
    parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
    parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

    parser.add_argument('--instance', '-i', help='the instance of the task to run ( for tasks with same name ), default is 1.', default=1, type=int)
    parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
    parser.add_argument('--hour', '-t', help='0 - 23 hour for which tasks will be executed', default='NOW')

    parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
    parser.add_argument('--force', '-force', help='no-op for compatibility with all.', action='store_true')

    cls.args = parser.parse_args()

    # initialize the project singleton with passed in parameters
    cls.initialize(
      cls.args.json,
      _task,
      cls.args.instance,
      cls.args.project,
      cls.args.user,
      cls.args.service,
      cls.args.client,
      cls.args.date,
      cls.args.hour,
      cls.args.verbose,
      cls.args.force
    )

  # set up the project singleton for execution of a script ( usually called by helper ), be sure to mimic defaults in helper
  # this function loads credentials from various source ( command line argument, json, default credentials )
  # it also sets up time zone aware date and various helper flags such as force and verbose
  @classmethod
  def initialize(cls, 
    _json=None,
    _task=None,
    _instance=1,
    _project=None,
    _user=None,
    _service=None,
    _client=None,
    _date='TODAY',
    _hour='NOW',
    _verbose=False,
    _force=False
  ):
    """Used in StarThinker scripts as programmatic entry point. 

       Usage example:

       from util.project import project

       if __name__ == "__main__":
         client = 'project.json'
         user = 'user.json'
         service = 'service.json' 
         project.initialize(_json=json, _user=user, _service=service, _verbose=True)

    Args:
      _json: (string) Path to recipe json file with tasks and or auth block.
      _task: (string) Task name form recipe json task list to execute.
      _instance: (integer) See module description.
      _project: (string) See module description.
      _user: (string) See module description.
      _service: (string) See module description.
      _client: (string) See module description.
      _date: (date) See module description.
      _hour: (integer) See module description.
      _verbose: (boolean) See module description.
      _force: (boolean) See module description.

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.* result in the same object.
    """

    # json path is optional if using project purely to interact with libraries ( just auth purposes )
    cls.configuration = get_project(_json) if _json else {}
    cls.verbose = _verbose
    cls.filepath = _json

    # add setup to json if not provided and loads command line credentials if given
    if 'setup' not in cls.configuration: cls.configuration['setup'] = {}
    if 'auth' not in cls.configuration['setup']: cls.configuration['setup']['auth'] = {}
    if _project: cls.configuration['setup']['id'] = _project
    if _service: cls.configuration['setup']['auth']['service'] = _service
    if _client: cls.configuration['setup']['auth']['client'] = _client
    # if user explicity specified by command line
    if _user: 
      cls.configuration['setup']['auth']['user'] = _user
    # or if user not give, then try default credentials
    elif not cls.configuration['setup']['auth'].get('user'): 
      cls.configuration['setup']['auth']['user'] = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)

    cls.id = cls.configuration['setup'].get('id')
    cls.uuid = cls.configuration['setup'].get('uuid')

    # find date based on timezone
    if _date == 'TODAY':
      tz = pytz.timezone(cls.configuration['setup'].get('timezone', 'America/Los_Angeles'))
      tz_datetime = datetime.now(tz)
      cls.date = tz_datetime.date()
      cls.hour = tz_datetime.hour if _hour == 'NOW' else int(_hour)

    # or if provided use local time
    else:
      cls.date = datetime.strptime(_date.replace('/', '-').replace('_', '-'), '%Y-%m-%d').date()
      cls.hour = datetime.now().hour if _hour == 'NOW' else int(_hour)

    # find task
    cls.task = None
    instance = 0
    if _task:
      for task in cls.configuration['tasks']:
        # remove script meta if copied with task
        if 'script' in task: del task['script'] 
        # ensure every task as a version
        if 'version' not in task.values()[0]: task.values()[0]['version'] = 0.1
        # stop when the instance of a task is found
        if instance == _instance: break 
        # otherwise increment the instance
        elif task.keys()[0] == _task: 
          cls.set_task(task.values()[0])
          #cls.task = task.values()[0]
          instance += 1

    if cls.verbose:
      print 'TASK:', _task 
      print 'DATE:', cls.date 
      print 'HOUR:', cls.hour 


  @classmethod
  def set_task(cls, json_definition):
    """Helper for setting task json in a project.  not recommended, use load and initialize instead.

    Args:
      json_difinition (json) the json to use as a task   

    Returns:
      Project singleton instance.
    """

    cls.task = json_definition
    return cls


  @classmethod
  def get_uuid(cls):
    """Helper for deploying to pub/sub.  Injects a UUID into the current project's json file.

    The project's underlying recipe json file is modified by this call and needs to be read / write.

    Returns:
      UUID, and changes underlying json recipe file.
    """

    if cls.filepath and not cls.uuid:
      cls.uuid = str(uuid.uuid4())
      with open(cls.filepath, 'r') as json_file: filedata = json_file.read()
      filedata = RE_UUID.sub(r'\1\2\1  "uuid":"%s",' % cls.uuid, filedata)
      with open(cls.filepath, 'w') as json_file: json_file.write(filedata)
      cls.configuration = get_project(cls.filepath)
    return cls.uuid 
