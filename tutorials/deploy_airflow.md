# Airflow Integration

StarThinker can be easily deployed to Cloud Composer / Airflow using a basic factory.
This allows recipe JSON built in StarThinker to execute on the [Apache Airflow](https://airflow.apache.org/) 
stack and [Google Cloud Composer](https://cloud.google.com/composer/).


## Setup

You must have Airflow installed or deployed on Google Cloud Composer. The 
[airflow.json][../starthinker/gtech/airflow.json] recipe has three tasks in it.

1. Airflow task.
1. Concerto task 
1. Python task.

A single recipe can define a workflow that deploys all three types in one recipe.
If a recipe uses an Airflow or Composer task, it must be deployed to Airflow.


## Example 

StarThinker has a helper used to generate an AirFlow Dag from a StarThinker JSON recipe.

Use this script to generate an Python script AirFlow uses to deploy a Dag. A
python module will be streamed to STDOUT, redirect output to a file in your 
Airflow folder. 

You can edit the underlying JSON recipe without re-generating the connector, 
this connector generates the DAG in real time whenever AirFlow calls it.

1. Generate the factory powered DAG:
```
python starthinker_airflow/helper.py starthinker/gtech/airflow.json > ~/airflow/dags/say_hello.py
```

1. The factory adds a helper that shows Airflow commands when you try to run it directly:
```
python ~/airflow/dags/say_hello.py
```

1. Run a StarThinker native python function as a task fromt he recipe:
```
airflow test "starthinker.gtech.say.hello.json" hello_1 2019-05-10
```

1. Run a native Airflow Operator as a task from the recipe:
```
airflow test "starthinker.gtech.say.hello.json" airflow_1 2019-05-10
```

5. Run a Project Concerto Operator as a task from the recipe:
```
airflow test "starthinker.gtech.say.hello.json" concerto_1 2019-05-10
```

## Development Progress

All Airflow and Concerto operators and parameters are mapped to the offical APIs.

- [Add A Concerto Operator](../starthinker_airflow/concerto/)
- [Use An Airflow Operator](https://airflow.apache.org/_api/index.html)
- [Create A Workflow Use Them](task.md)
- [Integrate With UI](recipe.md)


## Notes

The generated dag has a helper built in, if you execute it directly it will print the proper airflow command instead of erroring.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
