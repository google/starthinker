# The Rest Of This Document Is Pulled From Code Comments

# Python Scripts


## [/util/airflow/__init__.py](/util/airflow/__init__.py)

AirFlow connector for StarThinker, builds airflow workflow from json recipe.

Connector between AirFlow and StarThinker that turns all tasks into PythonOperators.
In future, as AirFlow matures and becomes more reliable, some handlers will migrate from 
StarThinker tasks to native AirFlow calls.

Any StarThinker task immediately becomes available as an Airflow endpoint using this code.
The DAG ID will be set to the the path of the JSON template with non alphanumeric characters
set to '.', to mimic python dot notation.




## class DAG_Factory

  A class factory that generates AirFlow Dag definitions from StarThinker JSON recipes.

  Called from an AirFlow Python Script, generates a single Dag mapped to each StarTHinker task handler.
  Loads a StartThinker JSON recipe and converts  it into an AirFlow DAG with Python operators.
  Each task int the JSON is converted to a PythonOperator, with the task passed in as a dict.
  The uuid inside the JSON recipe is used as the DAG ID.

  Sample calling wrapper, save this in your AirFlow dag directory:

    ```
    from starthinker.util.airflow import DAG_Factory
    dag = DAG_Factory('[path to a StarThinker JSON recipe]').execute()
    ```
  
  

# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Futil%2Fairflow%2FREADME.md)
