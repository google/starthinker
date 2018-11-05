# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Sheet Clear](sheets/script_sheets_clear.json)

Clear data from a sheet.

Maintained and supported by: mauriciod@google.com

### Fields

- sheets_sheet (string) 
- sheets_tab (string) 
- sheets_range (string)

### Instructions

- For the sheet, provide the full edit URL.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py sheets/script_sheets_clear.json -h`

`python script/run.py sheets/script_sheets_clear.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Sheet To Table](sheets/script_sheets_to_bigquery.json)

Import data from a sheet and move it to a BigQuery table.

Maintained and supported by: mauriciod@google.com

### Fields

- sheets_sheet (string) 
- sheets_tab (string) 
- sheets_range (string) 
- sheets_dataset (string) 
- sheets_table (string) 
- sheets_header (boolean) Default: True

### Instructions

- For the sheet, provide the full edit URL.
- If the tab does not exist it will be created.
- Empty cells in the range will be NULL.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py sheets/script_sheets_to_bigquery.json -h`

`python script/run.py sheets/script_sheets_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Sheet Copy](sheets/script_sheets_copy.json)

Copy tab from a sheet to a sheet.

Maintained and supported by: kenjora@google.com

### Fields

- from_sheet (string) 
- from_tab (string) 
- to_sheet (string) 
- to_tab (string)

### Instructions

- Provide the full edit URL for both sheets.
- Provide the tab name for both sheets.
- The tab will only be copied if it does not already exist.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py sheets/script_sheets_copy.json -h`

`python script/run.py sheets/script_sheets_copy.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

