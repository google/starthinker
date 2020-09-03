# StarThinker Cloud Service Credentials

## Create Service Credentials

Retrieve Service Account Key Credentials from: https://console.cloud.google.com/apis/credentials

![Cloud Service](images/cloud_service.png)
[View Cloud Service Setup Larger](images/cloud_service.png)

### Setup Steps

 1. Google Cloud Project -> APIs & Services -> Credentials -> Create Credentials -> Service Account Key.
 1. New Service Account.
   1. Role is Project Owner.
   1. Service Account Name is starthinker.
   1. Key Type is JSON.
 1. Click Create and open the downloaded file.
 1. Copy the contents and paste into the StarThinker deployment script when prompted for Service Credentials.
   - You may have to click CTRL+D after pasting the service crdentials.

### Verify

If all goes well, after deployment, the following file should exist with your credentials inside:

- starthinker_assets/service.json

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
