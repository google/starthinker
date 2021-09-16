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
"""Thin wrapper around Google Sevice API for integraton into StarThinker.

This does not change or augment the standard API calls other than the following:

  * Allows passing of auth parameter to constructor, required for switching.
  * Execute statement is overloaded to include iterator for responses with
  nextPageToken.
  * Retries handle some common errors and have a back off scheme.
  * JSON based configuration allows StarThinker recipe definitions.
  * Pre-defined functions for each API can be added to fix version and uri
  options.

"""

import base64
import json
import traceback
import httplib2
from datetime import date
from time import sleep
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource
from ssl import SSLError
from typing import Union

try:
  import httplib
except:
  import http.client as httplib

from starthinker.util.auth import get_service

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


def API_Retry(job, key=None, retries=3, wait=31):
  """ API retry that includes back off and some common error handling.

  CAUTION:  Total timeout cannot exceed 5 minutes or the SSL token expires for
  all future calls.

  For critical but recoverable errors, the back off executes [retry] times.
  Each time the [wait] is doubled.
  By default retries are: 0:31 + 1:02 + 2:04 = 3:37 ( minutes )
  The recommended minimum wait is 60 seconds for most APIs.

  * Errors retried: 429, 500, 503
  * Errors ignored: 409 - already exists ( triggered by create only and also
  returns None )
  * Errors raised: ALL OTHERS

  Args:
    * job: (object) API call path, everything before the execute() statement to retry.
    * key: (string) Optional key from json reponse to return.
    * retries: (int) Number of times to try the job.
    * wait: (seconds) Time to wait in seconds between retries.

  Returns:
    * JSON result of job or key value from JSON result if job succeed.
    * None if object already exists.

  Raises:
    * Any exceptions not listed in comments above.

  """

  try:
    # try to run the job and return the response
    data = job.execute()
    return data if not key else data.get(key, [])

  # API errors
  except HttpError as e:
    # errors that can be overcome or re-tried ( 403 is rate limit and others, needs deep dive )
    if e.resp.status in [403, 409, 429, 500, 503]:
      content = json.loads(e.content.decode())
      # already exists ( ignore benign )
      if content['error']['code'] == 409:
        return None
      # permission denied ( won't change on retry so raise )
      elif content.get('error', {}).get('status') == 'PERMISSION_DENIED' or content.get('error', {}).get('errors', [{}])[0].get('reason') == 'forbidden':
        print('ERROR DETAILS:', e.content.decode())
        raise
      elif retries > 0:
        print('API ERROR:', str(e))
        print('API RETRY / WAIT:', retries, wait)
        sleep(wait)
        return API_Retry(job, key, retries - 1, wait * 2)
      # if no retries, raise
      else:
        print('ERROR DETAILS:', e.content.decode())
        raise
    # raise all other errors that cannot be overcome
    else:
      raise

  # HTTP transport errors
  except RETRIABLE_EXCEPTIONS as e:
    if retries > 0:
      print('HTTP ERROR:', str(e))
      print('HTTP RETRY / WAIT:', retries, wait)
      sleep(wait)
      return API_Retry(job, key, retries - 1, wait * 2)
    else:
      raise

  # SSL timeout errors
  except SSLError as e:
    # most SSLErrors are not retriable, only timeouts, but
    # SSLError has no good error type attribute, so we search the message
    if retries > 0 and 'timed out' in e.message:
      print('SSL ERROR:', str(e))
      print('SSL RETRY / WAIT:', retries, wait)
      sleep(wait)
      return API_Retry(job, key, retries - 1, wait * 2)
    else:
      raise


def API_Iterator(function, kwargs, results=None, limit=None):
  """ See below API_Iterator_Instance for documentaion, this is just an iter wrapper.

      Returns:
        iter(API_Iterator_Instance(function, kwargs, results))
  """

  class API_Iterator_Instance():
    """A helper class that iterates multiple results, automatically called by execute.

      This is a standard python iterator definition, no need to document
      functions.

      The only job this has is to handle Google API iteration, as such it can be
      called
      on any API call that reurns a 'nextPageToken' in the result.

      For example if calling the DCM list placement API:

        https://developers.google.com/doubleclick-advertisers/v3.4/placements/list

        function = get_service(config, 'dfareporting', 'v3.4', 'user').placements().list
        kwargs = { 'profile_id':1234, 'archived':False }
        for placement in API_Iterator(function, kwargs):
          print(placement)

      Can be called independently but automatically built into API...execute()
      so
      use that instead.

      Args:
        function: (function) function of API call to iterate, definiton not
          instance. kwargs" (dict) arguments to be passed to the function on
          each fetch results (json) optional, the first set of results given (
          if already fetched )
       kwargs: (dict) arguments to pass to fucntion when making call.
       results: (object) optional / used recursively, prior call results to continue.
       limit: (int) maximum number of records to return

    Returns:
      Iterator over JSON objects.
    """

    def __init__(self, function, kwargs, results=None, limit=None):
      self.function = function
      self.kwargs = kwargs
      self.limit = limit
      self.results = results
      self.position = 0
      self.count = 0
      self.iterable = None
      self.__find_tag__()

    def __find_tag__(self):
      # find the only list item for a paginated response, JOSN will only have list type, so ok to be specific
      if self.results:  # None and {} both excluded
        for tag in iter(self.results.keys()):
          if isinstance(self.results[tag], list):
            self.iterable = tag
            break

        # this shouldn't happen but some APIs simply omit the key if no results
        if self.iterable is None:
          print('WARNING API RETURNED NO KEYS WITH LISTS:',
                ', '.join(self.results.keys()))

    def __iter__(self):
      return self

    def __next__(self):
      return self.next()

    def next(self):

      # if no initial results, get some, empty results {} different
      if self.results is None:
        self.results = API_Retry(self.function(**self.kwargs))
        self.__find_tag__()

      # if empty results or exhausted page, get next page
      if self.iterable and self.position >= len(self.results[self.iterable]):
        page_token = self.results.get('nextPageToken', None)
        if page_token:

          if 'body' in self.kwargs:
            self.kwargs['body']['pageToken'] = page_token
          else:
            self.kwargs['pageToken'] = page_token

          self.results = API_Retry(self.function(**self.kwargs))
          self.position = 0

        else:
          raise StopIteration

      # if results remain, return them ( sometimes the iterable is missing )
      if self.iterable and self.position < len(self.results.get(self.iterable, 0)):
        value = self.results[self.iterable][self.position]
        self.position += 1

        # if reached limit, stop
        if self.limit is not None:
          self.count += 1
          if self.count > self.limit:
            raise StopIteration

        # otherwise return next value
        return value

      # if pages and results exhausted, stop
      else:
        raise StopIteration

  return iter(API_Iterator_Instance(function, kwargs, results, limit))


class API():
  """A wrapper around Google API with built in helpers for StarThinker.

    The wrapper mimics function calls, storing the m in a stack, until it
    encounters
    execute().  Then it uses the stored stack and arguments to call the actual
    API.
    This allows handlers on execute such as API_Retry and API_Iterator.

    See module level description for wrapped changes to Google API.  The class
    is
    designed to be a connector to JSON, hence the configuraton is a JSON object.

    api = {
      "api":"doubleclickbidmanager",
      "version":"v1.1",
      "auth":"user",
      "iterate":False
    }
    api = API(config, api).placements().list(profile_id=1234,
    archived=False).execute()

    Args:
      config: (json) see example above, configures all authentication parameters
      api: (json) see example above, configures all API parameters

    Returns:
      If nextpageToken in result or iterate is True: return iterator of API
      response
      Otherwise: returns API response
  """

  def __init__(self, config, api):
    self.config = config
    self.api = api['api']
    self.version = api['version']
    self.auth = api['auth']
    self.uri = api.get('uri', None)
    self.key = api.get('key', None)
    self.function_stack = list(
        filter(None,
               api.get('function', '').split('.')))
    self.function_kwargs = API.__clean__(api.get('kwargs', {}))
    self.iterate = api.get('iterate', False)
    self.limit = api.get('limit', None)
    self.headers = api.get('headers', {})

    self.function = None
    self.job = None
    self.response = None

  # for debug purposes
  def __str__(self):
    return '%s.%s.%s' % (self.api, self.version, '.'.join(self.function_stack))

  # builds API function stack
  def __getattr__(self, function_name):
    self.function_stack.append(function_name)

    def function_call(**kwargs):
      self.function_kwargs = API.__clean__(kwargs)
      return self

    return function_call

  @staticmethod
  def __clean__(struct:Union[dict, list]) -> Union[dict, list]:
    """Helper to recursively clean up JSON data for API call.

    Converts bytes -> base64.
    Converts date -> str (yyyy-mm-dd).
    TODO: Add Converts datetime, time -> string.

    Args:
      struct: The kwargs being cleaned up.

    Returns:
      struct: The kwargs with replacments.

    """

    if isinstance(struct, dict):
      for key, value in struct.items():
        if isinstance(value, bytes):
          struct[key] = base64.standard_b64encode(value).decode("ascii")
        elif isinstance(value, date):
          struct[key] = str(value)
        else:
          API.__clean__(value)
    elif isinstance(struct, list):
      for index, value in enumerate(struct):
        if isinstance(value, bytes):
          struct[index] = base64.standard_b64encode(value).decode("ascii")
        elif isinstance(value, date):
          struct[index] = str(value)
        else:
          API.__clean__(value)
    return struct


  # for calling function via string ( chain using dot notation )
  def call(self, function_chain):
    for function_name in function_chain.split('.'):
      self.function_stack.append(function_name)
    return self

  # matches API execute with built in iteration and retry handlers
  def execute(self, run=True, iterate=False, limit=None):
    # start building call sequence with service object
    self.function = get_service(
        config=self.config,
        api=self.api,
        version=self.version,
        auth=self.auth,
        headers=self.headers,
        key=self.key,
        uri_file=self.uri)

    # build calls along stack
    # do not call functions, as the abstract is necessary for iterator page next calls
    for f_n in self.function_stack:
      #print(type(self.function), isinstance(self.function, Resource))
      self.function = getattr(
          self.function
          if isinstance(self.function, Resource) else self.function(), f_n)

    # for cases where job is handled manually, save the job
    self.job = self.function(**self.function_kwargs)

    if run:
      self.response = API_Retry(self.job)

      # if expect to iterate through records
      if iterate or self.iterate:
        return API_Iterator(self.function, self.function_kwargs, self.response, limit or self.limit)

      # if basic response, return object as is
      else:
        return self.response

    # if not run, just return job object ( for chunked upload for example )
    else:
      return self.job

  def upload(self, retries=5, wait=61):
    job = self.execute(run=False)
    response = None

    while response is None:
      error = None

      try:
        print('Uploading file...')
        status, response = job.next_chunk()
        if 'id' in response:
          print("Object id '%s' was successfully uploaded." % response['id'])
        else:
          exit('The upload failed with an unexpected response: %s' % response)

      except HttpError as e:
        if retries > 0 and e.resp.status in RETRIABLE_STATUS_CODES:
          error = 'A retriable HTTP error %d occurred:\n%s' % (
              e.resp.status, e.content.decode())
        else:
          raise

      except RETRIABLE_EXCEPTIONS as e:
        if retries > 0:
          error = 'A retriable error occurred: %s' % e
        else:
          raise

      if error is not None:
        print(error)
        retries -= 1
        wait = wait * 2
        print('Sleeping %d seconds and then retrying...' % wait)
        time.sleep(wait)


def API_BigQuery(config, auth, iterate=False):
  """BigQuery helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'bigquery',
      'version': 'v2',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_DBM(config, auth, iterate=False):
  """DBM helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'doubleclickbidmanager',
      'version': 'v1.1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Sheets(config, auth, iterate=False):
  """DBM helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'sheets',
      'version': 'v4',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_DCM(config, auth, iterate=False, internal=False):
  """DCM helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'dfareporting',
      'version': 'v3.5',
      'auth': auth,
      'iterate': iterate
  }

  if internal:
    from starthinker.util.cm_internalv34_uri import URI as DCM_URI
    api['version'] = 'internalv3.4'
    api['uri'] = DCM_URI

  return API(config, api)


def API_Datastore(config, auth, iterate=False):
  """Datastore helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'datastore',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_StackDriver(config, auth, iterate=False):
  """StackDriver helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'logging',
      'version': 'v2',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_PubSub(config, auth, iterate=False):
  """PubSub helper configuration for Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'pubsub',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_SearchAds(config, auth, iterate=False):
  """Search Ads helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'doubleclicksearch',
      'version': 'v2',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Analytics(config, auth, iterate=False):
  """Analytics helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'analytics',
      'version': 'v3',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_AnalyticsReporting(config, auth, iterate=False):
  """AnalyticsReporting helper configuration Google API.

  Defines agreed upon version for use in all tasks.
  """

  api = {
      'api': 'analyticsreporting',
      'version': 'v4',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_YouTube(config, auth, iterate=False):
  """YouTube helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'youtube',
      'version': 'v3',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Drive(config, auth, iterate=False):
  """Drive helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'drive',
      'version': 'v3',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Cloud(config, auth, iterate=False):
  """Cloud project helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'cloudresourcemanager',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_DV360(config, auth, iterate=False):
  """Cloud project helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'displayvideo',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Storage(config, auth, iterate=False):
  """Cloud storage helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'storage',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Gmail(config, auth, iterate=False):
  """Gmail helper configuration Google API.

  Defines agreed upon version.
  """

  api = {
      'api': 'gmail',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Compute(config, auth, iterate=False):
  """Compute helper configuration Google API.

     https://cloud.google.com/compute/docs/reference/rest/v1/
  """

  api = {
      'api': 'compute',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)


def API_Vision(config, auth, iterate=False):
  """Vision helper configuration Google API.

    https://cloud.google.com/vision/docs/reference/rest
  """

  api = {
      'api': 'vision',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(config, api)
