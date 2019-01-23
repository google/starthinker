# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=util%2Fdcm%2FREADME.md)


# Python Scripts


## [/util/dcm/__init__.py](/util/dcm/__init__.py)



### report_schema(headers):


   Helper to determine the schema of a given set of report headers.

  Using a match table generated from the DCM proto, each report header is matched
  to its type and a schema is assembled. If not found defaults to STRING.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  rows = report_clean(rows,  project.task.get('datastudio', False))
  schema = report_schema(rows.next())
  ```

  Args:
    * headers: (list) First row of a report.
   
  Returns:
    * JSON schema definition.

  


### report_clean(rows, datastudio=False):


   Helper to fix DCM report issues for BigQuery and ensure schema compliance.

  Memory efficiently cleans each row by fixing:
  * Strips header and footer to preserve only data rows.
  * Changes 'Date' to 'Report_Day' to avoid using reserved name in BigQuery.
  * Changes data format to match data studio if datastusio=True.

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

  


### conversions_upload(auth, account, floodlight_activity_id, conversion_type, conversion_rows, encryption_entity=None, update=False):


   Uploads an offline conversion list to DCM.

  BulletProofing: https://developers.google.com/doubleclick-advertisers/guides/conversions_upload

  Handles errors and segmentation of conversion so list can be any size.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * floodlight_activity_id: (int) ID of DCM floodlight to upload conversions to.
    * converstion_type: (string) One of the following: encryptedUserId, encryptedUserIdCandidates, gclid, mobileDeviceId.
    * conversion_rows: (iterator) List of the following rows: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId.
    * encryption_entity: (object) See EncryptionInfo docs: https://developers.google.com/doubleclick-advertisers/v3.2/conversions/batchinsert#encryptionInfo

  


### report_get(auth, account, report_id = None, name=None):


   Returns the DCM JSON definition of a report based on name or ID.
 
  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/get

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * JSON definition of report.

  


### report_to_rows(report):


   Helper to convert DCM files into iterator of rows, memory efficient.

  Usage example:

  ```
  filename, report = report_file(...)
  rows = report_to_rows(report)
  ```

  Args:
    * report: (iterator or file) Either an iterator or file that will be converted to rows.

  Returns:
    * Iterator of lists representing each row.

  


### report_build(auth, account, body):


   Creates a DCM report given a JSON definition.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/insert

  The body JSON provided will have the following fields overriden:
    * accountId - supplied as a parameter in account token.
    * ownerProfileId - determined from the current credentials.
    * advertiser_ids - supplied as a parameter in account token.
  
  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * body: (json) As defined in: https://developers.google.com/doubleclick-advertisers/v3.2/reports#resource

  Returns:
    * JSON definition of report created or existing.

  


### get_profile_id(auth, account_id):


  Return a DCM profile ID for the currently supplied credentials.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/userProfiles/get

  Handles cases of superuser, otherwise chooses the first matched profile.
  Allows DCM jobs to only specify account ID, which makes jobs more portable
  between accounts.

  Args:
    * auth: (string) Either user or service.
    * account_id: (int) Account number for which report is retrieved.

  Returns:
    * Profile ID.
       
  Raises:
    * If current credentials do not have a profile for this account.

  


### report_delete(auth, account, report_id = None, name=None):


   Deletes a DCM report based on name or ID.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/delete

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).

  Returns:
    * None

  


### report_file(auth, account, report_id=None, name=None, timeout=60, chunksize=DCM_CHUNK_SIZE):


   Retrieves most recent DCM file by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/files/get

  Timeout is in minutes ( retries will happen at 1 minute interval, default total time is 60 minutes )
  If chunksize is set to 0 then the whole file is downloaded at once.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.
    * chunksize: (int) number of bytes to download at a time, for memory constrained systems.

  Returns:
    * (filename, iterator) if file exists and is ready to download in chunks.
    * (filename, file) if file exists and chunking is off.
    * ('report_running.csv', None) if report is in progress.
    * (None, None) if file does not exist.

  


### parse_account(auth, account):


   Breaks a [account:advertiser@profile] string into parts if supplied.

  This function was created to accomodate supplying advertiser and profile information
  as a single token.  It needs to be refactored as this approach is messy.

  Possible variants include:
    * [account:advertiser@profile]
    * [account:advertiser]
    * [account@profile]

  Args:
    * auth: (string) Either user or service.
    * account: (string) A string represeting [account:advertiser@profile]

  Returns:
    * ( network_id, advertiser_ids, profile_id) after parsing the account token.

  


### report_fetch(auth, account, report_id=None, name=None, timeout = 60):


   Retrieves most recent DCM file JSON by name or ID, if in progress, waits for it to complete.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/files/get

  Timeout is in minutes ( retries will happen at 1 minute interval, default total time is 60 minutes )

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) ID of DCm report to fetch ( either or name ).
    * name: (string) Name of report to fetch ( either or report_id ).
    * timeout: (int) Minutes to wait for in progress report before giving up.

  Returns:
    * Report JSON if report exists and is ready. 
    * True if report is in progress but not ready.
    * False if report does not exist.

  


### report_list(auth, account):


   Lists all the DCM report configurations for an account given the current credentials.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/reports/list

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.

  Returns:
    * Iterator of JSONs.

  


### get_account_name(auth, account):


   Return the name of a DCM account given the account ID.

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.

  Returns:
    * Profile ID.
       
  Raises:
    * If current credentials do not have a profile for this account.

  


### report_files(auth, account, report_id):


   Lists all the files available for a given DCM report configuration.

  Bulletproofing: https://developers.google.com/doubleclick-advertisers/v3.2/files/list

  Args:
    * auth: (string) Either user or service.
    * account: (string) [account:advertiser@profile] token.
    * report_id: (int) DCM report identifier.

  Returns:
    * Iterator of JSONs.

  
