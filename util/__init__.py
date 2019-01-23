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


"""Generic utilities that do not belong in any specific sub module.

Add general utility functions that are used across many modules.  Do
not add classes here.
"""


def flag_last(o):
  """Flags the last loop of an iterator.

  Consumes an iterator, buffers one instance so it can look ahead.
  Returns True on last iteration.

  Args:
    * o: An iterator instance.

  Returns:
    * A tuple of ([True/False, iteration). Returns True on StopIteration.

  """

  it = o.__iter__()
  e = it.next()
  while True:
    try:
      nxt = it.next()
      yield (False, e)
      e = nxt
    except StopIteration:
      yield (True, e)
      break
