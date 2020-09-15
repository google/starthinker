###########################################################################
#
#  Copyright 2020 Google LLC
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

Connector between AirFlow and StarThinker that turns all tasks into
PythonOperators.
In future, as AirFlow matures and becomes more reliable, some handlers will
migrate from
StarThinker tasks to native AirFlow calls.

Any StarThinker task immediately becomes available as an Airflow endpoint using
this code.
The DAG ID will be set to the the path of the JSON template with non
alphanumeric characters
set to '.', to mimic python dot notation.

"""

from airflow.operators.bash_operator import BashOperator

import re
from datetime import datetime, date
from importlib import import_module

from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator

from starthinker.script.parse import json_set_fields


class DAG_Factory():
  """A class factory that generates AirFlow Dag definitions from StarThinker JSON recipes.

  Called from an AirFlow Python Script, generates a single Dag mapped to each
  StarTHinker task handler.
  Loads a StartThinker JSON recipe and converts  it into an AirFlow DAG with
  Python operators.
  Each task int the JSON is converted to a PythonOperator, with the task passed
  in as a dict.
  The uuid inside the JSON recipe is used as the DAG ID.

  Sample calling wrapper, save this in your AirFlow dag directory:

    ```
    from starthinker_airflow.factory import DAG_Factory
    dag = DAG_Factory([StarThinker recipe JSON]).execute()
    ```

  """

  def __init__(self, _dag_name, _script, _script_parameters=None):
    self.dag_name = _dag_name
    self.recipe = _script
    if _script_parameters:
      json_set_fields(self.recipe, _script_parameters)
    self.dag = None

  def apply_credentails(self,
                        user_conn_id=None,
                        gcp_conn_id='google_cloud_default'):
    """
       user_conn_id: The connection to use for user authentication.
       gcp_conn_id: The connection to use for service authentication.
    """

    self.recipe.setdefault('setup', {}).setdefault('auth', {})

    # If supplied, load "user" auth information into the recipe
    if user_conn_id:
      user_connection_extra = BaseHook.get_connection(user_conn_id).extra_dejson
      if user_connection_extra['extra__google_cloud_platform__key_path']:
        self.recipe['setup']['auth']['user'] = user_connection_extra[
            'extra__google_cloud_platform__key_path']
      elif user_connection_extra['extra__google_cloud_platform__keyfile_dict']:
        self.recipe['setup']['auth']['user'] = user_connection_extra[
            'extra__google_cloud_platform__keyfile_dict']
      if user_connection_extra['extra__google_cloud_platform__project']:
        self.recipe['setup']['id'] = user_connection_extra[
            'extra__google_cloud_platform__project']

    # Load "service" auth information into the recipe
    if gcp_conn_id:
      service_connection_extra = BaseHook.get_connection(
          gcp_conn_id).extra_dejson
      if service_connection_extra['extra__google_cloud_platform__key_path']:
        self.recipe['setup']['auth']['service'] = service_connection_extra[
            'extra__google_cloud_platform__key_path']
      elif service_connection_extra[
          'extra__google_cloud_platform__keyfile_dict']:
        self.recipe['setup']['auth']['service'] = service_connection_extra[
            'extra__google_cloud_platform__keyfile_dict']
        try:
          keyfile_dict_json = json.loads(service_connection_extra[
              'extra__google_cloud_platform__keyfile_dict'])
          if keyfile_dict_json and keyfile_dict_json['project_id']:
            self.recipe['setup']['id'] = keyfile_dict_json['project_id']
        except Exception as e:
          self.log.error('Failed parsing the Keyfile JSON for gcp_conn_id=%s',
                         self.gcp_conn_id)
          raise e
      if service_connection_extra['extra__google_cloud_platform__project']:
        self.recipe['setup']['id'] = service_connection_extra[
            'extra__google_cloud_platform__project']

  def python_task(self, function, instance):
    print('ST TASK:', function, instance)

    PythonOperator(
        task_id='%s_%d' % (function, instance),
        python_callable=getattr(
            import_module('starthinker.task.%s.run' % function), function),
        op_kwargs={
            'recipe': self.recipe,
            'instance': instance
        },
        dag=self.dag)

  def airflow_task(self, task, instance, parameters):
    print('AF TASK:', task, instance)

    def airflow_import_unroll(definition):
      return next(iter([i for i in definition.items() if i[0] != '__comment__']))

    af_path, af_module = airflow_import_unroll(parameters)
    af_module, af_operator = airflow_import_unroll(af_module)
    af_operator, af_parameters = airflow_import_unroll(af_operator)

    operator = getattr(import_module('%s.%s.%s' % (task, af_path, af_module)), af_operator)

    af_parameters['dag'] = self.dag
    af_parameters['task_id'] = '%s_%d' % (task, instance)

    operator(**af_parameters)

  def execute(self):
    print('DAG:', self.dag_name)

    self.dag = DAG(
        dag_id=self.dag_name,
        default_args={
            'owner': 'airflow',
            'start_date': datetime.now()
        },
        schedule_interval=None,
        catchup=False)

    instances = {}
    for task in self.recipe['tasks']:
      function = next(iter(task.keys()))

      # count instance per task
      instances.setdefault(function, 0)
      instances[function] += 1

      # if airflow operator
      if function in ('airflow', 'starthinker_airflow'):
        self.airflow_task(function, instances[function], task[function])

      # if native python operator
      else:
        self.python_task(function, instances[function])

    print('DONE')
    return self.dag

  def schedule(self):
    # for now simplest case is to execute all tasks sequentially
    pass

  def print_commandline(self):

    print('')
    print('DAG: %s' % self.dag_name)
    print('')

    instances = {}
    for task in self.recipe['tasks']:
      function = next(iter(task.keys()))

      # count instance per task
      instances.setdefault(function, 0)
      instances[function] += 1

      print('airflow test "%s" %s_%d %s' %
            (self.dag_name, function, instances[function], str(date.today())))
      print('')
