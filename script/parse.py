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

def json_get_fields(struct, path=[]):
  """Recusrsively finds fields in script JSON and returns them as a list.
     Field has format: { "field":{ "name":"???", "kind":"???", "default":???, "description":"???" }}

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      path: (list) Stack that keeps track of recursion depth. Not used externally.

    Returns:
      fields: (list) A list of dictionaries representing each field struct found in the JSON.

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

  if path == []: return sorted(fields.values(), key=lambda f: f.get('order', 0)) # sort only on last step of recursion
  else: return fields # do not sort if deep in recursion


def get_field_value(field, variables):
  value = None
  try:
    value = variables.get(field['name'], field.get('default', ''))
    if 'prefix' in field: # and isinstance(value, (basestring, int, long)): # why check this? It should never happen.
      value = "%s%s" % (field['prefix'], value)
  except KeyError:
    pass

  return value


def json_set_fields(struct, variables):
  """Recusrsively replaces fields in script JSON with values provided.
     Field has format: { "field":{ "name":"???", "kind":"???", "default":???, "description":"???" }}

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name of field.

    Returns:
      Nothig. Struct is modified in place.

  """

  if isinstance(struct, dict):
    for key, value in struct.items():
      if isinstance(value, dict) and 'field' in value:
        struct[key] = get_field_value(value['field'], variables)
      else:
        json_set_fields(value, variables)
  elif isinstance(struct, list) or isinstance(struct, tuple):
    for index, value in enumerate(struct):
      if isinstance(value, dict) and 'field' in value:
        struct[index] = get_field_value(value['field'], variables)
      else: json_set_fields(value, variables)


def json_set_instructions(struct, variables):
  """Replaces all fields in instructions with values provided.
     Checks if struct['script']['instructions'] exist.  The replaces all %(???)s variables
     with values provided.  Note: %(???)s must match { "field":{ "name":"???" }} in JOSN.

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name of field.

    Returns:
      Nothig. Instructions are modified in place.

  """

  if 'script' in struct:
    if 'instructions' in struct['script']:
      try: struct['script']['instructions'] = [instruction % variables for instruction in struct['script']['instructions']]
      except KeyError: pass


def json_set_description(struct, variables):
  """Replaces all fields in description with values provided.
     Checks if struct['script']['description'] exist.  The replaces all %(???)s variables
     with values provided.  Note: %(???)s must match { "field":{ "name":"???" }} in JOSN.

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name of field.

    Returns:
      Nothig. Description is modified in place.

  """

  if 'script' in struct:
    if 'description' in struct['script']:
      try: struct['script']['description'] = struct['script']['description'] % variables
      except KeyError: pass
