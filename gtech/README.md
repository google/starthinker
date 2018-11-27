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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_audience_mapper.json -h`

`python script/run.py /gtech/script_audience_mapper.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Deal Finder](/gtech/script_deal_finder.json)

Compares open vs. deal CPM, CPC, and CPA so that clients can decide which sites, inventory, and deals work best.

Maintained and supported by: kenjora@google.com

### Fields

- report (string) Name of report in DBM, should be unique.
- timezone (timezone) Timezone in 'America/Los_Angeles' format.
- dataset (string) Place where tables will be written in BigQuery.
- dbm_sheet (string) URL to sheet where DBM accounts will be read from.

### Instructions

- Wait for <b>BigQuery->StarThinker Data->%(name)s->Deal_Finder_Dashboard</b> to be created.
- Copy <a href='https://datastudio.google.com/open/1QrWNTurvQT6nx20vnzdDveSzSmRjqHxQ' target='_blank'>Deal Finder Sample Data</a>.
- Click Edit Connection, and change to <b>BigQuery->StarThinker Data->%(name)s->Deal_Finder_Dashboard</b>.
- Copy <a href='https://datastudio.google.com/open/1fjRI5AIKTYTA4fWs-pYkJbIMgCumlMyO' target='_blank'>Deal Finder Sample Report</a>.
- When prompted choose the new data source you just created.
- Or give these intructions to the client.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_deal_finder.json -h`

`python script/run.py /gtech/script_deal_finder.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Third Party MOAT Report](/gtech/script_moat.json)

Import MOAT and DBM data into a BigQuery table and connect to dashboard.

Maintained and supported by: kenjora@google.com

### Fields

- moat_link (string) 
- moat_attachment (string)

### Instructions

- The MOAT report must span 30 days back, and run daily.
- Send the MOAT report to <b>{{EMAIL_TOKEN}}</b>.
- The MOAT Display report must contain exactly the fields:<i><br/>Date<br/>Campaign ID<br/>Campaign Label<br/>Placement ID<br/>Placement Label<br/>Human and Viewable Impressions<br/>Human and Viewable Rate<br/>Human and Fully On-Screen Measurable Impressions<br/>Human and AVOC Impressions<br/>Human, Audible & Fully On-Screen for Half of Duration (15 sec. cap) Impressions</i>
- Wait for <b>BigQuery->StarThinker Data->{{DATASET}}->MOAT_CSV_Report</b> to be created or click Run Now.
- Copy <a href='https://datastudio.google.com/open/1HbMQSvyBkQu_J3hs83bHYgNGzDLJNwHk' target='_blank'>Third Party MOAT Sample Data Source</a>.
- Click Edit Connection, change to <b>BigQuery->StarThinker Data->{{DATASET}}->IAS_Dashboard</b>.
- Copy <a href='https://datastudio.google.com/open/1TIs6QweUTg8QaL830no-SSwUZ5anYKxb' target='_blank'>Third Party MOAT Sample Report</a> and choose the new data source you just created.
- Or give these intructions to the client.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_moat.json -h`

`python script/run.py /gtech/script_moat.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_pacing.json -h`

`python script/run.py /gtech/script_pacing.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

## [Third Party IAS Report](/gtech/script_ias.json)

Import IAS and DBM data into a BigQuery table and connect to dashboard.  Used to verify viewability data against third party.

Maintained and supported by: kenjora@google.com

### Fields



### Instructions

- In IAS set up automated daily xlsx report with  a <b>3MS Viewability</b> sheet, it must span 30 days back.
- Send the IAS report to <b>{{EMAIL_TOKEN}}</b>.
- The IAS report must contain exactly the fields:<i><br/>Date<br/>Campaign_Name<br/>Media_Partner_Name<br/>Placement_ID<br/>Placement_Name<br/>In_View_Impressions<br/>Out_of_View_Impressions<br/>Suspicious_Unblocked_Impressions<br/>Total_Out_of_View_Impressions<br/>Measured_Impressions<br/>Unmeasured_Impressions<br/>Viewable_Rate<br/>Measured_Rate<br/>In_View_IMP_Distribution<br/>Out_of_View_IMP_Distribution<br/>Unmeasured<br/>Total_Unblocked_Impressions<br/>Gross_Unblocked_Impressions<br/>Gross_Measured_Impressions<br/>Gross_Unblocked_Invalid_Impressions<br/>Net_Eligible_Impressions<br/>Net_Measured_Impressions<br/>Net_Viewable_Impressions<br/>Net_Non_Viewable_Impressions<br/>Net_Unmeasured_Impressions<br/>Net_Viewable_Rate<br/>Total_Net_Eligible_Impressions<br/>Total_Net_Measured_Impressions<br/>Total_Net_Unmeasured_Impressions<br/>Total_Net_Viewable_Rate<br/>Total_Net_Measured_Rate<br/>Total_Net_In_View<br/>Total_Net_Out_of_View<br/>Total_Net_Unmeasured</i>
- Wait for <b>BigQuery->StarThinker Data->{{DATASET}}->IAS_Dashboard</b> to be created.
- Copy <a href='https://datastudio.google.com/open/1sPP1SLzF5MVdSgFktYHm04c8U4PkRVqv' target='_blank'>Third Party IAS Sample Data Source</a>.
- Click Edit Connection, change to <b>BigQuery->StarThinker Data->{{DATASET}}->IAS_Dashboard</b>.
- Copy <a href='https://datastudio.google.com/open/1I9ZDuff-AAlIemYrY6KQxwmlUFOvwja4' target='_blank'>Third Party IAS Sample Report</a> and choose above data source.
- Or give these intructions to the client.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /gtech/script_ias.json -h`

`python script/run.py /gtech/script_ias.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

