# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=all%2FREADME.md)


# Python Scripts


## [/all/run.py](/all/run.py)

 Command line to execute all tasks in a recipe once. ( Common Entry Point )

This script dispatches all the tasks in a JSON recipe to handlers in sequence.
For each task, it calls a subprocess to execute the JSON instructions, waits
for the process to complete and dispatches the next task, until all tasks are 
complete or a critical failure ( exception ) is raised.

To execute a recipe run:

`python all/run.py [path to recipe file] [see optional arguments below] --force`

### Arguments

- path - run all tasks the specified recipe
- --project / -p - cloud id of project
- --user / -u - path to user credentials json file, defaults to GOOGLE_APPLICATION_CREDENTIALS
- --service / -s - path to service credentials json file
- --client / -c' - path to client credentials json file
- --verbose / -v - print all the steps as they happen.
- --force - execute all tasks regardless of schedule

### Notes

If an exception is raised in any task, all following tasks are not executed by design.
Obeys the schedule rules defined in /cron/README.md.
Uses credentials logic defined in /util/project/README.md.
For scheduled jobs this script is called by /cron/run.py.

### CAUTION

This script does NOT check if the last job finished, potentially causing overruns.

### Useful Development Features

To avoid running the entire script when debugging a single task, the command line 
can easily replace "all" with the name of any "task" in the json.  For example

`python all/run.py project/sample/say_hello.json`

Can be easily replaced with the following to run only the "hello" task:

`python task/hello/run.py project/sample/say_hello.json`

Or specified further to run only the second hello task:

`python task/hello/run.py project/sample/say_hello.json -i 2`


