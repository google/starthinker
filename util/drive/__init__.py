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

# https://developers.google.com/drive/api/v3/manage-uploads
# https://developers.google.com/drive/api/v3/reference/about#methods

import json
import mimetypes
from io import BytesIO
from StringIO import StringIO
from googleapiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload

from setup import BUFFER_SCALE
from util.project import project
from util.auth import get_service

CHUNKSIZE = int(200 * 1024000 * BUFFER_SCALE) # scale is controlled in setup.py

# This file is undergoing maintenanace, please start using new funtions further down

def files_copy(auth, file_id, body={}):
  drive = get_service('drive', 'v3', auth)
 
  return drive.files().copy(fileId=file_id, body=body).execute()


def find_file(auth, parent, name):
   drive = get_service('drive', 'v3', auth)
   return drive.files().list(q='name = \'%s\' and \'%s\' in parents' % (name, parent)).execute()


def create_folder(auth, parent, name):
   drive = get_service('drive', 'v3', auth)

   file_metadata = {
     'name' : name,
     'parents' : [parent],
     'mimeType' : 'application/vnd.google-apps.folder'
   }
   return drive.files().create(body=file_metadata, fields='id').execute()


# START NEW FUNCTIONS
# New handlers being built below this line ( with additional error handling and robustness


def _retry(job, retries=10, wait=5):
  try:
    data = job.execute()
  except HttpError, e:
    if project.verbose: print str(e)
    if e.resp.status in [403, 429, 500, 503]:
      if retries > 0:
        sleep(wait)
        if project.verbose: print 'DCM RETRY', retries
        return _retry(job, retries - 1, wait * 2)
      elif json.loads(e.content)['error']['code'] == 409:
        pass # already exists ( ignore )
      else:
        raise
    else:
      raise
  return data


def about(auth, fields='importFormats'):
  drive = get_service('drive', 'v3', auth)
  response = _retry(drive.about().get(fields=fields))
  #if project.verbose: print json.dumps(response, indent=4)
  return response


def file_find(auth, name, parent = None):
   drive = get_service('drive', 'v3', auth)

   query = "trashed = false and name = '%s'" % name
   if parent: query = "%s and '%s' in parents" % (query, parent)

   try: return (_retry(drive.files().list(q=query))['files'] or [None])[0]
   except HttpError: return None


def file_create(auth, name, filename, data, parent=None):
  """Checks if file with name already exists ( outside of trash ) and 
    if not, uploads the file.  Determines filetype based on filename extension
    and attempts to map to Google native such as Docs, Sheets, Slides, etc...

    For example:
      file_Create('user', 'Sample Document', 'sample.txt', StringIO('File contents')) 
      Creates a Google Document object in the user's drive.

      file_Create('user', 'Sample Sheet', 'sample.csv', StringIO('col1,col2\nrow1a,row1b\n')) 
      Creates a Google Sheet object in the user's drive.

    See: https://developers.google.com/drive/api/v3/manage-uploads 

    Args:
      auth: (string) specify 'service' or 'user' to toggle between credentials used to access
      name: (string) name of file to create, used as key to check if file exists
      filename: ( string) specified as "file.extension" only to automate detection of mime type.
      data: (StringIO) any file like object that can be read from
      parent: (string) the Google Drive to upload the file to

    Returns:
      Json specification of file created or existing.

    """

  # attempt to find the file by name ( not in trash )
  drive_file = file_find(auth, name, parent)

  # if file exists, return it, prevents obliterating user changes
  if drive_file:
    if project.verbose: print 'Drive: File exists.'

  # if file does not exist, create it
  else:
    if project.verbose: print 'Drive: Creating file.'

    # file mime is used for uplaod / fallback
    # drive mime attempts to map to a native Google format
    file_mime = mimetypes.guess_type(filename, strict=False)[0]
    drive_mime = about('importFormats')['importFormats'].get(file_mime, file_mime)[0]

    if project.verbose: print 'Drive Mimes:', file_mime, drive_mime

    # construct upload object, and stream upload in chunks
    body = {
      'name':name, 
      'parents' : [parent] if parent else [],
      'mimeType': drive_mime,
    }
  
    media = MediaIoBaseUpload(
      StringIO(data),
      mimetype=file_mime,
      chunksize=CHUNKSIZE,
      resumable=True
    )

    service = get_service('drive', 'v3', auth)
    drive_file = _retry(service.files().create(
      body=body,
      media_body=media,
      fields='id'
    ))
  
  # return JSON specification for the file
  return drive_file
