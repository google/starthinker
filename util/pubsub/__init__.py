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

from google.cloud import pubsub

def send_message(project_id, topic, data):
  client = pubsub.Client(project=project_id)
  topic = client.topic(topic)
  return topic.publish(data)

def receive_message(project_id, topic, subscription, wait=False, ack=True):
  client = pubsub.Client(project=project_id)
  topic = client.topic(topic)
  subscription = topic.subscription(subscription)

  results = subscription.pull(return_immediately=not wait)

  if ack:
    if results:
      subscription.acknowledge([ack_id for ack_id, message in results])

  return results
