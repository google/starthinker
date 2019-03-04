# -*- coding: utf-8 -*-

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

import json
from time import sleep

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from starthinker.ui.account.models import Account, token_generate
from starthinker.ui.project.models import Project
from starthinker.ui.recipe.scripts import Script
from starthinker.ui.ui.pubsub import send_message
from starthinker.manager.log import log_get

class Recipe(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  token = models.CharField(max_length=8, unique=True)

  project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

  name = models.CharField(max_length=64)
  active = models.BooleanField(default=True)

  week = models.CharField(max_length=64, default=json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']))
  hour = models.CharField(max_length=64, default=json.dumps([3]))

  timezone = models.CharField(max_length=32, blank=True, default='America/Los_Angeles')

  link = models.CharField(max_length=255, blank=True)

  tasks = models.TextField()

  _log = None

  def _get_log(self):
    if self._log is None: self._log = log_get(self.uid(), self.timezone)
    return self._log

  def _set_log(self, value):
    self._log = value

  log = property(_get_log, _set_log)

  def __unicode__(self):
    return self.name

  def save(self, *args, **kwargs):
    self.get_token()
    super(Recipe, self).save(*args, **kwargs)

  def uid(self):
    return "UI-RECIPE-%s" % (self.pk or 'NEW')

  def link_edit(self):
    return '/recipe/edit/%d/' % self.pk

  def link_delete(self):
    return '/recipe/delete/%d/' % self.pk

  def link_run(self):
    return '/recipe/run/%d/' % self.pk if self.pk else ''

  def link_download(self):
    return '/recipe/download/%d/' % self.pk if self.pk else ''

  def get_token(self):
    if not self.token: self.token = token_generate(Recipe)
    return self.token

  def get_values(self):
    constants = self.get_constants()
    tasks = json.loads(self.tasks or '[]')
    for task in tasks: task['values'].update(constants)
    return tasks

  def set_values(self, scripts):
    self.tasks = json.dumps(scripts)

  def get_hours(self):
    return json.loads(self.hour or '[]')

  def get_days(self):
    return json.loads(self.week or '[]')

  def get_icon(self): return '' #get_icon('')

  def get_credentials_user(self):
    return self.account.get_credentials_safe() if self.account else '{}'

  def get_credentials_service(self):
    return self.project.service if self.project and self.project.service else '{}'

  def get_project_identifier(self):
    return self.project.get_project_id() if self.project else ''
  
  def get_scripts(self):
    for value in self.get_values():  yield Script(value['tag'])

  def get_constants(self):
    return {
      'name':slugify(self.name),
      'token':self.get_token(),
      'timezone':self.timezone,
      'email':self.account.email if self.account else None,
      'email_token': self.account.email.replace('@', '+%s@' % self.get_token()) if self.account else None,
    }

  def get_json(self, credentials=True):
    filename = 'recipe_%d.json' % self.pk
    return filename, Script.get_json(
        self.uid(),
        self.get_project_identifier(),
        self.get_credentials_user() if credentials else '',
        self.get_credentials_service() if credentials else '',
        self.get_days(),
        self.get_hours(),
        self.get_values(),
        self.get_constants()
      )

  def run(self):
    filename, data = self.get_json()

    # remove schedule since this is a run now
    if 'day' in data['setup']: del data['setup']['day']
    if 'hour' in data['setup']: del data['setup']['hour']

    if settings.UI_TOPIC:
      # dispatch to pub/sub
      send_message(settings.UI_PROJECT, settings.UI_TOPIC, json.dumps(data))
    else:
      # write to local file
      with open(settings.UI_CRON + '/' + filename, 'w') as f:
        f.write(json.dumps(data))

    sleep(5) # give the task enough time to start and flag RUNNING
