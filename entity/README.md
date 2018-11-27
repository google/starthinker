# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

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

# Python Scripts


## [/entity/run.py](/entity/run.py)

Script that executes { "entity":{...}} task.

This script translates JSON instructions into operations on Entity Read File
transfer to BigQuery.  

### CAUTION 

ONLY PARTNER LEVEL LOG FILES ARE MOVED, no advertiser filters in 
this script. To filter by advertiser, add queries within BigQuery to create
additional tables.

See: https://developers.google.com/bid-manager/guides/entity-read/format-v2

### Table Names And Entities

The prefix value specified in JSON is used to name each table and avoid 
collisions.  All tables will be prefixed with "Entity_" by default. For
example 'Campaign' Entity Read becomes, 'Entity_Campaign'. You can
modify the preifx in the JSON script.

The following Entity Read Files Can Be Specified:

- Campaign 
- LineItem
- Creative
- UserList
- Partner
- Advertiser
- InsertionOrder
- Pixel
- InventorySource
- CustomAffinity
- UniversalChannel
- UniversalSite
- SupportedExchange
- DataPartner
- GeoLocation
- Language
- DeviceCriteria
- Browser
- Isp

### Notes

- Files are moved using an in memory buffer, controlled by BUFFER_SCALE in setup.py. 
- Bigger buffer means faster move but needs a machine with more memory.
- These transfers take a long time, two jobs can write over each other.
- The tables are filled over time, if you need instant data switch, use table copy after job.


