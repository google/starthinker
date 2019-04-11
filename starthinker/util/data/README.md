# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/util/data/__init__.py](/util/data/__init__.py)

Processes standard read / write JSON block for dynamic loading of data.

The goal is to create standard re-usable input output blocks.  These functions
are extensible, and should include additional sources and destinations over time.
Key benfits include:

  - Allows single point API revision for common read / write tasks.
  - Reduce risk with test case coverage for this module inherited by recipes using it.
  - Using standard blocks is a big time savings.




### get_rows(auth, source):


  Processes standard read JSON block for dynamic loading of data.
  
  Allows us to quickly pull a column or columns of data from and use it as an input 
  into a script. For example pull a list of ids from bigquery and act on each one.

  - When pulling a single column specify single_cell = True. Returns list AKA values. 
  - When pulling a multiple columns specify single_cell = False. Returns list of lists AKA rows.
  - Values are always given as a list ( single_cell will trigger necessary wrapping ).
  - Values, bigquery, sheet are optional, if multiple given result is one continous iterator.
  - Extensible, add a handler to define a new source ( be kind update the documentation json ).

  Include the following JSON in a recipe, then in the run.py handler when
  encountering that block pass it to this function and use the returned results.
  
    from utils.data import get_rows
  
    var_json = {
      "in":{
        "single_cell":[ boolean ],
        "values": [ integer list ],
        "bigquery":{
          "dataset": [ string ],
          "table": [ string ],
          "columns":[ integer list ],
          "legacy":[ boolean ]
        },
        "sheet":{
          "url":[ string - full URL, suggest using share link ],
          "tab":[ string ],
          "range":[ string - A1:A notation ]
        }
      } 
    } 
  
    values = get_rows('user', var_json)
  
  Or you can use it directly with project singleton.
  
    from util.project import project
    from utils.data import get_rows
  
    @project.from_parameters
    def something():
      values = get_rows(project.task['auth'], project.task['in'])
  
    if __name__ == "__main__":
      something()
  
  Args:
    auth: (string) The type of authentication to use, user or service.
    source: (json) A json block resembling var_json described above.

  Returns:
    If single_cell is False: Returns a list of row values [[v1], [v2], ... ]
    If single_cell is True: Returns a list of values [v1, v2, ...]



### put_rows(auth, destination, filename, rows, variant=''):


  Processes standard write JSON block for dynamic export of data.
  
  Allows us to quickly write the results of a script to a destination.  For example
  write the results of a DCM report into BigQuery.

  - Will write to multiple destinations if specified.
  - Extensible, add a handler to define a new destination ( be kind update the documentation json ).

  Include the following JSON in a recipe, then in the run.py handler when
  encountering that block pass it to this function and use the returned results.
  
    from utils.data import put_rows
  
    var_json = {
      "out":{
        "bigquery":{
          "dataset": [ string ],
          "table": [ string ]
          "schema": [ json - standard bigquery schema json ],
          "skip_rows": [ integer - for removing header ]
          "disposition": [ string - same as BigQuery documentation ]
        },
        "sheets":{
          "url":[ string - full URL, suggest using share link ],
          "tab":[ string ],
          "range":[ string - A1:A notation ]
          "delete": [ boolean - if sheet range should be cleared before writing ]
        },
        "storage":{
          "bucket": [ string ],
          "path": [ string ]
        },
        "directory":[ string - full path to place to write file ]
      } 
    } 
  
    values = put_rows('user', var_json)
  
  Or you can use it directly with project singleton.
  
    from util.project import project
    from utils.data import put_rows
  
    @project.from_parameters
    def something():
      values = get_rows(project.task['auth'], project.task['out'])
  
    if __name__ == "__main__":
      something()
  
  Args:
    auth: (string) The type of authentication to use, user or service.
    destination: (json) A json block resembling var_json described above.
    filename: (string) A unique filename if writing to medium requiring one, Usually gnerated by script.
    rows ( list ) The data being written as a list object.
    variant ( string ) Appends this to the destination name to create a variant ( for example when downloading multiple tabs in a sheet ).

  Returns:
    If single_cell is False: Returns a list of row values [[v1], [v2], ... ]
    If single_cell is True: Returns a list of values [v1, v2, ...]


# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Futil%2Fdata%2FREADME.md)
