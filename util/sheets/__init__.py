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

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#SheetProperties
import re
import time
import pprint

from util.auth import get_service
from util.project import project
from googleapiclient.errors import HttpError


def _retry(job, key=None, retries=10, wait=30):
  try:
    data = job.execute()
    #pprint.PrettyPrinter().pprint(data)
    return data if not key else data.get(key, [])
  except HttpError, e:
    if project.verbose: print str(e)
    if e.resp.status in [403, 409, 429, 500, 503]:
      if retries > 0:
        time.sleep(wait)
        return _retry(job, key, retries - 1, wait * 2)
      elif json.loads(e.content)['error']['code'] == 409:
        pass  # already exists ( ignore )
      else:
        raise


def sheets_id(url):
  # url is url like 
  # https://docs.google.com/spreadsheets/d/1uN9tnb-DZ9zZflZsoW4_34sf34tw3ff/edit#gid=4715
  # or directly only id as 1uN9tnb-DZ9zZflZsoW4_34sf34tw3ff
  m = re.search('^(?:https:\/\/docs.google.com\/spreadsheets\/d\/)?([a-zA-Z0-9-_]+)(?:\/.*)?$', url)
  if m:
    return m.group(1)
  return ''


def sheets_tab_range(sheet_tab, sheet_range):
  if sheet_range: return '%s!%s' % (sheet_tab, sheet_range)
  else: return sheet_tab


def sheets_get(auth, sheet_url):
  service = get_service('sheets', 'v4', auth)
  sheet_id = sheets_id(sheet_url)
  return _retry(service.spreadsheets().get(spreadsheetId=sheet_id))
  

def sheets_tab_id(auth, sheet_url, sheet_tab):
  tabs = sheets_get(auth, sheet_url)
  for tab in tabs.get('sheets', []):
    if tab['properties']['title'] == sheet_tab:
      return sheets_id(sheet_url), tab['properties']['sheetId']
  return sheets_id(sheet_url), None


def sheets_read(auth, sheet_url, sheet_tab, sheet_range):
  if project.verbose: print 'SHEETS READ', sheet_url, sheet_tab, sheet_range
  service = get_service('sheets', 'v4', auth)
  sheet_id = sheets_id(sheet_url)
  return _retry(service.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheets_tab_range(sheet_tab, sheet_range)), 'values')


# TIP: Specify sheet_range as 'Tab!A1' coordinate, the API will figure out length and height based on data
def sheets_write(auth, sheet_url, sheet_tab, sheet_range, data, valueInputOption='RAW'):
  if project.verbose: print 'SHEETS WRITE', sheet_url, sheet_tab, sheet_range
  service = get_service('sheets', 'v4', auth)
  sheet_id = sheets_id(sheet_url)
  range = sheets_tab_range(sheet_tab, sheet_range)
  body = {
    "values": list(data)
  }
  _retry(service.spreadsheets().values().update(spreadsheetId=sheet_id, range=range, body=body, valueInputOption=valueInputOption))


def sheets_clear(auth, sheet_url, sheet_tab, sheet_range):
  if project.verbose: print 'SHEETS CLEAR', sheet_url, sheet_tab, sheet_range
  service = get_service('sheets', 'v4', auth)
  sheet_id = sheets_id(sheet_url)
  _retry(service.spreadsheets().values().clear(spreadsheetId=sheet_id, range=sheets_tab_range(sheet_tab, sheet_range), body={}))


def sheets_tab_copy(auth, from_sheet_url, from_sheet_tab, to_sheet_url, to_sheet_tab):
  if project.verbose: print 'SHEETS COPY', from_sheet_url, from_sheet_tab, to_sheet_url, to_sheet_tab
  service = get_service('sheets', 'v4', auth)

  # convert human readable to ids
  from_sheet_id, from_tab_id = sheets_tab_id(auth, from_sheet_url, from_sheet_tab)
  to_sheet_id, to_tab_id = sheets_tab_id(auth, to_sheet_url, to_sheet_tab)

  # overwrite only if does not exist ( PROTECTION )
  if to_tab_id is None:
    # copy tab between sheets ( seriously, the name changes to be "Copy of [from_sheet_tab]" )
    request = _retry(service.spreadsheets().sheets().copyTo(spreadsheetId=from_sheet_id, sheetId=from_tab_id, body={
      "destinationSpreadsheetId": to_sheet_id,
    }))

    # change the name back ( remove "Copy of " )
    sheets_tab_rename(auth, to_sheet_url, 'Copy of %s' % from_sheet_tab, to_sheet_tab)


def sheets_batch_update(auth, sheet_url, data):
  service = get_service('sheets', 'v4', auth)
  sheet_id = sheets_id(sheet_url)
  _retry(service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=data))


def sheets_values_batch_update(auth, sheet_url, data):
  service = get_service('sheets', 'v4', auth)
  sheet_id = sheets_id(sheet_url)
  _retry(service.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=data))


def sheets_tab_create(auth, sheet_url, sheet_tab):
  sheet_id, tab_id = sheets_tab_id(auth, sheet_url, sheet_tab)
  if tab_id is None:
    sheets_batch_update(auth, sheet_url, {
      "requests":[{
        "addSheet": {
          "properties": {
            "title":sheet_tab
          }
        }
      }]
    }) 


def sheets_tab_delete(auth, sheet_url, sheet_tab):
  if project.verbose: print 'SHEETS DELETE', sheet_url, sheet_tab
  sheet_id, tab_id = sheets_tab_id(auth, sheet_url, sheet_tab)
  if tab_id is not None:
    sheets_batch_update(auth, sheet_url, {
      "requests":[{
        "deleteSheet": {
          "sheetId": tab_id,
        }
      }]
    }) 


def sheets_tab_rename(auth, sheet_url, old_sheet_tab, new_sheet_tab):
  sheet_id, tab_id = sheets_tab_id(auth, sheet_url, old_sheet_tab)
  if tab_id is not None:
    sheets_batch_update(auth, sheet_url, {
      "requests":[{
        "updateSheetProperties": {
          "properties": {
            "sheetId": tab_id,
            "title": new_sheet_tab
          },
          "fields":"title"
        }
      }]
    }) 
