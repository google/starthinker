# The Rest Of This Document Is Pulled From Code Comments

# Python Scripts


## [/airflow/helper.py](/airflow/helper.py)

Helper used to generate an AirFlow Dag from a StarThinker JSON recipe.

Use this script to generate an Python script AirFlow uses to deploy a Dag. A
python module will be streamed to STDOUT, redirect output to a file in your 
airflow folder. 

You can edit the underlying JSON recipe without re-generating the connector, 
this connector generates the DAG in real time whenever AirFlow calls it.

### Sample call:

```
python airflow/helper.py gtech/say_hello.json > ~/airflow/dags/say_hello.py
```

### Note

Use a recipe in the call, not a recipe template.  Recipe templates are script\_\*.json.
Recipes are generated from recipe templates using [/script/run.py](/script/run.py).



# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Fairflow%2FREADME.md)
