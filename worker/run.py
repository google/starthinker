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

import argparse
import json
import os
import uuid
from subprocess import check_output, CalledProcessError, STDOUT
from util.pubsub import send_message, receive_message

def worker(project_id, execution_topic_name, execution_subscription_name, project_dir, results_topic_name):


  while True:
    jobs = receive_message(project_id, execution_topic_name, execution_subscription_name, wait=True, ack=True)
    for ack, message in jobs:
      default_execution_id = str(uuid.uuid4().hex)
      job = json.loads(message.data)

      project_file_name = os.path.join(project_dir, job.get('execution_id', default_execution_id) + '.json')
      project_file = open(project_file_name, 'w')
      project_file.write(message.data)
      project_file.close()

      print 'Executing job %s' % job.get('execution_id', default_execution_id)

      result = {
        'execution_id': job.get('execution_id', default_execution_id),
        'status_code': 0
      }

      try:
        command = ['python', 'all/run.py', project_file_name, '--verbose']
        if not 'hour' in job['setup']:
          command.append('--force')

        result['stdout'] = check_output(command, stderr=STDOUT).split('\n')
      except CalledProcessError, ex:
        result['status_code'] = ex.returncode
        result['stdout'] = ex.output.split('\n')

      os.remove(project_file_name)

      send_message(project_id, results_topic_name, json.dumps(result))

      print json.dumps(result, indent=2)

      print 'Job %s is done' % job.get('execution_id', default_execution_id)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('gcloud_project', help='[gcloud_project] is the google cloud project id where pubsub is configured.')
  parser.add_argument('execution_topic_name', help='The topic from which to get jobs.')
  parser.add_argument('execution_subscription_name', help='The subscription name where to get jobs from.')
  parser.add_argument('results_topic_name', help='The topic name to in which to publish execution results.')
  parser.add_argument('project_dir', help='Directory in which project files should be stored.')
  args = parser.parse_args()

  worker(args.gcloud_project, args.execution_topic_name, args.execution_subscription_name, args.project_dir, args.results_topic_name)

if __name__ == '__main__':
  main()
