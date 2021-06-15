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

""" Recipe handler for "url" task.

Allows a list of URLs to be pulled from the web and places into a table or sheet.
Leverages get_rows and put_rows JSON pattern for IO. See docs.
For sample use see scripts/url.json. Allows flagging status and or content in response.

"""

from typing import Iterator
from urllib import request
from urllib.error import HTTPError
from http.client import InvalidURL

from starthinker.util.data import get_rows
from starthinker.util.data import put_rows


URL_SCHEMA = [
  { 'name': 'URI', 'type': 'STRING', 'mode': 'NULLABLE' },
  { 'name': 'URL', 'type': 'STRING', 'mode': 'REQUIRED' },
  { 'name': 'Status', 'type': 'INTEGER', 'mode': 'NULLABLE' },
  { 'name': 'Read', 'type': 'BYTES', 'mode': 'NULLABLE' },
]


def url_fetch(config, task) -> Iterator[dict]:
  """Fetch URL list and return both status code and/or contents.

  Takes no parameters, it operates on recipe JSON directly. Core
  function is to call urlopen on each passed in URL.

  Returns:
    Produces a dictionary generator with record matching URL_SCHEMA.

  """

  for url, uri in get_rows(config, task['auth'], task['urls']):

    if config.verbose:
      print('URL/URI', url, uri)

    record = {
      'URL':url,
      'URI':None if uri is None else str(uri)
    }

    url_request = request.Request(url, data=task.get('data'))
    try:
      url_response = request.urlopen(url_request)

      if task.get('status', False):
        record['Status'] = url_response.status

      if task.get('read', False):
        record['Read'] = url_response.read()

    except InvalidURL as error:
      if task.get('status', False):
        record['Status'] = 400

    except HTTPError as error:
      if task.get('status', False):
        record['Status'] = error.status

    except Exception as error:
      if task.get('status', False):
        record['Status'] = 500

    yield record


def url(config, task:dict) -> None:
  """Entry point for URL task, which pulls URL information from web.

  Designed solely to fetch status and/or content from a list of URLs.
  Leverages url_fetch as generator to preserve memory.

  """

  # Eventually add format detection or parameters to put_rows
  if 'bigquery' in task['to']:
    task['to']['bigquery']['format'] = 'JSON'

  put_rows(
    config,
    task['auth'],
    task['to'],
    url_fetch(config, task),
    URL_SCHEMA
  )
