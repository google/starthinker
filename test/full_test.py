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


import threading
import json
import copy
import time
from time import sleep

from starthinker import config
from starthinker.util.project import project
from starthinker.util.pubsub import topic_publish, subscription_pull
from starthinker.manager.log import log_job_dispatch, log_verbose
from starthinker.manager.manager import manager, manager_test

from log_test import TEST_RECIPE
from gcloud import GCloudDAO


if __name__ == '__main__':

  log_verbose()
  project.initialize(_project=config.UI_PROJECT, _service=config.UI_SERVICE, _verbose=True)

  if not GCloudDAO().pubsub_topic_exists(config.UI_PROJECT, config.UI_TOPIC + '_worker'):
    print "Creating worker topic..."
    GCloudDAO().create_pubsub_topic(config.UI_PROJECT, config.UI_TOPIC + '_worker')

  if not GCloudDAO().pubsub_topic_exists(config.UI_PROJECT, config.UI_TOPIC + '_maintenance'):
    print "Creating maintenance topic..."
    GCloudDAO().create_pubsub_topic(config.UI_PROJECT, config.UI_TOPIC + '_maintenance')

  if not GCloudDAO().pubsub_subscription_exists(config.UI_PROJECT, config.UI_TOPIC):
    print "Creating subscription..."
    GCloudDAO().create_pubsub_subscription(config.UI_PROJECT, config.UI_TOPIC + "_worker", config.UI_TOPIC)

  print "Clear recipe queue..."
  messages = 1
  while messages:
    messages = subscription_pull(
      'service', 
      config.UI_PROJECT,
      config.UI_TOPIC,
      acknowledge=True,
      maximum=100
    )

  print "Publish a recipe..."
  recipe = copy.deepcopy(TEST_RECIPE)
  recipe['setup']['uuid'] = 'RECIPE_TEST_PUB_SUB'
  topic_publish(
    'service', 
    config.UI_PROJECT, 
    config.UI_TOPIC + '_worker', 
    json.dumps(recipe)
  )

  print "Receive a recipe..."
  message = subscription_pull(
    'service', 
    config.UI_PROJECT,
    config.UI_TOPIC,
    acknowledge=True
  )[0]
 
  print 'PASS: Recipe equals' if recipe == json.loads(message) else 'FAIL: %s' % message

  print "Publish a worker recipe..."
  recipe = copy.deepcopy(TEST_RECIPE)
  recipe['setup']['uuid'] = 'RECIPE_TEST_WORKER_%d' %  int(time.time()) # ensures unique recipe every run
  log_job_dispatch(recipe)
  topic_publish(
    'service', 
    config.UI_PROJECT, 
    config.UI_TOPIC + '_worker', 
    json.dumps(recipe)
  )

  print "Launching manager listener..."
  manager_test()
  t = threading.Thread(target=manager)
  t.start()

  sleep(10)

  #print "Waiting for logs..."
  # wait until error, complete, or timeout after a bit
  # should use most recent deployed code tag?
  print 'END'
