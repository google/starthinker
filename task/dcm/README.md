# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=task%2Fdcm%2FREADME.md)


# Python Scripts


## [/task/dcm/run.py](/task/dcm/run.py)

Handler that executes { "dcm":{...}} task in recipe JSON.

This script translates JSON instructions into operations on DCM reporting.
It deletes, or creates, and/or downloads DCM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in setup.py.
For superusers, this script will use the internal API, bypassing the 
need for profiles.
Reports uploaded to BigQuery use automatic schema detection based on official
proto files.  



## [/task/dcm/helper.py](/task/dcm/helper.py)

Command line to get a DCM report or show list of report or files.

This is a helper to help developers debug and create reports. Prints using JSON for
copy and paste compatibility. The following command lines are available:

- To get list of reports: `python dcm/helper.py --account [id] --profile [id] --list -u [credentials]`
- To get report: `python dcm/helper.py --account [id] --profile [id] --report [id] -u [credentials]`
- To get report files: `python dcm/helper.py --account [id] --profile [id] --files [id] -u [credentials]`
- To get report sample: `python dcm/helper.py --account [id] --profile [id] --sample [id] -u [credentials]`
- To get report schema: `python dcm/helper.py --account [id] --profile [id] --schema [id] -u [credentials]`


