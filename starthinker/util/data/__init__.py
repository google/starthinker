###########################################################################
#
#  Copyright 2018 Google Inc.
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


"""Processes standard read / write JSON block for dynamic loading of data.

The goal is to create standard re-usable input output blocks.  These functions
are extensible, and should include additional sources and destinations over time.
Key benfits include:

  - Allows single point API revision for common read / write tasks.
  - Reduce risk with test case coverage for this module inherited by recipes using it.
  - Using standard blocks is a big time savings.

"""


import json
import pysftp
import datetime
import os
import sys
import traceback
from StringIO import StringIO

from starthinker.util.project import project
from starthinker.util.storage import parse_path, makedirs_safe, object_put, bucket_create
from starthinker.util.bigquery import query_to_rows, rows_to_table, json_to_table, incremental_rows_to_table
from starthinker.util.sheets import sheets_read, sheets_write, sheets_clear
from starthinker.util.csv import rows_to_csv


def get_rows(auth, source):
  """Processes standard read JSON block for dynamic loading of data.
  
  Allows us to quickly pull a column or columns of data from and use it as an input 
  into a script. For example pull a list of ids from bigquery and act on each one.

  - When pulling a single column specify single_cell = True. Returns list AKA values. 
  - When pulling a multiple columns specify single_cell = False. Returns list of lists AKA rows.
  - Values are always given as a list ( single_cell will trigger necessary wrapping ).
  - Values, bigquery, sheet are optional, if multiple given result is one continous iterator.
  - Extensible, add a handler to define a new source ( be kind update the documentation json ).

  Include the following JSON in a recipe, then in the run.py handler when
  encountering that block pass it to this function and use the returned results.
  
    from utils.data import get_rows
  
    var_json = {
      "in":{
        "single_cell":[ boolean ],
        "values": [ integer list ],
        "bigquery":{
          "dataset": [ string ],
          "query": [ string ],
          "legacy":[ boolean ]
        },
        "sheet":{
          "url":[ string - full URL, suggest using share link ],
          "tab":[ string ],
          "range":[ string - A1:A notation ]
        }
      } 
    } 
  
    values = get_rows('user', var_json)
  
  Or you can use it directly with project singleton.
  
    from util.project import project
    from utils.data import get_rows
  
    @project.from_parameters
    def something():
      values = get_rows(project.task['auth'], project.task['in'])
  
    if __name__ == "__main__":
      something()
  
  Args:
    auth: (string) The type of authentication to use, user or service.
    source: (json) A json block resembling var_json described above.

  Returns:
    If single_cell is False: Returns a list of row values [[v1], [v2], ... ]
    If single_cell is True: Returns a list of values [v1, v2, ...]
"""

  # if handler points to list, concatenate all the values from various sources into one list
  if isinstance(source, list):  
    for s in source:
      for r in get_rows(auth, s):
        yield r

  # if handler is an endpoint, fetch data
  else:
    if 'values' in source:
      for value in source['values']:
        yield value 

    if 'sheet' in source:
      rows = sheets_read(project.task['auth'], source['sheet']['url'], source['sheet']['tab'], source['sheet']['range'])

      for row in rows:
        yield row[0] if source.get('single_cell', False) else row

    if 'bigquery' in source:
      rows = query_to_rows(
        source['bigquery'].get('auth', auth),
        project.id,
        source['bigquery']['dataset'],
        source['bigquery']['query'],
        legacy=source['bigquery'].get('legacy', False)
      )
      for row in rows:
        yield row[0] if source.get('single_cell', False) else row


def put_rows(auth, destination, filename, rows, variant=''):
  """Processes standard write JSON block for dynamic export of data.
  
  Allows us to quickly write the results of a script to a destination.  For example
  write the results of a DCM report into BigQuery.

  - Will write to multiple destinations if specified.
  - Extensible, add a handler to define a new destination ( be kind update the documentation json ).

  Include the following JSON in a recipe, then in the run.py handler when
  encountering that block pass it to this function and use the returned results.
  
    from utils.data import put_rows
  
    var_json = {
      "out":{
        "bigquery":{
          "dataset": [ string ],
          "table": [ string ]
          "schema": [ json - standard bigquery schema json ],
          "skip_rows": [ integer - for removing header ]
          "disposition": [ string - same as BigQuery documentation ]
        },
        "sheets":{
          "url":[ string - full URL, suggest using share link ],
          "tab":[ string ],
          "range":[ string - A1:A notation ]
          "delete": [ boolean - if sheet range should be cleared before writing ]
        },
        "storage":{
          "bucket": [ string ],
          "path": [ string ]
        },
        "directory":[ string - full path to place to write file ]
      } 
    } 
  
    values = put_rows('user', var_json)
  
  Or you can use it directly with project singleton.
  
    from util.project import project
    from utils.data import put_rows
  
    @project.from_parameters
    def something():
      values = get_rows(project.task['auth'], project.task['out'])
  
    if __name__ == "__main__":
      something()
  
  Args:
    auth: (string) The type of authentication to use, user or service.
    destination: (json) A json block resembling var_json described above.
    filename: (string) A unique filename if writing to medium requiring one, Usually gnerated by script.
    rows ( list ) The data being written as a list object.
    variant ( string ) Appends this to the destination name to create a variant ( for example when downloading multiple tabs in a sheet ).

  Returns:
    If single_cell is False: Returns a list of row values [[v1], [v2], ... ]
    If single_cell is True: Returns a list of values [v1, v2, ...]
"""

  if 'bigquery' in destination:

    if destination['bigquery'].get('format' , 'CSV') == 'JSON':
      json_to_table(
        destination['bigquery'].get('auth', auth),
        destination['bigquery'].get('project_id', project.id),
        destination['bigquery']['dataset'],
        destination['bigquery']['table'] + variant,
        rows,
        destination['bigquery'].get('schema', []),
        destination['bigquery'].get('disposition', 'WRITE_TRUNCATE'),
      )
    
    elif destination['bigquery'].get('is_incremental_load', False) == True:
      incremental_rows_to_table( 
        destination['bigquery'].get('auth', auth),
        destination['bigquery'].get('project_id', project.id),
        destination['bigquery']['dataset'],
        destination['bigquery']['table'] + variant,
        rows,
        destination['bigquery'].get('schema', []),
        destination['bigquery'].get('skip_rows', 1), #0 if 'schema' in destination['bigquery'] else 1),
        destination['bigquery'].get('disposition', 'WRITE_APPEND'),
        billing_project_id=project.id
      )

    else:
      rows_to_table(
        destination['bigquery'].get('auth', auth),
        destination['bigquery'].get('project_id', project.id),
        destination['bigquery']['dataset'],
        destination['bigquery']['table'] + variant,
        rows,
        destination['bigquery'].get('schema', []),
        destination['bigquery'].get('skip_rows', 1), #0 if 'schema' in destination['bigquery'] else 1),
        destination['bigquery'].get('disposition', 'WRITE_TRUNCATE'),
      )

  if 'sheets' in destination:
    if destination['sheets'].get('delete', False): 
      sheets_clear(auth, destination['sheets']['sheet'], destination['sheets']['tab'] + variant, destination['sheets']['range'])
    sheets_write(auth, destination['sheets']['sheet'], destination['sheets']['tab'] + variant, destination['sheets']['range'], rows) 

  if 'directory' in destination:
    file_out = destination['directory'] + variant + filename
    if project.verbose: print 'SAVING', file_out
    makedirs_safe(parse_path(file_out))
    with open(file_out, 'wb') as save_file:
      save_file.write(rows_to_csv(rows).read())

  if 'storage' in destination and destination['storage'].get('bucket') and destination['storage'].get('path'):
    # create the bucket
    bucket_create(auth, project.id, destination['storage']['bucket'])

    # put the file
    file_out = destination['storage']['bucket'] + ':' + destination['storage']['path'] + variant + filename
    if project.verbose: print 'SAVING', file_out
    object_put(auth, file_out, rows_to_csv(rows))

  # deprecated do not use
  if 'trix' in destination:
    trix_update(auth, destination['trix']['sheet_id'], destination['trix']['sheet_range'], rows_to_csv(rows), destination['trix']['clear'])

  if 'email' in destination:
    pass

  if 'sftp' in destination:
    try:
      sys.stderr = StringIO();

      cnopts = pysftp.CnOpts()
      cnopts.hostkeys = None

      file_prefix = 'report'
      if 'file_prefix' in destination['sftp']:
        file_prefix = destination['sftp'].get('file_prefix')
        del destination['sftp']['file_prefix']

      #sftp_configs = destination['sftp']
      #sftp_configs['cnopts'] = cnopts
      #sftp = pysftp.Connection(**sftp_configs)

      sftp = pysftp.Connection(host=destination['sftp']['host'], username=destination['sftp']['username'], password=destination['sftp']['password'], port=destination['sftp']['port'], cnopts=cnopts)

      if 'directory' in destination['sftp']:
        sftp.cwd(destination['sftp']['directory'])

      tmp_file_name = '/tmp/%s_%s.csv' % (file_prefix, datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S'))

      tmp_file = open(tmp_file_name, 'wb')
      tmp_file.write(rows_to_csv(rows).read())
      tmp_file.close()

      sftp.put(tmp_file_name)

      os.remove(tmp_file_name)

      sys.stderr = sys.__stderr__;
    except e:
      print e
      traceback.print_exc()
