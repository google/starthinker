# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=task%2Ffloodlight_monitor%2FREADME.md)


# Python Scripts


## [/task/floodlight_monitor/run.py](/task/floodlight_monitor/run.py)

Pulls floodlights from a sheet, checks if impressions have changed significantly and sends an alert email.

For example ( modify floodlight_monitor/test.json to include your account and sheet ):

python floodlight_monitor/run.py floodlight_monitor/test.json -u [user credentials path]


