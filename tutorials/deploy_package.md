# Using StarThinker As A Python Package

This deployment is for non-developers who simply wish to use StarThinker.

## Install StarThinker

From the command line on any unix/linux machine install StarThinker.  All following examples begin with this step.

```
pip3 install git+https://github.com/google/starthinker
```

- If you get a permission error add: ```--user``` to the above command.
- If you get a PATH WARNING:
  1. Copy the new command PATH from the warning.
  1. Activate the new command path now, run: ```export PATH="[PASTE THE PATH HERE]":$PATH;```
  1. Activate for all future logins, run: ```echo 'export PATH="[PASTE THE PATH HERE]":$PATH;' >> ~/.bash_profile;```

## Optional Setup User Credentials

To run some recipes, functions, or helpers, user credentials are required.  To acquire user credentials run the
following utility and follow instructions on screen:

```
st_auth -h
```

## Run A Helper

There are several [command line helpers](helpers.md) packaged in StarThinker, simply PIP install it and use the comands.

## Use A Function
If all you need is one of the [utilities](../starthinker/util/) to build your own data pipe this is the smallest footprint.
This example creates a Google Sheet by name and lists all the DV360 reports under a user account. Simply PIP install it and run recipes...

```
import json

# import StarThinker functions
from starthinker.util.project import project
from starthinker.util.sheets import sheets_create
from starthinker.util.google_api import API_DBM

# initialize credentials
project.initialize(_user='[USER CREDENTIALS JSON STRING OR PATH]')

# create a sheet
sheets_create('user', 'Test Sheet', 'Test Tab')

# list all your reports in DV360
for report in API_DBM('user', iterate=True).queries().listqueries().execute():
  print(json.dumps(report, indent=2, sort_keys=True))
```

## Run A Recipe
You can use the StarThinker module directly in any python project to run a recipe. The following
example will execute two tasks in sequence in a single process.

```
from starthinker.util.project import project

if __name__ == "__main__":
  var_service = '[SERVICE CREDENTIALS JSON STRING OR PATH]'
  var_user = '[USER CREDENTIALS JSON STRING OR PATH]'
  var_cloud_id = '[GOOGLE CLOUD PROJECT ID]'

  var_recipe = {
    "setup":{
      "id":var_cloud_id
    },
    "tasks":[
      { "hello":{
        "auth":"user",
        "say":"Hello World"
      }},
      { "dataset":{
        "auth":"service",
        "dataset":"Test_Dataset"
      }}
    ]
  }

  project.initialize(_recipe=var_recipe, _user=var_user, _service=var_service, _verbose=True)
  project.execute()
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_package.md)

Next, review list of available tasks in the [Recipe Gallery](https://google.github.io/starthinker/) or [GIT Scripts Folder](../scripts/).

---
&copy; 2019 Google LLC - Apache License, Version 2.0
