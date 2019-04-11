# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [Audience Mapper](/gtech/script_audience_mapper.json)

Create custom audience mappings based on keywords.

Maintained and supported by: kenjora@google.com

### Fields

- timezone (timezone) Timezone in 'America/Los_Angeles' format.
- dataset (string) 
- report (string) Name of report in DBM, should be unique.
- sheet_url (string)

### Instructions

- Wait for <b>BigQuery->StarThinker Data->{{DATASET}}->Audience_Mapper_Dashboard</b> to be created.
- Copy <a href='https://datastudio.google.com/open/1QrWNTurvQT6nx20vnzdDveSzSmRjqHxQ' target='_blank'>Audinece Mapper Sample Data</a>.
- Change data source to <b>BigQuery->StarThinker Data->{{DATASET}}->Deal_Finder_Dashboard</b>.
- Copy <a href='https://datastudio.google.com/open/1fjRI5AIKTYTA4fWs-pYkJbIMgCumlMyO' target='_blank'>Audience Mapper Sample Report</a>.
- When prompted choose the new data source you just created.
- Create new dimensions in the sheet.
- Synch the DataStudio data source to pick up the new dimension.
- Create a DataStudio filter for each new dimension.
- Or give these intructions to the client.

### Task Code Used

Each task in the Audience Mapper recipe maps to the following stand alone python code modules:

- [/task/dataset](/task/dataset)
- [/task/dbm](/task/dbm)
- [/task/mapping](/task/mapping)
- [/task/sheets](/task/sheets)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_audience_mapper.json -h`

`python script/run.py /gtech/script_audience_mapper.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DCM To BigQuery](/gtech/script_dcm_to_bigquery.json)

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

### Task Code Used

Each task in the DCM To BigQuery recipe maps to the following stand alone python code modules:

- [/task/dcm](/task/dcm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dcm_to_bigquery.json -h`

`python script/run.py /gtech/script_dcm_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Dynamic Costs Reporting](/gtech/script_dynamic_costs.json)

Calculate DBM cost at the dynamic creative combination level.

Maintained and supported by: aritrab@google.com, kenjora@google.com

### Fields

- dcm_account (string) 
- configuration_sheet_url (string) 
- bigquery_dataset (string) Default: dynamic_costs

### Instructions

- Add a sheet URL. This is where you will enter advertiser and campaign level details.
- Specify the DCM network ID.
- Click run now once, and a tab called <strong>Dynamic Costs</strong> will be added to the sheet with instructions.
- Follow the instructions on the sheet; this will be your configuration.
- StarThinker will create two or three (depending on the case) reports in DCM named <strong>Dynamic Costs - ...</strong>.
- Wait for <b>BigQuery->{{PROJECT}}->{{DATASET}}->Dynamic_Costs_Analysis</b> to be created or click Run Now.
- Copy <a href='https://datastudio.google.com/open/1vBvBEiMbqCbBuJTsBGpeg8vCLtg6ztqA' target='_blank'>Dynamic Costs Sample Data ( Copy From This )</a>.
- Click Edit Connection, and Change to <b>BigQuery->{{PROJECT}}->{{DATASET}}->Dynamic_Costs_Analysis</b>.
- Copy <a href='https://datastudio.google.com/open/1xulBAdx95SnvjnUzFP6r14lhkvvVbsP8' target='_blank'>Dynamic Costs Sample Report ( Copy From This )</a>.
- When prompted, choose the new data source you just created.
- Edit the table to include or exclude columns as desired.
- Or, give the dashboard connection intructions to the client.

### Task Code Used

Each task in the Dynamic Costs Reporting recipe maps to the following stand alone python code modules:

- [/task/dynamic_costs](/task/dynamic_costs)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dynamic_costs.json -h`

`python script/run.py /gtech/script_dynamic_costs.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Email Fetch](/gtech/script_email_to_bigquery.json)

Import emailed csv or excel into a BigQuery table.

Maintained and supported by: kenjora@google.com

### Fields

- email_from (string) Must match from field.
- email_to (string) Must match to field.
- subject (string) Regular expression to match subject.
- link (string) Regular expression to match email.
- attachment (string) Regular expression to match atttachment.
- dataset (string) Existing dataset in BigQuery.
- table (string) Name of table to be written to.

### Instructions

- The person executing this recipe must be the recipient of the email.
- Schedule a CSV or Excel to be sent to <b>{{ EMAIL_TOKEN }}</b>.
- Give a regular expression to match the email subject, link or attachment.
- The data downloaded will overwrite the table specified.

### Task Code Used

Each task in the Email Fetch recipe maps to the following stand alone python code modules:

- [/task/email](/task/email)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_email_to_bigquery.json -h`

`python script/run.py /gtech/script_email_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Deal Finder](/gtech/script_deal_finder.json)

Compares open vs. deal CPM, CPC, and CPA so that clients can decide which sites, inventory, and deals work best.

Maintained and supported by: kenjora@google.com

### Fields

- report (string) Name of report in DBM, should be unique.
- timezone (timezone) Timezone in 'America/Los_Angeles' format.Default: America/Los_Angeles
- dataset (string) Place where tables will be written in BigQuery.
- sheet_url (string) URL to sheet where DBM accounts will be read from.

### Instructions

- Wait for <b>BigQuery->StarThinker Data->%(name)s->Deal_Finder_Dashboard</b> to be created.
- Copy <a href='https://datastudio.google.com/open/1QrWNTurvQT6nx20vnzdDveSzSmRjqHxQ' target='_blank'>Deal Finder Sample Data</a>.
- Click Edit Connection, and change to <b>BigQuery->StarThinker Data->%(name)s->Deal_Finder_Dashboard</b>.
- Copy <a href='https://datastudio.google.com/open/1fjRI5AIKTYTA4fWs-pYkJbIMgCumlMyO' target='_blank'>Deal Finder Sample Report</a>.
- When prompted choose the new data source you just created.
- Or give these intructions to the client.

### Task Code Used

Each task in the Deal Finder recipe maps to the following stand alone python code modules:

- [/task/bigquery](/task/bigquery)
- [/task/dataset](/task/dataset)
- [/task/dbm](/task/dbm)
- [/task/sheets](/task/sheets)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_deal_finder.json -h`

`python script/run.py /gtech/script_deal_finder.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Trends Places To Sheets Via Values](/gtech/script_trends_places_to_sheets_via_value.json)

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

### Task Code Used

Each task in the Trends Places To Sheets Via Values recipe maps to the following stand alone python code modules:

- [/task/twitter](/task/twitter)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_trends_places_to_sheets_via_value.json -h`

`python script/run.py /gtech/script_trends_places_to_sheets_via_value.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Storage To Table](/gtech/script_bigquery_storage.json)

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

### Task Code Used

Each task in the Storage To Table recipe maps to the following stand alone python code modules:

- [/task/bigquery](/task/bigquery)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_bigquery_storage.json -h`

`python script/run.py /gtech/script_bigquery_storage.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Sheet Clear](/gtech/script_sheets_clear.json)

Clear data from a sheet.

Maintained and supported by: mauriciod@google.com

### Fields

- sheets_sheet (string) 
- sheets_tab (string) 
- sheets_range (string)

### Instructions

- For the sheet, provide the full edit URL.

### Task Code Used

Each task in the Sheet Clear recipe maps to the following stand alone python code modules:

- [/task/sheets](/task/sheets)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_sheets_clear.json -h`

`python script/run.py /gtech/script_sheets_clear.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DBM Report](/gtech/script_dbm.json)

Create a DBM report.

Maintained and supported by: kenjora@google.com

### Fields

- body (json) Default: {}
- delete (boolean)

### Instructions

- Reference field values from the <a href='https://developers.google.com/bid-manager/v1/reports'>DBM API</a> to build a report.
- Copy and paste the JSON definition of a report.
- The report is only created, use a move script to move it.
- To reset a report, delete it from DBM reporting.

### Task Code Used

Each task in the DBM Report recipe maps to the following stand alone python code modules:

- [/task/dbm](/task/dbm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dbm.json -h`

`python script/run.py /gtech/script_dbm.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DBM To BigQuery](/gtech/script_dbm_to_bigquery.json)

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

### Task Code Used

Each task in the DBM To BigQuery recipe maps to the following stand alone python code modules:

- [/task/dbm](/task/dbm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dbm_to_bigquery.json -h`

`python script/run.py /gtech/script_dbm_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Line Item To BigQuery Via Query](/gtech/script_lineitem_read_to_bigquery_via_query.json)

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

### Task Code Used

Each task in the Line Item To BigQuery Via Query recipe maps to the following stand alone python code modules:

- [/task/lineitem](/task/lineitem)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_lineitem_read_to_bigquery_via_query.json -h`

`python script/run.py /gtech/script_lineitem_read_to_bigquery_via_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Column Mapping](/gtech/script_mapping.json)

Use sheet to define keyword to column mappings.

Maintained and supported by: 

### Fields

- sheet (string) 
- tab (string) 
- in_dataset (string) 
- in_table (string) 
- out_dataset (string) 
- out_view (string)

### Instructions

- For the sheet, provide the full URL.
- A tab called <strong>Mapping</strong> will be created.
- Follow the instructions in the tab to complete the mapping.
- The in table should have the columns you want to map.
- The out view will have the new columns created in the mapping.

### Task Code Used

Each task in the Column Mapping recipe maps to the following stand alone python code modules:

- [/task/mapping](/task/mapping)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_mapping.json -h`

`python script/run.py /gtech/script_mapping.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Trends Places To Sheets Via Query](/gtech/script_trends_places_to_sheets_via_query.json)

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

### Task Code Used

Each task in the Trends Places To Sheets Via Query recipe maps to the following stand alone python code modules:

- [/task/twitter](/task/twitter)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_trends_places_to_sheets_via_query.json -h`

`python script/run.py /gtech/script_trends_places_to_sheets_via_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Dataset](/gtech/script_dataset.json)

Create and permission a dataset in BigQuery.

Maintained and supported by: ceh@google.com, kenjora@google.com

### Fields

- dataset_dataset (string) Name of Google BigQuery dataset to create.
- dataset_emails (string_list) Comma separated emails.
- dataset_groups (string_list) Comma separated groups.

### Instructions

- Specify the name of the dataset.
- If dataset exists, it is inchanged.
- Add emails and / or groups to add read permission.
- CAUTION: Removing permissions in StarThinker has no effect.
- CAUTION: To remove permissions you have to edit the dataset.

### Task Code Used

Each task in the Dataset recipe maps to the following stand alone python code modules:

- [/task/dataset](/task/dataset)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dataset.json -h`

`python script/run.py /gtech/script_dataset.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Query To View](/gtech/script_bigquery_view.json)

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

### Task Code Used

Each task in the Query To View recipe maps to the following stand alone python code modules:

- [/task/bigquery](/task/bigquery)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_bigquery_view.json -h`

`python script/run.py /gtech/script_bigquery_view.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Line Item To BigQuery Via Values](/gtech/script_lineitem_read_to_bigquery_via_value.json)

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

### Task Code Used

Each task in the Line Item To BigQuery Via Values recipe maps to the following stand alone python code modules:

- [/task/lineitem](/task/lineitem)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_lineitem_read_to_bigquery_via_value.json -h`

`python script/run.py /gtech/script_lineitem_read_to_bigquery_via_value.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Pacing DBM](/gtech/script_pacing.json)

Pace the spend of DBM campaigns to hit targets.

Maintained and supported by: mauriciod@google.com

### Fields



### Instructions

- Provide a TRIX URL, we'll add new sheets with instructions.
- Wait for the pacing tables to be createdin the <b>{{DATASET}}</b> dataset.
- Copy and connect each datastudio source to it's respective table...
- Copy <a href='https://datastudio.google.com/open/0BxNSN-sP1UmzUzdobUhITUxKY0E'>Pacing Template LI Breakdown ( Copy From This )</a>.
- Copy <a href='https://datastudio.google.com/open/0BxNSN-sP1UmzWjU4ckl3ZUZrZE0'>Pacing Template Advertiser Spend Rollup ( Copy From This )</a>.
- Copy <a href='https://datastudio.google.com/open/0BxNSN-sP1UmzcEFzVEw3ZnM0WVk'>Pacing Template Pacing Impressions ( Copy From This )</a>.
- Copy <a href='https://datastudio.google.com/open/0BxNSN-sP1Umzd1BRVjV4QVFLd2M'>Pacing Template Pacing Datasource ( Copy From This )</a>.
- After the above datasets are set up...
- Copy <a href='https://datastudio.google.com/open/0BxNSN-sP1UmzMk5lVlVjR29KdFk' target='_blank'>Pacing Sample Report ( Copy From This )</a>.
- Select the data sources you created in the steps above.
- Or give these intructions to the client.

### Task Code Used

Each task in the Pacing DBM recipe maps to the following stand alone python code modules:

- [/task/dataset](/task/dataset)
- [/task/dbm](/task/dbm)
- [/task/entity](/task/entity)
- [/task/move](/task/move)
- [/task/sheets](/task/sheets)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_pacing.json -h`

`python script/run.py /gtech/script_pacing.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Twitter Targeting](/gtech/script_twitter.json)

Adjusts line item settings based on Twitter hashtags and locations specified in a sheet.

Maintained and supported by: kenjora@google.com

### Fields

- sheet_url (string) URL to sheet where Line Item settings will be read from.
- twitter_secret (string) Twitter API secret token.
- twitter_key (string) Twitter API key token.

### Instructions

- Provide a sheets URL. No account information required.
- Click <b>Run Now</b> once and a new tab called <b>Twitter Triggers</b> will be added to the sheet.
- Follow instructions on the sheets tab.
- Click <b>Run Now</b> again, trends are downloaded and triggered
- Or give these intructions to the client.

### Task Code Used

Each task in the Twitter Targeting recipe maps to the following stand alone python code modules:

- [/task/bigquery](/task/bigquery)
- [/task/dataset](/task/dataset)
- [/task/lineitem](/task/lineitem)
- [/task/sheets](/task/sheets)
- [/task/twitter](/task/twitter)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_twitter.json -h`

`python script/run.py /gtech/script_twitter.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DCM Report](/gtech/script_dcm.json)

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

### Task Code Used

Each task in the DCM Report recipe maps to the following stand alone python code modules:

- [/task/dcm](/task/dcm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dcm.json -h`

`python script/run.py /gtech/script_dcm.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Trends Places To BigQuery Via Query](/gtech/script_trends_places_to_bigquery_via_query.json)

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

### Task Code Used

Each task in the Trends Places To BigQuery Via Query recipe maps to the following stand alone python code modules:

- [/task/twitter](/task/twitter)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_trends_places_to_bigquery_via_query.json -h`

`python script/run.py /gtech/script_trends_places_to_bigquery_via_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Floodlight Monitor](/gtech/script_floodlight_monitor.json)

Monitor floodlight impressions specified in sheet and send email alerts.

Maintained and supported by: kenjora@google.com

### Fields

- dcm_account (string) Specify an account_id or account_id:subaccount_id.
- sheet_url (string) Full URL to Google Sheet, Floodlight Monitor tab will be added.

### Instructions

- Specify an account_id or account_id:subaccount_id.
- Will copy <a href='https://docs.google.com/spreadsheets/d/1tjF5styxMvFJsNETEa5x2F5DSmqleGl71cmujB7Ier8/edit?usp=sharing'>Floodlight Monitor Sheet</a> to the sheet you specify.
- Follow instructions on sheet.
- Emails are sent once a day.

### Task Code Used

Each task in the Floodlight Monitor recipe maps to the following stand alone python code modules:

- [/task/floodlight_monitor](/task/floodlight_monitor)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_floodlight_monitor.json -h`

`python script/run.py /gtech/script_floodlight_monitor.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DCM To Storage](/gtech/script_dcm_to_storage.json)

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

### Task Code Used

Each task in the DCM To Storage recipe maps to the following stand alone python code modules:

- [/task/dcm](/task/dcm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dcm_to_storage.json -h`

`python script/run.py /gtech/script_dcm_to_storage.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Conversion Upload Sheets](/gtech/script_conversion_upload_from_sheets.json)

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

### Task Code Used

Each task in the Conversion Upload Sheets recipe maps to the following stand alone python code modules:

- [/task/conversion_upload](/task/conversion_upload)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_conversion_upload_from_sheets.json -h`

`python script/run.py /gtech/script_conversion_upload_from_sheets.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Query To Table](/gtech/script_bigquery_query.json)

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

### Task Code Used

Each task in the Query To Table recipe maps to the following stand alone python code modules:

- [/task/bigquery](/task/bigquery)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_bigquery_query.json -h`

`python script/run.py /gtech/script_bigquery_query.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DCM Standard Bulk](/gtech/script_dcm_bulk_standard.json)

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

- See API docs for <a href='https://developers.google.com/doubleclick-advertisers/v3.2/dimensions' target='_blank'>Metrics</a>.
- DCM report name format '[Report Name] [Account ID] ( StarThinker )'.
- Specify either bucket and path or dataset and table.
- Schema is pulled from the official DCM specification.

### Task Code Used

Each task in the DCM Standard Bulk recipe maps to the following stand alone python code modules:

- [/task/dcm_bulk](/task/dcm_bulk)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dcm_bulk_standard.json -h`

`python script/run.py /gtech/script_dcm_bulk_standard.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Sheet To Table](/gtech/script_sheets_to_bigquery.json)

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

### Task Code Used

Each task in the Sheet To Table recipe maps to the following stand alone python code modules:

- [/task/sheets](/task/sheets)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_sheets_to_bigquery.json -h`

`python script/run.py /gtech/script_sheets_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DCM To Sheets](/gtech/script_dcm_to_sheets.json)

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

### Task Code Used

Each task in the DCM To Sheets recipe maps to the following stand alone python code modules:

- [/task/dcm](/task/dcm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dcm_to_sheets.json -h`

`python script/run.py /gtech/script_dcm_to_sheets.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Archive](/gtech/script_archive.json)

Wipe old information from a Storage bucket.

Maintained and supported by: kenjora@google.com

### Fields

- archive_days (integer) Default: 7
- archive_bucket (string) 
- archive_path (string) 
- archive_delete (boolean)

### Instructions

- Specify how many days back to retain data and which buckets and paths to purge.
- Everything under a path will be moved to archive or deleted depending on your choice.

### Task Code Used

Each task in the Archive recipe maps to the following stand alone python code modules:

- [/task/archive](/task/archive)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_archive.json -h`

`python script/run.py /gtech/script_archive.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [API To BigQuery](/gtech/script_google_api_to_bigquery.json)

Execute a Google API function and store results to BigQuery.

Maintained and supported by: kenjora@google.com

### Fields

- api (string) See developer guide.Default: doubleclickbidmanager
- version (string) Must be supported version.Default: v1
- function (string) Full function dot notation path.Default: reports.files.list
- kwargs (json) Dictionray object of name value pairs.Default: {u'profileId': 2782211, u'reportId': 132847265, u'accountId': 7480}
- iterate (boolean) Is the result a list?
- dataset (string) Existing dataset in BigQuery.
- table (string) Table to write API call results to.
- schema (json) Schema provided in JSON list format or empty list.

### Instructions

- Enter an api name and version.
- Specify the function using dot notation and arguments using json.
- If nextPageToken can be in response check iterate.
- Give BigQuery dataset and table where response will be written.

### Task Code Used

Each task in the API To BigQuery recipe maps to the following stand alone python code modules:

- [/task/google_api](/task/google_api)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_google_api_to_bigquery.json -h`

`python script/run.py /gtech/script_google_api_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Bucket](/gtech/script_bucket.json)

Create and permission a bucket in Storage.

Maintained and supported by: kenjora@google.com

### Fields

- bucket_bucket (string) Name of Google Cloud Bucket to create.
- bucket_emails (string_list) Comma separated emails.
- bucket_groups (string_list) Comma separated groups.

### Instructions

- Specify the name of the bucket and who will have owner permissions.
- Existing buckets are preserved.
- Adding a permission to the list will update the permissions but removing them will not.
- You have to manualy remove grants.

### Task Code Used

Each task in the Bucket recipe maps to the following stand alone python code modules:

- [/task/bucket](/task/bucket)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_bucket.json -h`

`python script/run.py /gtech/script_bucket.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DT To Table](/gtech/script_dt.json)

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

### Task Code Used

Each task in the DT To Table recipe maps to the following stand alone python code modules:

- [/task/dt](/task/dt)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dt.json -h`

`python script/run.py /gtech/script_dt.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Conversion Upload BigQuery](/gtech/script_conversion_upload_from_biguery.json)

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

### Task Code Used

Each task in the Conversion Upload BigQuery recipe maps to the following stand alone python code modules:

- [/task/conversion_upload](/task/conversion_upload)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_conversion_upload_from_biguery.json -h`

`python script/run.py /gtech/script_conversion_upload_from_biguery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DBM To Storage](/gtech/script_dbm_to_storage.json)

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

### Task Code Used

Each task in the DBM To Storage recipe maps to the following stand alone python code modules:

- [/task/dbm](/task/dbm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dbm_to_storage.json -h`

`python script/run.py /gtech/script_dbm_to_storage.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [DBM To Sheets](/gtech/script_dbm_to_sheets.json)

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

### Task Code Used

Each task in the DBM To Sheets recipe maps to the following stand alone python code modules:

- [/task/dbm](/task/dbm)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_dbm_to_sheets.json -h`

`python script/run.py /gtech/script_dbm_to_sheets.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Project IAM](/gtech/script_iam.json)

Sets project permissions for an email.

Maintained and supported by: kenjora@google.com

### Fields

- role (string) projects/[project name]/roles/[role name]
- email (string) Email address to grant role to.

### Instructions

- Provide a role in the form of projects/[project name]/roles/[role name]
- Enter an email to grant that role to.
- This only grants roles, you must remove them from the project manually.

### Task Code Used

Each task in the Project IAM recipe maps to the following stand alone python code modules:

- [/task/iam](/task/iam)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_iam.json -h`

`python script/run.py /gtech/script_iam.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Trends Places To BigQuery Via Values](/gtech/script_trends_places_to_bigquery_via_value.json)

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

### Task Code Used

Each task in the Trends Places To BigQuery Via Values recipe maps to the following stand alone python code modules:

- [/task/twitter](/task/twitter)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_trends_places_to_bigquery_via_value.json -h`

`python script/run.py /gtech/script_trends_places_to_bigquery_via_value.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Entity Read Files](/gtech/script_entity.json)

Import public and private <a href='https://developers.google.com/bid-manager/guides/entity-read/format-v2' target='_blank'>Entity Read Files</a> into a BigQuery dataset.<br/>CAUTION: PARTNER ONLY, ADVERTISER FILTER IS NOT APPLIED.

Maintained and supported by: kenjora@google.com

### Fields

- partners (integer_list) Comma sparated list of DBM partners.Default: []
- dataset (string) BigQuery dataset to write tables for each entity.

### Instructions

- Entity Read Files ONLY work at the partner level.
- Advertiser filter is NOT APPLIED.
- Specify one or more partners to be moved into the dataset.

### Task Code Used

Each task in the Entity Read Files recipe maps to the following stand alone python code modules:

- [/task/dataset](/task/dataset)
- [/task/entity](/task/entity)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_entity.json -h`

`python script/run.py /gtech/script_entity.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Line Item From BigQuery](/gtech/script_lineitem_write_from_bigquery.json)

Upload Line Items From BigQuery To DBM.

Maintained and supported by: kenjora@google.com

### Fields

- dataset (string) 
- query (string) Default: SELECT \* FROM `Dataset.Table`;
- legacy (boolean)

### Instructions

- Specify the table or view where the lineitem data is defined.
- The schema should match <a href='https://developers.google.com/bid-manager/guides/entity-write/format' target='_blank'>Entity Write Format</a>.

### Task Code Used

Each task in the Line Item From BigQuery recipe maps to the following stand alone python code modules:

- [/task/lineitem](/task/lineitem)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_lineitem_write_from_bigquery.json -h`

`python script/run.py /gtech/script_lineitem_write_from_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

## [Sheet Copy](/gtech/script_sheets_copy.json)

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

### Task Code Used

Each task in the Sheet Copy recipe maps to the following stand alone python code modules:

- [/task/sheets](/task/sheets)

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_sheets_copy.json -h`

`python script/run.py /gtech/script_sheets_copy.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.


# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Fgtech%2FREADME.md)
