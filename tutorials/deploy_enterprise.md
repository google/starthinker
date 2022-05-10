# Deploying StarThinker UI For Enterprise Multi User

When multiple users need to deploy and coordinate multiple reipces for multiple clients, stand up the UI.
The UI allows each user to authenticate and manage solutions leaving the development team free to create
and maintain the technical recipe scripts.  The UI deploys on AppEngine with a distributed worker back
end on Google Cloud Instances.  The instructions are the same for installing or updating StarThinker,
recipes and users are preserved between updates.

## Instructions
The Cloud Shell will do the following steps for you:
```
git clone https://github.com/google/starthinker
```
```
cd starthinker
```

For updating or installing run the following:
```
bash install/deploy.sh
```

 1. Set up [Google Cloud Project](https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md).
 1. Option 2) Enterprise Menu
 1. Option 1) Deploy UI And Workers using [Web Client Credentials](https://github.com/google/starthinker/blob/master/tutorials/cloud_client_web.md)
 1. Enable backups for your [Google Cloud SQL](https://console.cloud.google.com/sql).
 1. Enable Google [Cloud IAP](https://console.cloud.google.com/security/iap) to restrict access to the UI.
 1. Start using the UI to create and deploy jobs.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_enterprise.md)

Next, learn how to [deploy a recipe](https://google.github.io/starthinker/help/).


## Verification Warning

If you are not running gSuite, when you log into the UI you will be prompted with a [verification warning](https://github.com/google/starthinker/raw/master/tutorials/images/verification.png).
If you are running gSuite, you can select Internal Deployment and avoid the warning. All options for removing the warning are covered in the [oAuth API Verification FAQ](https://support.google.com/cloud/answer/9110914).

## Notes

 - The UI can be deployed as many times as necessary.
 - The workers can be deployed as many times as necessary.
 - Migrations are automatically run when deploying the UI.
 - See [Cost Sheet](cost_sheet.md) for estimated UI and worker costs.

## Debug

- All settings will be derived from a file in **starthinker_assets/config.sh**, the deployment script simply manages this file.
- Save and re-use the entire **starthinker_assets** directory to preseve all settings and credentials for future releases.
- AppEngine does not allow chaning regions once a deployment is done, choose carefully.
- Be sure AppEngine is enabled on the [Cloud Build Configuration](https://cloud.google.com/build/docs/securing-builds/configure-access-for-cloud-build-service-account) page.
- If you get 500 error, check the [APP Engine Error Logs](https://console.cloud.google.com/errors)</a> or change the UI to show errors:
```
source starthinker_assets/production.sh
vim app.yaml and set STARTHINKER_DEVELOPMENT: '1'
gcloud app deploy $STARTHINKER_ROOT/app.yaml --stop-previous-version
```
- If you get a 404 error, you may have to set a custom App Engine domain using the install deploy script.
- If you get a service credentials error, verify the file *starthinker_assets/service.json* has a valid credential, if not delete the file and run install again.
- If you get a  ModuleNotFoundError: No module named 'contextlib' error, try deleteing the **starthinker_virtualenv** directory and running install again. The problem may also be using "source install/deploy.sh" vs "bash install/deploy.sh", bash is preferd but try source as a last resort.
- If you get a database not found error, ensure your *starthinker_assets/config.sh* region is the same as your current [database region](https://console.cloud.google.com/sql/instances).
- If jobs all read queued and never change, odds are there was an error during deployment, scroll up and review.
- If updating, be sure the ZONE setting in **starthinker_assets/config.sh** matches the ZONE where the prior SQL database was deployed, otherwise the database will have to be migrated to match the new ZONE.
- If updating and you deleted prior migrations, you may have to run Django migrations manually.
- If updating, the new default region is us-west3, you may have to modify your config.sh to match your prior region.

## Cloud Resources

  - [Google Cloud AppEngine](https://console.cloud.google.com/appengine) - where your instance will deploy.
  - [Google Cloud AppEngine Cron Jobs](https://console.cloud.google.com/appengine/cronjobs) - where your cron will autoscale workers.
  - [Google Cloud SQL](https://console.cloud.google.com/sql) - where your database will deploy.
  - [Google Cloud StackDriver Logs](https://console.cloud.google.com/logs/viewer) - where your logs will be written ( select StarThinker under All Logs ).
  - [Google Cloud Storage](https://console.cloud.google.com/storage/browser) - where your user credentials will be stored ( keep this secure ).
  - [Google Compute Engine Instance Templates](https://console.cloud.google.com/compute/instanceTemplates) - where your workers will be configured.
  - [Google Compute Engine Instance Groups](https://console.cloud.google.com/compute/instanceGroups) - where your workers will be managed.
  - [Google Compute Engine Instances](https://console.cloud.google.com/compute/instances) - where your workers will be deployed.
  - [Google Compute Engine Images](https://console.cloud.google.com/compute/images) - where your worker copies will be deployed.
  - [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud IAP](https://console.cloud.google.com/security/iap) - where you restrict access to AppEngine.
  - [Google Cloud Billing](https://console.cloud.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2019 Google LLC - Apache License, Version 2.0
