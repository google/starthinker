import pprint
import argparse

from util.auth import get_service
from util.project import project
from util.dbm import report_get, report_list

if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('report', help='report ID to pull schema, or "list" to get index')
  parser.add_argument('--creds', help='path to credentials file', default=None)
  parser.add_argument('--json', help='path to project json file', default=None)
  parser.add_argument('--auth', '-a', help='user (default) or service.', default='user')
  parser.add_argument('--format', '-f', help='print StarThinker json instead of DBM json.', action='store_true')

  args = parser.parse_args()

  # initialize project from credentials
  if args.creds:
    if args.auth == 'user': project.initialize(_user=args.creds)
    elif args.auth == 'service': project.initialize(_service=args.creds)
  # initialize from project file
  elif args.json:
    project.initialize(args.json)
  else:
    print 'Please provide --creds or --json'
    exit()

  if args.report == 'list':
    for query in report_list(args.auth):
      print query['queryId'], query['metadata']['title']
  else:
    report = report_get(args.auth, report_id=args.report)
    if args.format:
      report = {
        'title':report['metadata']['title'],
        'type':report['params']['type'],
        'filters':report['params']['filters'],
        'dimensions':report['params']['groupBys'],
        'metrics':report['params']['metrics'],
      }   
    pprint.PrettyPrinter().pprint(report)
