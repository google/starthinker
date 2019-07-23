# Creating A Solution Script With Many Tasks

A solution is a script that contains to multiple tasks and defines a workflow.  Creating a solution
from a recipe adds the workflow to the UI and allows users to execute it with their own parameters.
It also adds the solution to the [Solution Gallery](https://google.github.io/starthinker/).

### 1. Continuing from the [recipe tutorial](recipe.md)...
starthinker/gtech/script_hello.json
```
{ 
  "script":{
    "license":"Apache License, Version 2.0",
    "copyright":"Copyright 2018 Google Inc.",
    "icon":"notifications",
    "product":"gTech",
    "title":"Say Hello",
    "description":"Recipe template for say hello.",
    "instructions":[
      "This should be called for testing only."
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

### 2. Create a solution file ( replace hello with your recipe script name ):
starthinker/gtech/script_hello.json
```
{ 
  "script":{
    "license":"Apache License, Version 2.0",
    "copyright":"Copyright 2018 Google Inc.",
    "icon":"notifications",
    "product":"gTech",
    "title":"Say Hello",
    "description":"Recipe template for say hello.",
    "instructions":[
      "This should be called for testing only."
    ],
    "authors":["kenjora@google.com"],
    "image":"https://storage.googleapis.com/starthinker-ui/barnacle.png",
    "sample":"https://datastudio.google.com/open/1gjxHm0jUlQUd0jMuxaOlmrl8gOX1kyKT",
    "requirements":[ "dcm", "datastudio", "bigquery" ],
    "catalysts":["security", "reporting"],
    "categories":["security", "reporting"],
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
    "instructions":[
      "Activate the recipe and wait for data sources to become avaialbe.",
      "Copy data studio dashboard."
    ]
  },
  "setup":{
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
  - image - Optional, public screen shot or diagram of solution.
  - sample - Optional, link to public sample with anonymized data.
  - requirements - Required, technical dependencies.
  - catalysts - Optional, list of gTech catalysts.
    - Acquisition - How do I reach growth by acquiring and reaching new customers? 
    - Monetization - How do I deliver the most value to my consumers and reach higher average revenue per order? 
    - Experience - How do I provide frictionless consumer experience to enable deeper engagement and loyalty to my brand?
    - Automation - How do I scale, optimize and automate processes to increase my proficiency? 
    - Insights - How do I get deeper consumer and brand insights to make better decisions? 
    - Data - How do I make my data usable and structured to measure and attribute my marketing efforts? 
  - categories - Optional, arbitrary categories, suggest including one of the following.
    - Strategy, Organization & Operations
    - Implementation, Onboarding & Data Architecture
    - Audience, Attribution & Advanced Analytics
    - Creative Services
    - Training
    - Managed Services
    - Automation
    - Site Testing & Personalization
  - pitches - Optional, short sentences describing value propositions.
  - impacts - Optional, level of impact for each metric, metrics are fixed ( 0 to 100  scale ), always list all even if 0.
    - spend optimization - How well does it help the client optimize budget.
    - spend growth - How well does it help the client grow their client base or account size.
    - time savings - How well does it reduce time for client performing specific tasks.
    - account health - How well does it reduce risk for the account.
    - csat improvement - How well does it improve client perception of Googles products and services.
  - instructions - Required, instructions for manual steps, supports HTML and links.
  - setup
    - day - Day of week to run recipe, setting to [] means its a manual task only run on user trigger. Leaving blank means run every day.
    - hour - Hour of day to run recipe, setting to [] means its a manual task only run on user trigger. Leaving blank means run every hour.
  - task
    - hour - Optional, hour of day to run this task.
 
### 3. Continue to the [testing tutorial](testing.md)...

### Notes 
- You will need to re-start the UI to pick up new scripts.
- The UI on load will print 'OK' next to your script.
- Validate your JSON using [json helper](../starthinker/gtech/helper.py).
- Always check [starthinker/gtech](../starthinker/gtech/) folder for solution samples.
- It is best practice to provide a test with each solution.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
