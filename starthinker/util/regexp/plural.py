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

ABERRANT_PLURAL_MAP = {
    'appendix': 'appendices',
    'barracks': 'barracks',
    'cactus': 'cacti',
    'child': 'children',
    'criterion': 'criteria',
    'deer': 'deer',
    'echo': 'echoes',
    'elf': 'elves',
    'embargo': 'embargoes',
    'focus': 'foci',
    'fungus': 'fungi',
    'goose': 'geese',
    'hero': 'heroes',
    'hoof': 'hooves',
    'index': 'indices',
    'knife': 'knives',
    'leaf': 'leaves',
    'life': 'lives',
    'man': 'men',
    'mouse': 'mice',
    'nucleus': 'nuclei',
    'person': 'people',
    'phenomenon': 'phenomena',
    'potato': 'potatoes',
    'self': 'selves',
    'syllabus': 'syllabi',
    'tomato': 'tomatoes',
    'torpedo': 'torpedoes',
    'veto': 'vetoes',
    'woman': 'women',
}

VOWELS = set('aeiou')


def pluralize(singular):
  """Return plural form of given lowercase singular word (English only).

  Based on
  ActiveState recipe http://code.activestate.com/recipes/413172/

  >>> pluralize('')
  ''
  >>> pluralize('goose')
  'geese'
  >>> pluralize('dolly')
  'dollies'
  >>> pluralize('genius')
  'genii'
  >>> pluralize('jones')
  'joneses'
  >>> pluralize('pass')
  'passes'
  >>> pluralize('zero')
  'zeros'
  >>> pluralize('casino')
  'casinos'
  >>> pluralize('hero')
  'heroes'
  >>> pluralize('church')
  'churches'
  >>> pluralize('x')
  'xs'
  >>> pluralize('car')
  'cars'

  """
  if not singular:
    return ''
  plural = ABERRANT_PLURAL_MAP.get(singular)
  if plural:
    return plural
  root = singular
  try:
    if singular[-1] == 'y' and singular[-2] not in VOWELS:
      root = singular[:-1]
      suffix = 'ies'
    elif singular[-1] == 's':
      if singular[-2] in VOWELS:
        if singular[-3:] == 'ius':
          root = singular[:-2]
          suffix = 'i'
        else:
          root = singular[:-1]
          suffix = 'ses'
      else:
        suffix = 'es'
    elif singular[-2:] in ('ch', 'sh'):
      suffix = 'es'
    else:
      suffix = 's'
  except IndexError:
    suffix = 's'
  plural = root + suffix
  return plural


if __name__ == '__main__':
  import doctest
  doctest.testmod()
