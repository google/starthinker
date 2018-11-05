# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Floodlight Monitor](floodlight_monitor/script_floodlight_monitor.json)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py floodlight_monitor/script_floodlight_monitor.json -h`

`python script/run.py floodlight_monitor/script_floodlight_monitor.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


# floodlight_monitor/run.py

Pulls floodlights from a sheet, checks if impressions have changed significantly and sends an alert email.

For example ( modify floodlight_monitor/test.json to include your account and sheet ):

python floodlight_monitor/run.py floodlight_monitor/test.json -u [user credentials path]


