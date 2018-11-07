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


"""Thin wrapper around Google Sevice API for integraton into StarThinker.

This does not change or augment the standard API calls other than the following:

  - Allows passing of auth parameter to constructor, required for switching.
  - Execute statement is overloaded to include iterator for responses with nextPageToken. 
  - Retries handle some common errors and have a back off scheme.
  - JSON based configuration allows StarThinker recipe definitions.
  - Pre-defined functions for each API can be added to fix version and uri options.

"""

import json
import traceback
from time import sleep
from googleapiclient.errors import HttpError

import os.path
from setup import EXECUTE_PATH, INTERNAL_MODE
from util.auth import get_service
from util.project import project


def API_Retry(job, retries=10, wait=10):
  """ API retry that includes back off and some common error handling.

  Args:
    job: (function) The type of authentication to use, user or service.
    retries: (integer) Number of times to attempt this operation.
    wait: (integer) Number of seconds to sleep between retries.

  Returns:
    If sucesful, returns the JOSN response form the call.

  Raises:
    All API exceptions other than 409 = Already Exists.
  """

  try:
    # try to run the job and return the response
    data = job.execute()
    return data

  except HttpError, e:
    # errors that can be overcome or re-tried
    if e.resp.status in [403, 429, 500, 503]:
      # already exists ( ignore benign )
      if json.loads(e.content)['error']['code'] == 409:
        return
      # check if retries left
      elif retries > 0:
        if project.verbose: print 'API RETRY:', retries
        sleep(wait)
        return API_Retry(job, retries - 1, wait * 2)
      # if no retries, raise
      else:
        raise
    # raise all other errors that cannot be overcome
    else:
      raise


def API_Iterator(function, kwargs, results = None):
  """ See below API_Iterator_Instance for documentaion, this is just an iter wrapper. 
      
      Returns:
        iter(API_Iterator_Instance(function, kwargs, results))
  """

  class API_Iterator_Instance():
    """A helper class that iterates multiple results, automatically called by execute.
    
      This is a standard python iterator definition, no need to document functions.

      The only job this has is to handle Google API iteration, as such it can be called
      on any API call that reurns a 'nextPageToken' in the result.
     
      For example if calling the DCM list placement API:
     
        https://developers.google.com/doubleclick-advertisers/v3.2/placements/list
    
        function = get_service('dfareporting', 'v3.2', 'user').placements().list
        kwargs = { 'profile_id':1234, 'archived':False } 
        for placement in API_Iterator(function, kwargs):
          print placement 

      Can be called independently but automatically built into API...execute() so
      use that instead.

      Args:
        function: (function) function of API call to iterate, definiton not instance.
        kwargs" (dict) arguments to be passed to the function on each fetch
        results (json) optional, the first set of results given ( if already fetched )

    Returns:
      Iterator over JSON objects.
    """
  
    def __init__(self, function, kwargs, results = None):
      self.function = function
      self.kwargs = kwargs
      self.results = results
      self.position = 0
      self.iterable = None
      self.__find_tag__()
  
    def __find_tag__(self):
      # find the only list item for a paginated response, JOSN will only have list type, so ok to be specific
      if self.results:
        for tag in self.results.keys():
          if isinstance(self.results[tag], list): 
            self.iterable = tag
            break
  
      # this shouldn't happen unless error or iterate
      if self.iterable is None:
        raise ValueError('JSON response with nextPageToken but no list type element.')
      
    def __iter__(self):
      return self
  
    def __next__(self):
      return self.next()
  
    def next(self):
  
      # if no initial results, get some
      if self.results is None:
        self.results = API_Retry(self.function(**self.kwargs))
        self.__find_tag__()
  
      # if exhausted page, get next page
      if self.position >= len(self.results[self.iterable]):
        self.kwargs['pageToken'] = self.results.get('nextPageToken', None)
        if self.kwargs['pageToken']:
          self.results = API_Retry(self.function(**self.kwargs))
          self.position = 0
        else: 
          raise StopIteration
  
      # if results remain, return them
      if self.position < len(self.results[self.iterable]):
        value = self.results[self.iterable][self.position]
        self.position += 1
        return value
  
      # if pages and results exhausted, stop
      else:
        raise StopIteration

  return iter(API_Iterator_Instance(function, kwargs, results))


class API():
  """A wrapper around Google API with built in helpers for StarThinker.
  
    The wrapper mimics function calls, storing the m in a stack, until it encounters
    execute().  Then it uses the stored stack and arguments to call the actual API.
    This allows handlers on execute such as API_Retry and API_Iterator.

    See module level description for wrapped changes to Google API.  The class is 
    designed to be a connector to JSON, hence the configuraton is a JSON object.

    configuration = {
      "api":"doubleclickbidmanager",
      "version":"v1",
      "auth":"user",
      "iterate":False
    }
    api = API(configuration).placements().list(profile_id=1234, archived=False).execute()

    Args:
      configuration: (json) see example above, configures all API parameters

    Returns:
      If nextpageToken in result or iterate is True: return iterator of API response
      Otherwise: returns API response
  """

  def __init__(self, configuration):
    self.api = configuration['api']
    self.version = configuration['version']
    self.auth = configuration['auth']
    self.uri = configuration.get('uri', None)
    self.function_stack = filter(None, configuration.get('function', '').split('.'))
    self.function_kwargs = configuration.get('kwargs', {})
    self.iterate = configuration.get('iterate', False)

  # for debug purposes
  def __str__(self):
    return '%s.%s.%s' (self.api, self.version, '.'.join(self.function_stack))

  # builds API function stack
  def __getattr__(self, function_name):
    self.function_stack.append(function_name)
    def function_call(**kwargs):
      self.function_kwargs = kwargs
      return self
    return function_call

  # matches API execute with built in iteration and retry handlers
  def execute(self, run=True):
    # start building call sequence with service object
    f = get_service(self.api, self.version, self.auth, uri_file=self.uri)

    # build calls along stack ( first call is different because it is a called function )
    # do not call functions, as the abstract is necessary for iterator page next calls
    for count, f_n in enumerate(self.function_stack):
      f = getattr(f if count == 0 else f(), f_n)

    # for cases where job is handled manually, save the job
    job = f(**self.function_kwargs)

    if run == True:
      # pass arguments to the last function in the call chain
      results = API_Retry(job)

      # if paginated, automatically iterate
      if 'nextPageToken' in results or self.iterate == True:
        return API_Iterator(f, self.function_kwargs, results)

      # if not pagenated, return object as is
      else:
        return results

    # if not run, just return job object ( for chunke dupload for example )
    else:
      return job


def API_BigQuery(auth, iterate=False):
  """BigQuery helper configuration for Google API. Defines agreed upon version.
  """

  configuration = {
    'api':'bigquery',
    'version':'v2',
    'auth':auth,
    'iterate':iterate
  }
  return API(configuration)


def API_DBM(auth, iterate=False):
  """DBM helper configuration for Google API. Defines agreed upon version.
  """

  configuration = {
    'api':'doubleclickbidmanager',
    'version':'v1',
    'auth':auth,
    'iterate':iterate
  }
  return API(configuration)


def API_DCM(auth, iterate=False):
  """DCM helper configuration for Google API. Defines agreed upon version.
  """

  configuration = {
    'api':'dfareporting',
    'version':'v3.2',
    'auth':auth,
    'iterate':iterate
  }

  if INTERNAL_MODE:
    # fetch discovery uri using: wget https://www.googleapis.com/discovery/v1/apis/dfareporting/internalv3.2/rest > util/dcm/internalv32_uri.json
    configuration['version'] = 'internalv3.2'
    configuration['uri'] = '%sutil/dcm/internalv32_uri.json' % EXECUTE_PATH

  return API(configuration)


def API_SNIPPETS(auth, iterate=False):
  """Snippets helper configuration for Google API. Defines agreed upon version.
  """

  # fetch discovery uri using: wget https://snippets-hrdb.googleplex.com/_ah/api/discovery/v1/apis/snippets/v1/rest
  configuration = {
    'api':'snippets',
    'version':'v1',
    'auth':auth,
    'iterate':iterate,
    'uri':'%sutil/snippets/snippets_v1.json' % EXECUTE_PATH
  }

  return API(configuration)
