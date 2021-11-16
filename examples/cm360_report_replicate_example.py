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
from starthinker.task.drive.run import drive
from starthinker.task.dataset.run import dataset
from starthinker.task.cm_report_replicate.run import cm_report_replicate


def recipe_cm360_report_replicate(config, auth_read, recipe_name, auth_write, account, recipe_slug, report_id, report_name, delete, Aggregate):
  """Replicate a report across multiple networks and advertisers.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       recipe_name (string) - Sheet to read ids from.
       auth_write (authentication) - Credentials used for writing data.
       account (integer) - CM network id.
       recipe_slug (string) - NA
       report_id (integer) - CM template report id, for template
       report_name (string) - CM template report name, empty if using id instead.
       delete (boolean) - Use only to reset the reports if setup changes.
       Aggregate (boolean) - Append report data to existing table, requires Date column.
  """

  drive(config, {
    'auth':'user',
    'copy':{
      'source':'https://docs.google.com/spreadsheets/d/1Su3t2YUWV_GG9RD63Wa3GNANmQZswTHstFY6aDPm6qE/',
      'destination':recipe_name
    }
  })

  dataset(config, {
    'auth':auth_write,
    'dataset':recipe_slug
  })

  cm_report_replicate(config, {
    'auth':auth_read,
    'report':{
      'account':account,
      'id':report_id,
      'name':report_name,
      'delete':delete
    },
    'replicate':{
      'sheets':{
        'sheet':recipe_name,
        'tab':'Accounts',
        'range':''
      }
    },
    'write':{
      'bigquery':{
        'dataset':recipe_slug,
        'is_incremental_load':Aggregate
      }
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Replicate a report across multiple networks and advertisers.

      1. Provide the name or ID of an existing report.
      2. Run the recipe once to generate the input sheet called .
      3. Enter network and advertiser ids to replicate the report.
      4. Data will be written to BigQuery &gt;  &gt;  &gt; _All
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-recipe_name", help="Sheet to read ids from.", default='')
  parser.add_argument("-auth_write", help="Credentials used for writing data.", default='service')
  parser.add_argument("-account", help="CM network id.", default='')
  parser.add_argument("-recipe_slug", help="", default='')
  parser.add_argument("-report_id", help="CM template report id, for template", default='')
  parser.add_argument("-report_name", help="CM template report name, empty if using id instead.", default='')
  parser.add_argument("-delete", help="Use only to reset the reports if setup changes.", default=False)
  parser.add_argument("-Aggregate", help="Append report data to existing table, requires Date column.", default=False)


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm360_report_replicate(config, args.auth_read, args.recipe_name, args.auth_write, args.account, args.recipe_slug, args.report_id, args.report_name, args.delete, args.Aggregate)
