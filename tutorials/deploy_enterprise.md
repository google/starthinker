# Deploying StarThinker UI For Enterprise Multi User 

When multiple users need to deploy and coordinate multiple reipces for multiple clients, stand up the UI.
The UI allows each user to authenticate and manage solutions leaving the development team free to create
and maintain the technical recipe scripts.  The UI deploys on AppEngine with a distributed worker back end
on Google Cloud Instances. Execute the following to stand up the UI:

```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh
```
- Option 3) Enterprise Setup Menu 
- Option 1) Deploy App Engine UI
- Option 2) Deploy Job Workers
- Option 1) Test - 1 Job


### When creating the oAuth Client:

- For credentials type choose: Web Application..
- For OAuth Consent Screen choose: Application Type Internal.
- Be sure to add callbacks to your OAuth Client:
```
http://localhost:8000/oauth_callback/	
https://[CLIENT_PROJECT_NAME].appspot.com/oauth_callback/	
```

If you DO NOT see Application Type Internal as an option, your project is not
a member of a [GSuite Organization](https://support.google.com/a/answer/6365252).
Having a GSuite Organization is the recommended setup, it provides additional
security and control over access to your cloud assets.  Alternatively you can
set up a verified domain and controll access using firewalls and other tools
available in Google Cloud.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=README.md)
