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

import json

from django.db import models
from django.utils.translation import gettext as _

from starthinker_ui.account.models import Account


class Project(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  identifier = models.CharField(max_length=255)
  service = models.TextField(default='')
  key = models.CharField(max_length=50, default='')
  share = models.CharField(max_length=50, default='')

  def __str__(self):
    if self.share == 'domain':
      return _('DOMAIN: %s | CAUTION: Be sure you trust this project.' % self.identifier)
    elif self.share == 'global':
      return _('GLOBAL: %s | CAUTION: Be sure you trust this project.' % self.identifier)
    else:
      return _('USER: %s | SAFE: Only you are using this service account.' % self.identifier)

  def link_edit(self):
    return '/project/edit/%d/' % self.pk

  def link_delete(self):
    return '/project/delete/%d/' % self.pk

  def get_credentials_service(self):
    return self.service if self.service else '{}'

  def get_client_email(self):
    return json.loads(self.get_credentials_service()).get('client_email', '')

  def get_project_id(self):
    return json.loads(self.get_credentials_service()).get('project_id', '')
