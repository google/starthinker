# Running A Recipe

The command line version of StarThinker runs directly on Python, other than some python
libraries, no intermediate frameworks are necessary. The goal is rapid development and iteration.

The most common parameters for helpers are:

- -u $STARTHINKER_USER - user credentials for accessing API endpoints.
- -c $STARTHINKER_CLIENT - client creddentials for authenticating, not needed if user credentials already exist.
- -s $STARTHINKER_SERVICE - service credentials for writing data.
- -p $STARTHINKER_PROJECT - cloud project to bill the data transfer to.
- --verbose - print all debug output to STDOUT.
- --force - if recipe has a schedule, ignore it and run all the tasks.

Before running any recipes make sure to [install](deploy_developer.md) and load the python virtual environment:

```
source starthinker_assets/development.sh
```

### Run All Tasks In Recipe

This srcript looks inside the recipe and kicks off a new process for each task in sequence.

```
python starthinker/tool/recipe.py scripts/say_hello.json -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT
```

### Run A Specific Task In A Recipe

This is a specific task run, the -i parameter specifies which instance of that task to execute if there is more than one.

```
python starthinker/tool/recipe.py scripts/say_hello.json -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT -i 1
```

## Recipes With Fields

Some recipes have { field:... } parameters because they are templates.  When run they will prompt
for the field values.  Alternatively a recipe can be saved with all the fields filled in:

python starthinker/tool/recipe.py scripts/hello.json -rc hello_with_values.json

## Notes
- If the credentials and project are defined inside a recipe, the command line -u -s -p parameters are optional.
- Add a -c $STARTHINKER_CLIENT_INSTALLED parameter to run the user auth while executing the recipe.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
