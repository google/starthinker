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

from starthinker.util.project import project
from starthinker.util.sdf import sdf_download, sdf_to_bigquery


@project.from_parameters
def sdf():
  if project.verbose:
    print('SDF')

  # Download sdf files
  sdf_zip_file = sdf_download(project.task['auth'], project.task['version'],
                              project.task['partner_id'],
                              project.task['file_types'],
                              project.task['filter_type'],
                              project.task['read']['filter_ids'])

  # Load data into BigQuery
  sdf_to_bigquery(sdf_zip_file, project.id, project.task['dataset'],
                  project.task['time_partitioned_table'],
                  project.task['create_single_day_table'],
                  project.task.get('table_suffix', ''))


if __name__ == '__main__':
  sdf()
