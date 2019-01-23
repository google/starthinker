# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [DT To Table](/dt/script_dt.json)

Move data from a DT bucket into a BigQuery table.

Maintained and supported by: kenjora@google.com

### Fields

- bucket (string) For example: dcdt_-dcm_account[Network ID]
- path (string) For example: dcm_account[Network ID]_match_table_campaigns_
- dataset (string) Existing dataset in BigQuery.
- table (string) Table to write DT files to.

### Instructions

- Ensure your user has <a href='https://developers.google.com/doubleclick-advertisers/dtv2/getting-started' target='_blank'>access to the bucket</a>.
- Provide the DT bucket name to read from.
- Provide the path of the files to read.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /dt/script_dt.json -h`

`python script/run.py /dt/script_dt.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

