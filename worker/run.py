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

import datetime
import argparse
import json
import os
import uuid
import logging

import subprocess
from subprocess import check_output, CalledProcessError, STDOUT, Popen
from util.pubsub import send_message, receive_message
from threading import Timer

def worker(project_id, execution_topic_name, execution_subscription_name, project_dir, results_topic_name):

  # Workers update themselves by exiting after being alive for a certain period
  # of time, which cause them to be restarted and pull the latest image from the docker registry.
  # This variable controls for how long workers should live, when the time is up it
  # will exit as soon as it becomes idle again.
  # Time to live in seconds
  worker_time_to_live = 60 * 60 * 1

  # This is how long a job can run on a worker in seconds
  worker_job_timeout = 60 * 60 * 3

  worker_expiration = datetime.datetime.now() + datetime.timedelta(seconds=worker_time_to_live)

  while datetime.datetime.now() < worker_expiration:
    jobs = receive_message(project_id, execution_topic_name, execution_subscription_name, wait=True, ack=True)
    for ack, message in jobs:
      job_id = 'REALLYBADERROR' # This is in case something really bad goes wrong, we get a log
      try:
        execution_id = str(uuid.uuid4().hex) # This is so we at least know the job when it breaks

        job_for_logging = json.loads(message.data)
        del job_for_logging['setup']['auth']
        job_id = job_for_logging.get('setup', {}).get('uuid', execution_id)
        logging.debug('%s: %s' % (job_id, json.dumps(job_for_logging)))

        job = json.loads(message.data)
        execution_id = job.get('execution_id', execution_id) # This is what we hope to use
        logging.debug('%s: Worker starting job' % job_id)

        project_file_name = os.path.join(project_dir, execution_id + '.json')
        project_file = open(project_file_name, 'w')
        project_file.write(message.data)
        project_file.close()


        print 'Executing job %s' % job_id

        result = {
          'execution_id': execution_id,
          'status_code': 0
        }

        try:
          command = ['python', 'all/run.py', project_file_name, '--verbose']
          if not 'hour' in job['setup']:
            command.append('--force')

          #result['stdout'] = check_output(command, stderr=STDOUT).split('\n')

          kill = lambda process: process.kill()
          p = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

          timer = Timer(worker_job_timeout, kill, [p])

          stderr = ''
          stdout = ''

          try:
            timer.start()
            stdout, stderr = p.communicate()
          finally:
            timer.cancel()

          for line in stdout.split('\n'):
            logging.info('%s: %s' % (job_id, line))

          for line in stderr.split('\n'):
            logging.info('%s: %s' % (job_id, line))

          logging.info('%s: Job finished' % job_id)

        except CalledProcessError, ex:
          result['status_code'] = ex.returncode
          result['stdout'] = ex.output.split('\n')

          for line in stdout['result']:
            logging.error('%s: %s' % (job_id, line))

          logging.error('%s: Job failed' % job_id)

        os.remove(project_file_name)

        send_message(project_id, results_topic_name, json.dumps(result))

        print json.dumps(result, indent=2)

        print 'Job %s is done' % job_id

      except Exception, e:
        logging.error('%s: WORKER ERROR: %s' % (job_id, str(e)))

def main():
  # TODO: mauriciod put logging configuration in a yaml file, and make it
  # rotating
  logging.basicConfig(filename='/var/log/worker.log', level=logging.DEBUG)

  parser = argparse.ArgumentParser()
  parser.add_argument('gcloud_project', help='[gcloud_project] is the google cloud project id where pubsub is configured.')
  parser.add_argument('execution_topic_name', help='The topic from which to get jobs.')
  parser.add_argument('execution_subscription_name', help='The subscription name where to get jobs from.')
  parser.add_argument('results_topic_name', help='The topic name to in which to publish execution results.')
  parser.add_argument('project_dir', help='Directory in which project files should be stored.')
  args = parser.parse_args()

  logging.info('Starting worker')
  logging.info('Project %s' % args.gcloud_project)
  logging.info('Execution Topic %s' % args.execution_topic_name)
  logging.info('Execution Subscription %s' % args.execution_subscription_name)
  logging.info('Project Dir %s' % args.project_dir)
  logging.info('Results Topic Name %s' % args.results_topic_name)
  worker(args.gcloud_project, args.execution_topic_name, args.execution_subscription_name, args.project_dir, args.results_topic_name)

if __name__ == '__main__':
  main()
