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

import argparse
import json
import pprint
import textwrap

from starthinker.util.configuration import commandline_parser, Configuration
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.google_api import API


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Command line interface for running Google API calls.  Any API works.  Allows developers to quickly test
      and debug API calls before building them into scripts.  Useful for debugging permission or call errors.

      Examples:
        - Pull a DBM report via API.
          - https://developers.google.com/bid-manager/v1/queries/getquery
          - python google_api.py -api doubleclickbidmanager -version v1 -function queries.getquery -kwargs '{ "queryId": 132865172 }' -u [credentials path]

        - Pull a list of placements:
          - https://developers.google.com/doubleclick-advertisers/v3.3/placements/list
          - python google_api.py -api dfareporting -version v3.3 -function placements.list -kwargs '{ "profileId":2782211 }' -u [credentials path]

        - Show schema for Campaign Manager advertiser list endpoint.
        - https://developers.google.com/doubleclick-advertisers/v3.4/advertisers/list
        - python google_api.py -api dfareporting -version v3.4 -function advertisers.list --schema
        - python google_api.py -api dfareporting -version v3.4 -function Advertiser --object
        - python google_api.py -api dfareporting -version v3.4 -function Advertiser --struct

  """))

  # get parameters
  parser.add_argument('-api', help='api to run, name of product api')
  parser.add_argument('-version', help='version of api')
  parser.add_argument('-function', help='function or resource to call in api')
  parser.add_argument('-uri', help='uri to use in api', default=None)
  parser.add_argument(
      '-developer-token',
      help='developer token to pass in header',
      default=None)
  parser.add_argument(
      '-login-customer-id',
      help='customer to log in with when manipulating an MCC',
      default=None)
  parser.add_argument(
      '-kwargs',
      help='kwargs to pass to function, json string of name:value pairs')
  parser.add_argument('--iterate', help='force iteration', action='store_true')
  parser.add_argument('--limit', type=int, help='optional, number of records to return', default=None)
  parser.add_argument(
      '--schema',
      help='return function as BigQuery schema, function = [endpoint.method]',
      action='store_true')
  parser.add_argument(
    '--object',
    help='return resource as JSON discovery document, function = [resource]',
    action='store_true'
  )
  parser.add_argument(
    '--struct',
    help='return resource as BigQuery structure, function = [resource]',
    action='store_true'
  )

  # initialize project
  parser = commandline_parser(parser, arguments=('-u', '-c', '-s', '-k', '-v'))
  args = parser.parse_args()
  config = Configuration(
    user=args.user,
    client=args.client,
    service=args.service,
    key=args.key,
    verbose=args.verbose
  )

  # show schema
  if args.object:
    print(json.dumps(Discovery_To_BigQuery(args.api, args.version).resource_json(args.function), indent=2, default=str))

  elif args.struct:
    print(Discovery_To_BigQuery(args.api, args.version).resource_struct(args.function))

  # show schema
  elif args.schema:
    print(json.dumps(Discovery_To_BigQuery(args.api, args.version).method_schema(args.function), indent=2, default=str))

  # or fetch results
  else:

    # the api wrapper takes parameters as JSON
    job = {
      'auth': 'service' if args.service else 'user',
      'api': args.api,
      'version': args.version,
      'function': args.function,
      'key': args.key,
      'uri': args.uri,
      'kwargs': json.loads(args.kwargs),
      'headers': {},
      'iterate': args.iterate,
      'limit': args.limit,
    }

    if args.developer_token:
      job['headers']['developer-token'] = args.developer_token

    if args.login_customer_id:
      job['headers']['login-customer-id'] = args.login_customer_id

    # run the API call
    results = API(config, job).execute()

    # display results
    if args.iterate:
      for result in results:
        pprint.PrettyPrinter().pprint(result)
    else:
      pprint.PrettyPrinter().pprint(results)


if __name__ == '__main__':
  main()
