# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/script/run.py](/script/run.py)

Command line to convert script with fields into a recipe with specific values.

Scripts are JSON templates that define a workflow.  Files in the format script_\*.json.
Each script can be converted to a recipe by replacing { field:{...}} elements with
actual vaues.

This program reads {{ field:{...}} values from the script JSON, translates them into 
command line arguments, and uses those arguments to fill in the JSON {{ field:{...}} values
and produce a specific recipe as STDOUT.  Which can be piped to a file.

Example:

  `python script/run.py dcm/script_dcm_to_bigquery.json`

  Will produce the following because it expects the arguments in the json script.

  ```
  usage: run.py [-h] json account report_id report_name dataset table
  run.py: error: too few arguments
  ```

  To see a detailed list of arguments run with the -h option:

  ```
  python script/run.py dcm/script_dcm_to_bigquery.json -h
  usage: run.py [-h] json account report_id report_name dataset table
  
  positional arguments:
    json         JSON recipe file to script.
    account      DCM network id.
    report_id    DCM report id from the UI.
    report_name  DCM report name, pass '' if using id instead.
    dataset      Dataset to be written to in BigQuery.
    table        Table to be written to in BigQuery.
  
  optional arguments:
    -h, --help   show this help message and exit
    --datastudio  Alter columns for datastudio, fixes nulls and date format.
  ```

  Then to turn the script into a recipe run:

  `python script/run.py dcm/script_dcm_to_bigquery.json 7880 1234567 "" "Test_Dataset" "Test_Table" --datastudio > test_recipe.json`

  To perform the work of the script for the now filled in recipe:
 
  `python all/run.py test_recipe.json`




### function parser_add_field(parser, field):


  Translates JOSN field specification into a command line argument.

    Args:
      parser: (ArgumentParser) An existing initalized argument parser to add fields to.
      field: (dict) A filed structured as: { "name":"???", "kind":"???", "default":???, "description":"???" }}

    Returns:
      Nothing.  Modifies parser in place.

    Raises:
      NotImplementedError: If field cannot be found.

  

## [/script/parse.py](/script/parse.py)



### function json_set_fields(struct, variables):


  Recusrsively replaces fields in script JSON with values provided.
     Field has format: { "field":{ "name":"???", "kind":"???", "default":???, "description":"???" }}

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name of field.

    Returns:
      Nothig. Struct is modified in place.

  


### function json_set_instructions(struct, variables):


  Replaces all fields in instructions with values provided.
     Checks if struct['script']['instructions'] exist.  The replaces all %(???)s variables
     with values provided.  Note: %(???)s must match { "field":{ "name":"???" }} in JOSN.

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name of field.

    Returns:
      Nothig. Instructions are modified in place.

  


### function json_get_fields(struct, path=[]):


  Recusrsively finds fields in script JSON and returns them as a list.
     Field has format: { "field":{ "name":"???", "kind":"???", "default":???, "description":"???" }}

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      path: (list) Stack that keeps track of recursion depth. Not used externally.

    Returns:
      fields: (list) A list of dictionaries representing each field struct found in the JSON.

  


### function json_set_description(struct, variables):


  Replaces all fields in description with values provided.
     Checks if struct['script']['description'] exist.  The replaces all %(???)s variables
     with values provided.  Note: %(???)s must match { "field":{ "name":"???" }} in JOSN.

    Args:
      struct: (dict) A dictionary representation fo the JSON script.
      variables: (dict) A lookup table of all values to be replaced, key is name of field.

    Returns:
      Nothig. Description is modified in place.

  
