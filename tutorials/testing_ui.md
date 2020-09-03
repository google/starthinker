# UI Tests

UI tests use the open source out of the box [Django Test Framework](https://docs.djangoproject.com/en/2.2/topics/testing/).
These are standard Python unit tests with a few additional Django helpers.  Tests use command line credentials.  Tests can
be excuted per Django instructons or via the helper bash script:

## Steps
```
bash install/deploy.sh
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

## Manual Testing

When the UI is active it saves recipes to the local database.  Those recipes can be executed by the worker
using the following commands:

```
source starthinker_assets/developer.sh
python starthinker_ui/manage.py job_worker --test --verbose --jobs 1
```

This will execute one loop of the worker, pulling one recipe at a time from the local databse and executing
it as the worker.


## Cloud Resources

  - [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://console.cloud.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
