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

import os
import re
import json
import pytz
import argparse
from datetime import datetime, timedelta
import uuid


RE_UUID = re.compile(r'(\s*)("setup"\s*:\s*{)')


def get_project(filepath):
  with open(filepath) as data_file:
    return json.load(data_file)


def load_project(data):
  return json.load(data)


def is_scheduled(project, task = None):
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
  verbose = False
  filepath = None
  task = None
  date = None

  # helper for loading parameters from command line and/or json ( used by ruun scripts )
  @classmethod
  def load(cls, _task = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('json', help='path to tasks json file')

    parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
    parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
    parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
    parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

    parser.add_argument('--instance', '-i', help='the instance of the task to run ( for tasks with same name ), default is 1.', default=1, type=int)
    parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
    parser.add_argument('--hour', '-t', help='0 - 23 hour for which tasks will be executed', default='NOW')

    parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
    parser.add_argument('--force', '-force', help='no-op for compatibility with all.', action='store_true')

    args = parser.parse_args()

    # initialize the project singleton with passed in parameters
    cls.initialize(
      args.json,
      _task,
      args.instance,
      args.project,
      args.user,
      args.service,
      args.client,
      args.date,
      args.hour,
      args.verbose,
      args.force
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
          cls.task = task.values()[0]
          instance += 1

    if cls.verbose:
      print 'TASK:', _task 
      print 'DATE:', cls.date 
      print 'HOUR:', cls.hour 


  #@classmethod
  #def authorize(cls, project_path):
  #  cls.filepath = project_path
  #  cls.configuration = get_project(project_path)
  #  cls.verbose = True
  #  cls.date = 'TODAY'
  #  cls.id = cls.configuration['setup']['id']
  #  cls.uuid = cls.configuration['setup'].get('uuid')
  #  cls.task = {'auth':'user'}


  @classmethod
  def get_uuid(cls):
    if cls.filepath and not cls.uuid:
      cls.uuid = str(uuid.uuid4())
      with open(cls.filepath, 'r') as json_file: filedata = json_file.read()
      filedata = RE_UUID.sub(r'\1\2\1  "uuid":"%s",' % cls.uuid, filedata)
      with open(cls.filepath, 'w') as json_file: json_file.write(filedata)
      cls.configuration = get_project(cls.filepath)
    return cls.uuid 
