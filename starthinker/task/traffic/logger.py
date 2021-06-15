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
"""Handles logging actions back to the Bulkdozer feed Log tab."""

import datetime

from starthinker.util.sheets import sheets_write, sheets_clear


class Timer(object):
  """Timer class responsible for measuring run time for performance profiling and optimization."""

  def __init__(self):
    """Constructor."""
    self._timers = {}

  def start_timer(self, timer_name):
    """Initializes a new timer.

    Args:
      timer_name: name of the timer to initialize, if not unique will reset
        existing timer.
    """
    self._timers[timer_name] = datetime.datetime.now()

  def check_timer(self, timer_name):
    """Checks and prints the elapsed time of a given timer.

    Args:
      timer_name: Name of the timer to check and print, it must have been
        initialized with start_timer.
    """
    if timer_name in self._timers:
      elapsed = datetime.datetime.now() - self._timers[timer_name]

      print('%s: %d.%d' % (timer_name, elapsed.seconds,
                           (elapsed.microseconds -
                            (elapsed.seconds * 60 * 1000000)) / 1000))
    else:
      print('timer %s not defined' % timer_name)


class Logger(object):
  """Logger class responsible for logging data into the Bulkdozer feed's Log tab."""

  def __init__(self, flush_threshold=10):
    """Initializes the logger object.

    This object is a signleton, and therefore when the application starts and
    reads the configuration of which sheet ID to use for the Bulkdozer feed, the
    trix_id and auth fields need to be updated.
    """
    self.trix_id = None
    self.config = None
    self.auth = None
    self._row = 1
    self._buffer = []
    self.buffered = True
    self._flush_threshold = flush_threshold

  def clear(self):
    """Clears the log tab in the Bulkdozer feed, useful when a new execution is starting."""
    sheets_clear(self.config, self.auth, self.trix_id, 'Log', 'A1:B')
    self._row = 1

  def log(self, message):
    """Logs a message to the Bulkdozer feed's Log tab.

    Args:
      message: The message to log to the feed, it will be appended at the bottom
        of the log, after the last message that was written.
    """
    self._buffer.append(
        [datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000%z'), message])

    if not self.buffered or (self._flush_threshold and
                             len(self._buffer) >= self._flush_threshold):
      self.flush()

  def flush(self):
    """Flushes the message buffer writing buffered messages to the sheet."""
    if self._buffer:
      sheets_write(
          self.config, self.auth, self.trix_id, 'Log', 'A1', self._buffer, append=True)

      self._row += len(self._buffer)

      self._buffer = []


logger = Logger()
timer = Timer()
