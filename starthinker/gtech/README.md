# Recipe And Solution Templates 

These JSON files are recipe temmplates that can be used to generate recipe workflows.
All templates start with 'script'. There are two types of templates:

## Recipe

Simple definitions for parameters passed to a specific task. Recipes are used by the
StarThinker UI to allow people to assemble their own workflows.  A task can have
multiple recipes defining overloading variants.  Even though it is not in the JSON spec,
Newlines are allowed in JSON used by StarThinker to allow readability of recipes.
Newlines will be removed before the JSON is parsed.

### JSON Schema

A recipe follows the following pattern.  The script section maps to the UI and open sourcing behavior.
The tasks section defines the actual call to the task handling python. 

```
{
  "script":{
    "license":"Apache License, Version 2.0", - Optional, include to open source.
    "copyright":"Copyright 2018 Google Inc.", - Required, always include.
    "icon":"notifications", - Get from: https://material.io/tools/icons/
    "product":"gTech", - Required, UI Menu to list under.
    "title":"Say Hello", - Required, unique name of recipe shown in UI.
    "description":"Recipe template for say hello.", - Required, informative description shown in UI.
    "instructions":[
      "This should be called for testing only." - Optional, additional instructions for this task.
    ],
    "authors":["kenjora@google.com"] - Required, list of people maintaining this task, show in UI.
  },
  "tasks":[ - Required, for recipe a single task parameters.
    { "hello":{ - Name of task in starthinker/task/*/run.py
      "auth":"user", - Run this task as user or service.
      "say":{"field":{ "name":"say_first", "kind":"string", "order":1, "default":"Hello Once", "description":"Type in a greeting." }}, - Parameter.
      "error":{"field":{ "name":"error", "kind":"string", "order":3, "default":"", "description":"Optional error for testing." }}, - Parameter.
      "sleep":{"field":{ "name":"sleep", "kind":"integer", "order":4, "default":0, "description":"Seconds to sleep." }} - Parameter.
    }}
  ]
}
```

### Creating A Template

When developing a new task, start with a hard coded recipe for development
and testing and create the template last.

- Copy stathinker/task/hello to stathinker/task/[new task]
- Modify the run.py code to perform your new task.
- Copy starthinker/gtech/script_hello.json to starthinker/gtech/script_[new task].json
- Modify the JSON to define the new task for the UI and parameters to pass.

To test the new task convert the template to a recipe:

```
python starthinker/script/run.py starthinker/gtech/script_[new task].json -h
```

To execute the generated recipe, when testing for example:

```
python starthinker/all/run.py [recipe from above step].json
```

To load the recipe into the UI, simply activate the development UI.  If UI is already
running, restart it.

```
source install/deploy.sh
1) Developer Menu
2) Launch Developer UI
```

Once you configure and save the new recipe in the UI, run a worker to test it.  The
worker grabs one task at a time in test mode so you may have to run it multiple times
to complete the entire recipe.

```
source starthinker_assets/development.sh
python starthinker_ui/manage.py job_worker --test --verbose
```

### Recipe Fields

Templates use fields to collect inputs.  A field with the same name in multiple palces will be requested form the user 
only once. Template defines a field using the following JSON:

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

## Solution

A solution is just a recipe with multiple tasks.  Solutions are displayed in the UI 
and designed to take the fewest parameters required for a complex workflow.

### JSON Schema

In addition to the fields in a recipe template, a solution JSON also has the following fields.

```
{
  "script":{
    "image":"https://storage.googleapis.com/starthinker-ui/barnacle.png", - Optional, public screen shot or diagram of solution.
    "sample":"https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT", - Optional, link to public sample with anonymized data.
    "requirements":[ "dcm", "datastudio", "bigquery" ], - Required, technical dependencies.
    "catalysts":["security", "reporting"], - Optional, list of gTech catalysts.
    "categories":["security", "reporting"], - Optional, arbitrary categories
    "pitches":[ - Optional, short sentences describing value propositions.
      "Meet contractual access reporting information.",
      "Reduce unauthorized use of DCM accounts and assets.",
      "Audit user access within DCM.",
      "Prevent malicious user access / behavior."
    ],
    "impacts":{ - Optional, level of impact for each metric, metrics are fixed ( 0 to 100  scale ).
      "spend optimization":0,
      "spend growth":0,
      "time savings":90,
      "account health":100,
      "csat improvement":90
    },
    "instructions":[ - Required, instructions for manual steps, supports HTML and links.
      "Activate the recipe and wait for data sources to become avaialbe.",
      "Copy data studio dashboard."
    ]
  },
  "setup":{ - Required, schedule to run this recipe when deployed, each task can specify a different hour
    "day":["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "hour":[1, 3, 8]
  }
}
```

### Catalysts

Use these catalysts when defining a solution.

- Acquisition - How do I reach growth by acquiring and reaching new customers? 
- Monetization - How do I deliver the most value to my consumers and reach higher average revenue per order? 
- Experience - How do I provide frictionless consumer experience to enable a deeper engagement and loyalty to my brand ?
- Automation - How do I scale, optimize and automate processes to increase my proficiency? 
- Insights - How do I get deeper consumer and brand insights to make better decisions? 
- Data - How do I make my data usable and structured to measure and attribute my marketing efforts? 

### Categories

Use at least one of the following categories when defining a solution.

- Strategy, Organization & Operations
- Implementation, Onboarding & Data Architecture
- Audience, Attribution & Advanced Analytics
- Creative Services
- Training
- Managed Services
- Automation
- Site Testing & Personalization

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
