###########################################################################
#
#  Copyright 2021 Google LLC
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

'''Helper utility for scraping field types from various reports.

Pull report field definitions from public sources.
Unfortunately discovery documents do not present reporting fields.

Typically the output of this tool is saved as a dictionary lookup for scripts.
Scripts will fetch the report and cross reference fields with types.

Right now only supports SA360.
'''

import json
import textwrap
import argparse

from urllib.request import urlopen
from html.parser import HTMLParser


def sa_fields():
  '''Parse SA360 public pages and pull down all field types'''

  fields = {}

  pages = [
    'account',
    'ad',
    'advertiser',
    'adGroup',
    'adGroupTarget',
    'bidStrategy',
    'campaign',
    'campaignTarget',
    'conversion',
    'feedItem',
    'floodlightActivity',
    'keyword',
    'negativeAdGroupKeyword',
    'negativeAdGroupTarget',
    'negativeCampaignKeyword',
    'negativeCampaignTarget',
    'paidAndOrganic',
    'productAdvertised',
    'productGroup',
    'productLeadAndCrossSell',
    'productTarget',
    'visit'
  ]

  # all other types will default to STRING
  types = {
    'String':'STRING',
    'Integer':'INTEGER',
    'Boolean':'BOOLEAN',
    'Date':'DATE',
    'ID':'STRING',
    'Money':'FLOAT',
    'Number':'INTEGER',
    'Timestamp':'TIMESTAMP'
  }


  class SAHTMLParser(HTMLParser):
    is_fields = False
    is_header = False
    is_row = False
    header = []
    rows = []
    row = []
    cell = ''

    def handle_starttag(self,
    tag, attrs):
      if tag == 'table' and attrs == [('class', 'matchpre')]:
        self.is_fields = True
      elif self.is_fields and tag == 'th':
        self.is_header = True
        self.is_row = False
      elif self.is_fields and tag == 'td':
        self.is_header = False
        self.is_row = True

    def handle_endtag(self, tag):
      if self.is_fields:
        if tag == 'table':
          self.is_fields = False
        elif self.is_fields and tag == 'th':
          self.header.append(self.cell.strip())
          self.cell = ''
        elif self.is_fields and tag == 'td':
          self.row.append(self.cell.strip())
          self.cell = ''
        elif self.is_row and tag == 'tr':
          self.rows.append(self.row)
          self.row = []

    def handle_data(self, data):
      self.cell += data

  for page in pages:
    print('PROCESSING:', page)
    parser = SAHTMLParser()
    parser.feed(urlopen('https://developers.google.com/search-ads/v2/report-types/%s' % page).read().decode('utf-8'))
    #parser.header
    #parser.rows

    # Convert all fields to types, default uknowns to STRING
    for row in parser.rows:
      fields[row[0]] = types.get(row[3], 'STRING')

  return fields


def main():
  # get parameters
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Attempts to collect all available reporting fields.

    Currently supported:
      - sa - search ads report schemas from: https://developers.google.com/search-ads/v2/report-types

    Examples:
      Search Ads fields: `python feilds.py --sa`

  """))

  # get parameters
  parser.add_argument('--sa', action='store_true', help='pull search ads fields')
  args = parser.parse_args()

  if args.sa:
    print(json.dumps(sa_fields(), indent=2))


if __name__ == '__main__':
  main()
