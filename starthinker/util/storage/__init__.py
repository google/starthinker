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

import os
import errno
import json
import httplib2
from time import sleep
from io import BytesIO

from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from starthinker.config import BUFFER_SCALE
from starthinker.util.project import project
from starthinker.util.auth import get_service
from starthinker.util.google_api import API_Storage, API_Retry
from starthinker.util.csv import find_utf8_split

CHUNKSIZE = int(200 * 1024000 *
                BUFFER_SCALE)  # scale is controlled in config.py
RETRIES = 3


def makedirs_safe(path):
  try:
    os.makedirs(path)
  except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else:
      raise


def parse_path(path):
  try:
    return path.rsplit('/', 1)[0]
  except:
    return ''


def parse_filename(path, url=False):
  f = path
  try:
    if url:
      f = f.split('?', 1)[0]
    f = f.rsplit('/', 1)[1]
  except:
    pass
  return f


def media_download(request, chunksize, encoding=None):
  data = BytesIO()
  leftovers = b''

  media = MediaIoBaseDownload(data, request, chunksize=chunksize)

  retries = 0
  done = False
  while not done:
    error = None
    try:
      progress, done = media.next_chunk()
      if progress:
        print('Download %d%%' % int(progress.progress() * 100))

      data.seek(0)

      if encoding is None:
        yield data.read()

      elif encoding.lower() == 'utf-8':
        position = find_utf8_split(data)
        yield (leftovers + data.read(position)).decode(encoding)
        leftftovers = data.read()

      else:
        yield data.read().decode(encoding)

      data.seek(0)
      data.truncate(0)
    except HttpError as err:
      error = err
      if err.resp.status < 500:
        raise
    except (httplib2.HttpLib2Error, IOError) as err:
      error = err

    if error:
      retries += 1
      if retries > RETRIES:
        raise error
      else:
        sleep(5 * retries)
    else:
      retries = 0

  print('Download 100%')


def object_exists(auth, path):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)
  try:
    service.objects().get(bucket=bucket, object=filename).execute()
    return True
  except:
    return False


def object_get(auth, path):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)
  return service.objects().get_media(bucket=bucket, object=filename).execute()


def object_get_chunks(auth, path, chunksize=CHUNKSIZE, encoding=None):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)

  data = BytesIO()
  request = service.objects().get_media(bucket=bucket, object=filename)
  yield from media_download(request, chunksize, encoding)


def object_put(auth, path, data, mimetype='application/octet-stream'):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)

  media = MediaIoBaseUpload(
      data, mimetype=mimetype, chunksize=CHUNKSIZE, resumable=True)
  request = service.objects().insert(
      bucket=bucket, name=filename, media_body=media)

  response = None
  errors = 0
  while response is None:
    error = None
    try:
      status, response = request.next_chunk()
      if project.verbose and status:
        print('Uploaded %d%%.' % int(status.progress() * 100))
    except HttpError as e:
      if e.resp.status < 500:
        raise
      error = e
    except (httplib2.HttpLib2Error, IOError) as e:
      error = e

    errors = (errors + 1) if error else 0
    if errors > RETRIES:
      raise error

  if project.verbose:
    print('Uploaded 100%.')


def object_list(auth, path, raw=False, files_only=False):
  bucket, prefix = path.split(':', 1)
  for item in API_Storage(
      auth, iterate=True).objects().list(
          bucket=bucket, prefix=prefix).execute():
    if files_only and item['name'].endswith('/'):
      continue
    yield item if raw else '%s:%s' % (bucket, item['name'])


def object_copy(auth, path_from, path_to):
  from_bucket, from_filename = path_from.split(':', 1)
  to_bucket, to_filename = path_to.split(':', 1)

  body = {
      'kind': 'storage#object',
      'bucket': to_bucket,
      'name': to_filename,
      'storageClass': 'REGIONAL',
  }

  service = get_service('storage', 'v1', auth)
  return service.objects().rewrite(
      sourceBucket=from_bucket,
      sourceObject=from_filename,
      destinationBucket=to_bucket,
      destinationObject=to_filename,
      body=body).execute()


def object_delete(auth, path):
  bucket, filename = path.split(':', 1)
  service = get_service('storage', 'v1', auth)
  return service.objects().delete(bucket=bucket, object=filename).execute()


def object_move(auth, path_from, path_to):
  object_copy(auth, path_from, path_to)
  object_delete(auth, path_from)


def bucket_get(auth, name):
  service = get_service('storage', 'v1', auth)
  try:
    return service.buckets().get(bucket=name).execute()
  except HttpError as e:
    if e.resp.status == 404:
      return None
    elif e.resp.status in [403, 500, 503]:
      sleep(5)
    else:
      raise


def bucket_create(auth, project, name, location='us-west1'):
  if bucket_get(auth, name) is None:
    body = {
        'kind': 'storage#bucket',
        'name': name,
        'storageClass': 'REGIONAL',
        'location': location,
    }
    service = get_service('storage', 'v1', auth)

    try:
      return service.buckets().insert(project=project, body=body).execute()
      sleep(1)
    except HttpError as e:
      if e.resp.status in [403, 500, 503]:
        sleep(5)
      elif json.loads(e.content.decode())['error']['code'] == 409:
        pass  # already exists ( ignore )
      else:
        raise


def bucket_delete(auth, name):
  service = get_service('storage', 'v1', auth)
  return service.buckets().delete(bucket=name).execute()


#role = OWNER, READER, WRITER
def bucket_access(auth,
                  project,
                  name,
                  role,
                  emails=[],
                  groups=[],
                  services=[],
                  domains=[]):
  service = get_service('storage', 'v1', auth)

  entities = map(lambda e: 'user-%s' % e, emails) + \
    map(lambda e: 'group-%s' % e, groups) + \
    map(lambda e: 'user-%s' % e, services) + \
    map(lambda e: 'domain-%s' % e, domains)

  for entity in entities:
    body = {
        'kind': 'storage#bucketAccessControl',
        'bucket': name,
        'entity': entity,
        'role': role
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
