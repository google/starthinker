# Recipe Tests

Recipe tests are integration tests, since StarThinker is mostly an integration platform.  They are recipes
with values hard coded and designed to be run by anyone with access to the underlying resources.  To help 
test recipes, StarThinker has a [Test Task](../starthinker/task/test/). It is like any other task
in StarThinker except that it doesn't do any work.  It simply compares and asserts endpoints.  

### Available Test Tasks

1. check if sheet matches given values
```
{ "test": {
  "auth":"user",
  "sheets": {
    "url":"https://docs.google.com/spreadsheets/d/1h-Ic-DlCv-Ct8-k-VJnpo_BAkqsS70rNe0KKeXKJNx0/edit?usp=sharing",
    "tab":"Sheet_Clear",
    "range":"A1:C",
    "values":[
      ["Animal", "Age", "Weight ( lbs )"],
      ["dog", 7, 67],
      ["cat", 5, 1.5],
      ["bird", 12, 0.44],
      ["lizard", 22, 1],
      ["dinosaur", 1600, 273.97]
    ]
  }
}}
```
1. check if bigquery table has given values or has data
```
{ "test": {
  "auth":"user",
  "bigquery":{
    "dataset":"Test",
    "table":"Sheet_To_BigQuery",
    "schema":[
      {"name": "Animal", "type": "STRING"},
      {"name": "Age", "type": "INTEGER"},
      {"name": "Weight_lbs", "type": "FLOAT"}
    ],
    "values":[
      ["dog", 7, 67],
      ["cat", 5, 1.5],
      ["bird", 12, 0.44],
      ["lizard", 22, 1],
      ["dinosaur", 1600, 273.97]
    ]
  }
}}
```
1. assert recipe has executed all tasks before this point
```
{ "test": {
  "assert":"Completed all tasks."
}}
``` 
1. check if path exists
```
{ "test": {
  "path":"somefile.txt"
}}

### Running Tests
Tests are just recipes with some additional tasks sprinkeld in. You can run a test just like a recipe.  
Run a single test like any other recipe from the command line. [See Developer Notes](deploy_developer.md)

Run all test using:

1. Option 1) Developer Menu
1. Option 4) Test Tasks
  - You may be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
  - You may be asked for [Service Credentials](cloud_service.md).
  - You may be asked for [Installed Client Credentials](cloud_client_installed.md).

The test controller is located in:
  - [starthinker/test/helper.py](../starthinker/test/helper.py)
  - Any file named __test_\*.json__ is considered a test recipe.

### Creating Tests

When creating new recipes, tests should be added to the framework so future developers don't break the code.
To create a test:

1. Create a __test_[recipe].json__ like you would any other recipe.
1. Add {'test':...} tasks to it between your normally executing tasks.
1. The [Test Helper](../starthinker/test/helper.py) will pick up the new test and execute it.

### Notes

- When developing a new recipe write the test recipe first.
- Ensure the test is re-entrant.
- Ensure any test assets are shared with starthinker-assets@googlegroups.com.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
