# The Rest Of This Document Is Pulled From Code Comments

# JOSN Recipes

## [DBM Report](dbm/script_dbm.json)

Create a DBM report.

Maintained and supported by: mauriciod@google.com, kenjora@google.com

### Fields

- dbm_title (string) 
- dbm_partners (integer_list) 
- dbm_advertisers (integer_list) 
- dbm_type (string) Default: TYPE_CROSS_PARTNER
- dbm_timezone (string) Default: America/Los_Angeles
- dbm_dimensions (string_list) Default: [u'FILTER_DATE', u'FILTER_ADVERTISER', u'FILTER_INSERTION_ORDER', u'FILTER_CREATIVE_ID', u'FILTER_ADVERTISER_CURRENCY']
- dbm_metrics (string_list) Default: [u'METRIC_REVENUE_ADVERTISER', u'METRIC_IMPRESSIONS']
- dbm_filters (json) Default: []
- dbm_datastudio (boolean)

### Instructions

- Reference field values from the <a href='https://developers.google.com/bid-manager/v1/reports'>DBM API</a> to build a report.
- Filters for partners and advertisers are added from the partners and advertisers field.
- The report is only created, use a move script to move it.
- A report with a ( Starthinker ) suffix will be created in DBM.
- To reset a report, delete it from DBM reporting.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py dbm/script_dbm.json -h`

`python script/run.py dbm/script_dbm.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [DBM To BigQuery](dbm/script_dbm_to_bigquery.json)

Move existing DBM reports into a BigQuery table.

Maintained and supported by: kenjora@google.com

### Fields

- dbm_report_id (integer) DBM report ID given in UI, not needed if name used.
- dbm_report_name (string) Name of report, not needed if ID used.
- dbm_dataset (string) Existing BigQuery dataset.
- dbm_table (string) Table to create from this report.
- dbm_datastudio (boolean) Format date and column nulls for DataStudio?Default: True
- dbm_schema (json) Schema provided in JSON list format or empty list.Default: []

### Instructions

- Specify either report name or report id to move a report.
- A schema is recommended, if not provided it will be guessed.
- The most recent valid file will be moved to the table.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py dbm/script_dbm_to_bigquery.json -h`

`python script/run.py dbm/script_dbm_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [DBM To Storage](dbm/script_dbm_to_storage.json)

Move existing DBM report into a Storage bucket.

Maintained and supported by: kenjora@google.com

### Fields

- dbm_report_id (integer) DBM report ID given in UI, not needed if name used.
- dbm_report_name (string) Name of report, not needed if ID used.
- dbm_bucket (string) Google cloud bucket.
- dbm_path (string) Path and filename to write to.
- dbm_datastudio (boolean) Format date and column nulls for DataStudio?Default: True

### Instructions

- Specify either report name or report id to move a report.
- The most recent valid file will be moved to the bucket.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py dbm/script_dbm_to_storage.json -h`

`python script/run.py dbm/script_dbm_to_storage.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [DBM To Sheets](dbm/script_dbm_to_sheets.json)

Move existing DBM report into a Sheets tab.

Maintained and supported by: kenjora@google.com

### Fields

- report_id (integer) DBM report ID given in UI, not needed if name used.
- report_name (string) Name of report, not needed if ID used.
- sheet (string) Full URL to sheet being written to.
- tab (string) Existing tab in sheet to write to.

### Instructions

- Specify either report name or report id to move a report.
- The most recent valid file will be moved to the sheet.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py dbm/script_dbm_to_sheets.json -h`

`python script/run.py dbm/script_dbm_to_sheets.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


# dbm/run.py

Script that executes { "dbm":{...}} task.

This script translates JSON instructions into operations on DBM reporting.
It deletes, or creates, and/or downloads DBM reports.  See JSON files in
this directory for examples of operations.

This script uses put_rows as defined in util/data/README.md. This allows
multiple destinations for downloaded reports. To add a destination modify
the util/data/__init__.py functions.

Note

The underlying libraries use streaming download buffers, no disk is used.
Buffers are controlled in setup.py.



# dbm/helper.py

Command line to get a DBM report or show list of reports.

This is a helper to help developers debug and create reports.

To get list: python dbm/helper.py --list -u [credentials]
To get report: python dbm/helper.py --report [id] -u [credentials]


