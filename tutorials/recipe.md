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
- default - Default value to insert if blank given by UI or command line. If default is omitted, the field is removed from JSON entirely, allowing the task handler to detect a missing key and creatign its own default value.
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


### 3. Add Schedule ( Optional )
This will force the recipe or task to run at a specific time of day ( as defined by timezone ) regardless of what the user selects.

scripts/script_hello.json
```
{
  "setup":{
    "timezone": "America/Los_Angeles",
    "day":["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "hour":[1, 3, 8]
  },
  "tasks":[
    { "hello":{
        "hour":[0,1,2],
        "auth":"user",
        "say":{"field":{ "name":"say_first", "kind":"string", "order":1, "default":"Hello Once", "description":"Type in a greeting." }},
      }
    }
  ]
}
```

#### Setup Parameters
  - setup - Optional for recipes that mus run at a specific time regardless of user settings.
    - timezone - Affects hour of the day, [see Timezones](https://github.com/google/starthinker/blob/master/starthinker_ui/ui/timezones.py)
    - day - Day of week to run recipe, setting to [] means its a manual task only run on user trigger. Leaving blank means run every day.
    - hour - Hour of day to run recipe, setting to [] means its a manual task only run on user trigger. Leaving blank means run every hour.
  - task
    - hour - Optional, hour of day to run this task, if not set runs at global recipe schedule.

#### Using Fields In Text

The __instructions__ and __description__ parameters can also use fields to help construct instructions.

Text fields are {field:[string]} or {field:[string], prefix:[string]} where field is a field from the JSON
parameters in a task and prefix is a string value that gets appended to the value from variables.


### 4. Add meta data to the script to it can be found in the Solution Gallery:
scripts/script_hello.json
```
{
  "script":{
    "license":"Apache License, Version 2.0",
    "copyright":"Copyright 2020 Google LLC",
    "icon":"notifications",
    "title":"Say Hello",
    "description":"Recipe template for say hello.",
    "instructions":[
      "This should be called for testing only."
    ],
    "authors":["kenjora@google.com"],
    "image":"https://storage.googleapis.com/starthinker-ui/barnacle.png",
    "sample":"https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT",
    "document":"https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/",
    "from":["cm"],
    "to":["bigquery", "datastudio"],
    "pitches":[
      "Meet contractual access reporting information.",
      "Reduce unauthorized use of DCM accounts and assets.",
      "Audit user access within DCM.",
      "Prevent malicious user access / behavior."
    ],
    "impacts":{
      "spend optimization":0,
      "spend growth":0,
      "time savings":90,
      "account health":100,
      "csat improvement":90
    },
  },
  "tasks":[
    { "hello":{
        "auth":"user",
        "say":{"field":{ "name":"say_first", "kind":"string", "order":1, "default":"Hello Once", "description":"Type in a greeting." }},
      }
    }
    { "bye":{
        "hour":[21,22,23],
        "auth":"user",
        "say":{"field":{ "name":"say_second", "kind":"string", "order":1, "default":"Bye Once", "description":"Type in a farewwll." }},
      }
    }
  ]
}
```

### Solution Parameters
  - license - Optional, include to open source.
  - copyright - Required, always include.
  - icon - Get from: https://material.io/tools/icons/
  - title - Required, unique name of recipe shown in UI.
  - description - - Required, informative description shown in UI.
  - instructions - Optional, additional instructions for this task.
  - authors - - Required, list of people maintaining this task, show in UI.
  - impacts - Required, level of impact for each metric, metrics are fixed ( 0 to 100  scale ), always list all even if 0.
    - spend optimization - How well does it help the client optimize budget.
    - spend growth - How well does it help the client grow their client base or account size.
    - time savings - How well does it reduce time for client performing specific tasks.
    - account health - How well does it reduce risk for the account.
    - csat improvement - How well does it improve client perception of Googles products and services.
  - image - Optional, public screen shot or diagram of solution.
  - sample - Optional, link to public sample with anonymized data.
  - document - Optional, link to public communications document.
  - test - Optional, link to public test document.
  - from - Required, list of endpoints data is pulled from, used in UI.
  - to - Required, list of endpoints data is written to, used in UI.
  - pitches - Optional, list of short sentences describing value propositions.
  - instructions - Required, instructions for manual steps, supports embedded HTML and links.

### 5. Continue to the [testing tutorial](testing.md)...

### Notes
- You will need to re-start the UI to pick up new scripts.
- The UI on load will print 'OK' next to your script.
- Validate your JSON using [json helper](../scripts/helper.py).
- Always check [scripts](../scripts/) folder for solution samples.
- It is best practice to provide a test with each solution.

---
&copy; 2019 Google LLC - Apache License, Version 2.0
