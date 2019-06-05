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
"""Utility to read and write configuration data to the Bulkdozer feed.

"""

import json

from starthinker.util.sheets import sheets_read, sheets_write


class Config(object):
  """Class that handles reading and writing of configuration to the Bulkdozer feed.

  """

  def __init__(self):
    """Initializes Config with default mode to ALWAYS.

    """
    self.trix_id = None
    self.auth = None

    self.mode = 'ALWAYS'

  def load(self):
    """Loads configs from Bulkdozer feed and applies values to object properties.

    """
    if self.trix_id:
      data = sheets_read(self.auth, self.trix_id, 'Store', 'B3', retries=0)
      if data:
        self.mode = data[0][0]

  def update(self):
    """Writes configurations back to the Bulkdozer feed.

    """
    sheets_write(self.auth, self.trix_id, 'Store', 'B3', [[self.mode]])


config = Config()
