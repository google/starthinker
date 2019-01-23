# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Ftask%2Fhello%2FREADME.md)


# Python Scripts


## [/task/hello/run.py](/task/hello/run.py)

Handler that executes { "hello":{...}} task in recipe JSON.

This is meant as an example only, it executes no useful tasks. Use this as 
a template for how to connect a handler to a JSON recipe task.  It 
illustrates how to use JOSN variables, access constants in the system, and 
best practices for using this framework.  Credentials are not required for 
this recipe handler.

Call from the command line using:

`python all/run.py gtech/say_hello.json`

### Notes

- See [/all/README.md](/all/README.md) to learn about running recipes.
- See [/cron/README.md](/cron/README.md) to learn about scheduling recipes.
- See [/auth/README.md](/auth/README.md) to learn about setting up credentials.


