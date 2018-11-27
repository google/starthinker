# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [Conversion Upload Sheets](/conversion_upload/script_conversion_upload_from_sheets.json)

Move form Sheets to DCM.

Maintained and supported by: kenjora@google.com

### Fields

- dcm_account (string) 
- floodlight_activity_id (integer) 
- floodlight_conversion_type (choice) Default: encryptedUserId
- encryption_entity_id (integer) 
- encryption_entity_type (choice) Default: DCM_ACCOUNT
- encryption_entity_source (choice) Default: DATA_TRANSFER
- sheet_url (string) 
- sheet_tab (string) 
- sheet_range (string)

### Instructions

- Specify a DCM Account ID, Floodligh Activity ID and Conversion Type.
- Include Sheets url, tab, and range, omit headers in range.
- Columns: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId
- Include encryption information if using encryptedUserId or encryptedUserIdCandidates.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /conversion_upload/script_conversion_upload_from_sheets.json -h`

`python script/run.py /conversion_upload/script_conversion_upload_from_sheets.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Conversion Upload BigQuery](/conversion_upload/script_conversion_upload_from_biguery.json)

Move from BigQuery to DCM.

Maintained and supported by: kenjora@google.com

### Fields

- account (string) 
- floodlight_activity_id (integer) 
- floodlight_conversion_type (choice) Default: encryptedUserId
- encryption_entity_id (integer) 
- encryption_entity_type (choice) Default: DCM_ACCOUNT
- encryption_entity_source (choice) Default: DATA_TRANSFER
- bigquery_dataset (string) 
- bigquery_table (string) 
- bigquery_legacy (boolean) Default: True

### Instructions

- Specify a DCM Account ID, Floodligh Activity ID and Conversion Type.
- Include BigQuery dataset and table.
- Columns: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId
- Include encryption information if using encryptedUserId or encryptedUserIdCandidates.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /conversion_upload/script_conversion_upload_from_biguery.json -h`

`python script/run.py /conversion_upload/script_conversion_upload_from_biguery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

