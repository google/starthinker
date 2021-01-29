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
from starthinker.util.project import project


@project.from_parameters
def dataset():
  if project.verbose:
    print('DATASET', project.id, project.task['dataset'])

  if project.task.get('delete', False):
    if project.verbose:
      print('DATASET DELETE')
    # In order to fully delete a dataset, it needs to first have all tables
    # deleted, which is done with the delete_contents=True, and then the actual
    # dataset can be deleted, which is done with delete_contents=false.
    datasets_delete(
        project.task['auth'],
        project.id,
        project.task['dataset'],
        delete_contents=True
    )
    datasets_delete(
        project.task['auth'],
        project.id,
        project.task['dataset'],
        delete_contents=False
    )
  else:
    if project.task.get('clear', False):
      if project.verbose:
        print('DATASET CLEAR')
      datasets_delete(
          project.task['auth'],
          project.id,
          project.task['dataset'],
          delete_contents=True
      )

    if project.verbose:
      print('DATASET CREATE')
    datasets_create(
        project.task['auth'],
        project.id,
        project.task['dataset']
    )

    if project.verbose:
      print('DATASET ACCESS')
    datasets_access(
        project.task['auth'],
        project.id,
        project.task['dataset'],
        emails=project.task.get('emails', []),
        groups=project.task.get('groups', [])
    )


if __name__ == '__main__':
  dataset()
