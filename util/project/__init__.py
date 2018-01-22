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
  if not 'hour' in project['setup']:
    return True

  tz = pytz.timezone(project['setup'].get('timezone', 'America/Los_Angeles'))
  tz_datetime = datetime.now(tz)
  tz_day, tz_hour =  tz_datetime.strftime('%a'), tz_datetime.hour
  if task:
    return tz_day in project['setup'].get('day', project['setup'].get('week', [])) and tz_hour in task.get('hour', project['setup']['hour'])
  else:
    return tz_day in project['setup'].get('day', project['setup'].get('week', [])) and tz_hour in project['setup']['hour']


class project:
  verbose = False
  filepath = None
  task = None
  date = None

  @classmethod
  def load(cls, _task = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('project', help='path to project json file')
    parser.add_argument('--instance', '-i', help='the instance of the task to run ( if multiple tasks with same name ) default will be 1.', default=1, type=int)
    parser.add_argument('--verbose', '-v', help='print all the steps as they happen.', action='store_true')
    parser.add_argument('--date', '-d', help='YYYY-MM-DD format date for which these reports are to be run, default will be today.', default='TODAY')
    parser.add_argument('--hour', '-t', help='0 - 23 hour for which tasks will be executed', default='NOW')
    parser.add_argument('--force', '-force', help='no-op for compatibility with all.', action='store_true')

    args = parser.parse_args()

    cls.filepath = args.project
    cls.configuration = get_project(args.project)
    cls.verbose = args.verbose
    cls.id = cls.configuration['setup']['id']
    cls.uuid = cls.configuration['setup'].get('uuid')

    # find date based on timezone
    if args.date == 'TODAY':
      tz = pytz.timezone(cls.configuration['setup'].get('timezone', 'America/Los_Angeles'))
      tz_datetime = datetime.now(tz)
      cls.date = tz_datetime.date()
      cls.hour = tz_datetime.hour if args.hour == 'NOW' else int(args.hour)

    # or if provided use local time
    else:
      cls.date = datetime.strptime(args.date.replace('/', '-').replace('_', '-'), '%Y-%m-%d').date()
      cls.hour = datetime.now().hour if args.hour == 'NOW' else int(args.hour)

    # find task
    cls.task = None
    instance = 0
    if _task:
      for task in cls.configuration['tasks']:
        if 'script' in task: del task['script'] # remove script meta used by ui
        if instance == args.instance: break # stop when the instance of a task is found
        if task.keys()[0] == _task: 
          cls.task = task.values()[0]
          instance += 1

    # create service credentials ( needed as this always gets loaded )
    #try: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cls.configuration['setup']['auth']['service']
    #except: pass

    if cls.verbose:
      print 'TASK:', _task 
      print 'DATE:', cls.date 
      print 'HOUR:', cls.hour 


  @classmethod
  def authorize(cls, project_path):
    cls.filepath = project_path
    cls.configuration = get_project(project_path)
    cls.verbose = True
    cls.date = 'TODAY'
    cls.id = cls.configuration['setup']['id']
    cls.uuid = cls.configuration['setup'].get('uuid')
    cls.task = {'auth':'user'}


  @classmethod
  def get_uuid(cls):
    if not cls.uuid:
      cls.uuid = str(uuid.uuid4())
      with open(cls.filepath, 'r') as json_file: filedata = json_file.read()
      filedata = RE_UUID.sub(r'\1\2\1  "uuid":"%s",' % cls.uuid, filedata)
      with open(cls.filepath, 'w') as json_file: json_file.write(filedata)
      cls.configuration = get_project(cls.filepath)
    return cls.uuid 
