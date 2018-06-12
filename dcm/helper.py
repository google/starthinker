import argparse
import pprint

from util.project import project
from util.google_api import API_DCM
from util.dcm import account_profile_kwargs


if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('account', help='account ID to use to pull the report.')
  parser.add_argument('report', help='report ID to pull the achema, or "list" to get index')
  parser.add_argument('--files', '-f', help='list files within the report.', action='store_true')

  # initialize project
  project.load(parser=parser)
  auth = 'service' if project.args.service else 'user'

  # get report
  if project.args.report == 'list':
    kwargs = account_profile_kwargs(auth, project.args.account)
    for report in API_DCM(auth).reports().list(**kwargs).execute():
      pprint.PrettyPrinter().pprint(report)
  else:
    if project.args.files:
      kwargs = account_profile_kwargs(auth, project.args.account, reportId=project.args.report)
      for report_file in API_DCM(auth).reports().files().list(**kwargs).execute():
        pprint.PrettyPrinter().pprint(report_file)
    else: 
      kwargs = account_profile_kwargs(auth, project.args.account, reportId=project.args.report)
      report = API_DCM(auth).reports().get(**kwargs).execute()
      pprint.PrettyPrinter().pprint(report)

'''
Example:
python dcm/helper.py 7480 132847265 -u /Users/kenjora/.credentials/kenjora_user.json --files
'''
