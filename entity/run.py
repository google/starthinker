###########################################################################
#
#  Copyright 2017 Google Inc.
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

# https://developers.google.com/bid-manager/guides/entity-read/format-v2

import json
import os
import sys
import time
from datetime import datetime, timedelta
from io import BytesIO

from util.project import project
from util.storage import object_get_chunks
from util.bigquery import local_file_to_table, datasets_create, csv_to_table
from entity.schema import Entity_Schema_Lookup

CHUNK_SIZE = 1024000 * 200  # 200 MB
PUBLIC_FILES = ('SupportedExchange', 'DataPartner', 'UniversalSite',
                'GeoLocation', 'Language', 'DeviceCriteria', 'Browser', 'Isp')


def get_entity(path):
  delimiter = ',\r\r'
  first = True
  view = ''

  for chunk in object_get_chunks(project.task['auth'], path, CHUNK_SIZE):
    # read the next chunk, remove all newlines, leaving only '\r\r' between records ( clever use of non display characters for parsing )
    view += chunk.getvalue().replace('\n', '')

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
  if project.task['version'] >= 0.2 and 'prefix' in project.task: table = '%s_%s' % (project.task['prefix'], table)

  # read the entity file in parts
  for data in get_entity(path):
    # write each part
    csv_to_table(
        project.task.get('out', project.task)['auth'],
        project.id,
        project.task.get('out', project.task)['dataset'],
        table,
        BytesIO(data),
        schema=schema,
        structure='NEWLINE_DELIMITED_JSON',
        disposition=disposition)
    disposition = 'WRITE_APPEND'


def entity():
  if project.verbose: print 'ENTITY'

  # legacy translations ( changed partners, advertisers to accounts with "partner_id:advertiser_id" )
  if 'partner_id' in project.task:
    project.task['accounts'] = [project.task['partner_id']]

  # create entities
  for entity in project.task['entities']:
    if project.verbose: print 'ENTITY:', entity

    # write public files only once
    if entity in PUBLIC_FILES:
      path = 'gdbm-public:entity/%s.0.%s.json' % (project.date.strftime('%Y%m%d'), entity)
      schema = Entity_Schema_Lookup[entity]
      move_entity(project, path, entity, schema, 'WRITE_TRUNCATE')

    # supports multiple partners, first one resets table, others append
    else:
      disposition = 'WRITE_TRUNCATE'
      for account in project.task['accounts']:
        # if advertiser given do not run it ( SAFETY )
        if ':' in str(account):
          print 'WARNING: Skipping advertiser: ', account
          continue
        if project.verbose: print 'PARTNER:', account
        path = 'gdbm-%s:entity/%s.0.%s.json' % (account, project.date.strftime('%Y%m%d'), entity)
        schema = Entity_Schema_Lookup[entity]
        move_entity(project, path, entity, schema, disposition)
        disposition = 'WRITE_APPEND'


if __name__ == '__main__':
  project.load('entity')
  entity()
