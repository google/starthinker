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

#https://cloud.google.com/compute/docs/reference/rest/v1/instanceGroupManagers

from django.conf import settings
from starthinker.util.configuration import Configuration
from starthinker.util.google_api import API_Compute


def group_instances_resize(count):
  return API_Compute(
    Configuration(
      service=settings.UI_SERVICE,
      project=settings.UI_PROJECT
    ),
    auth='service'
  ).instanceGroupManagers().resize(
    project=settings.UI_PROJECT,
    zone=settings.UI_ZONE,
    instanceGroupManager='starthinker-worker-group',
    size=count
  ).execute()


def group_instances_delete(name):
  return API_Compute(
    Configuration(
      service=settings.UI_SERVICE,
      project=settings.UI_PROJECT
    ),
    auth='service'
  ).instanceGroupManagers().deleteInstances(
    project=settings.UI_PROJECT,
    zone=settings.UI_ZONE,
    instanceGroupManager='starthinker-worker-group',
    body={
      'instances': ['zones/%s/instances/%s' % (settings.UI_ZONE, name)],
      'type': 'PROACTIVE'
    }
  ).execute()


def group_instances_list(statuses=[]):
  return API_Compute(
    Configuration(
      service=settings.UI_SERVICE,
      project=settings.UI_PROJECT
    ),
    auth='service',
    iterate=True
  ).instanceGroupManagers().listManagedInstances(
    project=settings.UI_PROJECT,
    zone=settings.UI_ZONE,
    instanceGroupManager='starthinker-worker-group',
    filter=' OR '.join(['(instanceStatus = "%s")' % status for status in statuses]),
    orderBy='creationTimestamp desc'
  ).execute()
