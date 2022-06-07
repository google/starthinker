###########################################################################
#
#  Copyright 2022 Google LLC
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

import base64

from starthinker.util.google_api import API_SecretManager


class SecretManager():
  '''Implement secert manager functionality.
     See: https://cloud.google.com/secret-manager/docs/reference/rest
  '''

  def __init__(self, config, auth:str) -> None:
    '''Accept configuration and authentication.
    '''

    self.config = config
    self.auth = auth


  def create(self, project_id, secret_id, data):
    '''Create a secret and version for the data in one step.
    '''

    parent = 'projects/{}'.format(project_id.replace(':', '.'))
    name = 'projects/{}/secrets/{}'.format(project_id.replace(':', '.'), secret_id)

    try:
      secret = API_SecretManager(self.config, self.auth).projects().secrets().get(
        name=name
      ).execute()
    except:
      secret = API_SecretManager(self.config, self.auth).projects().secrets().create(
        parent=parent,
        secretId=secret_id,
        body={
          'replication': {'automatic': {}}
        }
      ).execute()

    # add version to existing or new
    new_version = API_SecretManager(self.config, self.auth).projects().secrets().addVersion(
      parent=name,
      body={'payload': {'data':data.encode()}}
    ).execute()

    # destroy prior versions
    for prior_version in API_SecretManager(self.config, self.auth, iterate=True).projects().secrets().versions().list(
      parent=name
    ).execute():
      if prior_version['name'] != new_version['name'] and prior_version['state'] != 'DESTROYED':
        API_SecretManager(self.config, self.auth).projects().secrets().versions().destroy(
          name=prior_version['name']
        ).execute()


  def access(self, project_id, secret_id):
    '''Retrieve a secret and decode into a UTF-8 string.
    '''
    return base64.b64decode(
      API_SecretManager(self.config, self.auth).projects().secrets().versions().access(
        name = 'projects/{}/secrets/{}/versions/latest'.format(project_id.replace(':', '.'), secret_id)
      ).execute()['payload']['data']
    ).decode('UTF-8')


  def delete(self, project_id, secret_id):
    '''Delete a secret.
    '''
    API_SecretManager(self.config, self.auth).projects().secrets().delete(
      name = 'projects/{}/secrets/{}'.format(project_id.replace(':', '.'), secret_id)
    ).execute()
