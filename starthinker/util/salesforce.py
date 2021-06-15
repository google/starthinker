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
from urllib import request, parse

from simple_salesforce import Salesforce


def authenticate(domain, client_id, client_secret, username, password):

  data = parse.urlencode({
      'grant_type': 'password',
      'client_id': client_id,
      'client_secret': client_secret,
      'username': username,
      'password': password
  }).encode()

  req = request.Request('https://%s/services/oauth2/token' % domain, data=data)
  creds = json.loads(request.urlopen(req).read())
  return Salesforce(
      instance_url=creds['instance_url'], session_id=creds['access_token'])


def query(service, query, header=False):
  for record in service.query_all(query)['records']:
    if header:
      yield [column for column in record.keys() if column != 'attributes']
      header = False
    yield [record[column] for column in record.keys() if column != 'attributes']
