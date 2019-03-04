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


import re
import json
from time import sleep

from django.conf import settings

from starthinker.config import CLOUD_PROJECT, CLOUD_SERVICE
from starthinker.manager.log import log_get
from starthinker.util.project import project
from starthinker.util.storage import bucket_create, bucket_access, object_list, object_get
from starthinker.ui.ui.pubsub import send_message

RE_UID = re.compile(r'\W+')


class Storage():
  name = ''
  status = {}
  filename_storage = ''
  filename_local = ''
  link_storage = ''
  link_run = ''

  _log = None

  def _get_log(self):
    if self._log is None: self._log = log_get(self.uid(), {})
    return self._log

  def _set_log(self, value):
    self._log = value

  log = property(_get_log, _set_log)

  def __init__(self, filename_storage):
    self.name = filename_storage.split(':', 1)[1]
    self.filename_storage = filename_storage
    self.filename_local = RE_UID.sub('_', filename_storage.replace('starthinker', 'storage', 1))
    self.link_storage = 'https://storage.cloud.google.com/%s' % filename_storage.replace(':', '/', 1)
    self.link_run = '/storage/run/%s/' % self.name
    self.json = None
    self.log = None

  def uid(self):
    return self.filename_local


# create and permission bucket ( will do nothing if it exists )
def storage_create(account):
  bucket = account.get_bucket(full_path=False)
  project.initialize(_project=CLOUD_PROJECT, _service=CLOUD_SERVICE)
  bucket_create('service', CLOUD_PROJECT, bucket)
  bucket_access('service', CLOUD_PROJECT, bucket, 'OWNER', emails=[account.email])


# retrieve recipes from bucket and add status
def storage_list(account):
  path = '%s:' % account.get_bucket(full_path=False)
  project.initialize(_project=CLOUD_PROJECT, _service=CLOUD_SERVICE)

  try:
    for filename_storage in object_list('service', path, files_only=True):
      yield Storage(filename_storage)
  except:
    pass # if no bucket then skip ( maybe not set up yet )


# gets a recipe stored in a bucket
def storage_get(account, recipe_name):

  # converst to storage class to get helpers such as uid

  # fetch recipe from storage ( always base bucket name on account, never pass full bucket path )
  path = '%s:%s' % (account.get_bucket(full_path=False), recipe_name)
  project.initialize(_project=CLOUD_PROJECT, _service=CLOUD_SERVICE)

  recipe = Storage(path)
  data = json.loads(object_get('service', path))

  # ensure there is a setup auth section
  data['setup'] = data.get('setup', {})
  data['setup']['auth'] = data['setup'].get('auth', {})

  # add a UUID to the setup section ( overwritten by UI for logging purposes )
  data['setup']['uuid'] = recipe.uid()

  # add user credentials to recipe ( always override if given )
  data['setup']['auth']['user'] = account.get_credentials_safe()

  # add service credentials to recipe or clear them if invalid ( prevent path injection )
  try: data['setup']['auth']['service'] = account.project_set.get(identifier=data['setup']['auth'].get('service', '')).service
  except: 
    try: del data['setup']['auth']['service']
    except: pass

  return data


# runs a recipe stored in a bucket
def storage_run(account, recipe_name):
  data = storage_get(account, recipe_name)

  # remove schedule since this is a run now
  if 'day' in data['setup']: del data['setup']['day']
  if 'hour' in data['setup']: del data['setup']['hour']

  if settings.UI_TOPIC:
    # dispatch to pub/sub
    send_message(settings.UI_PROJECT, settings.UI_TOPIC, json.dumps(data))
    sleep(5) # give the task enough time to start and flag RUNNING
  else:
    # write to local file
    with open(settings.UI_CRON + '/storage_%d_%s' % (account.pk, recipe_name) , 'w') as f:
      f.write(json.dumps(data))
