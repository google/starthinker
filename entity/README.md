# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Entity Read Files](/entity/script_entity.json)

Import public and private <a href='https://developers.google.com/bid-manager/guides/entity-read/format-v2' target='_blank'>Entity Read Files</a> into a BigQuery dataset.<br/>CAUTION: PARTNER ONLY, ADVERTISER FILTER IS NOT APPLIED.

Maintained and supported by: kenjora@google.com

### Fields

- partners (integer_list) Comma sparated list of DBM partners.Default: []
- dataset (string) BigQuery dataset to write tables for each entity.

### Instructions

- Entity Read Files ONLY work at the partner level.
- Advertiser filter is NOT APPLIED.
- Specify one or more partners to be moved into the dataset.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /entity/script_entity.json -h`

`python script/run.py /entity/script_entity.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

