# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Ftask%2Fdbm%2FREADME.md)


# Python Scripts


## [/task/dbm/run.py](/task/dbm/run.py)

Handler that executes { "dbm":{...}} task in recipe JSON.

This script translates JSON instructions into operations on DBM reporting.
It deletes, or creates, and/or downloads DBM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in setup.py.



## [/task/dbm/helper.py](/task/dbm/helper.py)

Command line to get a DBM report or show list of reports.

This is a helper to help developers debug and create reports. The following
calls are valid:

- To get list of reports: `python dbm/helper.py --list -u [credentials]`
- To get report json: `python dbm/helper.py --report [id] -u [credentials]`
- To get report schema: `python dbm/helper.py --schema [id] -u [credentials]`
- To get report sample: `python dbm/helper.py --sample [id] -u [credentials]`


