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

#SEE: https://pymotw.com/2/sys/tracing.html

import sys

from starthinker.config import TRACE_FILE

STARTHINKER_TRACE_TO_FILE = False
STARTHINKER_TRACE_TO_PRINT = False


def is_starthinker_module(frame):
  if '__file__' in frame.f_globals:
    module_path = frame.f_globals['__file__']
    return 'starthinker' in module_path and 'starthinker_virtualenv' not in module_path
  else:
    return False


def starthinker_trace_log(entry):
  global STARTHINKER_TRACE_TO_PRINT
  global STARTHINKER_TRACE_TO_FILE

  if STARTHINKER_TRACE_TO_PRINT:
    print(entry)

  if STARTHINKER_TRACE_TO_FILE:
    with open(TRACE_FILE, 'a+') as log_file:
      log_file.write('%s\n' % entry)


def starthinker_trace(frame, event, arg, returns=True):

  co = frame.f_code
  func_name = co.co_name
  line_no = frame.f_lineno
  filename = co.co_filename

  if event == 'exception':
    exc_type, exc_value, exc_traceback = arg
    starthinker_trace_log(
        'Exception: %s on line %s of %s with type %s and value %s' %
        (func_name, line_no, filename, exc_type.__name__, exc_value))
    return

  elif is_starthinker_module(frame):

    if event == 'call':
      starthinker_trace_log('Call To: %s on line %s of %s' %
                            (func_name, line_no, filename))
      return starthinker_trace

    elif event == 'return' and returns:
      starthinker_trace_log('Return From: %s on line %s of %s with value %s' %
                            (func_name, line_no, filename, arg))
      return

  return


def starthinker_trace_start(to_print=True, to_file=False):
  global STARTHINKER_TRACE_TO_PRINT
  global STARTHINKER_TRACE_TO_FILE

  STARTHINKER_TRACE_TO_PRINT = to_print
  STARTHINKER_TRACE_TO_FILE = to_file

  if STARTHINKER_TRACE_TO_PRINT or STARTHINKER_TRACE_TO_FILE:
    sys.settrace(starthinker_trace)


if __name__ == '__main__':

  def c():
    raise RuntimeError('exception message goes here')

  def b():
    try:
      c()
    except Exception as e:
      pass
    return 'response_from_b '

  def a():
    val = b()
    return val.replace('_b', '_a')

  from starthinker.util.regexp import date_to_str

  starthinker_trace_start()
  a()

  date_to_str(None)
