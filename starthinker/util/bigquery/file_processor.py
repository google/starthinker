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

import os
import re
import csv


class FileProcessor(object):

  def entity_read_dict_to_schema(self, source, prefix=''):
    a = self.__entity_read_analyze_schema__(source, prefix)
    return self.__entity_read_convert__(a)

  def __entity_read_analyze_schema__(self, source, prefix):
    result = {}
    for key in source:
      item = source[key]

      if type(item) is str or type(item) is unicode:
        result[key] = {
            'name': str(key),
            'type': 'STRING',
            'mode': 'NULLABLE'
        }
      elif type(item) is int:
        result[key] = {
            'name': str(key),
            'type': 'INTEGER',
            'mode': 'NULLABLE'
        }
      elif type(item) is bool:
        result[key] = {
            'name': str(key),
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }
      elif type(item) is float:
        result[key] = {
            'name': str(key),
            'type': 'FLOAT',
            'mode': 'NULLABLE'
        }
      elif type(item) is list and len(item) > 0:
        t = 'RECORD'
        if type(item[0]) is str or type(item[0]) is unicode:
          t = 'STRING'
        elif type(item[0]) is int:
          t = 'INTEGER'
        elif type(item[0]) is float:
          t = 'FLOAT'

        if t == 'RECORD':
          result[key] = {
            'name': str(key),
            'type': t,
            'mode': 'REPEATED',
            'fields':  self.__entity_read_analyze_schema__(item[0], prefix + '\t')
          }
        else:
          result[key] = {
            'name': str(key),
            'type': t,
            'mode': 'REPEATED'
          }
      elif type(item) is dict:
        result[key] = {
          'name': str(key),
          'type': 'RECORD',
          'mode': 'NULLABLE',
          'fields': self.__entity_read_analyze_schema__(item, prefix + '\t')
        }
      else:
        raise Exception(type(item).__name__ + ' is not supported!')

    return result

  def __entity_read_convert__(self, src):
    converted = []
    for key in src:
      try:
        fields = []
        if 'fields' in src[key]:
          fields = self.__entity_read_convert__(src[key]['fields'])

        converted.append({
            'name':src[key]['name'],
            'type':src[key]['type'],
            'mode':src[key]['mode'],
            'fields':fields=fields
          }
        )


      except Exception:
        raise
    return converted

  def field_list_to_schema(self, field_list):
    result = []
    field_names = []

    for field in field_list:
      field_name = re.sub(r'[ \=\:\-\/\(\)\+\&\%]', '_', field.strip())

      suffix = ''
      ct = 0
      while field_name + suffix in field_names:
        ct += 1
        suffix = '_' + str(ct)

      field_name += suffix
      field_names.append(field_name)

      result.append({
        'name':field_name,
        'type':'STRING',
        'mode':'NULLABLE'
      })

    return result


  def clean_csv(self, input_file, output_file_name, num_fields, header=True, append_to_lines=''):
    if os.path.isfile(output_file_name):
      os.remove(output_file_name)

    output_file = open(output_file_name, 'w')

    for line in input_file:
      if header:
        header = False
      elif len(line) > 1:
        line = line.strip()
        while line.count(',') < (num_fields - 1):
          line += ','
        output_file.write(line + append_to_lines + '\n')
      else:
        break

    output_file.close()
