###########################################################################
#
#  Copyright 2020 Google LLC
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

import base64

from starthinker.util.google_api import API_PubSub


def topic_create(config, auth, project_id, topic):
  api = API_PubSub(config, auth).projects().topics().create(
      topic='projects/%s/topics/%s' % (project_id, topic), body={}).execute()


def subscription_create(config, auth, project_id, topic, subscription):
  body = {
      'topic': 'projects/%s/topics/%s' % (project_id, topic),
      'pushConfig': {},
      'ackDeadlineSeconds': 600,
      'messageRetentionDuration': '86400s',  # 24 hours
      'retainAckedMessages': False,
  }

  api = API_PubSub(config, auth).projects().subscriptions().create(
      name='projects/%s/subscriptions/%s' % (project_id, subscription),
      body=body).execute()


def topic_publish(config, auth, project_id, topic, data):
  body = {'messages': [{'data': base64.b64encode(data)}]}
  api = API_PubSub(config, auth).projects().topics().publish(
      topic='projects/%s/topics/%s' % (project_id, topic), body=body).execute()
  return api['messageIds'][0]


def subscription_acknowledge(config, auth, project_id, subscription, ack_id):
  if isinstance(ack_id, str):
    ack_id = [ack_id] if ack_id else []

  if ack_id:
    body = {'ackIds': ack_id}
    API_PubSub(config, auth).projects().subscriptions().acknowledge(
        subscription='projects/%s/subscriptions/%s' %
        (project_id, subscription),
        body=body).execute()


def subscription_pull(config, auth,
                      project_id,
                      subscription,
                      immediate=True,
                      maximum=1,
                      acknowledge=False):
  messages = []

  if maximum <= 0:
    return messages

  body = {'returnImmediately': immediate, 'maxMessages': maximum}

  for message in API_PubSub(
      auth, iterate=True).projects().subscriptions().pull(
          subscription='projects/%s/subscriptions/%s' %
          (project_id, subscription),
          body=body).execute():
    messages.append({
        'ackId': message['ackId'],
        'data': base64.b64decode(message['message']['data'])
    })

  # if acknowledge, then acknowledge all messages and return only data
  if acknowledge:
    subscription_acknowledge(config, auth, project_id, subscription,
                             [m['ackId'] for m in messages])
    return [m['data'] for m in messages]
  # or return ack and data as a dictionary
  else:
    return messages
