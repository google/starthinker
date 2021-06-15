# Using StarThinker As A Python Package

This deployment is for non-developers who simply wish to use StarThinker.

## Install StarThinker

To run StarThinker you will need the folowing:

1. A unix / linux command line.
2. A version of Python 3.7 or greater.

From the command line on any unix/linux machine install StarThinker.  All following examples begin with this step.
Choose only one of the following, the first one is recommended for most users:

```
python3 -m pip install starthinker
python3 -m pip install git+https://github.com/google/starthinker
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

## Use A Function
The functions in [util](../starthinker/util/) or [task](../starthinker/task/) are directly usable.
This example creates a Google Sheet by name and lists all the DV360 reports under a user account.
Simply PIP install it and run recipes...

```
import json

# import StarThinker functions
from starthinker.util.configuration import Configuration
from starthinker.util.sheets import sheets_create
from starthinker.util.google_api import API_DBM

# initialize credentials
config = Configuration(user='[USER CREDENTIALS JSON STRING OR PATH]')

# create a sheet
sheets_create(config, 'user', 'Test Sheet', 'Test Tab')

# list all your reports in DV360
for report in API_DBM(config, 'user', iterate=True).queries().listqueries().execute():
  print(json.dumps(report, indent=2, sort_keys=True))
```

For more stand alone examples see [tools directory](../starthinker/tool/).

## Run A Recipe
You can use the StarThinker module directly in any python project to run a recipe. The following
example will execute two tasks in sequence in a single process.

```
from starthinker.util.onfiguration import execute, Configuration

if __name__ == "__main__":
  TASKS = [
    { "hello":{
      "auth":"user",
      "say":"Hello World"
    }},
    { "dataset":{
      "auth":"service",
      "dataset":"Test_Dataset"
    }}
  ]

  execute(
    config=Configuration(
      client='[CLIENT CREDENTIALS JSON STRING OR PATH]',
      user='[USER CREDENTIALS JSON STRING OR PATH]',
      service='[SERVICE CREDENTIALS JSON STRING OR PATH]',
      project='[GOOGLE CLOUD PROJECT ID]',
      verbose=True
    ),
    tasks=TASKS,
    force=True
  )
```

## Additional Resources

Try this in a few seconds using Google Cloud Shell...

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_tutorial=tutorials/deploy_package.md)

Next, review list of available tasks in the [Recipe Gallery](https://google.github.io/starthinker/), view [Scripts](../scripts/), or check [Command Line Helpers](helpers.md).

---
&copy; 2019 Google LLC - Apache License, Version 2.0
