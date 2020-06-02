# Deploying StarThinker UI For Enterprise Multi User 

When multiple users need to deploy and coordinate multiple reipces for multiple clients, stand up the UI.
The UI allows each user to authenticate and manage solutions leaving the development team free to create
and maintain the technical recipe scripts.  The UI deploys on AppEngine with a distributed worker back 
end on Google Cloud Instances.  The instructions are the same for installing or updating StarThinker, 
recipes and users are preserved between updates.

## Instructions
```
git clone https://github.com/google/starthinker
```
```
cd starthinker
```
```
bash install/deploy.sh
```

 1. Option 1) Pull Latest GitHub Version
 1. Option 2) Enterprise Setup Menu 
 1. Option 1) Deploy UI And Workers
     - You will be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
     - You will be asked for Web Client Credentials. [See Instructions](cloud_client_web.md)
 1. Enable backups for your Google Cloud SQL. [Visit Application](https://console.cloud.google.com/sql)
 1. Enable Google Cloud IAP to restrict access to the UI. [Visit Application](https://console.cloud.google.com/security/iap) 
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

- If you get 500 error, change the UI to show errors:
```
source starthinker_assets/production.sh
vim app.yaml and set STARTHINKER_DEVELOPMENT: '1'
gcloud app deploy $STARTHINKER_ROOT/app.yaml --stop-previous-version
```
- If you get a 404 error, you may have to set a custom App Engine domain using the install deploy script.
- If your jobs all read queued and never change, odds are there was an error during deployment, scroll up and review.
- If you are updating you may have to run the follwing SQL command in your database once to trigger a recipe refresh, or re-save each receipe via the UI:
```
UPDATE recipe_recipe SET job_utm=1 WHERE job_utm=0;
```
- If you are updating and you deleted prior migrations, you may have to run Django migrations manually.
- If you are updating, the new default region is us-west3, you may have to modify your config.sh to match your prior region.

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
