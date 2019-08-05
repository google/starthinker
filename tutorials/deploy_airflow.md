# Airflow Integration

StarThinker can be easily deployed to Cloud Composer / Airflow using a basic factory.
This allows recipe JSON built in STarThinker to execute on the Airflow stack.

## Setup

You must have airflow installed or deployed on Google Cloud.

## Example 

Helper used to generate an AirFlow Dag from a StarThinker JSON recipe.

Use this script to generate an Python script AirFlow uses to deploy a Dag. A
python module will be streamed to STDOUT, redirect output to a file in your 
airflow folder. 

You can edit the underlying JSON recipe without re-generating the connector, 
this connector generates the DAG in real time whenever AirFlow calls it.

```
python starthinker_airflow/helper.py starthinker/gtech/say_hello.json > ~/airflow/dags/say_hello.py
python ~/airflow/dags/say_hello.py
airflow test "starthinker.gtech.say.hello.json" hello_1 2019-05-10
```

## Development Progress

The CSE team is building airflow modules, as they become available and tested StarThinker 
will integrate with them. Until those modules become available StarThinker will continue
to use the product supported APIs. 

### Note

The generated dag has a helper built in, if you execute it directly it will print the proper airflow command instead of erroring.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
