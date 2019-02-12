# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/task/google_api/helper.py](/task/google_api/helper.py)

Command line interface for running Google API calls.  Any API works.

Allows developers to quickly test and debug API calls before building them
into scripts.  Useful for debugging permission or call errors.

For example, pull a DBM report via API: https://developers.google.com/bid-manager/v1/queries/getquery

python google_api/helper.py -api doubleclickbidmanager -version v1 -function queries.getquery -kwargs '{ "queryId": 132865172 }' -u [credentials path] 

For example, pull a list of placements: https://developers.google.com/doubleclick-advertisers/v3.2/placements/list

python task/google_api/helper.py -api dfareporting -version v3.2 -function placements.list -kwargs '{ "profileId":2782211 }' -u [credentials path]



# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Ftask%2Fgoogle_api%2FREADME.md)
