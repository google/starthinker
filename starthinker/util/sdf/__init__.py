###########################################################################
#
#  Copyright 2019 Google Inc.
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

from starthinker.util.auth import get_service
from googleapiclient.http import MediaIoBaseDownload
from starthinker.util.data import get_rows
from starthinker.util.csv import column_header_sanitize
from starthinker.util.bigquery import io_to_table, table_create, table_exists
from starthinker.util.sdf.schema.Lookup import SDF_Field_Lookup
from starthinker.util.google_api import API_DV360_Beta


def sdf_download(auth, version, partner_id, file_types, filter_type, filter_ids_obj):
  #Read Filter Ids
  filter_ids = list(get_rows(auth, filter_ids_obj))

  body = {
    "version": version,
    "partnerId": partner_id,
    "parentEntityFilter": {
      "fileType": file_types,
      "filterType": filter_type,
      "filterIds": filter_ids
    },
    "idFilter": None
  }

  operation = API_DV360_Beta(auth).sdfdownloadtasks().create(body=body).execute()

  if operation or 'name' not in operation:
    request = API_DV360_Beta(auth).sdfdownloadtasks().operations().get(name=operation['name'])

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

  return download_media('user', response['response']['resourceName']) 


def sdf_to_bigquery(sdf_zip_file, project_id, dataset, time_partitioned_table, create_single_day_table):
  with zipfile.ZipFile(sdf_zip_file) as d: 
    file_names = d.namelist()
    for file_name  in file_names:
      with d.open(file_name) as file:
        header = file.read().split(b'\n')[0]
        schema = sdf_schema(header.decode('utf-8').split(','))
        wrapper = io.TextIOWrapper(file, encoding='utf-8')
        table_name = file_name.split('.')[0].replace('-','_')

        # Check if each SDF should have a dated table
        if create_single_day_table:
          table_name_dated = table_name + date.today().strftime("%Y_%m_%d")
          
          # Create table and upload data
          table_create('service', project_id, dataset, table_name_dated)    
          io_to_table('service', project_id, dataset, table_name_dated, wrapper, 
            schema=schema, 
            skip_rows=1, 
            disposition='WRITE_TRUNCATE')

        # Create end result table if it doesn't already exist
        if not table_exists('service', project_id, dataset, table_name):
          table_create('service', project_id, dataset, table_name, is_time_partition=time_partitioned_table)

        io_to_table('service', project_id, dataset, table_name, wrapper, 
          schema=schema, 
          skip_rows=1, 
          disposition='WRITE_APPEND' if time_partitioned_table else 'WRITE_TRUNCATE')


def sdf_schema(header):
  schema = []

  for h in header:
    schema.append({ 
      'name':column_header_sanitize(h), 
      'type':SDF_Field_Lookup.get(h, 'STRING'), 
      'mode':'NULLABLE' 
    })

  return schema 


def download_media(auth, resource_name):
  downloadRequest = API_DV360_Beta(auth).media().download_media(resourceName=resource_name).execute(run=False)

  # Create output stream for downloaded file
  outStream = io.BytesIO()

  # Make downloader object
  downloader = MediaIoBaseDownload(outStream, downloadRequest)

  # Download media file in chunks until finished
  download_finished = False
  while download_finished is False:
    _, download_finished = downloader.next_chunk()

  return outStream
