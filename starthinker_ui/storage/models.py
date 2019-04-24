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

from django.conf import settings

from starthinker.util.project import project
from starthinker.util.pubsub import topic_publish
from starthinker.util.storage import bucket_create, bucket_access, object_list, object_get
from starthinker_ui.job.models import job_update, job_status


class Storage():
  name = ''
  filename_storage = ''
  link_storage = ''
  link_run = ''

  def __init__(self, account, filename_storage):
    self.account = account
    self.name = filename_storage.split(':', 1)[1]
    self.filename_storage = filename_storage
    self.link_storage = 'https://storage.cloud.google.com/%s' % filename_storage.replace(':', '/', 1)
    self.link_run = '/storage/run/%s/' % self.name
    self.json = None

  def uid(self):
    return 'storage_%d_%s' % (self.account.pk, self.name)

  def get_log(self):
    return job_status(self.account, self.uid())


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
      yield Storage(account, filename_storage)
  except:
    pass # if no bucket then skip ( maybe not set up yet )


# gets a recipe stored in a bucket
def storage_get(account, recipe_uid):

  # fetch recipe from storage ( always base bucket name on account, never pass full bucket path )
  path = '%s:%s' % (account.get_bucket(full_path=False), recipe_uid)
  project.initialize(_project=settings.RECIPE_PROJECT, _service=settings.RECIPE_SERVICE)

  recipe = Storage(account, path)
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


# runs all recipes stored in the bucket
def storage_run_all(account, remote=True):
  for recipe in storage_list(account):
    storage_run(account, recipe.uid(), force=False, remote=remote)


# runs a recipe stored in a bucket
def storage_run(account, recipe_uid, force=True, remote=True):
  recipe = storage_get(account, recipe_uid)
  if remote:
    job_update(account, recipe, force=force, pause=False)
  elif settings.UI_CRON:
    with open(settings.UI_CRON + '/storage_%d_%s' % (account.pk, recipe_uid) , 'w') as f:
      f.write(json.dumps(recipe))
  else:
    raise Exception('Neither UI_CRON configured nor remote set.')
