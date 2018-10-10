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
"""Handles logging actions back to the Bulkdozer feed Log tab.

"""

from util.project import project
import datetime
import json

from util.sheets import sheets_read, sheets_write, sheets_clear


class Logger(object):
  """Logger class responsible for logging data into the Bulkdozer feed's Log tab.

  """

  def __init__(self):
    """Initializes the logger object.

    This object is a signleton, and therefore when the application starts and
    reads the configuration of which sheet ID to use for the Bulkdozer feed, the
    trix_id and auth fields need to be updated.
    """
    self.trix_id = None
    self.auth = None
    self._row = 1

  def clear(self):
    """Clears the log tab in the Bulkdozer feed, useful when a new execution is starting.

    """
    sheets_clear(self.auth, self.trix_id, 'Log', 'A1:B')
    self._row = 1

  def log(self, message):
    """Logs a message to the Bulkdozer feed's Log tab.

    Args:
      message: The message to log to the feed, it will be appended at the bottom
        of the log, after the last message that was written.
    """
    sheets_write(self.auth, self.trix_id, 'Log', 'A' + str(self._row),
                 [[datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000%z'), message]])

    self._row += 1


logger = Logger()
