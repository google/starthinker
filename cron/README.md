# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=cron%2FREADME.md)


# Python Scripts


## [/cron/run.py](/cron/run.py)

Command line to schedule recipe execution.

This script is meant to run persistently ( in a screen session ).  Once an hour, 
it will read a directory and check each *.json recipe for a schedule.  If the
recipe has a task to run during the current time zone adjusted hour, it is executed.

To add a schedule to any recipe include the following JSON.

  {
    "setup": {
      "timezone": "America/Los_Angeles",
      "day": [ "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ],
      "hour": [ "3", "18" ]
    }
  }

To execute each task at a different hour add the following JSON to each task.  Each hour
must match at least one in the the setup section.  Tasks with no hours specified execute
every hour in setup section.

  {
    "tasks": [
      "sample_task": {
        "hour":[3]
       }
    ]
  }

To start a scheduled cron from the command line: 

python cron/run.py [path to recipe directory] [see optional arguments below]

To execute all recipes in a directory once run:

python cron/run.py [path to recipe directory] [see optional arguments below] --force

Arguments

  path - run all json files in the specified path
  --project / -p - cloud id of project
  --user / -u - path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS
  --service / -s - path to service credentials json file
  --client / -c' - path to client credentials json file
  --verbose / -v - print all the steps as they happen.
  --force / -f - execute all scripts once then exit.
  --remote / -r - execute scripts remotely, requires pub/sub ( not set up yet )

Each recipe can run under different credentials, specify project, client, user, and service 
values in the JSON for each recipe. See /util/project/README.md.

CAUTION

This script triggers the all/run.py script if the schedule matches the current hour.
This script does NOT check if the last job finished, potentially causing overruns.


