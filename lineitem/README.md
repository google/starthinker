# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [Line Item To BigQuery Via Query](/lineitem/script_lineitem_read_to_bigquery_via_query.json)

Move using an Id query.

Maintained and supported by: kenjora@google.com

### Fields

- id_dataset (string) 
- id_query (string) Default: SELECT \* FROM `Dataset.Table`;
- id_legacy (boolean) 
- destination_dataset (string) 
- destination_table (string)

### Instructions

- Specify the query that will pull the lineitem ids to download.
- Specify the dataset and table where the lineitems will be written.
- The schema will match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /lineitem/script_lineitem_read_to_bigquery_via_query.json -h`

`python script/run.py /lineitem/script_lineitem_read_to_bigquery_via_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Line Item To BigQuery Via Values](/lineitem/script_lineitem_read_to_bigquery_via_value.json)

Move using hard coded Id values.

Maintained and supported by: kenjora@google.com

### Fields

- ids (integer_list) 
- destination_dataset (string) 
- destination_table (string)

### Instructions

- Provide a comma delimited list of line item ids.
- Specify the dataset and table where the lineitems will be written.
- The schema will match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /lineitem/script_lineitem_read_to_bigquery_via_value.json -h`

`python script/run.py /lineitem/script_lineitem_read_to_bigquery_via_value.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Line Item From BigQuery](/lineitem/script_lineitem_write_from_bigquery.json)

Upload Line Items From BigQuery To DBM.

Maintained and supported by: kenjora@google.com

### Fields

- dataset (string) 
- query (string) Default: SELECT \* FROM `Dataset.Table`;
- legacy (boolean)

### Instructions

- Specify the table or view where the lineitem data is defined.
- The schema should match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /lineitem/script_lineitem_write_from_bigquery.json -h`

`python script/run.py /lineitem/script_lineitem_write_from_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


## [/lineitem/helper.py](/lineitem/helper.py)

Command line interface for fetching line items via API.

Helps developers quickl debug lineitem issues or permissions access issues.

For example: https://developers.google.com/bid-manager/v1/lineitems/downloadlineitems
python lineitem/helper.py [line item id] -u [credentials]

