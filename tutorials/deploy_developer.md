# Deploying For Development

The development deployment is intended for a basic command line only deployment of Starthinker ideal
for testing and creating recipes.  Each developer should have a unigue Google Cloud project to fully
utilize StarThinker out of the box.  StarThinker is fully extensible.

## Command Line Deploy
```
git clone https://github.com/google/starthinker
```
```
cd starthinker
```
```
source install/deploy.sh 
```

1. Option 1) Developer Menu
1. Option 1) Install StarThinker
  - You will be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
  - You will be asked for [Service Credentials](cloud_service.md).
  - You will be asked for [Installed Client Credentials](cloud_client_installed.md).
1. Option 9) Quit
1. Then run a recipe using:
```
source starthinker_assets/development.sh
```
```
python starthinker/all/run.py starthinker/gtech/say_hello.json -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT --verbose 
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=README.md)

Next, learn how to [create a recipe](../starthinker/gtech/README.md) or look at the [cheat sheet of commands](cheat_sheet.md). 

## UI For Development Deploy

```
git clone https://github.com/google/starthinker
```
```
cd starthinker
```
```
source install/deploy.sh 
```

1. Option 1) Developer Menu
1. Option 2) Deploy Development UI
  - You may be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
  - You may be asked for [Service Credentials](cloud_service.md).
  - You will be asked for [Web Client Credentials](cloud_client_web.md).
1. Follow on screen instructions for how to access the UI via browser.


[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_developer.md)

Next, learn how to [create a recipe](../starthinker/gtech/README.md) or look at the [cheat sheet of commands](cheat_sheet.md). 

## Cloud Resources

  - [Google Cloud Credentials](https://pantheon.corp.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://pantheon.corp.google.com/billing/linkedaccount) - examine costs in real time.


---
&copy; 2019 Google Inc. - Apache License, Version 2.0
