# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [DCM Standard Bulk](dcm_bulk/script_dcm_bulk_standard.json)

Aggregate multiple standard DCM reports into one BigQuery or Sheet.

Maintained and supported by: kenjora@google.com

### Fields

- accounts (integer_list) 
- name (string) 
- range (choice) Default: LAST_7_DAYS
- dcm_dimensions (string_list) Default: [u'date', u'platformType', u'creativeType', u'state', u'dmaRegion']
- dcm_metrics (string_list) Default: [u'impressions']
- dataset (string) 
- table (string) 
- bucket (string) 
- path (string) Default: DCM_Report
- delete (boolean) 
- datastudio (boolean) Default: True

### Instructions

- See API docs for <a href='https://developers.google.com/doubleclick-advertisers/v3.0/dimensions' target='_blank'>Metrics</a>.
- DCM report name format '[Report Name] [Account ID] ( StarThinker )'.
- Specify either bucket and path or dataset and table.
- Schema is pulled from the official DCM specification.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py dcm_bulk/script_dcm_bulk_standard.json -h`

`python script/run.py dcm_bulk/script_dcm_bulk_standard.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

