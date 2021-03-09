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
import re

from django.db import models
from django.utils.translation import gettext as _

from starthinker_ui.account.models import Account

RE_IDENTIFIER = re.compile(r'@(.*?)(\.google)?\.iam\.gserviceaccount\.com', re.DOTALL)


class Project(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  identifier = models.CharField(max_length=255)
  service = models.TextField(default='')
  key = models.CharField(max_length=50, default='')
  share = models.CharField(max_length=50, default='')

  def __str__(self):
    label = self.get_project_id()
    client_email = self.get_client_email()

    if client_email:
      label += ' / ' + client_email

    if self.key:
      label += _(' / API Key')

    if self.share == 'domain':
      return _('%s / Domain Visible' % label)
    elif self.share == 'global':
      return _('%s / Global Visible' % label)
    else:
      return _('%s / User Visible' % label)

  def save(self, *args, **kwargs):
    if self.service is None:
       self.service = ''

    if not self.identifier and self.service:
      try:
        self.identifier = json.loads(self.service)['project_id']
      except:
        pass

    super(Project, self).save(*args, **kwargs)

  def link_edit(self):
    return '/project/edit/%d/' % self.pk

  def link_delete(self):
    return '/project/delete/%d/' % self.pk

  def get_credentials_service(self):
    return self.service if self.service else '{}'

  def get_client_email(self):
    return json.loads(self.get_credentials_service()).get('client_email', '')

  def get_project_id(self):
    # temporary transitional, phase out in ~6 months
    # current: identifier is project id
    # legacy: identifier is service account email
    results = RE_IDENTIFIER.search(self.identifier)
    if results:
      return results.group(1)
    else:
      return self.identifier
