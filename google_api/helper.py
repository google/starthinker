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

  # initialize project
  project.load(parser=parser)

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

''' 
Examples

python google_api/helper.py -api doubleclickbidmanager -version v1 -function queries.getquery -kwargs '{ "queryId": 132865172 }' -u /usr/local/google/home/kenjora/.credentials/kenjora_user.json

python google_api/helper.py -api dfareporting -version v3.0 -function placements.list -kwargs '{ "profileId":2782211 }' -u /usr/local/google/home/kenjora/.credentials/kenjora_user.json
'''
