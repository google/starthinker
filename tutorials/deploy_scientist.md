# Deployment For Data Science Analysts

To execute recipes on a regular schedule, for example moving a report every day. Find an always
on machine, like a Google Cloud Instance. Download the open source code, and execute the following:

```
git clone https://github.com/google/starthinker
```
```
cd starthinker
```
```
source install/deploy.sh 
```
1. Option 2) Data Scientist Menu
1. Option 1) Install StarThinker
1. Option 5) Add Recipe or Option 6) Generate Recipe
1. Option 2) Start Cron

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_scientist.md)

Next, learn how to [create a recipe](../starthinker/gtech/README.md).

## Notes

 - The deploy script starts a cronjob you can view with corntab -l and edit with crontab -e.
 - Recipes are uploaded to the directory starthinker_cron.
 - The user and service credentials configured are passed to each recipe, even if it has its own.
 - Generating recipes uses recipe script templates.


## Cloud Resources

  - [Google Cloud Credentials](https://pantheon.corp.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://pantheon.corp.google.com/billing/linkedaccount) - examine costs in real time.


---
&copy; 2019 Google Inc. - Apache License, Version 2.0
