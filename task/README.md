# Tasks
  
DISCLAIMER: This is only a reference implmentation.  We strongly recommend an internal
security and privacy review before using this code in production.

## Tasks Are Just Python Functions

Each task in StarThinker is just a python function that takes JSON as parameters.
The [project class](/util/project/__init__.py) has logic to pass the right JSON
task from a recipe to the task function in python.

- Call to a task from command line, project handles arguments.
- Call to a task from another function, just pass in JSON and instance.

## Task To JSON Recipe Mapping

Each task in a JSON recipe maps to a task script in the task directory.

- Every recipe has a { "tasks":[...tasks...] } section.
- Every task is { "function":{...parameters...] }.
- Every "function" maps to task/[function]/run.py.
- Inside every run.py is a def [function] that the parametes are passed to.
- Inside every def [function] project.task references the parameters passed in.

## Using Existing Tasks

All task definitions are stored in files script\_\*.json.  They are located in the [/gtech](/gtech) folder.
Copy each task into your custom recipe, use the UI to assemble a recipe, or use [/script](/script) to change
the task recipe into an actual call with parameters you pass in.

### Creating A New Task

A new task is a new python script and the JSON template to call it. It must be named "script\_\*.json" to
be automatically included in the UI.  Follow these steps to create a new task:

- Follow the task/hello/run.py sample.
- Create a new task/[your new task]/run.py
- Create a new task/[your new task]/\_\_init\_\_.py

Then create a JSON definition for the parameters your task takes.

- Mimic the JSON structure of any gtech/script\_\*.josn file.
- Create a new gtech/script\_[your new task].json.

### Best Practices

- Your task can have muliple parameter configurations, use a different json template for each.
- Use [/util/data/__init__.py](/util/data/__init__.py) to read and write standard data blocks in your task.
- For reference, its faster to copy and repurpose recipes in [/gtech](/gtech) folder.

# The Rest Of This Document Is Pulled From Code Comments
