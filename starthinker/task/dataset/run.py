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


from starthinker.util.bigquery import datasets_access
from starthinker.util.bigquery import datasets_create
from starthinker.util.bigquery import datasets_delete


def dataset(config, task):
  if config.verbose:
    print('DATASET', config.project, task['dataset'])

  if task.get('delete', False):
    if config.verbose:
      print('DATASET DELETE')
    # In order to fully delete a dataset, it needs to first have all tables
    # deleted, which is done with the delete_contents=True, and then the actual
    # dataset can be deleted, which is done with delete_contents=false.
    datasets_delete(
        config,
        task['auth'],
        config.project,
        task['dataset'],
        delete_contents=True
    )
    datasets_delete(
        config,
        task['auth'],
        config.project,
        task['dataset'],
        delete_contents=False
    )
  else:
    if task.get('clear', False):
      if config.project:
        print('DATASET CLEAR')
      datasets_delete(
          config,
          task['auth'],
          config.project,
          task['dataset'],
          delete_contents=True
      )

    if config.verbose:
      print('DATASET CREATE')
    datasets_create(
        config,
        task['auth'],
        config.project,
        task['dataset']
    )

    if config.verbose:
      print('DATASET ACCESS')
    datasets_access(
        config,
        task['auth'],
        config.project,
        task['dataset'],
        emails=task.get('emails', []),
        groups=task.get('groups', [])
    )
