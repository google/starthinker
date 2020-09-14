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
import textwrap
import pprint
import json

from starthinker.util.project import project
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
          - python google_api/helper.py -api doubleclickbidmanager -version v1 -function queries.getquery -kwargs '{ "queryId": 132865172 }' -u [credentials path]

        - Pull a list of placements:
          - https://developers.google.com/doubleclick-advertisers/v3.3/placements/list
          - python task/google_api/helper.py -api dfareporting -version v3.3 -function placements.list -kwargs '{ "profileId":2782211 }' -u [credentials path]

  """))

  # get parameters
  parser.add_argument('-api', help='api to run, name of product api')
  parser.add_argument('-version', help='version of api')
  parser.add_argument('-function', help='function to call in api')
  parser.add_argument('-uri', help='function to call in api', default=None)
  parser.add_argument(
      '-kwargs',
      help='kwargs to pass to function, json string of name:value pairs')
  parser.add_argument(
      '--iterate', help='set to true to force iteration', action='store_true')

  # initialize project ( used to load standard credentials parameters )
  project.from_commandline(parser=parser, arguments=('-u', '-c', '-s', '-v'))

  # the api wrapper takes parameters as JSON
  job = {
      'auth': 'service' if project.args.service else 'user',
      'api': project.args.api,
      'version': project.args.version,
      'function': project.args.function,
      'uri': project.args.uri,
      'kwargs': json.loads(project.args.kwargs),
      'iterate': project.args.iterate,
  }

  # run the API call
  results = API(job).execute()

  # display results
  if project.args.iterate:
    for result in results:
      pprint.PrettyPrinter().pprint(result)
  else:
    pprint.PrettyPrinter().pprint(results)


if __name__ == '__main__':
  main()
