# Creating A Python Task

A task in StarThinker is a python function that can be executed by the framework given a set of JSON parameters called a [recipe](recipe.md).
It is just python, with a thin [project singleton wrapper](../starthinker/util/project/__init__.py)  that pulls parameters from the command line or passed in, saving developers
the trouble of re-coding common tasks like scheduling, authentication, and UI integration.

### 1. Create a new task... ( rename hello to your task ):
starthinker/task/hello/\_\_init\_\_.py
```
```
starthinker/task/hello/run.py
```
from starthinker.util.project import project

@project.from_parameters
def hello():
  print project.task

if __name__ == "__main__":
  hello()
```

### 2. Thats it, the python code is integrated, now create a script to pass parameters to  your task:
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
### 4. Execute your new task.
```
source starthinker_assets/development.sh
```
```
python starthinker/all/run.py hello.json -u $STARTHINKER_USER -s $STARTHINKER_SERVICE -p $STARTHINKER_PROJECT --verbose
```

### 5. Continue to the [recipe  tutorial](recipe.md)...

## Notes

- The [@project.from_parameters](../starthinker/util/project/__init__.py)  decorator is StarThinker.  Everything else is just python.
- Using the [util library](../starthinker/util/) is optional but convenient.
- Always check [starthinker/task](../starthinker/task/) folder for task samples.
- Always check [scripts](../scripts/) folder for script samples.
- New scopes for user authentication can be added at [starthinker/config.py](../starthinker/config.py).
- You can remove scopes if you are not planning to use the tasks requiring them.
- The Google API helper can be extended by adding an endpoint at [starthinker/util/google_api/\_\_init\_\_.py](../starthinker/util/google_api/__init__.py).
- It is best practice to provide at least one or more [reference recipes](recipe.md) for a task.
- When develoing a new task, the first script should be a [test script](testing.md).
- Even the credentials are optional, each script is pure python parameters not tied to any Cloud Service.
- A script may call the same task multiple times with the same or different parameters.
- A script may call multiple tasks.
- Each task must have a unique name.

---
&copy; 2019 Google LLC - Apache License, Version 2.0
