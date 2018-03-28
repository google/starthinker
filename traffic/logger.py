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

from util.project import project
import json

from util.sheets import sheets_read, sheets_write, sheets_clear


class Logger(object):

  def __init__(self):
    self.trix_id = None
    self.auth = None
    self._row = 1

  def clear(self):
    sheets_clear(self.auth, self.trix_id, 'Log', 'A1:A')
    self._row = 1

  def log(self, message):
    sheets_write(self.auth, self.trix_id, 'Log', 'A' + str(self._row), [[message]])

    self._row += 1


logger = Logger()
