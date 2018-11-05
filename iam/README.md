# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Project IAM](/iam/script_iam.json)

Sets project permissions for an email.

Maintained and supported by: kenjora@google.com

### Fields

- role (string) projects/[project name]/roles/[role name]
- email (string) Email address to grant role to.

### Instructions

- Provide a role in the form of projects/[project name]/roles/[role name]
- Enter an email to grant that role to.
- This only grants roles, you must remove them from the project manually.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /iam/script_iam.json -h`

`python script/run.py /iam/script_iam.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

