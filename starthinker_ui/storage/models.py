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

from starthinker.manager.log import log_get, log_job_dispatch
from starthinker.util.project import project
from starthinker.util.pubsub import topic_publish
from starthinker.util.storage import bucket_create, bucket_access, object_list, object_get

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
  project.initialize(_project=settings.RECIPE_PROJECT, _service=settings.RECIPE_SERVICE)
  bucket_create('service', settings.RECIPE_PROJECT, bucket)
  bucket_access('service', settings.RECIPE_PROJECT, bucket, 'OWNER', emails=[account.email])


# retrieve recipes from bucket and add status
def storage_list(account):
  path = '%s:' % account.get_bucket(full_path=False)
  project.initialize(_project=settings.RECIPE_PROJECT, _service=settings.RECIPE_SERVICE)

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
  project.initialize(_project=settings.RECIPE_PROJECT, _service=settings.RECIPE_SERVICE)

  recipe = Storage(path)
  data = json.loads(object_get('service', path))

  # ensure there is a setup auth section
  data['setup'] = data.get('setup', {})
  data['setup']['auth'] = data['setup'].get('auth', {})

  # add a UUID to the setup section ( overwritten by UI for logging purposes )
  data['setup']['uuid'] = recipe.uid()

  # add user credentials to recipe ( always override if given )
  data['setup']['auth']['user'] = account.get_credentials_path()

  # add service credentials to recipe or clear them if invalid ( prevent path injection )
  try: data['setup']['auth']['service'] = account.project_set.get(identifier=data['setup']['auth'].get('service', '')).service
  except: 
    try: del data['setup']['auth']['service']
    except: pass

  return data


# runs a recipe stored in a bucket
def storage_run(account, recipe_name, force=True, topic=settings.UI_TOPIC):
  recipe = storage_get(account, recipe_name)

  # remove schedule since this is a run now
  if force: 
    if 'day' in recipe['setup']: del recipe['setup']['day']
    if 'hour' in recipe['setup']: del recipe['setup']['hour']

  if topic:
    # dispatch to pub/sub
    log_job_dispatch(recipe)
    project.initialize(_project=settings.UI_PROJECT, _service=settings.UI_SERVICE)
    topic_publish( 'service', settings.UI_PROJECT, topic + '_worker', json.dumps(recipe))
    sleep(5) # give the task enough time to start and flag RUNNING
  else:
    # write to local file
    with open(settings.UI_CRON + '/storage_%d_%s' % (account.pk, recipe_name) , 'w') as f:
      f.write(json.dumps(recipe))
