# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Dynamic Costs Reporting](dynamic_costs/script_dynamic_costs.json)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py dynamic_costs/script_dynamic_costs.json -h`

`python script/run.py dynamic_costs/script_dynamic_costs.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


# dynamic_costs/run.py



### function view_combine(name, combos_table, main_table, shadow_table):


    query = 
      SELECT
        combos.\*,
        (combos.Impressions / main.Impressions) \* shadow.Dbm_Cost_Account_Currency AS Scaled_Dbm_Cost_Account_Currency
      FROM `%(project)s.%(dataset)s.%(combos_table)s` combos
      JOIN `%(project)s.%(dataset)s.%(main_table)s` main
      ON combos.Placement_Id = main.Placement_Id
      JOIN `%(project)s.%(dataset)s.%(shadow_table)s` shadow
      ON STARTS_WITH(shadow.Placement, combos.Placement)
       % {
    query = 
      SELECT
        combos.\*,
        (combos.Impressions / main.Impressions) \* main.Dbm_Cost_Account_Currency AS Scaled_Dbm_Cost_Account_Currency
      FROM `%(project)s.%(dataset)s.%(combos_table)s` combos
      JOIN `%(project)s.%(dataset)s.%(main_table)s` main
      ON combos.Placement_Id = main.Placement_Id
       % {
