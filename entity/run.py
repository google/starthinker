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

import json
import os
import time
from datetime import datetime, timedelta
from io import BytesIO

from util.project import project
from util.storage import object_download, object_get
from util.bigquery.file_processor import FileProcessor
from util.bigquery import local_file_to_table, datasets_create, csv_to_table

dest_folder = '/tmp'
file_processor = FileProcessor()
buff = ''

def merge_list(target, source):
  items = []

  if source <> None and len(source) > 0:
    items += source
  if target <> None and len(target) > 0:
    items += target

  if len(items) > 1:
    if isinstance(items[0], dict):
      merged = {}
      for item in items:
        merge(merged, item)
      return [merged]
    else:
      return items[:1]
  else:
    return items


def merge(a, b, path=None):
  try:
    "merges b into a"
    if path is None: path = []
    for key in b:
      if key in a:
        if isinstance(b[key], list) or isinstance(a[key], list):
          a[key] = merge_list(a[key] if key in a else None, b[key])
        if isinstance(a[key], dict) and isinstance(b[key], dict):
            merge(a[key], b[key], path + [str(key)])
        elif isinstance(a[key], list) and isinstance(b[key], list):
          if (not len(a[key]) == 0 and isinstance(a[key][0], dict)) and (not len(b[key]) == 0 and isinstance(b[key][0], dict)):
            item = {}

            for s in a[key]:
              if isinstance(s, dict):
                merge(item, s)
            for s in b[key]:
              if isinstance(s, dict):
                merge(item, s)

            a[key] = [item]
      elif isinstance(b[key], dict):
        a[key] = {}
        merge(a[key], b[key])
      elif isinstance(b[key], list):
        a[key] = merge_list(None, b[key])
      else:
        a[key] = b[key]
    return a
  except Exception:
    print a, b
    print 'key:' + key
    raise


def cleanup(item):
  if item.has_key('default_target_list') and not item['default_target_list'].has_key('inventory_sources'):
    item['default_target_list']['inventory_sources'] = []

  if item.has_key('target_list') and not item['target_list'].has_key('inventory_sources'):
    item['target_list']['inventory_sources'] = []

  #return json.dumps(item).replace(', {"excluded": false}', '').replace('{"excluded": false}', '')
  return json.dumps(item)


def _read(entity_file):
  global buff
  result = ''

  if len(buff) == 0:
    buff = entity_file.read(1024)

  if len(buff) > 0:
    result = buff[0]
    buff = buff[1:]

  return result

def read_next_object(entity_file):
  result = ''
  line = entity_file.readline()
  while line and line[0] != '{':
    line = entity_file.readline()

  result += line

  while line and not line.startswith(']') and not line.startswith('}'):
    line = entity_file.readline()
    result += line

  if result:
    try:
      if line.startswith('},'):
        result = result[:-3]
      else:
        result = result[:-1]
      return json.loads(result)
    except:
      print result
      print line
      raise
  else:
    return None


def process_file_for_bq(file_name, output='processed.json', cleanup=None, schema_template=None):
  start = datetime.now()

  result = {} if schema_template == None else schema_template

  f = open(file_name, 'r')

  if os.path.isfile(output):
    os.remove(output)

  out = open(output, 'w')

  global buff
  buff = ''
  item = read_next_object(f)
  while item != None:
    merge(result, item)
    out.write(json.dumps(item) if cleanup == None else cleanup(item))
    out.write('\n')
    item = read_next_object(f)

  out.close()

  schema = file_processor.entity_read_dict_to_schema(result)

  return {
    'schema': schema,
    'file_name': output,
    'schema_template': result
  }


def get_entities(entity_file):
  start = 0
  end = 0
  depth = 0
  quote = False
  view = entity_file
  
  while end < len(view):
    if quote:
      if view[end] == '\\': end += 1
      elif view[end] == '"': quote = False
    else:
      if view[end] == '"': quote = True
      elif view[end] == '{': 
        if depth ==0: start = end
        depth += 1 
      elif view[end] == '}': 
        depth -= 1 
        if depth == 0: 
          #print view[start:end+1]
          yield json.loads(view[start:end+1])
          start = end + 1
    end += 1 

  if depth != 0: raise 'Invalid structure'


def entity():
  if project.verbose: print 'ENTITY'
  
  if 'bucket' in project.task: # compatible with UI solutions deployment

    # create dataset
    if project.verbose: print 'Dataset', project.task['dataset']
    datasets_create(project.task['auth'], project.id, project.task['dataset'])

    # create entities  
    for entity in project.task['entities']:
      output = BytesIO()
      table = '%s_%s' % (project.task['prefix'], entity)
      if project.verbose: print 'Table', table

      for partner_id in project.task['partners']:
        if project.verbose: print 'Partner', partner_id
        path = 'gdbm-%s:entity/%s.0.%s.json' % (partner_id, time.strftime('%Y%m%d'), entity) 

        #path = 'starthinker-entity-read:20170818.0.Advertiser.json'
        data = object_get(project.task['auth'], path)

        if project.verbose: print 'SIZE', len(data)

        # compute the schema
        for item in get_entities(data):
          output.write(cleanup(item))
          output.write('\n')

        csv_to_table(project.task['auth'], project.id, project.task['dataset'], table, output, structure='NEWLINE_DELIMITED_JSON')

  else: # legacy task ( not compatible with UI Solutions )
    partner_id = project.task['partner_id']
    auth = project.task['auth']
    gc_project = project.id
    dataset = project.task['dataset']
    datasets_create(auth, project.id, dataset)

    for entity in project.task['entities']:
      if project.verbose: print('Loading %s for partner %s' % (entity, partner_id))
      bucket_name = 'gdbm-%s' % partner_id
      object_name = time.strftime('entity/%Y%m%d.0.{0}.json').format(entity)
      local_path  = dest_folder + '/%s-%s' % (partner_id, object_name[7:])
      entity_file_name = object_download(gc_project, bucket_name, object_name, local_path)
      result = process_file_for_bq(entity_file_name, '/tmp/processed.json', cleanup)
      local_file_to_table(auth, dataset, entity, result['schema'], result['file_name'], replace=True)
      os.remove(result['file_name'])
      os.remove(entity_file_name)


if __name__ == "__main__":
  project.load('entity')
  entity()
