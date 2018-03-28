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

import re
import json
import argparse
import uuid

RE_NAME = re.compile(r'[^a-zA-Z0-9_]')
RE_UUID = re.compile(r'(\s*)("setup"\s*:\s*{)')

from google.cloud import pubsub
from setup import UI_SERVICE


def send_message(project_id, topic, data):
  client = pubsub.Client.from_service_account_json(UI_SERVICE)
  topic = client.topic(topic)
  return topic.publish(data)


def set_constants(struct, constants):
  if isinstance(struct, dict):
    for key, value in struct.items():
      if isinstance(value, dict) and 'constant' in value:
        struct[key] = constants.get(value['constant'], None)
        if 'prefix' in value and struct[key]: struct[key] = value['prefix'] + struct[key]
      else:
        set_constants(value, constants)
  elif isinstance(struct, list) or isinstance(struct, tuple):
    for index, value in enumerate(struct):
      if isinstance(value, dict) and 'constant' in value:
        struct[index] = constants.get(value['constant'], None)
        if 'prefix' in value and struct[index]: struct[index] = value['prefix'] + struct[index]
      else: set_constants(value, constants)


def make_solution(filename, uuid, project_id, credentials_user, credentials_service, credentials_client, constants, remote):
  solution = {}

  with open(filename, 'r') as solution_file:
    solution = json.load(solution_file)

  tasks = solution['tasks']
  set_constants(tasks, constants)

  return {
    "setup":{
      "uuid":uuid,
      "id":project_id,
      "timezone":constants['timezone'],
      "auth":{
        "source":"remote" if remote else "local",
        "user":credentials_user,
        "service":credentials_service,
        "client":credentials_client
      }
    },
    "tasks":tasks
  }


if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('solution', help='path to solution json file')

  # add credentials ( solutions have no credentials by default )
  parser.add_argument('--project', '-p', help='cloud id of project, defaults to None', default=None)
  parser.add_argument('--user', '-u', help='path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS', default=None)
  parser.add_argument('--service', '-s', help='path to service credentials json file, defaults None', default=None)
  parser.add_argument('--client', '-c', help='path to client credentials json file, defaults None', default=None)

  # specify deployment ( may require access to pub/sub )
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--directory', '-d', help='write solution scripts to a directory')
  group.add_argument('--topic', '-t', help='execute solution using pub/sub topic')
  args = parser.parse_args()

  # get script name
  script = args.solution.rsplit('.', 1)[0].rsplit('/', 1)[-1]

  # load configuration
  solution = json.load(open(args.solution))

  # add computed variables
  name = RE_NAME.sub('', solution['constants']['name'])
  solution['constants']['email_token'] = solution['constants']['email'].replace("@", "+%s@" % solution['constants']['token'])
  solution['constants']['report'] = name + ' ( StarThinker )'
  solution['constants']['dataset'] = name
  solution['constants']['bucket'] = name

  # create a UUID ( all templates get same with suffix )
  master_uuid = str(uuid.uuid4())

  # create scripts for each template
  for template in solution['templates']:

    # get solution tag for uuid
    tag = template.rsplit('.', 1)[0].rsplit('/', 1)[-1]

    # construct script from solution template
    recipe = make_solution(
      template,
      '%s_%s' % (master_uuid, tag),
      args.project,
      args.user,
      args.service,
      args.client,
      solution['constants'],
      bool(args.topic) 
    )

    #print json.dumps(recipe, indent=2)

    # if remote ( pub/sub )
    if args.topic:
      print 'SOLUTON REMOTE'
      send_message(recipe['setup']['id'], args.topic, json.dumps(recipe))

    # if local
    else:
      filename = '%s%s%s_%s.json' % (args.directory, '' if args.directory[-1] == '/' else '/', script, tag)
      print 'SOLUTION SCRIPT', filename
      with open(filename, 'w') as outfile:
        json.dump(recipe, outfile)
