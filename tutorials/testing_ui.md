# UI Tests

UI tests use the open source out of the box [Django Test Framework](https://docs.djangoproject.com/en/2.2/topics/testing/).
These are standard Python unit tests with a few additional Django helpers.  Tests use command line credentials.  Tests can 
be excuted per Django instructons or via the helper bash script:

## Steps
```
source install/deploy.sh 
```

1. Option 1) Developer Menu
1. Option 3) Test UI
  - You may be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
  - You may be asked for [Service Credentials](cloud_service.md).
  - You may be asked for [Installed Client Credentials](cloud_client_installed.md).

## Code

  - [starthinker_ui/recipe/tests.py](../starthinker_ui/recipe/tests.py)
  - [starthinker_ui/website/tests.py](../starthinker_ui/website/tests.py)
  - [starthinker_ui/account/tests.py](../starthinker_ui/account/tests.py)
  - [starthinker_ui/project/tests.py](../starthinker_ui/project/tests.py)

## Cloud Resources

  - [Google Cloud Credentials](https://pantheon.corp.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://pantheon.corp.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
