# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [DCM To BigQuery](/dcm/script_dcm_to_bigquery.json)

Move existing DCM report into a BigQuery table.

Maintained and supported by: kenjora@google.com

### Fields

- account (integer) DCM network id.
- report_id (integer) DCM report id, empty if using name .
- report_name (string) DCM report name, empty if using id instead.
- dataset (string) Dataset to be written to in BigQuery.
- table (string) Table to be written to in BigQuery.
- datastudio (boolean) Alter columns for datastudio, fixes nulls and date format.Default: True

### Instructions

- Specify an account id.
- Specify either report name or report id to move a report.
- The most recent valid file will overwrite the table.
- Schema is pulled from the official DCM specification.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /dcm/script_dcm_to_bigquery.json -h`

`python script/run.py /dcm/script_dcm_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [DCM Report](/dcm/script_dcm.json)

Create a DCM report from a JSON definition.

Maintained and supported by: kenjora@google.com

### Fields

- account (string) 
- body (json) Default: {}
- delete (boolean)

### Instructions

- Add a an account as [account_id]@[profile_id]
- Fetch the report JSON definition. Arguably could be better.
- The account is automatically added to the report definition.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /dcm/script_dcm.json -h`

`python script/run.py /dcm/script_dcm.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [DCM To Storage](/dcm/script_dcm_to_storage.json)

Move existing DCM report into a Storage bucket.

Maintained and supported by: kenjora@google.com

### Fields

- account (integer) 
- report_id (integer) 
- report_name (string) 
- bucket (string) 
- path (string) Default: DCM_Report
- datastudio (boolean) Default: True

### Instructions

- Specify an account id.
- Specify either report name or report id to move a report.
- The most recent file will be moved to the bucket.
- Schema is pulled from the official DCM specification.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /dcm/script_dcm_to_storage.json -h`

`python script/run.py /dcm/script_dcm_to_storage.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [DCM To Sheets](/dcm/script_dcm_to_sheets.json)

Move existing DCM report into a Sheet tab.

Maintained and supported by: kenjora@google.com

### Fields

- account (integer) 
- report_id (integer) 
- report_name (string) 
- sheet (string) 
- tab (string)

### Instructions

- Specify an account id.
- Specify either report name or report id to move a report.
- The most recent valid file will be moved to the sheet.
- Schema is pulled from the official DCM specification.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /dcm/script_dcm_to_sheets.json -h`

`python script/run.py /dcm/script_dcm_to_sheets.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


## [/dcm/run.py](/dcm/run.py)

Handler that executes { "dcm":{...}} task in recipe JSON.

This script translates JSON instructions into operations on DCM reporting.
It deletes, or creates, and/or downloads DCM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in setup.py.
For superusers, this script will use the internal API, bypassing the 
need for profiles.
Reports uploaded to BigQuery use automatic schema detection based on official
proto files.  



## [/dcm/helper.py](/dcm/helper.py)

Command line to get a DCM report or show list of report or files.

This is a helper to help developers debug and create reports. Prints using JSON for
copy and paste compatibility. The following command lines are available:

- To get list of reports: `python dcm/helper.py --account [id] --profile [id] --list -u [credentials]`
- To get report: `python dcm/helper.py --account [id] --profile [id] --report [id] -u [credentials]`
- To get report files: `python dcm/helper.py --account [id] --profile [id] --files [id] -u [credentials]`
- To get report sample: `python dcm/helper.py --account [id] --profile [id] --sample [id] -u [credentials]`
- To get report schema: `python dcm/helper.py --account [id] --profile [id] --schema [id] -u [credentials]`


