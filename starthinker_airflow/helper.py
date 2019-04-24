###########################################################################
# 
#  Copyright 2019 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################


"""Helper used to generate an AirFlow Dag from a StarThinker JSON recipe.

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

"""

import argparse

AIRFLOW_TEMPLATE = '''from starthinker_airflow.factory import DAG_Factory
  
dag_factory = DAG_Factory('%s')
dag = dag_factory.execute()

if __name__ == "__main__":
  dag_factory.print_commandline()
'''

if __name__ == "__main__":

  # assemble parameters
  parser = argparse.ArgumentParser(usage='python starthinker_airflow/helper.py starthinker/gtech/say_hello.json > ~/airflow/dags/say_hello.py\nTo get DAG testing commands run: python ~/airflow/dags/say_hello.py\n')
  parser.add_argument('recipe', help='JSON recipe to connect to airflow.')
  args = parser.parse_args()

  # print AirFlow connector code to STDOUT ( use > to pipe to correct Python file in Dag folder. )
  print AIRFLOW_TEMPLATE % args.recipe
