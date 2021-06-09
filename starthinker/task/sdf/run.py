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

from starthinker.util.project import from_parameters
from starthinker.util.sdf import sdf_download, sdf_to_bigquery


@from_parameters
def sdf(project, task):
  if project.verbose:
    print('SDF')

  # Download sdf files
  sdf_zip_file = sdf_download(task['auth'], task['version'],
                              task['partner_id'],
                              task['file_types'],
                              task['filter_type'],
                              task['read']['filter_ids'])

  # Load data into BigQuery
  sdf_to_bigquery(sdf_zip_file, project.id, task['dataset'],
                  task['time_partitioned_table'],
                  task['create_single_day_table'],
                  task.get('table_suffix', ''))


if __name__ == '__main__':
  sdf()
