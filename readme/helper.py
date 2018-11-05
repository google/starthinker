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


"""Helper command line that creates README.md files from code comments.

This script reads both script_*.json files and *.py files and appends
code comments to README.md files in the same directory. Allows comments
to be made in code, without duplicate effort.

How to include comments in README.md file...

- Create a script_*.json or a *.py file
- Include a comment inside triple quotes.
- Both module level comments and class / function comments are valid.

To preview output run: python readme/helper.py
To create README.md files run: python readme/helper.py --write
To check README.md coverage: python readme/helper.py --check

"""

import os
import sys
import re
import json
import argparse
import subprocess

from setup import EXECUTE_PATH
from script.parse import json_get_fields

RE_PY = re.compile(r'.*\.py')
RE_TEST = re.compile(r'^test.*\.json')
RE_SCRIPT = re.compile(r'^script_.*\.json$')

RE_COMMENT = re.compile(r'"""', re.I)
RE_CLASS = re.compile(r'class \w+', re.I)
RE_DEF = re.compile(r'def \w+\(', re.I)

README_DIVIDER = '# The Rest Of This Document Is Pulled From Code Comments'


def parse_readme(filepath):
  doc = ''

  try:
    with open(filepath) as f:
      for line in f.readlines():
        doc += line
        if line.startswith(README_DIVIDER): break
  except IOError:
    doc = README_DIVIDER 

  return doc


def parse_py(filepath):

  doc = ''
  crawl = {}
  crawl_class = ''
  crawl_def = '' 

  in_comment = False

  with open(filepath) as f:
    for line in f.readlines():

      if in_comment or RE_COMMENT.search(line):
        crawl.setdefault(crawl_class, {}).setdefault(crawl_def, '')
        crawl[crawl_class][crawl_def] += line.replace('"""', '') 
        if RE_COMMENT.search(line): in_comment = not in_comment

      elif RE_CLASS.search(line):
        crawl_class = line
        crawl_def = ''

      elif RE_DEF.search(line):
        crawl_def = line

      #print crawl_class, crawl_def, in_comment, line.strip()

  if crawl:
    doc = '\n# %s\n\n' % filepath.replace(EXECUTE_PATH, '')
    for cls in crawl.keys():
      if cls: doc += '\n\n## %s\n\n' % cls.split('(', 1)[0]
 
      for func in crawl[cls].keys():
        if func: doc += '\n\n### %s\n\n' % func.replace('def ', 'function ')
        doc += crawl[cls][func]

  return doc.replace('*', '\*')


def parse_json(filepath):
  doc = ''

  with open(filepath) as f:
    try:
      script = json.load(f)
    except Exception, e:
      print 'JSON ERROR', filepath, str(e) 
      exit()

    params = script['script']
    params['path'] = filepath.replace(EXECUTE_PATH, '')
    params['tasks'] = json.dumps(script['tasks'], indent=2)
    params['instructions'] = '- ' + '\n- '.join(script['script'].get('instructions', []))
    params['authors'] = ', '.join(script['script'].get('authors', []))

    params['fields'] = ''
    for field in json_get_fields(script):
      params['fields'] += '- %s (%s) %s' % (field['name'], field['kind'], field.get('description', ''))
      if field.get('default', ''): params['fields'] += 'Default: %s' % str(field['default'])
      params['fields'] += '\n'

    params['fields'] = params['fields'].strip()

    doc = '''## [%(title)s](%(path)s)

%(description)s

Maintained and supported by: %(authors)s

### Fields

%(fields)s

### Instructions

%(instructions)s

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py %(path)s -h`

`python script/run.py %(path)s [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

''' % params

  return doc.replace('*', '\*')



if __name__ == "__main__":

  # get parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--write', help='writes to files instead of stdout', action='store_true')
  parser.add_argument('--check', help='checks if README exists', action='store_true')

  args = parser.parse_args()

  check = { 'ok':[], 'fail':[] }

  for root, dirs, files in os.walk(EXECUTE_PATH):
    if '/project' in root and not '/util' in root: continue
    if '/.git' in root: continue
    if '/third_party' in root: continue
    if '/readme' in root: continue
    if '/ui' in root: continue
    if '/paper' in root: continue


    if args.check:
      check['ok' if 'README.md' in files else 'fail'].append(root)      

    else:
      doc_json = ''
      doc_py = ''


      for filename in files:
        if RE_SCRIPT.match(filename): doc_json += parse_json(root + '/' + filename)

      for filename in files:
        if RE_PY.match(filename): doc_py += parse_py(root + '/' + filename)


      if doc_py or doc_json:
        doc = parse_readme(root + '/README.md') + '\n\n'
        if doc_json:  doc += '# JOSN Recipes\n\n' + doc_json
        if doc_py:  doc += '# Python Scripts\n\n' + doc_py

        if args.write:
          print root + '/README.md'
          with open(root + '/README.md', 'w') as readme_file:
            readme_file.write(doc)
        else:
          print ''
          print root + '/README.md'
          print doc 

  if args.check:
    for filename in check['ok']: print 'OK', filename
    for filename in check['fail']: print 'MISSING', filename

    ok = len(check['ok'])
    fail = len(check['fail'])
    total = ok + fail


    print '%d / %d - %d%% OK' % (ok, total, ok * 100 / total)
    print '%d / %d - %d%% MISSING' % (fail, total, fail * 100 / total)
