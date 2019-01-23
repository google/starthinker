# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=util%2Fproject%2FREADME.md)


# Python Scripts


## [/util/project/__init__.py](/util/project/__init__.py)

The core singleton class of StarThinker that translates json to python.

Project loads JSON and parameters and combines them for execturion.  It handles 
three important concepts:

  1. Load the JSON and make all task parameters available to python scripts.
  2. Load authentication, all three parameters are optional if scripts do not
     use them.  The following parameters can be passed for authentication.

    user.json - user credentials json ( generated from client ), is refreshed
                by StarThinker as required.  Can be provided as a local path
                or a Cloud Bucket Storage path for distributed jobs.

    service.json - service credentials json ( generated from cloud project ).
                   Passed as a local path or an embedded json object for 
                   distributed jobs.
 
    client.json - client credentials json ( generated from cloud project ).
                  Also require a user json path which will be written to after
                  client authnetication.  Once authenticated this client is not
                  required. 

    Credentials can be specified in one of three ways for maximum flexibility:

    A. Specify credentials on command line ( highest priority if given )
       --user / -u = user credentials path
       --client / -c = client credentials path ( requires user credentials path )
       --service / -s = service credentials path

    B. Define credentials paths in JSON ( overruled by command line )
       In each json file create the following entry ( client, or user, or service )

         {
           "setup":{
             "id":"[cloud project id]",
             "auth":{
               "client":"[/home/.credentials/hello-world_client.json]",
               "service":"[/home/.credentials/hello-world_service.json]",
               "user":"[/home/.credentials/hello-world_user.json]"
             }
          },
         }

    C. Use default credentials ( lowest priority, last resort )
       If neither the json not the command line provides a path, the environmental 
       variable GOOGLE_APPLICATION_CREDENTIALS will be used for service accounts.  
       It is created by google cloud utilities.



### is_scheduled(project, task = None):


  Determines if given tasks is executing this hour in a time zone safe way. 

     Used as a helper for any cron job running projects.  Keeping this logic in project
     helps avoid time zone detection issues and scheduling discrepencies between machines.

    Args:
      project: (Project Class) The instance of the project being evaluated ( not sure this is required ).
      task: ( dictionary / JSON ) The specific task being considered for execution.

    Returns:
      Task is scheduled for exection this hour ias True / False. 
    


### get_project(filepath, debug=False):


  Loads json for Project Class.  Intended for this module only. Available as helper.
     Able to load JSON with newlines ( strips all newlines before load ).

    Args:
      filepath: (string) The local file path to the recipe json file to load.
      debug: (boolean) If true, newlines are not stripped to correctly identify error line numbers.

    Returns:
      Json of recipe file.
    


## class project:


  A singleton that represents the loaded recipe within python scripts.

  All access to json scripts within StarThinker must pass through the project
  class.  It handles parameters, time zones, permissions management, and 
  scheduling overhead.

  Project is meant as the entry point into all StarThinker scripts as follows:

    from util.project import project

    def task():
      pass # execute work using project.* as data from json

    if __name__ == "__main__":
      project.load('task')
      task()

  Project is meant to be used by a helper.

    import argparse
    from util.project import project

    if __name__ == "__main__":

      # custom parameters
      parser = argparse.ArgumentParser()
      parser.add_argument('custom', help='custom parameter to be added to standard project set.')

      # initialize project
      project.load(parser=parser)

      # access arguments
      auth = 'service' if project.args.service else 'user'
      print project.args.custom

  Project can also be initialized directly for non-json tasks:

    from util.project import project

    if __name__ == "__main__":
      var_json = '/somepath/recipe.json'
      var_user = '/somepath/user.json'
      var_service = '/somepath/service.json'

      project.initialize(_json=var_json, _user=var_user, _service=var_service, _verbose=True)

  Attributes:
    
    Dealing with authentication...
      project: (string) The Google Cloud project id.
      user: (string) Path to the user credentials json file.  It can also be a Google Cloud Bucket path when passed to the class directly.
      service: (string) Path to the service credentials json file.  It can also be a json object when passed to the project class directly.
      client: (string) Path to the client credentials json file.  It can only be a local path.

    Dealing with execution data...
      instance: (integer) When executing all tasks, it is the one based index offset of the task to run.
      date: (date) A specific date or 'TODAY', which is changed to today's date, passed to python scripts for reference.
      hour: (integer) When executing all tasks, it is the hour if spefified for a task to execute.

    Dealing with debugging...
      verbose: (boolean) Prints all debug information in StarThinker code.  See: if project.verbose: print '...'.
      force: (boolean) For recipes with specific task hours, forces all tasks to run regardless of hour specified.
  


###   set_task(cls, json_definition):


    Helper for setting task json in a project.  not recommended, use load and initialize instead.

    Args:
      json_difinition (json) the json to use as a task   

    Returns:
      Project singleton instance.
    


###   load(cls, _task = None, parser = None):


    Used in StarThinker scripts as entry point for command line calls. Loads json for execution.

       Usage example:

         from util.project import project

         def task():
           pass # execute work using project.* as data from json

         if __name__ == "__main__":
           project.load('task')
           task()
    
    Args:
      task: (string) Name of task to execute, matching task in json, hard coded by calling script.
      parser: (ArgumentParser) optional custom argument parser ( json argument becomes optional if not None )

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.* result in the same object.

    


###   initialize(cls, 


    Used in StarThinker scripts as programmatic entry point. 

       Usage example:

       from util.project import project

       if __name__ == "__main__":
         client = 'project.json'
         user = 'user.json'
         service = 'service.json' 
         project.initialize(_json=json, _user=user, _service=service, _verbose=True)

    Args:
      _json: (string) Path to recipe json file with tasks and or auth block.
      _task: (string) Task name form recipe json task list to execute.
      _instance: (integer) See module description.
      _project: (string) See module description.
      _user: (string) See module description.
      _service: (string) See module description.
      _client: (string) See module description.
      _date: (date) See module description.
      _hour: (integer) See module description.
      _verbose: (boolean) See module description.
      _force: (boolean) See module description.

    Returns:
      Nothing, this manipulates a singleton object.  All calls to project.* result in the same object.
    


###   get_uuid(cls):


    Helper for deploying to pub/sub.  Injects a UUID into the current project's json file.

    The project's underlying recipe json file is modified by this call and needs to be read / write.

    Returns:
      UUID, and changes underlying json recipe file.
    
