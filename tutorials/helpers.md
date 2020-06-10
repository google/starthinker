# List Of StarThinker Command Line Helpers

Developing solutions is easier with helpers that automate common development 
tasks. Here are a few you can run from the command line.  Before running any 
helpers make sure to install the [developer environment](deploy_developer.md)
and load the python virtual environment:

```
source starthinker_assets/development.sh
```

The most common parameters for helpers are:

- -u $STARTHINKER_USER - user credentials for accessing API endpoints.
- -c $STARTHINKER_CLIENT - client creddentials for authenticating, not needed if user credentials already exist.
- -s $STARTHINKER_SERVICE - service credentials for writing data.
- -p $STARTHINKER_PROJECT - cloud project to bill the data transfer to.

Examples exist within the python code for each helper, but a typical run is:

```
python dbm/helper.py --list -u $STARTHINKER_USER
```

## List Of Helper Utilities

- [Execute Google Oauth](../starthinker/auth/helper.py) 
  - Helps create user credentials form client credendtials.
  - Minimal example of oAuth.
- [CM Report Inspector](../starthinker/task/dcm/helper.py) 
  - Pull CM Report shema, files, and fields.
  - Useful for building the dbm task JSON.
  - Minimal CM API example.
- [DV360 LineItem Inspector](../starthinker/task/lineitem/helper.py) 
  - Pull DV360 Line Item schema or data.
  - Useful for building the lineitem task JSON.
  - Minimal DV360 Line Item API example.
- [DV360 Report Inspector](../starthinker/task/dbm/helper.py) 
  - Pull DV360 Report shema, files, and fields.
  - Useful for building the dbm task JSON.
  - Minimal DV360 API example.
- [DV360 LineItem Download](../starthinker/task/dv360_beta/helper.py) 
  - Pull DV360 Beta APi LineItems.
  - Minimal DV360 Beta API example.
- [Send An Email Template](../starthinker/task/newsletter/helper.py) 
  - Quickly send a nicely [formatted email](../starthinker/util/email/template.py), including tables, to anyone.
  - Useful for automating reporting emails.
- [Call Any Google API Endpoint](../starthinker/task/google_api/helper.py) 
  - Quickly see the results of any Google API Endpoint, great for debugging format and access.
- [Run Automated Tests](../tests/helper.py) 
  - Execute one or all automated tests within StarThinker.
- [Verify JSON is Valid](../scripts/helper.py) 
  - StarThinker JSON allows newlines for queries etc.
  - This utility checks and correctly prints error locations.
- [Pull BigQuery Table Schema](../starthinker/task/bigquery/helper.py) 
  - Quickly pull table schema and modify for a recipe.

---
&copy; 2020 Google LLC - Apache License, Version 2.0
