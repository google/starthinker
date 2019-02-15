import json

from django.db import models

from starthinker.ui.account.models import Account

class Project(models.Model):
  account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True)
  identifier = models.CharField(max_length=255)
  service = models.TextField()

  def __unicode__(self):
    return self.identifier

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
