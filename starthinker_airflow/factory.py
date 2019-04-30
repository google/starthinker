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


"""AirFlow connector for StarThinker, builds airflow workflow from json recipe.

Connector between AirFlow and StarThinker that turns all tasks into PythonOperators.
In future, as AirFlow matures and becomes more reliable, some handlers will migrate from 
StarThinker tasks to native AirFlow calls.

Any StarThinker task immediately becomes available as an Airflow endpoint using this code.
The DAG ID will be set to the the path of the JSON template with non alphanumeric characters
set to '.', to mimic python dot notation.

"""

import re
from datetime import datetime, date
from importlib import import_module

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from starthinker.util.project import get_project

RE_DAG_NAME = re.compile('([^\s\w]|_)+')

class DAG_Factory():
  """A class factory that generates AirFlow Dag definitions from StarThinker JSON recipes.

  Called from an AirFlow Python Script, generates a single Dag mapped to each StarTHinker task handler.
  Loads a StartThinker JSON recipe and converts  it into an AirFlow DAG with Python operators.
  Each task int the JSON is converted to a PythonOperator, with the task passed in as a dict.
  The uuid inside the JSON recipe is used as the DAG ID.

  Sample calling wrapper, save this in your AirFlow dag directory:

    ```
    from starthinker.util.airflow import DAG_Factory
    dag = DAG_Factory('[path to a StarThinker JSON recipe]').execute()
    ```
  
  """


  def __init__(self, _recipe_path):
    self.recipe_path = _recipe_path
    self.recipe = get_project(_recipe_path)
    self.dag = None


  def dag_id(self):
    return RE_DAG_NAME.sub('.', self.recipe_path)


  def execute(self):
    self.dag = DAG(
      dag_id = self.dag_id(),
      default_args = {
        'owner': 'airflow',
        'start_date': datetime.now()
      },
      schedule_interval = None,
      catchup=False
    )

    instances = {}
    for task in self.recipe['tasks']:
      function = task.items()[0][0]

      # count instance per task
      instances.setdefault(function, 0)
      instances[function] += 1

      # in future, ad logic here to dispatch some operators to AirFlow built in operators
      PythonOperator(
        task_id='%s_%d' % (function, instances[function]),
        python_callable = getattr(import_module('starthinker.task.%s.run' % function), function),
        op_kwargs = {'recipe': self.recipe, 'instance':instances[function]},
        dag=self.dag
      )

    return self.dag


  def schedule(self):
    # for now simplest case is to execute all directories locally
    pass


  def print_commandline(self):

    print ''
    print 'DAG: %s' % self.dag_id()
    print ''
 
    instances = {}
    for task in self.recipe['tasks']:
      function = task.items()[0][0]

      # count instance per task
      instances.setdefault(function, 0)
      instances[function] += 1

    print 'airflow test "%s" %s_%d %s' % (self.dag_id(), function, instances[function], str(date.today()))
    print ''
