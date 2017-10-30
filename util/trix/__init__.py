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

from util.auth import get_service

def trix_update(auth, sheet_id, sheet_range, data, clear=False, valueInputOption='RAW'):
  sheets = get_service('sheets', 'v4', auth)
  if clear:
    sheets.spreadsheets().values().clear(spreadsheetId=sheet_id, range=sheet_range, body={}).execute()

  sheets.spreadsheets().values().update(
      spreadsheetId=sheet_id, range=sheet_range, body=data, valueInputOption=valueInputOption).execute()


def trix_batch_update(auth, sheet_id, data):
  sheets = get_service('sheets', 'v4', auth)
  sheets.spreadsheets().values().batchUpdate(spreadsheetId=sheet_id, body=data).execute()


def trix_read(auth, sheet_id, sheet_range):
  sheets = get_service('sheets', 'v4', auth)
  return sheets.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_range).execute()


