# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Archive](archive/script_archive.json)

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

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py archive/script_archive.json -h`

`python script/run.py archive/script_archive.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

