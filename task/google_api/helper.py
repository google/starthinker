###########################################################################
# 
#  Copyright 2018 Google Inc.
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


"""Command line interface for running Google API calls.  Any API works.

Allows developers to quickly test and debug API calls before building them
into scripts.  Useful for debugging permission or call errors.

For example, pull a DBM report via API: https://developers.google.com/bid-manager/v1/queries/getquery

python google_api/helper.py -api doubleclickbidmanager -version v1 -function queries.getquery -kwargs '{ "queryId": 132865172 }' -u [credentials path] 

For example, pull a list of placements: https://developers.google.com/doubleclick-advertisers/v3.2/placements/list

python google_api/helper.py -api dfareporting -version v3.2 -function placements.list -kwargs '{ "profileId":2782211 }' -u [credentials path]

"""


import argparse
import pprint
import json

from util.project import project
from util.google_api import API


if __name__ == "__main__":

 # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('-api', help='api to run, name of product api')
  parser.add_argument('-version', help='version of api')
  parser.add_argument('-function', help='function to call in api')
  parser.add_argument('-uri', help='function to call in api', default=None)
  parser.add_argument('-kwargs', help='kwargs to pass to function, json string of name:value pairs')
  parser.add_argument('--iterate', help='set to true to force iteration', action='store_true')

  # initialize project ( used to load standard credentials parameters )
  project.load(parser=parser)

  # the api wrapper takes parameters as JSON
  job = { 
    "auth":'service' if project.args.service else 'user',
    "api":project.args.api,
    "version":project.args.version,
    "function":project.args.function,
    "uri":project.args.uri,
    "kwargs":json.loads(project.args.kwargs),
    "iterate":project.args.iterate,
  }

  results = API(job).execute()

  if project.args.iterate:
    for result in results:
      pprint.PrettyPrinter().pprint(result)
  else:
    pprint.PrettyPrinter().pprint(results)
