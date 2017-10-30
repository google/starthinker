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
import argparse
from datetime import timedelta
import uuid

from util.regexp import str_to_date

RE_UUID = re.compile(r'(\s*)("setup"\s*:\s*{)')

def get_project(filepath):
  with open(filepath) as data_file:    
    return json.load(data_file)

def load_project(data):
  return json.load(data)

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
    args = parser.parse_args()

    cls.filepath = args.project
    cls.configuration = get_project(args.project)
    cls.verbose = args.verbose
    cls.date = str_to_date(args.date)
    cls.id = cls.configuration['setup']['id']
    cls.uuid = cls.configuration['setup'].get('uuid')

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


  @classmethod
  def authorize(cls, _credetials):
    cls.configuration = {
      "setup":{
        "auth":{
          "client":"/usr/local/google/home/kenjora/.credentials/%s_client.json" % _credetials,
          "service":"/usr/local/google/home/kenjora/.credentials/%s_service.json" % _credetials,
          "user":"/usr/local/google/home/kenjora/.credentials/%s_user.json" % _credetials,
          "salesforce":"/usr/local/google/home/kenjora/.credentials/%s_salesforce.json" % _credetials,
        }
      }
    }

  @classmethod
  def get_uuid(cls):
    if not cls.uuid:
      cls.uuid = str(uuid.uuid4())
      with open(cls.filepath, 'r') as json_file: filedata = json_file.read()
      filedata = RE_UUID.sub(r'\1\2\1  "uuid":"%s",' % cls.uuid, filedata)
      with open(cls.filepath, 'w') as json_file: json_file.write(filedata)
      cls.configuration = get_project(cls.filepath)
    return cls.uuid 
