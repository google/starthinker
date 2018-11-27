# The Rest Of This Document Is Pulled From Code Comments


# JSON Recipes

## [API To BigQuery](/google_api/script_google_api_to_bigquery.json)

Execute a Google API function and store results to BigQuery.

Maintained and supported by: kenjora@google.com

### Fields

- api (string) See developer guide.Default: doubleclickbidmanager
- version (string) Must be supported version.Default: v1
- function (string) Full function dot notation path.Default: reports.files.list
- kwargs (json) Dictionray object of name value pairs.Default: {u'profileId': 2782211, u'reportId': 132847265, u'accountId': 7480}
- iterate (boolean) Is the result a list?
- dataset (string) Existing dataset in BigQuery.
- table (string) Table to write API call results to.
- schema (json) Schema provided in JSON list format or empty list.

### Instructions

- Enter an api name and version.
- Specify the function using dot notation and arguments using json.
- If nextPageToken can be in response check iterate.
- Give BigQuery dataset and table where response will be written.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py /google_api/script_google_api_to_bigquery.json -h`

`python script/run.py /google_api/script_google_api_to_bigquery.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

# Python Scripts


## [/google_api/helper.py](/google_api/helper.py)

Command line interface for running Google API calls.  Any API works.

Allows developers to quickly test and debug API calls before building them
into scripts.  Useful for debugging permission or call errors.

For example, pull a DBM report via API: https://developers.google.com/bid-manager/v1/queries/getquery

python google_api/helper.py -api doubleclickbidmanager -version v1 -function queries.getquery -kwargs '{ "queryId": 132865172 }' -u [credentials path] 

For example, pull a list of placements: https://developers.google.com/doubleclick-advertisers/v3.2/placements/list

python google_api/helper.py -api dfareporting -version v3.2 -function placements.list -kwargs '{ "profileId":2782211 }' -u [credentials path]


