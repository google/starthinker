# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Email Fetch](/email/script_email_to_bigquery.json)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /email/script_email_to_bigquery.json -h`

`python script/run.py /email/script_email_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

