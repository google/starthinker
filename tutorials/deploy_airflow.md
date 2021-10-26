# Composer Integration

StarThinker can be easily deployed to [Apache Airflow](https://airflow.apache.org/) stack and [Google Cloud Composer](https://cloud.google.com/composer/).

## All Scripts Available As Airflow Dags

Airflow can wrap any Python function in a [PythonOperator](https://airflow.apache.org/howto/operator/python.html).  Because
[StarThinker tasks](../starthinker/task/) are just python functions with [JSON parameters](../scripts/), they can be quickly
[deployed to Airflow](../starthinker/airflow/operators/) using a simple [DAG factory](../starthinker/airflow/factory.py).

## Instructions

1. First [install airflow](https://airflow.apache.org/docs/stable/start.html) and the [StarThinker package](deploy_package.md).

  ```
  apache-airflow
  starthinker
  ```

1. Copy a [StarThinker DAG](../dags/) to your Airflow folder or bucket.
1. Modify the copied file.
1. Execute the DAG like any other Airflow DAG.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_enterprise.md)

## Sample DAG Recipe

The [airflow.json](../scripts/airflow.json) recipe has three tasks in it.
These three tasks represent the three possible ways to use ST with Airflow.
1. Using a native Airflow Operator in a recipe.
1. Using a custom Airflow Operator in a recipe.
1. Using any StarThinker task in a recipe.

```
cp dags/sample_dag.py ~/airflow/dags/sample_dag.py
python ~/airflow/dags/sample_dag.py
```

1. Run a native Airflow Operator as a task from the recipe:
```
airflow tasks test "sample" airflow_1 2020-09-14
```

1. Run a custom Airflow Operator as a task from the recipe:
```
airflow tasks test "sample" starthinker_airflow_1 2020-09-14
```

1. Run a StarThinker native python function as a task from the recipe:
```
airflow tasks test "sample" hello_1 2020-09-14
```

## Using User Credentials In Airflow

Storing user credentials inside a connector variable will work for single jobs because the refresh token
is refreshed when loaded.  However, for multiple jobs the refresh token must be shared across jobs.
StarThinker solves this by allowing a GCP Storage path for user credentials.





## Cloud Resources

  - [Google Cloud Composer](https://console.cloud.google.com/composer) - where your instance will deploy.
  - [Google Cloud Storage](https://console.cloud.google.com/storage/browser) - where your user credentials will be stored ( keep this secure ).
  - [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://console.cloud.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2019 Google LLC - Apache License, Version 2.0
