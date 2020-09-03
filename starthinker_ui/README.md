# StarThinker UI Reference Implementation

DISCLAIMER: This is only a reference implmentation.  We strongly recommend an internal
security and privacy review before using this code in production.

## Concepts

This code sample is a sample UI wrapped around the StartThinker solution deployment
framework. It illustrates:

- Connecting a UI to the JSON templates.
- Autheticating users and storing credentials in a recipe.
- Inserting service credentials into a recipe.
- Assembling custom recipes from basic task building blocks.



## UI Technology

This sample UI is built using open source [Django Open Source Framework](https://www.djangoproject.com/).
Thank you to the Django team for developing an amazing framework.



## Running The UI Locally For Development

The local deployment uses an sqlite database and does not launch any workers, just the UI.  Workers
can be launched manually from the command line. To launch the UI locally:

```
source install/deploy.sh
```
- Option 1) Developer Menu
- Option 2) Launch Developer UI
- Follow instructions on screen.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=README.md)



## Running The UI In AppEngine

To launch the UI fully in AppEngine with a production databse execute the following:

```
source install/deploy.sh
```
- Option 3) Enterprise Setup Menu
- Option 1) Deploy App Engine UI
- Option 2) Deploy Job Workers
- Option 1) Test - 1 Job

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=README.md)



## UI Command Line Helpers

Pull recipe from UI with credentails and execute from command line regardless of schedule ( uses UI user credentails ).

```
source starthinker_assets/production.sh
python starthinker_ui/manage.py recipe_to_json --recipe [RECIPE # FROM UI EDIT URL]
python starthinker/all/run $STARTHINKER_CRON/[FILE WRITEN BY ABOVE COMMAND] --force
```

Start the workers manually from the command line:

```
source starthinker_assets/development.sh
python starthinker_ui/manage.py job_worker --test --verbose --jobs 1
```

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
