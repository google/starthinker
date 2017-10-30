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

