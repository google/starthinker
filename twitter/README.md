# The Rest Of This Document Is Pulled From Code Comments

# JOSN Recipes

## [Trends Places To Sheets Via Values](twitter/script_trends_places_to_sheets_via_value.json)

Move using hard coded WOEID values.

Maintained and supported by: kenjora@google.com

### Fields

- secret (string) 
- key (string) 
- places_dataset (string) 
- places_query (string) 
- places_legacy (boolean) 
- destination_sheet (string) 
- destination_tab (string)

### Instructions

- Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
- Provide a comma delimited list of WOEIDs.
- Specify Sheet url and tab to write API call results to.
- Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
- Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py twitter/script_trends_places_to_sheets_via_value.json -h`

`python script/run.py twitter/script_trends_places_to_sheets_via_value.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Trends Places To Sheets Via Query](twitter/script_trends_places_to_sheets_via_query.json)

Move using a WOEID query.

Maintained and supported by: kenjora@google.com

### Fields

- secret (string) 
- key (string) 
- places_dataset (string) 
- places_query (string) 
- places_legacy (boolean) 
- destination_sheet (string) 
- destination_tab (string)

### Instructions

- Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
- Provide BigQuery WOEID source query.
- Specify Sheet url and tab to write API call results to.
- Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
- Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py twitter/script_trends_places_to_sheets_via_query.json -h`

`python script/run.py twitter/script_trends_places_to_sheets_via_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Trends Places To BigQuery Via Query](twitter/script_trends_places_to_bigquery_via_query.json)

Move using a WOEID query.

Maintained and supported by: kenjora@google.com

### Fields

- secret (string) 
- key (string) 
- places_dataset (string) 
- places_query (string) 
- places_legacy (boolean) 
- destination_dataset (string) 
- destination_table (string)

### Instructions

- Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
- Provide BigQuery WOEID source query.
- Specify BigQuery dataset and table to write API call results to.
- Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
- Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py twitter/script_trends_places_to_bigquery_via_query.json -h`

`python script/run.py twitter/script_trends_places_to_bigquery_via_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Trends Places To BigQuery Via Values](twitter/script_trends_places_to_bigquery_via_value.json)

Move using hard coded WOEID values.

Maintained and supported by: kenjora@google.com

### Fields

- secret (string) 
- key (string) 
- woeids (integer_list) 
- destination_dataset (string) 
- destination_table (string)

### Instructions

- Provide <a href='https://apps.twitter.com/' target='_blank'>Twitter credentials</a>.
- Provide a comma delimited list of WOEIDs.
- Specify BigQuery dataset and table to write API call results to.
- Writes: WOEID, Name, Url, Promoted_Content, Query, Tweet_Volume
- Note Twitter API is rate limited to 15 requests per 15 minutes. So keep WOEID lists short.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py twitter/script_trends_places_to_bigquery_via_value.json -h`

`python script/run.py twitter/script_trends_places_to_bigquery_via_value.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

