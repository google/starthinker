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
"""Handler that executes { "salesforce":{...}} task in recipe JSON.

This script translates JSON instructions into operations on salesforce
reporting.

"""

from starthinker.util.data import put_rows
from starthinker.util.salesforce import authenticate, query


def salesforce(config, task):
  if config.verbose:
    print('Salesforce')

  sf = authenticate(
    task['domain'],
    task['client'],
    task['secret'],
    task['username'],
    task['password']
  )

  if 'query' in task:
    rows = query(sf, task['query'])
    if rows:
      put_rows(
        config,
        task['auth'],
        task['out'],
        rows
      )
