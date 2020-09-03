# Composer Integration

StarThinker can be easily deployed to [Apache Airflow](https://airflow.apache.org/) stack and [Google Cloud Composer](https://cloud.google.com/composer/).

## All Scripts Available As Airflow Dags

Airflow can wrap any Python function in a [PythonOperator](https://airflow.apache.org/howto/operator/python.html).  Because
[StarThinker tasks](../starthinker/task/) are just python functions with [JSON parameters](../scripts/), they can be quickly
[deployed to Airflow](../starthinker_airflow/operators/) using a simple [DAG factory](../starthinker_airflow/factory.py).

## Instructions

1. First install airflow and the StarThinker libraries.

```
pip install apache-airflow
pip install git+https://github.com/google/starthinker
```

1. Copy a [StarThinker DAG](../dags/) to your airflow folder or bucket.
1. Modify the copied file.
1. Execute the DAG like any other airflow DAG.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_enterprise.md)

## Sample DAG Recipe

The [airflow.json](../scripts/airflow.json) recipe has three tasks in it.
You can edit the underlying JSON recipe without re-generating the connector,
this connector generates the DAG in real time whenever AirFlow calls it.

```
cp startinker/dags/say_hello.py ~/airflow/dags/say_hello.py
python ~/airflow/dags/say_hello.py
```

1. Run a StarThinker native python function as a task from the recipe:
```
airflow test "scripts.say.hello.json" hello_1 2019-05-10
```

1. Run a native Airflow Operator as a task from the recipe:
```
airflow test "scripts.say.hello.json" airflow_1 2019-05-10
```

5. Run a custom Airflow Operator as a task from the recipe:
```
airflow test "scripts.say.hello.json" concerto_1 2019-05-10
```

## Cloud Resources

  - [Google Cloud Composer](https://console.cloud.google.com/composer) - where your instance will deploy.
  - [Google Cloud Storage](https://console.cloud.google.com/storage/browser) - where your user credentials will be stored ( keep this secure ).
  - [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) - where you manage your credentials.
  - [Google Cloud Billing](https://console.cloud.google.com/billing/linkedaccount) - examine costs in real time.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
