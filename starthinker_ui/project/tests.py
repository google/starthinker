# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals

import os

from django.test import TestCase
from django.conf import settings

from starthinker_ui.account.tests import account_create
from starthinker_ui.project.models import Project


def project_create(share=''):

  with open(
    os.environ.get('STARTHINKER_SERVICE', 'MISSING RUN deploy.sh TO SET'),
    'r'
  ) as f:
    service = f.read()

  key = os.environ.get('STARTHINKER_API_KEY', 'MISSING RUN deploy.sh TO SET'),

  project = Project.objects.create(
      account=account_create(),
      service=service,
      key=key,
      share=share
  )

  return project


class ProjectTest(TestCase):

  def setUp(self):
    self.account = account_create()

    self.project_user = project_create()
    self.project_domain = project_create('domain')
    self.project_global = project_create('global')

  def test_ui_project(self):

    # not logged in ( blank )
    resp = self.client.get('/project/')
    self.assertEqual(resp.status_code, 200)

    self.client.force_login(
        self.account, backend=settings.AUTHENTICATION_BACKENDS[0])

    # logged in
    resp = self.client.get('/project/')
    self.assertEqual(resp.status_code, 200)

    self.assertContains(resp, self.project_user.identifier)
    self.assertContains(resp, self.project_domain.identifier)
    self.assertContains(resp, self.project_global.identifier)
    self.assertContains(resp, self.project_domain.share.upper())
    self.assertContains(resp, self.project_global.share.upper())

  def test_ui_project_edit(self):

    # not logged in ( blank )
    resp = self.client.get('/project/')
    self.assertEqual(resp.status_code, 200)

    self.client.force_login(self.account)

    # logged in
    resp = self.client.get('/project/edit/')
    self.assertEqual(resp.status_code, 200)

  def test_ui_recipe_edit(self):

    # not logged in ( redirect )
    resp = self.client.get('/recipe/edit/')
    self.assertEqual(resp.status_code, 302)

    self.client.force_login(
      self.account,
      backend=settings.AUTHENTICATION_BACKENDS[0]
    )

    # logged in ( projects in form )
    resp = self.client.get('/recipe/edit/')
    self.assertEqual(resp.status_code, 200)
    self.assertContains(resp, self.project_user)
    self.assertContains(resp, self.project_domain)
    self.assertContains(resp, self.project_global)


  def test_identifier_and_service(self):
    project = Project.objects.create(
      account=self.account,
      identifier='starthinker@project-12.iam.gserviceaccount.com',
      service=None
    )
    self.assertEqual(project.get_project_id(), 'project-12')

    project = Project.objects.create(
      account=self.account,
      identifier='starthinker@project-34.google.iam.gserviceaccount.com',
      service=None
    )
    self.assertEqual(project.get_project_id(), 'project-34')

    project = Project.objects.create(
      account=self.account,
      identifier='project-56',
      service=None
    )
    self.assertEqual(project.get_project_id(), 'project-56')

    project = Project.objects.create(
      account=self.account,
      identifier='',
      service='{"project_id":"project-78"}'
    )
    self.assertEqual(project.get_project_id(), 'project-78')

    project = Project.objects.create(
      account=self.account,
      identifier='project-90',
      service='{"project_id":"project-90"}'
    )
    self.assertEqual(project.get_project_id(), 'project-90')

    project = Project.objects.create(
      account=self.account,
      identifier='project-90',
      service='{"project_id":"project-90"}'
    )
    self.assertEqual(project.get_project_id(), 'project-90')

    self.assertEqual(Project.objects.filter(identifier='project-90').count(), 2)
