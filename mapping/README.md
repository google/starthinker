# The Rest Of This Document Is Pulled From Code Comments


# JOSN Recipes

## [Column Mapping](mapping/script_mapping.json)

Use sheet to define keyword to column mappings.

Maintained and supported by: 

### Fields

- sheet (string) 
- tab (string) 
- in_dataset (string) 
- in_table (string) 
- out_dataset (string) 
- out_view (string)

### Instructions

- For the sheet, provide the full URL.
- A tab called <strong>Mapping</strong> will be created.
- Follow the instructions in the tab to complete the mapping.
- The in table should have the columns you want to map.
- The out view will have the new columns created in the mapping.

### Quick Command Line

To see all required parameters and generate a recipe from this script template run:

`python script/run.py mapping/script_mapping.json -h`

`python script/run.py mapping/script_mapping.json [all required parameters] > projects/recipe.json`

After [getting Google Cloud Credentials](/auth/README.md), execute the recipe created run the following:

`python all/run.py projects/recipe.json -u [user credentials path] -s [service credentials path]`

Any two or more recipes can be combined by copying and pasting task JSON into the task [...] list.  All tasks execute in sequence.

For scheduled recipes, see [Recipe Corn Job](/cron/README.md) or [Deplyment Script](/deploy/README.md)

