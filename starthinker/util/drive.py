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

# https://developers.google.com/drive/api/v3/manage-uploads
# https://developers.google.com/drive/api/v3/reference/about#methods

import re
import mimetypes
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

from starthinker.config import BUFFER_SCALE
from starthinker.util.google_api import API_Drive

CHUNKSIZE = int(200 * 1024000 *
                BUFFER_SCALE)  # scale is controlled in config.py

#https://drive.google.com/open?id=1um2RlasnKTvF_I6uVUsbmk4ioyW1Zemj
#https://drive.google.com/open?id=1NQH5-yP9LM2dGTuGvdOA31KO1OwblruC-dK92F5IVLE
#https://drive.google.com/open?id=1IM-Dnq5Pc1Lje6eTKrN1ubpclRcbvAROrmSn23xl7UI
#https://drive.google.com/open?id=1XMFEUBxpRuAy8qG5tg3AM0NVm9bklpCc6SelZHpPj-g

#https://docs.google.com/document/d/1XMFEUBxpRuAy8qG5tg3AM0NVm9bklpCc6SelZHpPj-g/edit
#https://docs.google.com/presentation/d/1IM-Dnq5Pc1Lje6eTKrN1ubpclRcbvAROrmSn23xl7UI/edit
#https://docs.google.com/spreadsheets/d/1YU8zXzmeqgQhnnRIs4FpNKfbZ2B_aN77XbSKHBEa_gc/edit
#https://datastudio.google.com/c/reporting/0B1dzmNeF4E-MZ21Zb1h6SnRoc28/page/L1MF
#https://datastudio.google.com/c/datasources/1a6K-XdPUzCYRXZp1ZcmeOUOURc9wn2Jj


def about(config, auth, fields='importFormats'):
  response = API_Drive(config, auth).about().get(fields=fields).execute()
  return response


def file_id(config, auth, url_or_name):

  if url_or_name.startswith('https://drive.google.com/open?id='):
    return url_or_name.split('?id=', 1)[-1]

  elif url_or_name.startswith('https://docs.google.com/'):
    m = re.search(
        '^(?:https:\/\/docs.google.com\/\w+\/d\/)([a-zA-Z0-9-_]+)(?:\/.*)?$',
        url_or_name)
    if m:
      return m.group(1)

  elif url_or_name.startswith('https://datastudio.google.com/'):
    m = re.search(
        '^(?:https:\/\/datastudio.google.com\/c\/\w+\/)([a-zA-Z0-9-_]+)(?:\/.*)?$',
        url_or_name)
    if m:
      return m.group(1)

  # check if name given convert to ID "Some Document"
  else:
    document = file_find(config, auth, url_or_name)
    if document:
      return document['id']

      # check if just ID given, "1uN9tnb-DZ9zZflZsoW4_34sf34tw3ff"
    else:
      m = re.search('^([a-zA-Z0-9-_]+)$', url_or_name)
      if m:
        return m.group(1)

  # probably a mangled id or name does not exist
  if config.verbose:
    print('DOCUMENT DOES NOT EXIST', url_or_name)
  return None


def file_get(config, auth, drive_id):
  return API_Drive(config, auth).files().get(fileId=drive_id).execute()


def file_exists(config, auth, name):
  drive_id = file_id(config, auth, name)
  if drive_id:
    try:
      API_Drive(config, auth).files().get(fileId=drive_id).execute()
      return True
    except HttpError:
      return False
  return False


def file_find(config, auth, name, parent=None):
  query = "trashed = false and name = '%s'" % name
  if parent:
    query = "%s and '%s' in parents" % (query, parent)

  try:
    return next(API_Drive(config, auth, iterate=True).files().list(q=query).execute())
  except StopIteration:
    return None


def file_delete(config, auth, name, parent=None):
  drive_id = file_id(config, auth, name)

  if drive_id:
    API_Drive(config, auth).files().delete(fileId=drive_id).execute()
    return True
  else:
    return False


def file_create(config, auth, name, filename, data, parent=None):
  """ Checks if file with name already exists ( outside of trash ) and

    if not, uploads the file.  Determines filetype based on filename extension
    and attempts to map to Google native such as Docs, Sheets, Slides, etc...

    For example:
    -  ```file_create('user', 'Sample Document', 'sample.txt', BytesIO('File
    contents'))```
    -  Creates a Google Document object in the user's drive.

    -  ```file_Create('user', 'Sample Sheet', 'sample.csv',
    BytesIO('col1,col2\nrow1a,row1b\n'))````
    -  Creates a Google Sheet object in the user's drive.

    See: https://developers.google.com/drive/api/v3/manage-uploads

    ### Args:
    -  * auth: (string) specify 'service' or 'user' to toggle between
    credentials used to access
    -  * name: (string) name of file to create, used as key to check if file
    exists
    -  * filename: ( string) specified as "file.extension" only to automate
    detection of mime type.
    -  * data: (BytesIO) any file like object that can be read from
    -  * parent: (string) the Google Drive to upload the file to

    ### Returns:
    -  * JSON specification of file created or existing.

    """

  # attempt to find the file by name ( not in trash )
  drive_file = file_find(config, auth, name, parent)

  # if file exists, return it, prevents obliterating user changes
  if drive_file:
    if config.verbose:
      print('Drive: File exists.')

  # if file does not exist, create it
  else:
    if config.verbose:
      print('Drive: Creating file.')

    # file mime is used for uplaod / fallback
    # drive mime attempts to map to a native Google format
    file_mime = mimetypes.guess_type(filename, strict=False)[0]
    drive_mime = about(config, auth, 'importFormats')['importFormats'].get(
        file_mime, file_mime)[0]

    if config.verbose:
      print('Drive Mimes:', file_mime, drive_mime)

    # construct upload object, and stream upload in chunks
    body = {
        'name': name,
        'parents': [parent] if parent else [],
        'mimeType': drive_mime,
    }

    media = MediaIoBaseUpload(
        BytesIO(data or ' '),  # if data is empty BAD REQUEST error occurs
        mimetype=file_mime,
        chunksize=CHUNKSIZE,
        resumable=True)

    drive_file = API_Drive(config, auth).files().create(
        body=body, media_body=media, fields='id').execute()

  return drive_file


def file_copy(config, auth, source_name, destination_name):
  destination_id = file_id(config, auth, destination_name)

  if destination_id:
    if config.verbose:
      print('Drive: File exists.')
    return file_get(config, auth, destination_id)

  else:
    source_id = file_id(config, auth, source_name)

    if source_id:
      body = {'visibility': 'PRIVATE', 'name': destination_name}
      return API_Drive(config, auth).files().copy(fileId=source_id, body=body).execute()
    else:
      return None


def folder_create(config, auth, name, parent=None):
  body = {
      'name': name,
      'parents': [parent] if parent else [],
      'mimeType': 'application/vnd.google-apps.folder'
  }
  return API_Drive(config, auth).files().create(body=body, fields='id').execute()
