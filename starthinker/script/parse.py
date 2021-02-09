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

import re
from collections import defaultdict

from starthinker.util.project import get_project

RE_TEXT_FIELD = re.compile(r'\{\w+:(\w+)(, .*?)?}')


def fields_to_string(fields, values={}):
  items = [
      repr(field['name']) + ': ' +
      repr(values.get(field['name'], field.get('default', ''))) + ',' +
      ('  # %s' % field['description'] if 'description' in field else '')
      for field in fields
  ]
  return '{\n  %s\n}' % ('\n  '.join(items))


def dict_to_string(value, char_indent='  ', char_line='\n', skip=[], indent=0):
  nlch = char_line + char_indent * (indent + 1)
  if type(value) is dict:
    is_skip = any(k in value for k in skip)
    items = [('' if is_skip else nlch) + repr(key) + ': ' +
             dict_to_string(value[key], '' if is_skip else char_indent,
                            '' if is_skip else char_line, skip, indent + 1)
             for key in value]
    return '{%s}' % (','.join(items) +
                     ('' if is_skip else char_line + char_indent * indent))
  elif type(value) is list:
    items = [
        nlch + dict_to_string(item, char_indent, char_line, skip, indent + 1)
        for item in value
    ]
    return '[%s]' % (','.join(items) + char_line + char_indent * indent)
  elif type(value) is tuple:
    items = [
        nlch + dict_to_string(item, char_indent, char_line, skip, indent + 1)
        for item in value
    ]
    return '(%s)' % (','.join(items) + char_line + char_indent * indent)
  else:
    return repr(value)


def json_set_auths(struct, auth):
  """Recusrsively finds auth in script JSON and sets them.

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      auth: (string) Either 'service' or 'user'.

    Returns:
      (struct) same structure but with all auth fields replaced.

  """

  if isinstance(struct, dict):
    if 'auth' in struct:
      struct['auth'] = auth
    for key, value in struct.items():
      json_set_auths(value, auth)
  elif isinstance(struct, list) or isinstance(struct, tuple):
    for index, value in enumerate(struct):
      json_set_auths(value, auth)

  return struct


def json_get_fields(struct, path=[]):
  """Recusrsively finds fields in script JSON and returns them as a list.

     Field has format: { "field":{ "name":"???", "kind":"???", "default":???,
     "description":"???" }}

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      path: (list) Stack that keeps track of recursion depth. Not used
        externally.

    Returns:
      fields: (list) A list of dictionaries representing each field struct found
      in the JSON.

  """

  fields = {}
  path = path[:]
  if isinstance(struct, dict):
    if 'field' in struct:
      fields[struct['field']['name']] = struct['field']
    else:
      for key, value in struct.items():
        fields.update(json_get_fields(value, path + [key]))
  elif isinstance(struct, list) or isinstance(struct, tuple):
    for index, value in enumerate(struct):
      fields.update(json_get_fields(value, path + [index]))

  if path == []:
    return sorted(
        fields.values(),
        key=lambda f: f.get('order', 0))  # sort only on last step of recursion
  else:
    return fields  # do not sort if deep in recursion


def get_field_value(field, variables):
  value = None
  try:
    value = variables.get(field['name'], field.get('default'))
    if value is not None and 'prefix' in field:
      value = '%s%s' % (field['prefix'], value)
    if value is not None and 'suffix' in field:
      value = '%s%s' % (value, field['suffix'])
  except KeyError:
    pass

  return value


def json_set_fields(struct, variables):
  """Recusrsively replaces fields in script JSON with values provided.

     Field has format: { "field":{ "name":"???", "kind":"???", "default":???,
     "description":"???" }}

     If field value is empty and field default is null, the value is removed
     from JSON as a parameter,
     allowing the python task to pick a default value. Allows optional
     parameters to exist.

    Args:
      struct: (dict) A dictionary representation of the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name
        of field.

    Returns:
      Nothig. Struct is modified in place.

  """

  if isinstance(struct, dict):
    for key, value in list(struct.items()):
      if isinstance(value, dict) and 'field' in value:
        variable_value = get_field_value(value['field'], variables)
        if variable_value is None and value.get('default') is None:
          del struct[key]
        else:
          struct[key] = get_field_value(value['field'], variables)
      else:
        json_set_fields(value, variables)
  elif isinstance(struct, list) or isinstance(struct, tuple):
    for index, value in enumerate(struct):
      if isinstance(value, dict) and 'field' in value:
        struct[index] = get_field_value(value['field'], variables)
      else:
        json_set_fields(value, variables)


def text_set_fields(text, variables):
  """Replaces fields in text with values from recipe.

     Fields in text are just are {field}, where field is a name of the variable.
     Missing fields default to blanks.

     Args:
       text (string) A paragraph possible containing {field} entries
       variables: (dict) The keys mapping to field, and values to replace

     Returns:
       A string with all values replaced. Or if an error occurs, original text.

  """

  text = RE_TEXT_FIELD.sub(r'{\1}', text)
  try:
    return text.format_map(defaultdict(str, variables))
  except ValueError:
    return text


def json_set_instructions(struct, variables):
  """Replaces all fields in instructions with values provided.

     Checks if struct['script']['instructions'] exist.  The replaces all %(???)s
     variables
     with values provided.  Note: %(???)s must match { "field":{ "name":"???" }}
     in JSON.

    Args:
      struct: (dict) A dictionary representation of the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name
        of field.

    Returns:
      Nothig. Instructions are modified in place.

  """

  if 'script' in struct:
    if 'instructions' in struct['script']:
      try:
        struct['script']['instructions'] = [
            text_set_fields(instruction, variables)
            for instruction in struct['script']['instructions']
        ]
      except KeyError:
        pass


def json_set_description(struct, variables):
  """Replaces all fields in description with values provided.

     Checks if struct['script']['description'] exist.  The replaces all %(???)s
     variables
     with values provided.  Note: %(???)s must match { "field":{ "name":"???" }}
     in JOSN.

    Args:
      struct: (dict) A dictionary representation of the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name
        of field.

    Returns:
      Nothig. Description is modified in place.

  """

  if 'script' in struct:
    if 'description' in struct['script']:
      try:
        struct['script']['description'] = text_set_fields(
            struct['script']['description'], variables)
      except KeyError:
        pass
