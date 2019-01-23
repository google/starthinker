# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=util%2Fgoogle_api%2FREADME.md)


# Python Scripts


## [/util/google_api/__init__.py](/util/google_api/__init__.py)

Thin wrapper around Google Sevice API for integraton into StarThinker.

This does not change or augment the standard API calls other than the following:

  * Allows passing of auth parameter to constructor, required for switching.
  * Execute statement is overloaded to include iterator for responses with nextPageToken. 
  * Retries handle some common errors and have a back off scheme.
  * JSON based configuration allows StarThinker recipe definitions.
  * Pre-defined functions for each API can be added to fix version and uri options.




### API_Iterator(function, kwargs, results = None):


   See below API_Iterator_Instance for documentaion, this is just an iter wrapper. 
      
      Returns:
        iter(API_Iterator_Instance(function, kwargs, results))
  


### API_Retry(job, key=None, retries=50, wait=30):


   API retry that includes back off and some common error handling.

  The back off executes [retry] times.  Each time the [wait] is doubled.
  By default retries are: 0:30 + 1:00 + 2:00 + 4:00 + 8:00 = 15:30

  * Errors retried: 403, 429, 500, 503
  * Errors ignored: 409 - already exists ( triggered by create only and also returns None )
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

  


## class API

  A wrapper around Google API with built in helpers for StarThinker.
  
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
  


### API_DBM(auth, iterate=False):


  DBM helper configuration for Google API. Defines agreed upon version.
  


### API_SNIPPETS(auth, iterate=False):


  Snippets helper configuration for Google API. Defines agreed upon version.
  


### API_DCM(auth, iterate=False):


  DCM helper configuration for Google API. Defines agreed upon version.
  


### API_Sheets(auth, iterate=False):


  DBM helper configuration for Google API. Defines agreed upon version.
  


### API_BigQuery(auth, iterate=False):


  BigQuery helper configuration for Google API. Defines agreed upon version.
  


##   class API_Iterator_Instance

    A helper class that iterates multiple results, automatically called by execute.
    
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
    
