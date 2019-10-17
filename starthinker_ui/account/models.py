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

from random import choice

from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from starthinker.util.auth.wrapper import CredentialsUserWrapper
from starthinker_ui.account.apps import USER_BUCKET


def fix_picture(picture_url):
  return picture_url.replace('/photo.jpg', '/s32-c/photo.jpg') 


def token_generate(model_class, model_field, length=8):
  token = None
  while not token: 
    token = ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length)])
    try:
      if model_class.objects.filter(**{model_field:token}).exists(): token = None
    except Exception:
      pass
  return token


class AccountManager(BaseUserManager):

  def create_user(self, profile, credentials=None, password=None):
    account = self.model(
      identifier=profile['id'], 
      email=self.normalize_email(profile['email']),
      name=profile['given_name'],
      picture=fix_picture(profile['picture']),
    )
    account.set_credentials(credentials) 
    account.set_password(password)
    account.save(using=self._db)
    return account

  def get_or_create_user(self, profile, credentials=None, password=None):
    try: 
      account = Account.objects.get(identifier=profile['id'])
      account.email = self.normalize_email(profile['email'])
      account.name = profile['given_name']
      account.picture = fix_picture(profile['picture'])
      account.set_credentials(credentials)
      account.set_password(password)
      account.save(using=self._db)
    except:
      account = self.create_user(profile, credentials, password)
    return account

  def create_superuser(self, profile, credentials, password):
    account = self.create_user(profile, credentials, password)
    account.is_admin = True
    account.save(using=self._db)
    return account


class Account(AbstractBaseUser):
  identifier = models.CharField(max_length=64, unique=True, db_index=True)
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255, blank=True, default='')
  picture = models.CharField(max_length=255, blank=True, default='')
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = AccountManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['identifier']

  def get_full_name(self):
    return self.email

  def get_short_name(self):
    return self.email

  def __unicode__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True

  @property
  def is_staff(self):
    return self.is_admin

  def set_credentials(self, credentials):
    # check if refresh token exists before saving credentials ( only given first time through auth )?
    if self.identifier:
      buffer = CredentialsUserWrapper()
      buffer.from_credentials(credentials)
      buffer.save(self.get_credentials_path()) 

  def get_credentials(self):
    return CredentialsUserWrapper(self.get_credentials_path()) if self.identifier else None

  def get_credentials_path(self):
    return '%s:ui/%s.json' % (USER_BUCKET, self.identifier)
