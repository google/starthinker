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
from starthinker.task.sheets.run import sheets
from starthinker.task.video.run import video


def recipe_video(config, auth_read, sheet, tab, project, dataset, table):
  """Add images, text, and audio to videos.

     Args:
       auth_read (authentication) - Credentials used for reading data.
       sheet (string) - Name or URL of sheet.
       tab (string) - Name of sheet tab.
       project (string) - Google Cloud Project Identifier.
       dataset (string) - Name of dataset.
       table (string) - Name of table.
  """

  sheets(config, {
    '__comment__':'Copy the tamplate sheet to the users sheet.  If it already exists, nothing happens.',
    'auth':auth_read,
    'template':{
      'sheet':'https://docs.google.com/spreadsheets/d/1BXRHWz-1P3gNS92WZy-3sPZslU8aalXa8heOgygWEFs/edit#gid=0',
      'tab':'Video'
    },
    'sheet':sheet,
    'tab':tab
  })

  video(config, {
    '__comment__':'Read video effects and values from sheet and/or bigquery.',
    'auth':auth_read,
    'sheets':{
      'sheet':sheet,
      'tab':tab
    },
    'bigquery':{
      'project':project,
      'dataset':dataset,
      'table':table
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Add images, text, and audio to videos.

      1. Provide either a sheet or a BigQuery table.
      2. Each video edit will be read from the sheet or table.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_read", help="Credentials used for reading data.", default='user')
  parser.add_argument("-sheet", help="Name or URL of sheet.", default='')
  parser.add_argument("-tab", help="Name of sheet tab.", default='')
  parser.add_argument("-project", help="Google Cloud Project Identifier.", default='')
  parser.add_argument("-dataset", help="Name of dataset.", default='')
  parser.add_argument("-table", help="Name of table.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_video(config, args.auth_read, args.sheet, args.tab, args.project, args.dataset, args.table)
