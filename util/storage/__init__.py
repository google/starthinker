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

#https://google.github.io/google-api-python-client/docs/epy/googleapiclient.http-module.html
#https://raw.githubusercontent.com/GoogleCloudPlatform/storage-file-transfer-json-python/master/chunked_transfer.py
#https://cloud.google.com/storage/docs/json_api/v1/buckets/insert#try-it
#https://cloud.google.com/storage/docs/json_api/v1/buckets/setIamPolicy
#https://developers.google.com/resources/api-libraries/documentation/storage/v1/python/latest/index.html

import os
import errno
import json
import traceback
import httplib2
from time import sleep
from io import BytesIO

from google.cloud import storage
from apiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from starthinker.setup import BUFFER_SCALE
from starthinker.util.project import project
from starthinker.util.auth import get_service, get_client
from starthinker.util.google_api import API_Retry


CHUNKSIZE = int(200 * 1024000 * BUFFER_SCALE) # scale is controlled in setup.py
RETRIES = 3


def makedirs_safe(path):
  try: os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path): pass
    else: raise


def parse_path(path):
  try: return path.rsplit('/', 1)[0]
  except: return ''


def parse_filename(path, url=False):
  f = ''
  try: 
    f = path.rsplit('/', 1)[1]
    if url: f = f.split('?', 1)[0]
  except: pass
  return f


def media_download(request, chunksize):
  data = BytesIO()
  media = MediaIoBaseDownload(data, request, chunksize=chunksize)

  retries = 0
  done = False
  while not done:
    error = None
    try:
      progress, done = media.next_chunk()
      if progress: print 'Download %d%%' % int(progress.progress() * 100)
      data.seek(0)
      yield data
      data.seek(0)
      data.truncate(0)
    except HttpError, err:
      error = err
      if err.resp.status < 500: raise
    except (httplib2.HttpLib2Error, IOError), err:
      error = err

    if error:
      retries += 1
      if retries > RETRIES: raise error
      else: sleep(5 * retries)
    else:
      retries = 0

  print 'Download 100%'


def object_get(auth, path):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)
  return service.objects().get_media(bucket=bucket, object=filename).execute()


def object_get_chunks(auth, path, chunksize=1024000):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)

  data = BytesIO()
  request = service.objects().get_media(bucket=bucket, object=filename)
  media = MediaIoBaseDownload(data, request, chunksize=chunksize)

  retries = 0
  done = False
  while not done:
    error = None
    try:
      progress, done = media.next_chunk()
      if progress: print 'Download %d%%' % int(progress.progress() * 100)
      data.seek(0)
      yield data
      data.seek(0)
      data.truncate(0)
    except HttpError, err:
      error = err
      if err.resp.status < 500: raise
    except (httplib2.HttpLib2Error, IOError), err:
      error = err

    if error:
      retries += 1
      if retries > RETRIES: raise error
      else: sleep(5 * retries)
    else:
      retries = 0

  print 'Download End'


def object_put(auth, path, data, mimetype='application/octet-stream'):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)

  media = MediaIoBaseUpload(data, mimetype=mimetype, chunksize=CHUNKSIZE, resumable=True)
  request = service.objects().insert(bucket=bucket, name=filename, media_body=media)

  response = None
  errors = 0
  while response is None:
    error = None
    try:
      status, response = request.next_chunk()
      if project.verbose and status: print "Uploaded %d%%." % int(status.progress() * 100)
    except HttpError, e:
      if e.resp.status < 500: raise
      error = e
    except (httplib2.HttpLib2Error, IOError), e:
      error = e

    errors = (errors + 1) if error else 0
    if errors > RETRIES: raise error

  if project.verbose: print "Uploaded 100%."


def object_list(auth, path, raw=False, files_only=False):
  bucket, prefix = path.split(':', 1)
  service = get_service('storage', 'v1', auth)
  next_page = None
  while next_page != '':
    response = service.objects().list(bucket=bucket, prefix=prefix).execute()
    next_page = response.get('nextPageToken', '')
    for item in response.get('items', []): 
      if files_only and item['name'].endswith('/'): continue
      yield item if raw else '%s:%s' % (bucket, item['name']) 


def object_copy(auth, path_from, path_to):
  from_bucket, from_filename = path_from.split(':', 1)
  to_bucket, to_filename = path_to.split(':', 1)

  body = {
    "kind": "storage#object",
    "bucket":to_bucket,
    "name":to_filename,
    "storageClass":"REGIONAL",
  }

  service = get_service('storage', 'v1', auth)
  return service.objects().rewrite(sourceBucket=from_bucket, sourceObject=from_filename, destinationBucket=to_bucket, destinationObject=to_filename, body=body).execute()


def object_delete(auth, path):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)
  return service.objects().delete(bucket=bucket, object=filename).execute()


def object_move(auth, path_from, path_to):
  object_copy(auth, path_from, path_to)
  object_delete(auth, path_from)


def bucket_get(auth, name):
  service = get_service('storage', 'v1', auth)
  try: return service.buckets().get(bucket=name).execute()
  except HttpError, e:
    if e.resp.status == 404: return None
    elif e.resp.status in [403, 500, 503]: sleep(5)
    else: raise


def bucket_create(auth, project, name):
  if bucket_get(auth, name) is None:
    body = {
      "kind": "storage#bucket",
      "name":name,
      "storageClass":"REGIONAL",
      "location":"us-west1",
    }
    service = get_service('storage', 'v1', auth)

    try:
      return service.buckets().insert(project=project, body=body).execute()
      sleep(1)
    except HttpError, e:
      if e.resp.status in [403, 500, 503]: sleep(5)
      elif json.loads(e.content)['error']['code'] == 409: pass # already exists ( ignore )
      else: raise


def bucket_delete(auth, name):
  service = get_service('storage', 'v1', auth)
  return service.buckets().delete(bucket=name).execute()


#role = OWNER, READER, WRITER
def bucket_access(auth, project, name,  role, emails=[], groups=[], services=[], domains=[]):
  service = get_service('storage', 'v1', auth)

  entities = map(lambda e: 'user-%s' % e, emails) + \
    map(lambda e: 'group-%s' % e, groups) + \
    map(lambda e: 'user-%s' % e, services) + \
    map(lambda e: 'domain-%s' % e, domains)

  for entity in entities:
    body = {
      "kind": "storage#bucketAccessControl",
      "bucket":name,
      "entity":entity,
      "role":role
    }
    API_Retry(service.bucketAccessControls().insert(bucket=name, body=body))

# Alternative for managing permissions ( overkill? )
#  if emails or groups or services or groups:
#    access = service.buckets().getIamPolicy(bucket=name).execute(num_retries=RETRIES)
#
#    access['bindings'] = []
#    for r in role:
#      access['bindings'].append({
#        "role":"roles/storage.object%s" % r,
#        "members": ['user:%s' % m for m in emails] + \
#                   ['group:%s' % m for m in groups] + \
#                   ['serviceAccount:%s' % m for m in services] + \
#                   ['domain:%s' % m for m in domains]
#      })
#
#    job = service.buckets().setIamPolicy(bucket=name, body=access).execute(num_retries=RETRIES)
#    sleep(1)


# USE: object_get function above ( it will pull the download down in memory, no need for a file write )
def object_download(gc_project, bucket_name, object_name, local_path, auth='user'):
  client = get_client('storage', auth=auth)

  print "BN", bucket_name

  try:
    bucket = client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=object_name)

    dest = local_path if local_path != None else object_name

    for blob in blobs:
      with open(dest, 'wb') as file_obj:
        blob.download_to_file(file_obj)

    return dest if os.path.isfile(dest) else None
  except Exception, ex:
    traceback.print_exc()

