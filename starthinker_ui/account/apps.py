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

from django.apps import AppConfig
from django.conf import settings

from starthinker.util.configuration import Configuration
from starthinker.util.storage import bucket_create

USER_BUCKET = '%s-starthinker-credentials' % settings.UI_PROJECT.split(
    ':', 1)[-1]  # remove domain: part
USER_LOCATION = settings.UI_ZONE.rsplit('-',
                                        1)[0]  # take only region part of zone


class AccountConfig(AppConfig):
  name = 'starthinker_ui.account'

  def ready(self):
    print('CHECKING IF USER BUCKET EXISTS:', USER_BUCKET, USER_LOCATION)
    bucket_create(
      Configuration(
        service=settings.UI_SERVICE,
        project=settings.UI_PROJECT
      ),
      'service',
      settings.UI_PROJECT,
      USER_BUCKET,
      USER_LOCATION
    )
