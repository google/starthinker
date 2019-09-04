# Recipe Tests

Recipe tests are integration tests, since StarThinker is mostly an integration platform.  They are recipes
with values hard coded and designed to be ran by anyone with access to the underlying resources.  To help 
test recipes, StarThinker has a [Test Task](../starthinker/task/test/). It is like any other task
in StarThinker except that it doesn't do any work.  It simply compares and asserts endpoints.  



### Setting up the Testing Framework

The steps below will get Starthinker testing framework set up with values from your account so you are able to successfully run all Starthinker tests.

Starthinker tests require a config file and a Google Sheet that Starthinker will read off of to perform integration tests.  The config file will be auto-generated during the Developer Deployment and the Starthinker Testing Sheet will need to be copied from a template linked below.  After these two resources have been generated they will each require a developer to enter values specific to your account so these tests have the correct priviledges to run in your environment.

1. If you have not yet completed the developer deployment, visit the link below and go through all the steps outlined:
```
https://github.com/google/starthinker/blob/master/tutorials/deploy_developer.md
```

2. The config file will be created and is added at the location below, open up this file and enter in the information for each test you would like to run.  We recommend filling out the information for each test so you have full coverage of knowing when something breaks.
```
{{Your Starthinker Directory}}/starthinker/test/config.json
```

3. Visit the URL below and use "File -> Make a Copy" to create a copy of this sheet that you can edit.
```
https://docs.google.com/spreadsheets/d/1aH_eT3N7M14YGLl2y429doz1m6RWp6oQHidfXkIaMdU/edit?usp=sharing
```

4. Rename your copy of the sheet to the name below:
```
Primary Test Sheet ( StarThinker )
```

5. Go through the tabs of the sheet and fill out tabs with missing information.  Note: If information isn't filled out for a test's tab of the sheet, ONLY that specific test will fail.

6. Testing is all set up! Please continue reading to learn how to run tests 



### Running Tests

Tests are just recipes with some additional tasks sprinkeld in. You can run a test just like a recipe.  
Run a single test like any other recipe from the command line. [See Developer Notes](deploy_developer.md)

Run all test using:

1. Option 1) Developer Menu
2. Option 7) Test Tasks
  - You may be asked for a Cloud Project ID ( use the ID, not the Name, not the Number )
  - You may be asked for [Service Credentials](cloud_service.md).
  - You may be asked for [Installed Client Credentials](cloud_client_installed.md).

The test controller is located in:
  - [starthinker/test/helper.py](../starthinker/test/helper.py)
  - All test files are located in [starthinker/test/test_recipes/]



### Logging

Running all the tests will result in the writing on a log file to see the output of each test.  The log file is located at the location below:
```
starthinker/test/log.txt
```



### Creating A New Test

When creating new recipes, tests should be added to the framework so future developers don't break the code.
To create a test:

1. Create a test under the test repository [starthinker/test/test_recipes/]
2. Run a task that is the same as the feature you just wrote.
3. Add a {'test':...} task that will determine if the task you just ran was successful.  There are a few examples of how to create a test task.
  -Check out the testing run file to determine how to test your recipes. [starthinker/starthinker/task/test/run.py]


It is important for your tests to be usable by other developers on your team who may have different permissions to resources.  In order to create a test that will update values in the config file so your fellow teammates can enter in their own values to your test follow to style below:

1. Go through your test file and determine which parameters should be customizable and which should be hardcoded for the test
2. For those who need to be customizable follow the format below
  -Note: You can have multiple fields with the same name, this will result in the user being asked once for that value then it will be populated everywhere
```
{"field":{ "name":"{{Variable name}}", "kind":"{{variable type}}", "default":"{{default value}}" }

Example:
"tab":{"field":{ "name":"tab", "kind":"string", "default":"Campaign Automation" }},
``` 
3. To test your new recipe, you can re-run the developer install which will go through all the recipes under test_recipes/ and add any necessary fields to the config.json object



### Testing Examples

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
```
1. check if storage file exists
```
{ "test":{
  "auth":"service",
  "storage":{
    "bucket":"bucket_name",
    "file":"file.png",
    "delete":true
   }
}}
```
1. check if storage file exists
```
{ "test":{
  "auth":"service",
  "drive":{
    "file":"Some File Name Or URL",
    "delete":true
   }
}}
```

### Notes

- When developing a new recipe write the test recipe first.
- Ensure the test is re-entrant.
- Ensure any test assets are shared with starthinker-assets@googlegroups.com.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
