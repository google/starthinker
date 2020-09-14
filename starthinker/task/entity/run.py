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
"""Script that executes { "entity":{...}} task.

This script translates JSON instructions into operations on Entity Read File
transfer to BigQuery.

### CAUTION

ONLY PARTNER LEVEL LOG FILES ARE MOVED, no advertiser filters in
this script. To filter by advertiser, add queries within BigQuery to create
additional tables.

See: https://developers.google.com/bid-manager/guides/entity-read/format-v2

### Table Names And Entities

The prefix value specified in JSON is used to name each table and avoid
collisions.  All tables will be prefixed with "Entity_" by default. For
example 'Campaign' Entity Read becomes, 'Entity_Campaign'. You can
modify the preifx in the JSON script.

The following Entity Read Files Can Be Specified:

- Campaign
- LineItem
- Creative
- UserList
- Partner
- Advertiser
- InsertionOrder
- Pixel
- InventorySource
- CustomAffinity
- UniversalChannel
- UniversalSite
- SupportedExchange
- DataPartner
- GeoLocation
- Language
- DeviceCriteria
- Browser
- Isp

### Notes

- Files are moved using an in memory buffer, controlled by BUFFER_SCALE in
config.py.
- Bigger buffer means faster move but needs a machine with more memory.
- These transfers take a long time, two jobs can write over each other.
- The tables are filled over time, if you need instant data switch, use table
copy after job.

"""

from starthinker.config import BUFFER_SCALE
from starthinker.util.project import project
from starthinker.util.storage import object_get_chunks
from starthinker.util.bigquery import json_to_table
from starthinker.util.data import get_rows
from starthinker.task.entity.schema import Entity_Schema_Lookup

CHUNK_SIZE = int(200 * 1024000 * BUFFER_SCALE)  # 200 MB * scale in config.py
PUBLIC_FILES = ('SupportedExchange', 'DataPartner', 'UniversalSite',
                'GeoLocation', 'Language', 'DeviceCriteria', 'Browser', 'Isp')


def get_entity(path):
  delimiter = ',\r\r'
  first = True
  view = ''

  for chunk in object_get_chunks(project.task['auth'], path, CHUNK_SIZE):
    # read the next chunk, remove all newlines, leaving only '\r\r' between records ( clever use of non display characters for parsing )
    view += chunk.decode().replace('\n', '')

    # first time through, scrap the leading bracket
    if first:
      view = view.strip('[\r\r')
      first = False

    # after replacing all newlines, only '\r\r' are left, clever Googlers
    end = view.rfind(delimiter)
    if end > -1:
      yield view[:end].replace(delimiter, '\n')
      view = view[end + 1:]

  # last one never delimits, so opportunity to trim extra bracket
  yield view.strip('\r\r]')


def move_entity(project, path, table, schema, disposition):
  if 'prefix' in project.task:
    table = '%s_%s' % (project.task['prefix'], table)

  if 'out' in project.task:
    auth = project.task['out']['bigquery'].get('auth', project.task['auth'])
    dataset = project.task['out']['bigquery']['dataset']
  # deprecated, need out to allow auth mix on in and out
  else:
    auth = project.task['auth']
    dataset = project.task['dataset']

  # read the entity file in parts
  records = get_entity(path)

  # write each part
  json_to_table(
      auth,
      project.id,
      dataset,
      table,
      records,
      schema=schema,
      disposition=disposition)
  # after first write switch to append
  #disposition = 'WRITE_APPEND'


@project.from_parameters
def entity():
  if project.verbose:
    print('ENTITY')

  # legacy translations ( changed partners, advertisers to accounts with "partner_id:advertiser_id" )
  if 'partner_id' in project.task:
    project.task['accounts'] = [project.task['partner_id']]

  # create entities
  for entity in project.task['entities']:
    if project.verbose:
      print('ENTITY:', entity)

    # write public files only once
    if entity in PUBLIC_FILES:
      path = 'gdbm-public:entity/%s.0.%s.json' % (
          project.date.strftime('%Y%m%d'), entity)
      schema = Entity_Schema_Lookup[entity]
      move_entity(project, path, entity, schema, 'WRITE_TRUNCATE')

    # supports multiple partners, first one resets table, others append
    else:
      disposition = 'WRITE_TRUNCATE'
      for account in get_rows('user', project.task['partners']):

        #for account in project.task['accounts']:
        # if advertiser given do not run it ( SAFETY )
        if ':' in str(account):
          print('WARNING: Skipping advertiser: ', account)
          continue
        if project.verbose:
          print('PARTNER:', account)
        path = 'gdbm-%s:entity/%s.0.%s.json' % (
            account, project.date.strftime('%Y%m%d'), entity)
        schema = Entity_Schema_Lookup[entity]
        move_entity(project, path, entity, schema, disposition)
        disposition = 'WRITE_APPEND'


if __name__ == '__main__':
  entity()
