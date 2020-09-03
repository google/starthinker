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
python starthinker/all/run.py scripts/say_hello.json -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT
```

### Run A Specific Task In A Recipe

This is a specific task run, the -i parameter specifies which instance of that task to execute if there is more than one.

```
python starthinker/tasks/hello/run.py scripts/say_hello.json -i 1 -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT
```

## Converting A Script To A Recipe

Scripts have { field:... } parameters because they are templates.  To run them you must first convert
the fields to values using the [script helper](../starthinker/script/run.py). An example below:

### Interactive Conversion

```
python starthinker/script/run.py scripts/script_hello.json

(1 of 4) Recipe file to create from scripts/script_hello.json template.

Full Path TO JSON File:hello.json

(2 of 4) Type in a greeting.  ( Default to "Hello Twice" if blank. )

say_second ( string ):

(3 of 4) Type in a greeting.  ( Default to "Hello Once" if blank. )

say_first ( string ):Hello Me

(4 of 4) Optional error for testing.  ( Default to "" if blank. )

error ( string ):

(5 of 4) Seconds to sleep.  ( Default to "0" if blank. )

sleep ( integer ):

JSON Written To:  hello.json
```

### Shell Script Conversion
```
python starthinker/script/run.py scripts/script_hello.json -h
usage: run.py [-h] [--say_second SAY_SECOND] [--say_first SAY_FIRST]
              [--error ERROR] [--sleep SLEEP]
              json

positional arguments:
  json                  JSON recipe template to configure.

optional arguments:
  -h, --help            show this help message and exit
  --say_second SAY_SECOND
                        Type in a greeting.
  --say_first SAY_FIRST
                        Type in a greeting.
  --error ERROR         Optional error for testing.
  --sleep SLEEP         Seconds to sleep.

python starthinker/script/run.py scripts/script_hello.json --say_second "Two" --say_first "One" --error "" > hello.json
```

Now the script is converted to a recipe with values, the recipe can be executed:

```
python starthinker/all/run.py hello.json -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT
```

## Notes
- If the credentials and project are defined inside a recipe, the command line -u -s -p parameters are optional.
- Add a -c $STARTHINKER_CLIENT_INSTALLED parameter to run the user auth while executing the recipe.
- Each task is execured as its own process.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
