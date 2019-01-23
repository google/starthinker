# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Futil%2Fdbm%2FREADME.md)


# Python Scripts


## [/util/dbm/__init__.py](/util/dbm/__init__.py)



### report_fetch(auth, report_id=None, name=None, timeout = 4):


   Retrieves most recent DBM file JSON by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/getquery

  Timeout is in minutes ( retries will happen at 5 minute interval, default total time is 20 minutes )

  Args:
    * auth: (string) Either user or service.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.

  Returns:
    * Report JSON if report exists and is ready. 
    * True if report is in progress but not ready.
    * False if report does not exist.

  


### lineitem_read(auth, advertisers=[], insertion_orders=[], lineitems=[]):


   Reads line item configurations from DBM.
  
  Bulletproofing: https://developers.google.com/bid-manager/v1/lineitems/downloadlineitems 

  Args:
    * auth: (string) Either user or service.
    * advertisers (list) List of advertiser ids ( exclusive with insertion_orders and lineitems ).
    * insertion_orders (list) List of insertion_order ids ( exclusive with advertisers and lineitems ).
    * lineitems (list) List of ilineitem ids ( exclusive with insertion_orders and advertisers ).
  
  Returns:
    * Iterator of lists: https://developers.google.com/bid-manager/guides/entity-write/format

  


### report_list(auth):


   Lists all the DBM report configurations for the current credentials.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/listqueries

  Args:
    * auth: (string) Either user or service.

  Returns:
    * Iterator of JSONs.

  


### report_build(auth, body):


   Creates a DBM report given a JSON definition.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/createquery

  The report will be automatically run the first time.

  The body JSON provided will have the following fields added if not present:
    * schedule - set to run daily and expire in one year.
  
  Args:
    * auth: (string) Either user or service.
    * body: (json) As defined in: https://developers.google.com/doubleclick-advertisers/v3.2/reports#resource

  Returns:
    * JSON definition of report created or existing.

  


### report_to_rows(report):


   Helper to convert DBM files into iterator of rows, memory efficient.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  ```

  Args:
    * report: (iterator or file) Either an iterator or file that will be converted to rows.

  Returns:
    * Iterator of lists representing each row.

  


### report_delete(auth, report_id=None, name=None):


   Deletes a DBM report based on name or ID.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/deletequery

  Args:
    * auth: (string) Either user or service.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * None

  


### report_get(auth, report_id=None, name=None):


   Returns the DBM JSON definition of a report based on name or ID.
 
  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/getquery

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * JSON definition of report.

  


### report_clean(rows, datastudio=False, nulls=False):


   Helper to fix DBM report issues for BigQuery and ensure schema compliance.

  Memory efficiently cleans each row by fixing:
  * Strips header and footer to preserve only data rows.
  * Changes 'Date' to 'Report_Day' to avoid using reserved name in BigQuery.
  * Changes data format to match data studio if datastusio=True.
  * Changes cell string Unknown to blank ( None ) if nulls=True.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  rows = report_clean(rows,  project.task.get('datastudio', False))
  ```

  Args:
    * rows: (iterator) Rows to clean.
   
  Returns:
    * Iterator of cleaned rows.

  


### lineitem_write(auth, rows, dry_run=True):


   Writes a list of lineitem configurations to DBM.

  Bulletproofing: https://developers.google.com/bid-manager/v1/lineitems/uploadlineitems

   Args:
    * auth: (string) Either user or service.
    * rows (iterator) List of lineitems: https://developers.google.com/bid-manager/guides/entity-write/format
    * dry_run (boolean) If set to True no write will occur, only a test of the upload for errors.
  
  Returns:
    * Results of upload.

  


### report_file(auth, report_id=None, name=None, timeout = 60, chunksize = None):


   Retrieves most recent DBM file by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/bid-manager/v1/queries/getquery

  Timeout is in minutes ( retries will happen at 1 minute interval, default total time is 60 minutes )
  If chunksize is set to None then the whole file is downloaded at once.

  Args:
    * auth: (string) Either user or service.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.
    * chunksize: (int) number of bytes to download at a time, for memory constrained systems.

  Returns:
    * (filename, iterator) if file exists and is ready to download in chunks.
    * (filename, file) if file exists and chunking is off.
    * ('report_running.csv', None) if report is in progress.
    * (None, None) if file does not exist.

  
