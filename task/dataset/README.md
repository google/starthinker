# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [Dataset](/dataset/script_dataset.json)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /dataset/script_dataset.json -h`

`python script/run.py /dataset/script_dataset.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

