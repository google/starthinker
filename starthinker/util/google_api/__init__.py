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

import json
import traceback
import httplib2
from time import sleep
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource
from ssl import SSLError

try:
  import httplib
except:
  import http.client as httplib

from starthinker.util.auth import get_service
from starthinker.util.project import project

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
    * job: (object) Everything before the execute() statement.
    * key: (string) key of value from data to return.
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
      elif content.get(
          'error', {}).get('status') == 'PERMISSION_DENIED' or content.get(
              'error', {}).get('errors', [{}])[0].get('reason') == 'forbidden':
        raise
      elif retries > 0:
        if project.verbose:
          print('API ERROR:', str(e))
        if project.verbose:
          print('API RETRY / WAIT:', retries, wait)
        sleep(wait)
        return API_Retry(job, key, retries - 1, wait * 2)
      # if no retries, raise
      else:
        raise
    # raise all other errors that cannot be overcome
    else:
      raise

  # HTTP transport errors
  except RETRIABLE_EXCEPTIONS as e:
    if retries > 0:
      if project.verbose:
        print('HTTP ERROR:', str(e))
      if project.verbose:
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
      if project.verbose:
        print('SSL ERROR:', str(e))
      if project.verbose:
        print('SSL RETRY / WAIT:', retries, wait)
      sleep(wait)
      return API_Retry(job, key, retries - 1, wait * 2)
    else:
      raise


def API_Iterator(function, kwargs, results=None):
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

        https://developers.google.com/doubleclick-advertisers/v3.3/placements/list

        function = get_service('dfareporting', 'v3.3', 'user').placements().list
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

    Returns:
      Iterator over JSON objects.
    """

    def __init__(self, function, kwargs, results=None):
      self.function = function
      self.kwargs = kwargs
      self.results = results
      self.position = 0
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
        if self.iterable is None and project.verbose:
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

      # if results remain, return them
      if self.iterable and self.position < len(self.results[self.iterable]):
        value = self.results[self.iterable][self.position]
        self.position += 1
        return value

      # if pages and results exhausted, stop
      else:
        raise StopIteration

  return iter(API_Iterator_Instance(function, kwargs, results))


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

    configuration = {
      "api":"doubleclickbidmanager",
      "version":"v1",
      "auth":"user",
      "iterate":False
    }
    api = API(configuration).placements().list(profile_id=1234,
    archived=False).execute()

    Args:
      configuration: (json) see example above, configures all API parameters

    Returns:
      If nextpageToken in result or iterate is True: return iterator of API
      response
      Otherwise: returns API response
  """

  def __init__(self, configuration):
    self.api = configuration['api']
    self.version = configuration['version']
    self.auth = configuration['auth']
    self.uri = configuration.get('uri', None)
    self.key = configuration.get('key', None)
    self.function_stack = list(
        filter(None,
               configuration.get('function', '').split('.')))
    self.function_kwargs = configuration.get('kwargs', {})
    self.iterate = configuration.get('iterate', False)
    self.headers = configuration.get('headers', {})

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
      self.function_kwargs = kwargs
      return self

    return function_call

  # for calling function via string ( chain using dot notation )
  def call(self, function_chain):
    for function_name in function_chain.split('.'):
      self.function_stack.append(function_name)
    return self

  # matches API execute with built in iteration and retry handlers
  def execute(self, run=True, iterate=True):
    # start building call sequence with service object
    self.function = get_service(
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

      # if paginated, automatically iterate
      if (iterate and (self.iterate or (isinstance(self.response, dict) and
                                        'nextPageToken' in self.response))):
        return API_Iterator(self.function, self.function_kwargs, self.response)

      # if not paginated, return object as is
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


def API_BigQuery(auth, iterate=False):
  """BigQuery helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'bigquery',
      'version': 'v2',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_DBM(auth, iterate=False):
  """DBM helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'doubleclickbidmanager',
      'version': 'v1.1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Sheets(auth, iterate=False):
  """DBM helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'sheets',
      'version': 'v4',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_DCM(auth, iterate=False, internal=False):
  """DCM helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'dfareporting',
      'version': 'v3.4',
      'auth': auth,
      'iterate': iterate
  }

  if internal:
    from starthinker.util.dcm.internalv33_uri import URI as DCM_URI
    configuration['version'] = 'internalv3.3'
    configuration['uri'] = DCM_URI

  return API(configuration)


def API_SNIPPETS(auth, iterate=False):
  """Snippets helper configuration for Google API.

  Defines agreed upon version.
  """

  from starthinker.util.snippets.snippets_v1 import URI as SNIPPETS_URI

  # fetch discovery uri using: wget https://snippets-hrdb.googleplex.com/_ah/api/discovery/v1/apis/snippets/v1/rest
  configuration = {
      'api': 'snippets',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate,
      'uri': SNIPPETS_URI
  }

  return API(configuration)


def API_Datastore(auth, iterate=False):
  """Datastore helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'datastore',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_StackDriver(auth, iterate=False):
  """StackDriver helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'logging',
      'version': 'v2',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_PubSub(auth, iterate=False):
  """PubSub helper configuration for Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'pubsub',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Analytics(auth, iterate=False):
  """Analytics helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'analytics',
      'version': 'v3',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_YouTube(auth, iterate=False):
  """YouTube helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'youtube',
      'version': 'v3',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Drive(auth, iterate=False):
  """Drive helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'drive',
      'version': 'v3',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Cloud(auth, iterate=False):
  """Cloud project helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'cloudresourcemanager',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_DV360(auth, iterate=False):
  """Cloud project helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'displayvideo',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Storage(auth, iterate=False):
  """Cloud storage helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'storage',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Gmail(auth, iterate=False):
  """Gmail helper configuration Google API.

  Defines agreed upon version.
  """

  configuration = {
      'api': 'gmail',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)


def API_Compute(auth, iterate=False):
  """Compute helper configuration Google API.

     https://cloud.google.com/compute/docs/reference/rest/v1/
  """

  configuration = {
      'api': 'compute',
      'version': 'v1',
      'auth': auth,
      'iterate': iterate
  }
  return API(configuration)
