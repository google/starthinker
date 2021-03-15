# Running StarThinker Recipes Via Cloud Function

This serverless deployment will create a Cloud Function and a sample Cloud Scheduler recipe.
Only one [StarThinker Cloud Function](https://github.com/google/starthinker/tree/master/scripts/starthinker/cloud_function/)
is required to run all [StarThinker Recipes](https://github.com/google/starthinker/tree/master/scripts).
The [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) defines the task, credentials, and schedule
for each recipe.

## Create and Configure The Google Cloud Function

## Instructions

This only needs to be done once, after cloud functon creation, all recipes are run via scheduler configuration.
This deployment leverages the latest [StarThinker PYPI](https://pypi.org/project/starthinker/) package, which is the last tagged version in the repository.

```
bash install/deploy.sh
```

 1. Set up [Google Cloud Project](https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md).
 1. Option 4) Deploy Cloud Function
 1. Note the trigger URL and start using the scheduler to run recipes.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_clouf_function.md)

## Recipe Quick Start
 - A sample cloud scheduler job is ready: https://console.cloud.google.com/cloudscheduler
 - It will run a simple hello world task: https://github.com/google/starthinker/tree/master/starthinker/task/hello
 - Extend the sample with scripts from: https://github.com/google/starthinker/tree/master/scripts
 - Convert a script to a recipe, replaces {"field":{...}} with values: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#run-a-script
 - If you need service cerdentials see: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md
 - If you need user cerdentials see: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials
 - To make the cron scheduler easier to use: https://crontab.guru/

Next, review list of available tasks in the [Recipe Gallery](https://google.github.io/starthinker/), view [Scripts](../scripts/), or check [Command Line Helpers](helpers.md).

## Cloud Resources

  - [Google Cloud Functions](https://console.cloud.google.com/cloudfunctions) - where your function will deploy.
  - [Google Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) - where your recipe workflows will deploy.
  - [Google Cloud StackDriver Logs](https://console.cloud.google.com/logs/viewer) - where your logs will be written.
  - [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://console.cloud.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2021 Google LLC - Apache License, Version 2.0
