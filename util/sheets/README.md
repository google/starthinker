# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=util%2Fsheets%2FREADME.md)


# Python Scripts


## [/util/sheets/__init__.py](/util/sheets/__init__.py)



### sheets_create(auth, name, parent=None):


   Checks if sheet with name already exists ( outside of trash ) and
  if not, creates the sheet.

  Args:
    * auth: (string) Either user or service.
    * name: (string) name of sheet to create, used as key to check if it exists in the future.
    * parent: (string) the Google Drive to upload the file to. 

  Returns:
    * JSON specification of the file created or existing.

  
