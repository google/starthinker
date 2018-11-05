# The Rest Of This Document Is Pulled From Code Comments

# JOSN Recipes

## [Storage To Table](bigquery/script_bigquery_storage.json)

Move using bucket and path prefix.

Maintained and supported by: kenjora@google.com

### Fields

- bucket (string) Google cloud bucket.
- path (string) Path prefix to read from, no \* required.
- dataset (string) Existing BigQuery dataset.
- table (string) Table to create from this query.
- schema (json) Schema provided in JSON list format or empty list.Default: []

### Instructions

- Specify a bucket and path prefix, \* suffix is NOT required.
- Every time the job runs it will overwrite the table.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py bigquery/script_bigquery_storage.json -h`

`python script/run.py bigquery/script_bigquery_storage.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Query To View](bigquery/script_bigquery_view.json)

Create a BigQuery view.

Maintained and supported by: kenjora@google.com

### Fields

- query (text) SQL with newlines and all.
- dataset (string) Existing BigQuery dataset.
- view (string) View to create from this query.
- legacy (boolean) Query type must match source tables.Default: True

### Instructions

- Specify a single query and choose legacy or standard mode.
- For PLX use: SELECT \* FROM [plx.google:FULL_TABLE_NAME.all] WHERE...
- If the view exists, it is unchanged, delete it manually to re-create.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py bigquery/script_bigquery_view.json -h`

`python script/run.py bigquery/script_bigquery_view.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Query To Table](bigquery/script_bigquery_query.json)

Save query results into a BigQuery table.

Maintained and supported by: kenjora@google.com

### Fields

- query (text) SQL with newlines and all.
- dataset (string) Existing BigQuery dataset.
- table (string) Table to create from this query.
- legacy (boolean) Query type must match source tables.Default: True

### Instructions

- Specify a single query and choose legacy or standard mode.
- For PLX use: SELECT \* FROM [plx.google:FULL_TABLE_NAME.all] WHERE...
- Every time the query runs it will overwrite the table.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py bigquery/script_bigquery_query.json -h`

`python script/run.py bigquery/script_bigquery_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

