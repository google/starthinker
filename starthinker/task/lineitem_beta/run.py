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

from starthinker.util.project import project
from starthinker.util.data import put_rows, get_rows
from starthinker.util.dbm import lineitem_get_v1, lineitem_patch_v1
from starthinker.util.dbm.schema import LineItem_Read_Schema


def handle_entity_status(input_li, dv_li):
  """Handles DV360 entity status field by applying changes from the input_li to the dv_li

  Args:
    input_li: object representing the input line item from the input data
    dv_li: object representing the DV360 line item
  Returns: List of strings representing the fields to patch
  """
  if 'Active' in input_li:
    if input_li['Active'] != '':
      dv_li['entityStatus'] = 'ENTITY_STATUS_ACTIVE' if input_li[
          'Active'] == 'TRUE' else 'ENTITY_STATUS_PAUSED'
      return ['entityStatus']

  return []


def handle_fixed_bid(input_li, dv_li):
  """Handles DV360 fixed bid field by applying changes from the input_li to the dv_li

  Args:
    input_li: object representing the input line item from the input data
    dv_li: object representing the DV360 line item
  Returns: List of strings representing the fields to patch
  """
  if 'Fixed Bid' in input_li:
    if input_li['Fixed Bid'] != '':
      dv_li['bidStrategy'] = {
          'fixedBid': {
              'bidAmountMicros': float(input_li['Fixed Bid']) * 1000000
          }
      }
      return ['bidStrategy.fixedBid.bidAmountMicros']

  return []


def handle_patch(input_li, dv_li):
  """Handles that patch operation by leveraging the handler functions to apply changes represented by the input_li to the dv_li

  Args:
    input_li: object representing the input line item from the input data
    dv_li: object representing the DV360 line item
  Returns: List of strings representing the fields to patch
  """
  result = []

  result += handle_entity_status(input_li, dv_li)
  result += handle_fixed_bid(input_li, dv_li)

  return result


@project.from_parameters
def lineitem_beta():
  """Main entry point of the lineitem_beta StarThinker task, here is the task definition:{

      "lineitem_beta":{
        "auth":"user",
        "read":{
          "sheet":{
            "sheet":
            "https://docs.google.com/spreadsheets/d/109jJpQa6QUIjtoY6wI5yPAkixzrmh33q9AE-zjwcsTE/edit#gid=0",
            "tab": "Rules",
            "range": "A1:D"
          }
        },
        "patch": {}
      }
    }

  read: represents the input data for operating in the line items
  patch: indicates a patch operation should be performed
  """
  if project.verbose:
    print('LINEITEM_BETA')

  li_map = {}

  if 'read' in project.task:
    #TODO this has been developed to work with sheets in this initial phase,
    # need to check how to handle headers in case of reading from other sources such as BQ
    rows = get_rows(project.task['auth'], project.task['read'])

    header = False

    for row in rows:
      if not header:
        header = row
      else:
        li = {}
        for idx, field in enumerate(header):
          li[field] = row[idx]

        dv_li = lineitem_get_v1(project.task['auth'], li['Advertiser ID'],
                                li['Line Item ID'])

        li_map[li['Line Item ID']] = {'input_li': li, 'dv_li': dv_li}

  if 'patch' in project.task:
    patch = []

    for li_id in li_map.keys():
      input_li = li_map[li_id]['input_li']
      dv_li = li_map[li_id]['dv_li']

      patch = handle_patch(input_li, dv_li)

      if patch:
        lineitem_patch_v1(project.task['auth'], ','.join(patch), dv_li)


if __name__ == '__main__':
  lineitem_beta()
