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

import argparse
import textwrap
from json import JSONDecodeError

from starthinker.util.project import get_project


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Evaluate the validity of a json file. Helps in debugging recipes.
      Print the line and character position of any errors in the given json file.

      Example: python helper.py scripts/say_hello.json
  """))

  parser.add_argument('file', help='A JSON file.')
  args = parser.parse_args()

  try:
    project = get_project(args.file)
    print('JSON OK:', args.file)
  except JSONDecodeError as e:
    print(str(e))


if __name__ == '__main__':
  main()
