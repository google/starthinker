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

from starthinker.util.project import project
from starthinker.util.dbm import lineitem_read


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Command line interface for fetching line items via legacy API.
      Helps developers quickly debug lineitem issues or permissions access issues.

      Example: python helper.py [line item id] -u [user credentials]
  """))

  parser = argparse.ArgumentParser()
  parser.add_argument(
      'lineitem', help='lineitem ID to pull schema, or "list" to get index')

  # initialize project
  project.from_commandline(parser=parser, arguments=('-u', '-c', '-s', '-v'))
  auth = 'service' if project.args.service else 'user'

  # print lineitem
  for row in lineitem_read(auth, lineitems=[project.args.lineitem]):
    print(row)


if __name__ == '__main__':
  main()
