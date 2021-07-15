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

import time
import csv
import io
import zipfile
import io

from datetime import date
from googleapiclient.http import MediaIoBaseDownload

from starthinker.util.bigquery import rows_to_table, table_create, table_exists
from starthinker.util.csv import column_header_sanitize, csv_to_rows
from starthinker.util.data import get_rows
from starthinker.util.google_api import API_DV360
from starthinker.util.sdf_schema import SDF_Field_Lookup


# Desired file name: InsertionOrders, LineItems, *Camel case of the filetype
def get_single_sdf_rows(config, auth, version, partner_id, file_types, filter_type,
                        filter_ids_obj, desired_file_type):
  sdf_zip_file = sdf_download(config, auth, version, partner_id, file_types,
                              filter_type, filter_ids_obj)

  with zipfile.ZipFile(sdf_zip_file, 'r', zipfile.ZIP_DEFLATED) as d:
    file_names = d.namelist()
    for file_name in file_names:

      # make sure to only get the one file
      if desired_file_type != file_name.split('-')[1].split(
          '.')[0] or 'Skipped' in file_name:
        continue

      if config.verbose:
        print('SDF: Loading: ' + file_name)
      with d.open(file_name) as sdf_file:
        rows = csv_to_rows(sdf_file.read().decode('utf-8'))

        return rows


def sdf_download(config, auth, version, partner_id, file_types, filter_type,
                 filter_ids_obj):
  #Read Filter Ids
  filter_ids = list(get_rows(config, auth, filter_ids_obj))

  body = {
      'version': version,
      'partnerId': partner_id,
      'parentEntityFilter': {
          'fileType': file_types,
          'filterType': filter_type,
          'filterIds': filter_ids
      },
      'idFilter': None
  }

  operation = API_DV360(config, auth).sdfdownloadtasks().create(body=body).execute()

  if operation and 'name' in operation:
    request = API_DV360(config, auth).sdfdownloadtasks().operations().get(
        name=operation['name'])

    # This is the eng recommended way of getting the operation
    while True:
      response = request.execute()
      if 'done' in response and response['done']:
        break
      time.sleep(30)
  else:
    print('error')

  if 'error' in response:
    raise Exception(response['error']['message'])

  return download_media(config, 'user', response['response']['resourceName'])


def add_seekable_to_file(f):
  if not hasattr(f, 'seekable'):
    f.seekable = lambda: True


def sdf_to_bigquery(config,
                    auth,
                    sdf_zip_file,
                    project_id,
                    dataset,
                    time_partitioned_table,
                    create_single_day_table,
                    table_suffix=''):
  with zipfile.ZipFile(sdf_zip_file, 'r', zipfile.ZIP_DEFLATED) as d:
    file_names = d.namelist()
    for file_name in file_names:
      if config.verbose:
        print('SDF: Loading: ' + file_name)
      with d.open(file_name) as sdf_file:
        rows = csv_to_rows(sdf_file.read().decode('utf-8'))
        if not rows:
          if config.verbose:
            print('SDF: Empty file ' + file_name)
          continue
        table_name = file_name.split('.')[0].replace('-', '_') + table_suffix
        schema = sdf_schema(next(rows))

        # Check if each SDF should have a dated table
        if create_single_day_table:
          table_name_dated = table_name + date.today().strftime('%Y_%m_%d')

          # Create table and upload data
          table_create(auth, project_id, dataset, table_name_dated)
          rows_to_table(
              config,
              auth,
              project_id,
              dataset,
              table_name_dated,
              rows,
              schema=schema,
              skip_rows=1,
              disposition='WRITE_TRUNCATE')

        # Create end result table if it doesn't already exist
        if not table_exists(config, auth, project_id, dataset, table_name):
          table_create(
              config,
              auth,
              project_id,
              dataset,
              table_name,
              is_time_partition=time_partitioned_table)

        rows_to_table(
             config,
            auth,
            project_id,
            dataset,
            table_name,
            rows,
            schema=schema,
            skip_rows=1,
            disposition='WRITE_APPEND'
            if time_partitioned_table else 'WRITE_TRUNCATE')


def sdf_schema(header):
  schema = []

  for h in header:
    schema.append({
        'name': column_header_sanitize(h),
        'type': SDF_Field_Lookup.get(h, 'STRING'),
        'mode': 'NULLABLE'
    })

  return schema


def download_media(config, auth, resource_name):
  if config.verbose:
    print('SDF: Start Download')

  downloadRequest = API_DV360(config, auth).media().download_media(
      resourceName=resource_name).execute(run=False)

  # Create output stream for downloaded file
  outStream = io.BytesIO()

  # Make downloader object
  downloader = MediaIoBaseDownload(outStream, downloadRequest)

  # Download media file in chunks until finished
  download_finished = False
  while download_finished is False:
    _, download_finished = downloader.next_chunk()

  if config.verbose:
    print('SDF: End Download')

  return outStream
