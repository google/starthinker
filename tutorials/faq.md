# Frequenty Asked Questions

---
### Is gSuite needed to deploy StarThinker?
No, but without it users logging in will have to click past a [verification warning](https://github.com/google/starthinker/raw/master/tutorials/images/verification.png).

---
### Worker jobs are timing out, what do I do?
Increasing the number and size of the workers will directly impact the speed and size of jobs StarThinker can process.  Increase the workers deployed to the next size available.  Ideally you are running at least medium workers for most enterprise jobs.  Workers can be adjusted using the deploy script.

---
### Can I run StarThinker locally on my machine?
Yes, StarThinker can be executed on any machine supporting python.  In the deploy script select the development menu.

---
### Mac OSX and the missing command line 'cc' error?
Installing xCode and Command Line tools will resolve the 'cc' error on Mac OSX.

---
### Do I run any part of this as sudo?
No, StarThinker is designed to execute within a virtual environment.  The deploy scripts set this up first.  No part of the install on your local machine requires the use of running the deploy script or any StarThinker scripts as sudo.

---
### The Google Cloud Project ID is invalid?
Be sure to copy the Google Cloud Project ID not the Name. The Project Id might include the organization name and a colon, or a dash and a number.

---
### The Google Project callback URL is invalid?
When setting up Google Cloud Client Credentials, be sure to edit the credentials and cofigure both the oAuth Consent Screen, as well as the callback URL on the client credentials edit screen.

---
### Does StarThinker write logs?
Yes, all UI logs are writtent to Google Cloud StackDriver under the category StarThinker.  Logs include the recipe and commands ran.  Logs do not include PII such as credentials or task details which may contain PII.  Command line logs are written to standard output and error.

---
### How do I reset all StarThinker settings?
Delete the starthinker_assets/production.sh, service.json, user.json, client_web.json, and client_installed.json.

---
### Can I run multiple StarThinker instances on the same machine?
Yes, however each StarThinker will need to run under a different user with distinct environmental variables.

---
### Can StarThinker settings in Google Cloud Console be shared?
No, The Google Cloud Console is tied to your user and cannot be shared.  To share deployment settings launch starthinkers form a virtual machine shared with multiple users.

---
### Service cannot be reached when trying to enable it, the Google Cloud UI is timing out.
There may be an issue internally with that service.  Wait a few hours and try again at a later time.

---
### I'm getting an error on Mac OS X.
You may have to install developer tools, specifically Command Line Tools using the command:
```
xcode-select --install
```

---
### I'm getting an admin_policy_enforced error.
The error may occur if the [StarThinker Scopes](../starthinker/config.py) do not match the [oAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent).

---
### I'm getting an SSH Connection Timeout error.
Odds are your firewall settings are not up to date for the machine you're on.  To enable ssh access to other machines, add the current machines IP to the firewall rules by running...
```
gcloud compute firewall-rules create default-allow-ssh --allow tcp:22
```

---
### How do I completely revoke access to my user credentials for StarThinker?
Visit [Google Account Permissions](https://myaccount.google.com/permissions) to revoke access to StarThinker.

---
&copy; 2020 Google LLC - Apache License, Version 2.0
