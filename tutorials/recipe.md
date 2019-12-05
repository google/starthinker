# Creating A Script For A Single Task 

A script in StarThinker is a set of JSON parameters mapping back to [tasks](task.md). Creating a script
makes the task executable from the command line.  Connecting the script to the UI makes it executable by any user
using the UI, it also makes it available in the [Recipe Gallery](https://google.github.io/starthinker/code/).

Note, a recipe is a JSON file with hard coded values specific to a client while a script or solution is a JSON file 
with a structure __script\*.json__ and { 'field':{...}} placeholders that act as a template instead of values.

![UI Recipe Architecture](images/ui_recipe_map.png)
[UI Recipe  Architecture Larger](images/ui_recipe_map.png)

### 1. Continuing from the [task tutorial](task.md)...
hello.json
```
{
  "tasks":[
    { "hello":{
        "auth":"user",
        "say":"Hello World"
      }
    }
  ]
}
  ```

### 2. Create a script file ( replace hello with your recipe script name ):
scripts/script_hello.json
```
{
  "tasks":[
    { "hello":{
        "auth":"user",
        "say":{"field":{ "name":"say_first", "kind":"string", "order":1, "default":"Hello Once", "description":"Type in a greeting." }}
      }
    }
  ]
}
```

#### Script JSON Fields

A field with the same name in multiple palces will be requested form the user only once. A script defines a field using the following JSON:

```
{"field":{ "name":"say_first", "kind":"string", "order":1, "default":"Hello Once", "description":"Type in a greeting." }}
```

- name: Shown in UI and used as key to store value.
- default - Default value to insert if none given by UI or command line.
- description - Test explaining use of field value.
- prefix - Appended to the value given by the user for name-spacing purposes.
- order - The sequence in which fieds will be asked for in UI or command line.
- kind: Determines type of input asked from user in UI or command line.
  - string
  - email ( validates )
  - integer
  - boolean
  - text ( long string )
  - choice ( additional parameter choices = [list] )
  - timezone ( in UI triggers specific drop down )
  - json ( validates )
  - integer_list
  - string_list

#### UI Specific Fields
The UI provides a few constants to every recipe.  If these field names are included in the script, they will
bu auto populated and not presented to the user for input in the UI.  This does not apply to a script being
converted to a recipe on the command line, it only applies to the UI.

  - recipe_project - the project id from the service credentials used for the recipe.
  - recipe_name - a slugified [a-zA-Z0-9_] unique name of the recipe given by the user.
  - recipe_token - a random hexadecimal string, unique per recipe.
  - recipe_timezone - select by user in the UI.
  - recipe_email - the email of the user deploying the recipe.
  - recipe_email_token - the email with the token appended using + to join.


### 3. Connect the script to the UI so non-coding users can use it in a recipe:
scripts/script_hello.json
```
{
  "script":{
    "license":"Apache License, Version 2.0",
    "copyright":"Copyright 2018 Google Inc.",
    "icon":"notifications",
    "product":"gTech",
    "title":"Say Hello",
    "description":"Recipe template for {field:recipe_name}.",
    "instructions":[
      "This should be called for testing only."
      "It will print {field:say_first}."
    ],
    "authors":["kenjora@google.com"]
  },
  "tasks":[
    { "hello":{
        "auth":"user",
        "say":{"field":{ "name":"say_first", "kind":"string", "order":1, "default":"Hello Once", "description":"Type in a greeting." }},
      }
    }
  ]
}
```

#### Script Parameters
  - license - Optional, include to open source.
  - copyright - Required, always include.
  - icon - Get from: https://material.io/tools/icons/
  - product - Required, UI Menu to list under.
  - title - Required, unique name of recipe shown in UI.
  - description - - Required, informative description shown in UI.
  - instructions - Optional, additional instructions for this task.
  - authors - - Required, list of people maintaining this task, show in UI.

#### Using Fields In Text

The __instructions__ and __description__ parameters can also use fields to help construct instructions.

Text fields are {field:[string]} or {field:[string], prefix:[string]} where field is a field from the JSON 
parameters in a task and prefix is a string value that gets appended to the value from variables.


### 4. Continue to the [solution tutorial](solution.md)...

## Notes
- You will need to re-start the UI to pick up new scripts.
- The UI on load will print 'OK' next to your script.
- Validate your JSON using [json helper](../scripts/helper.py).
- Always check [scripts](../scripts/) folder for script samples.
- It is best practice to provide at least one or more [reference recipe scripts](recipe.md) for a task.
- Overloaded tasks can have more than one recipe or script defining more than one input configuration.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
