# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Futil%2Fdrive%2FREADME.md)


# Python Scripts


## [/util/drive/__init__.py](/util/drive/__init__.py)



### file_create(auth, name, filename, data, parent=None):


   Checks if file with name already exists ( outside of trash ) and 
    if not, uploads the file.  Determines filetype based on filename extension
    and attempts to map to Google native such as Docs, Sheets, Slides, etc...

    For example:
    -  ```file_create('user', 'Sample Document', 'sample.txt', StringIO('File contents'))``` 
    -  Creates a Google Document object in the user's drive.

    -  ```file_Create('user', 'Sample Sheet', 'sample.csv', StringIO('col1,col2\nrow1a,row1b\n'))````
    -  Creates a Google Sheet object in the user's drive.

    See: https://developers.google.com/drive/api/v3/manage-uploads 

    ### Args:
    -  * auth: (string) specify 'service' or 'user' to toggle between credentials used to access
    -  * name: (string) name of file to create, used as key to check if file exists
    -  * filename: ( string) specified as "file.extension" only to automate detection of mime type.
    -  * data: (StringIO) any file like object that can be read from
    -  * parent: (string) the Google Drive to upload the file to

    ### Returns:
    -  * JSON specification of file created or existing.

    
