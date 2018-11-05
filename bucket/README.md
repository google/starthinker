# The Rest Of This Document Is Pulled From Code Comments

# JOSN Recipes

## [Bucket](bucket/script_bucket.json)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py bucket/script_bucket.json -h`

`python script/run.py bucket/script_bucket.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

