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

""" Enable the Vision API to use a URI as request/response key instead of order.

The vision API does not return the imageURI in the response, relying instead
on the order of the resonse objects to map to the order of the request objects.
For bulk calls or databases like BigQuery the order of the responses is
not deterministic.

This modeul preserves the imageURI value between request and response. Enabling
a mapping between the two based on a unique key.

Also for convenience the 16 item request limit is abstracted away.
"""

from urllib.error import HTTPError

from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_Vision
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project


def vision_annotate():

  body = {
    "requests":[],
    "parent": 'projects/' + project.id
  }

  uri_buffer = []

  for request_index, request in enumerate(get_rows(project.task['auth'], project.task['requests'], as_object=True)):

   # submit 16 requests at a time
   if request_index > 0 and request_index % 16 == 0:
     for response_index, response in enumerate(API_Vision(project.task['auth'], iterate=True).images().annotate(body=body).execute()):
       response['imageUri'] = uri_buffer[response_index]
       yield response

     uri_buffer = []
     body['requests'] = []

   # buffer the URI, and add requests to the batch request
   else:
     uri = request['image'].get('source', {}).get('imageUri', 'image %s' % request_index)
     uri_buffer.append(uri)

     if project.verbose:
       print('URI', uri)

     if 'content' in request['image'] and 'source' in request['image']:
       del request['image']['source']

     body['requests'].append(request)

   # clean up last requests
   if body['requests']:
     for response_index, response in enumerate(API_Vision(project.task['auth'], iterate=True).images().annotate(body=body).execute()):
       response['imageUri'] = uri_buffer[response_index]
       yield response


@project.from_parameters
def vision_api():

  # Eventually add format detection or parameters to put_rows
  if 'bigquery' in project.task['responses']:
    project.task['responses']['bigquery']['format'] = 'JSON'

  schema = Discovery_To_BigQuery(
    'vision',
    'v1'
  ).resource_schema(
    'AnnotateImageResponse'
  )

  # append URI to results for mapping
  schema.insert(0, {'description': 'Mapping back to request.', 'name': 'imageUri', 'type': 'STRING', 'mode': 'REQUIRED'})

  put_rows(
    project.task['auth'],
    project.task['responses'],
    vision_annotate(),
    schema
  )

if __name__ == '__main__':
  vision_api()
