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

import json
#from random import choice


class Colab:

  def __init__(self, name, version='4.0'):
    self.markdown_lines = []
    self.code_lines = []
    self.colab = {
        'license': 'Licensed under the Apache License, Version 2.0',
        'copyright': 'Copyright 2020 Google LLC',
        'nbformat': version.split('.', 1)[0],
        'nbformat_minor': version.split('.', 1)[1],
        'metadata': {
            'colab': {
                'name': name,
                'provenance': [],
                'collapsed_sections': [],
                'toc_visible': True
            },
            'kernelspec': {
                'name': 'python3',
                'display_name': 'Python 3'
            }
        },
        'cells': []
    }

  def _code(self):
    if self.code_lines:
      self.colab['cells'].append({
          'cell_type': 'code',
          'metadata': {
              #"id": ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(12)]),
              'colab_type': 'code'
          },
          'source': self.code_lines
      })
      self.code_lines = []

  def _markdown(self):
    if self.markdown_lines:
      self.colab['cells'].append({
          'cell_type': 'markdown',
          'metadata': {
              #"id": ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(12)]),
              'colab_type': 'text'
          },
          'source': self.markdown_lines
      })
      self.markdown_lines = []

  def code(self, code):
    self._markdown()
    self.code_lines.extend(['%s\n' % c for c in code.split('\n')])

  def header(self, text, level=1, indent=0):
    self._code()
    self.markdown_lines.append('%s%s%s\n' % ('>' * indent, '#' * level, text))

  def paragraph(self, text, indent=0):
    self._code()
    self.markdown_lines.extend(
        ['%s%s\n' % ('>' * indent, t) for t in text.split('\n')])

  def image(self, name, link):
    self._code()
    self.markdown_lines.append('![%s](%s)\n' % (name, link))

  def list(self, items, ordered=True, indent=0):
    self._code()
    self.markdown_lines.extend([
        '%s %s %s\n' % ('>' * indent, '1.' if ordered else '*', t)
        for t in items
    ])

  def render(self):
    self._code()
    self._markdown()
    return json.dumps(self.colab, indent=2)
