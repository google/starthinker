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


import uuid
import json
import os
from datetime import datetime
from subprocess import Popen, PIPE

from starthinker.manager.log import log_job_start
from starthinker.util.project import day_hour_scheduled
from starthinker.config import UI_PROJECT, UI_ROOT, UI_TOPIC, UI_ZONE, DEVELOPMENT_MODE, INTERNAL_MODE


def get_docker_tag(recipe):
  version = recipe['setup'].get('version', 'latest')
  docker_tag = 'gcr.io/%s/starthinker:%s' % (UI_PROJECT.replace(':', '/'), version)

  return docker_tag


def docker_pull(docker_tag):
  docker_pull_job = Popen(['gcloud', 'docker', '--', 'pull', docker_tag])
  docker_pull_job.wait()
  docker_pull_job.poll()

  if docker_pull_job.returncode != 0:
    raise Exception('Docker image not found: %s' % docker_tag)


def run_job(recipe):
  docker_tag = get_docker_tag(recipe)
  docker_pull(docker_tag)

  job_id = str(uuid.uuid1())
  job_file_name = '/tmp/%s' % job_id
  job_file = open(job_file_name, 'wb')
  job_file.write(json.dumps(recipe))
  job_file.close()

  command = [
    'docker', 'run', '--name', job_id, '--rm', 
    '-e', 'STARTHINKER_SCALE=6',
    '-e', 'STARTHINKER_WORKERS=1',
    '-e', 'STARTHINKER_PROJECT="%s"' % UI_PROJECT,
    '-e', 'STARTHINKER_ZONE="%s"' % UI_ZONE,
    '-e', 'STARTHINKER_TOPIC="%s"' % UI_TOPIC,
    '-e', 'STARTHINKER_CLIENT="/home/starthinker_assets/client.json"',
    '-e', 'STARTHINKER_SERVICE="/home/starthinker_assets/service.json"',
    '-e', 'STARTHINKER_CRON="/home/starthinker_assets/cron"',
    '-e', 'STARTHINKER_CODE="/home/starthinker/"',
    '-e', 'STARTHINKER_ROOT="/home"',
    '-e', 'STARTHINKER_DEVELOPMENT=%d' % (1 if DEVELOPMENT_MODE else 0 ),
    '-e', 'STARTHINKER_INTERNAL=%d' % (1 if INTERNAL_MODE else 0 ),
    '-v', '%s/starthinker_assets/:/home/starthinker_assets' % UI_ROOT, 
    '-v', '/tmp:/tmp', 
    docker_tag,
    'python', '/home/sarthinker/all/run.py', job_file_name, '--verbose'
  ]

  if INTERNAL_MODE: 
    command.insert(-4, '-v')
    command.insert(-4, '/home/mauriciod/credentials:/home/credentials')
    command.insert(-4, '-v')
    command.insert(-4, '/home/mauriciod/.config:/root/.config')

  if not 'hour' in recipe['setup']: command.append('--force')

  print ' '.join(command)

  job = Popen(command, stdout=PIPE, stderr=PIPE)

  # All tasks in a recipe must exist within 24 hours, add to logs so we can identify multi hour recipes as one workflow
  tz_date, tz_day, tz_hour = day_hour_scheduled(recipe)

  # recipe will keep state for logging purposes
  recipe['worker'] = {
    'job': job,
    'container_name': job_id,
    'start_datetime': datetime.utcnow(),
    'job_file_name': job_file_name,
    'job_date':tz_date,
  }
  recipe.setdefault('setup', {})
  recipe['setup'].setdefault('uuid', job_id)
  recipe['setup'].setdefault('timeout_seconds', 4 * 60 * 60)

  log_job_start(recipe)

  return recipe
