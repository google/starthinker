import argparse
import pprint

from util.project import project
from util.google_api import API_DBM
from util.dcm import account_profile_kwargs


if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('report', help='report ID to pull the achema, or "list" to get index')

  # initialize project
  project.load(parser=parser)
  auth = 'service' if project.args.service else 'user'

  # get report
  if project.args.report == 'list':
    for report in API_DBM(auth, iterate=True).queries().listqueries().execute():
      pprint.PrettyPrinter().pprint(report)
  else:
    report = API_DBM(auth).queries().getquery(queryId=project.args.report).execute()
    pprint.PrettyPrinter().pprint(report)

'''
Example:
python dbm/helper.py list -u /Users/kenjora/.credentials/kenjora_user.json -c /Users/kenjora/.credentials/kenjora_client.json
'''
