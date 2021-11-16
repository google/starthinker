###########################################################################
#
#  Copyright 2021 Google LLC
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
#
#  This code generated (see scripts folder for possible source):
#    - Command: "python starthinker_ui/manage.py example"
#
###########################################################################

import argparse
import textwrap

from starthinker.util.configuration import Configuration
from starthinker.task.google_api.run import google_api


def recipe_google_api_to_bigquery(config, auth_read, api, version, function, kwargs, kwargs_remote, api_key, developer_token, login_customer_id, dataset, table):
  """Execute any Google API function and store results to BigQuery.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       api (string) - See developer guide.
       version (string) - Must be supported version.
       function (string) - Full function dot notation path.
       kwargs (json) - Dictionray object of name value pairs.
       kwargs_remote (json) - Fetch arguments from remote source.
       api_key (string) - Associated with a Google Cloud Project.
       developer_token (string) - Associated with your organization.
       login_customer_id (string) - Associated with your Adwords account.
       dataset (string) - Existing dataset in BigQuery.
       table (string) - Table to write API call results to.
  """

  google_api(config, {
    'auth':auth_read,
    'api':api,
    'version':version,
    'function':function,
    'kwargs':kwargs,
    'kwargs_remote':kwargs_remote,
    'key':api_key,
    'headers':{
      'developer-token':developer_token,
      'login-customer-id':login_customer_id
    },
    'results':{
      'bigquery':{
        'dataset':dataset,
        'table':table
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Execute any Google API function and store results to BigQuery.

      1. Enter an api name and version.
      2. Specify the function using dot notation.
      3. Specify the arguments using json.
      4. Iterate is optional, use if API returns a list of items that are not unpacking correctly.
      5. The 1-API Key may be required for some calls.
         5.1 - API Key: https://cloud.google.com/docs/authentication/api-keys
      6. The 1-Developer Token may be required for some calls.
         6.1 - Developer Token: https://developers.google.com/google-ads/api/docs/first-call/dev-token
      7. Give BigQuery dataset and table where response will be written.
      8. All API calls are based on 1-discovery document, for example the 2-Campaign Manager API.
         8.1 - discovery document: https://developers.google.com/discovery/v1/reference
         8.2 - Campaign Manager API: https://developers.google.com/display-video/api/reference/rest/v1/advertisers/list
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-api", help="See developer guide.", default='displayvideo')
  parser.add_argument("-version", help="Must be supported version.", default='v1')
  parser.add_argument("-function", help="Full function dot notation path.", default='advertisers.list')
  parser.add_argument("-kwargs", help="Dictionray object of name value pairs.", default={'partnerId': 234340})
  parser.add_argument("-kwargs_remote", help="Fetch arguments from remote source.", default={})
  parser.add_argument("-api_key", help="Associated with a Google Cloud Project.", default='')
  parser.add_argument("-developer_token", help="Associated with your organization.", default='')
  parser.add_argument("-login_customer_id", help="Associated with your Adwords account.", default='')
  parser.add_argument("-dataset", help="Existing dataset in BigQuery.", default='')
  parser.add_argument("-table", help="Table to write API call results to.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_google_api_to_bigquery(config, args.auth_read, args.api, args.version, args.function, args.kwargs, args.kwargs_remote, args.api_key, args.developer_token, args.login_customer_id, args.dataset, args.table)
