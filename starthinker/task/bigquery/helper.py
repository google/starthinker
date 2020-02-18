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


"""Command line to get table schema from BigQuery.

This is a helper to help developers debug and create tables. 

- To get table schema: `python bigquery/helper.py --project [id] --dataset [name] --table [name] -u [credentials] -s [credentials]`

"""

import json
import argparse

from starthinker.util.project import project
from starthinker.util.bigquery import table_to_schema

if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--dataset', help='name of BigQuery dataset', default=None)
  parser.add_argument('--table', help='name of BigQuery table', default=None)

  # initialize project
  project.from_commandline(parser=parser)
  auth = 'service' if project.args.service else 'user'

  # print schema
  print(json.dumps(table_to_schema(auth, project.id, project.args.dataset, project.args.table)['fields'], indent=2))
