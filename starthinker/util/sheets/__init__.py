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

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets

import re

from googleapiclient.errors import HttpError

from starthinker.util.project import project
from starthinker.util.google_api import API_Sheets
from starthinker.util.drive import file_delete
from starthinker.util.drive import file_find


def sheets_id(auth, url_or_name):
  # check if URL given, convert to ID "https://docs.google.com/spreadsheets/d/1uN9tnb-DZ9zZflZsoW4_34sf34tw3ff/edit#gid=4715"
  if url_or_name.startswith('https://docs.google.com/spreadsheets/d/'):
    m = re.search(
        '^(?:https:\/\/docs.google.com\/spreadsheets\/d\/)?([a-zA-Z0-9-_]+)(?:\/.*)?$',
        url_or_name)
    if m:
      return m.group(1)

  # check if name given convert to ID "Some Document"
  else:
    sheet = file_find(auth, url_or_name)
    if sheet:
      return sheet['id']

      # check if just ID given, "1uN9tnb-DZ9zZflZsoW4_34sf34tw3ff"
    else:
      m = re.search('^([a-zA-Z0-9-_]+)$', url_or_name)
      if m:
        return m.group(1)

  # probably a mangled id or name does not exist
  if project.verbose:
    print('SHEET DOES NOT EXIST', url_or_name)
  return None


def sheets_url(auth, url_or_name):
  sheet_id = sheets_id(auth, url_or_name)
  return 'https://docs.google.com/spreadsheets/d/%s/' % sheet_id


def sheets_tab_range(sheet_tab, sheet_range):
  if sheet_range:
    return '%s!%s' % (sheet_tab, sheet_range)
  else:
    return sheet_tab


def sheets_get(auth, sheet_url_or_name):
  sheet_id = sheets_id(auth, sheet_url_or_name)
  if sheet_id:
    return API_Sheets(auth).spreadsheets().get(spreadsheetId=sheet_id).execute()
  else:
    return None


def sheets_tab_id(auth, sheet_url_or_name, sheet_tab):
  sheet_id = None
  tab_id = None
  spreadsheet = sheets_get(auth, sheet_url_or_name)
  if spreadsheet:
    sheet_id = spreadsheet['spreadsheetId']
    for tab in spreadsheet.get('sheets', []):
      if tab['properties']['title'] == sheet_tab:
        tab_id = tab['properties']['sheetId']
        break
  return sheet_id, tab_id


def sheets_read(auth, sheet_url_or_name, sheet_tab, sheet_range='', retries=10):
  if project.verbose:
    print('SHEETS READ', sheet_url_or_name, sheet_tab, sheet_range)
  sheet_id = sheets_id(auth, sheet_url_or_name)
  if sheet_id is None:
    raise (OSError('Sheet does not exist: %s' % sheet_url_or_name))
  else:
    return API_Sheets(auth).spreadsheets().values().get(
      spreadsheetId=sheet_id,
      range=sheets_tab_range(sheet_tab, sheet_range)
    ).execute().get('values')


# TIP: Specify sheet_range as 'Tab!A1' coordinate, the API will figure out length and height based on data
def sheets_write(auth,
                 sheet_url_or_name,
                 sheet_tab,
                 sheet_range,
                 data,
                 append=False,
                 valueInputOption='RAW'):
  if project.verbose:
    print('SHEETS WRITE', sheet_url_or_name, sheet_tab, sheet_range)
  sheet_id = sheets_id(auth, sheet_url_or_name)
  range = sheets_tab_range(sheet_tab, sheet_range)
  body = {'values': list(data)}

  if append:
    API_Sheets(auth).spreadsheets().values().append(
      spreadsheetId=sheet_id,
      range=range,
      body=body,
      valueInputOption=valueInputOption,
      insertDataOption='OVERWRITE'
    ).execute()
  else:
    API_Sheets(auth).spreadsheets().values().update(
      spreadsheetId=sheet_id,
      range=range,
      body=body,
      valueInputOption=valueInputOption
    ).execute()


def sheets_clear(auth, sheet_url_or_name, sheet_tab, sheet_range):
  if project.verbose:
    print('SHEETS CLEAR', sheet_url_or_name, sheet_tab, sheet_range)
  sheet_id = sheets_id(auth, sheet_url_or_name)
  API_Sheets(auth).spreadsheets().values().clear(
    spreadsheetId=sheet_id,
    range=sheets_tab_range(sheet_tab, sheet_range),
    body={}
  ).execute()


def sheets_tab_copy(auth,
                    from_sheet_url_or_name,
                    from_sheet_tab,
                    to_sheet_url_or_name,
                    to_sheet_tab,
                    overwrite=False):
  if project.verbose:
    print('SHEETS COPY', from_sheet_url_or_name, from_sheet_tab,
          to_sheet_url_or_name, to_sheet_tab)

  # convert human readable to ids
  from_sheet_id, from_tab_id = sheets_tab_id(auth, from_sheet_url_or_name,
                                             from_sheet_tab)
  to_sheet_id, to_tab_id = sheets_tab_id(auth, to_sheet_url_or_name,
                                         to_sheet_tab)

  # overwrite only if does not exist
  if overwrite or to_tab_id is None:

    # copy tab between sheets, the name changes to be "Copy of [from_sheet_tab]"
    copy_sheet = API_Sheets(auth).spreadsheets().sheets().copyTo(
      spreadsheetId=from_sheet_id,
      sheetId=from_tab_id,
      body={
        'destinationSpreadsheetId': to_sheet_id,
      }
    ).execute()

    body = {'requests': []}

    # if destination tab exists, delete it
    if to_tab_id:
      body['requests'].append({'deleteSheet': {'sheetId': to_tab_id}})

    # change the copy name to the designated name, remove "Copy of "
    body['requests'].append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': copy_sheet['sheetId'],
                'title': to_sheet_tab
            },
            'fields': 'title'
        }
    })

    API_Sheets(auth).spreadsheets().batchUpdate(
      spreadsheetId=to_sheet_id,
      body=body
    ).execute()


def sheets_batch_update(auth, sheet_url_or_name, data):
  sheet_id = sheets_id(auth, sheet_url_or_name)
  API_Sheets(auth).spreadsheets().batchUpdate(
    spreadsheetId=sheet_id,
    body=data
  ).execute()


def sheets_values_batch_update(auth, sheet_url_or_name, data):
  sheet_id = sheets_id(auth, sheet_url_or_name)
  API_Sheets(auth).spreadsheets().values().batchUpdate(
    spreadsheetId=sheet_id,
    body=data
  ).execute()


def sheets_tab_create(auth, sheet_url_or_name, sheet_tab):
  sheet_id, tab_id = sheets_tab_id(auth, sheet_url_or_name, sheet_tab)
  if tab_id is None:
    sheets_batch_update(
        auth, sheet_url_or_name,
        {'requests': [{
            'addSheet': {
                'properties': {
                    'title': sheet_tab
                }
            }
        }]})


def sheets_tab_delete(auth, sheet_url_or_name, sheet_tab):
  if project.verbose:
    print('SHEETS DELETE', sheet_url_or_name, sheet_tab)

  spreadsheet = sheets_get(auth, sheet_url_or_name)
  if spreadsheet:
    if len(
        spreadsheet['sheets']
    ) == 1 and spreadsheet['sheets'][0]['properties']['title'] == sheet_tab:
      file_delete(auth, spreadsheet['properties']['title'], parent=None)
    else:
      sheet_id, tab_id = sheets_tab_id(auth, sheet_url_or_name, sheet_tab)
      # add check to see if only tab, then delete whole sheet
      if tab_id is not None:
        sheets_batch_update(
            auth, sheet_url_or_name,
            {'requests': [{
                'deleteSheet': {
                    'sheetId': tab_id,
                }
            }]})


def sheets_tab_rename(auth, sheet_url_or_name, old_sheet_tab, new_sheet_tab):
  sheet_id, tab_id = sheets_tab_id(auth, sheet_url_or_name, old_sheet_tab)
  if tab_id is not None:
    sheets_batch_update(
        auth, sheet_url_or_name, {
            'requests': [{
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': tab_id,
                        'title': new_sheet_tab
                    },
                    'fields': 'title'
                }
            }]
        })


def sheets_create(auth,
                  sheet_name,
                  sheet_tab,
                  template_sheet=None,
                  template_tab=None):
  """ Checks if sheet with name already exists ( outside of trash ) and

  if not, creates the sheet. Both sheet and tab must be provided or both must be
  omitted to create
  a blank sheet and tab.

  Args:
    * auth: (string) Either user or service.
    * sheet_name: (string) name of sheet to create, used as key to check if it
      exists in the future.
    * sheet_tab: (string) name of the tab to create.
    * template_sheet: (string) optional sheet to copy tempalte from.
    * template_tab: (string) optional tab to copy template from.
    * parent: (string) the Google Drive to upload the file to.

  Returns:
    * JSON specification of the file created or existing.

  """

  created = False

  # check if sheet and tab exist
  sheet_id, tab_id = sheets_tab_id(auth, sheet_name, sheet_tab)

  # if no sheet create it and the tab
  if sheet_id is None:
    if project.verbose:
      print('SHEET CREATE', sheet_name, sheet_tab)
    body = {
        'properties': {
            'title': sheet_name,
        },
        'sheets': [{
            'properties': {
                'title': sheet_tab,
            }
        }]
    }
    spreadsheet = API_Sheets(auth).spreadsheets().create(body=body).execute()
    sheet_id = spreadsheet['spreadsheetId']
    tab_id = spreadsheet['sheets'][0]['properties']['title']
    created = True

  # if creating tab from template
  if (created or tab_id is None) and template_sheet and template_tab:
    if project.verbose:
      print('SHEET TAB COPY', sheet_tab)
    sheets_tab_copy(auth, template_sheet, template_tab, sheet_id, sheet_tab,
                    True)

  # if creating a blank tab
  elif tab_id is None:
    if project.verbose:
      print('SHEET TAB CREATE', sheet_name, sheet_tab)
    sheets_tab_create(auth, sheet_name, sheet_tab)

  # if sheet and tab already exist
  else:
    if project.verbose:
      print('SHEET EXISTS', sheet_name, sheet_tab)

  return sheet_id, tab_id, created
