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
PythonOperators.  In future, as AirFlow matures and becomes more reliable,
some handlers will migrate from StarThinker tasks to native AirFlow calls.

Any StarThinker task immediately becomes available as an Airflow endpoint using
this code. The DAG ID will be set to the the path of the JSON template with non
alphanumeric characters set to '.', to mimic python dot notation.

"""


from datetime import timedelta, datetime, date
from importlib import import_module
from random import randint

from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from starthinker.util.configuration import Configuration
from starthinker.util.configuration import execute
from starthinker.util.recipe import json_set_fields

CONNECTION_SERVICE = "starthinker_service"
CONNECTION_USER = "starthinker_user"


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
    from starthinker.airflow.factory import DAG_Factory
    dag = DAG_Factory([StarThinker recipe JSON]).generate()
    ```

  """

  def __init__(self, _dag_name, _script, _script_parameters=None):
    self.dag_name = _dag_name
    self.recipe = _script
    self.dag = None

    if _script_parameters:
      json_set_fields(self.recipe, _script_parameters)

    self.recipe.setdefault('setup', {}).setdefault('auth', {})

    # If user credentials given in recipe, skip load from connection
    if self.recipe['setup']['auth'].get('user'):
      print('Loaded User Credentials From: RECIPE JSON')

    # If not given in recipe, try "user" auth information from connection
    else:
      try:
        user_connection_extra = BaseHook.get_connection(CONNECTION_USER).extra_dejson
        if user_connection_extra['extra__google_cloud_platform__key_path']:
          self.recipe['setup']['auth']['user'] = user_connection_extra[
            'extra__google_cloud_platform__key_path']
          print('Loaded User Credentials From: %s, Keyfile Path' % CONNECTION_USER)
        elif user_connection_extra['extra__google_cloud_platform__keyfile_dict']:
          self.recipe['setup']['auth']['user'] = user_connection_extra[
            'extra__google_cloud_platform__keyfile_dict']
          print('Loaded User Credentials From: %s, Keyfile JSON ' % CONNECTION_USER)
      except Exception as e:
        pass

    # If service credentials given in recipe, skip load from connection
    if self.recipe['setup']['auth'].get('service'):
      print('Loaded Service Credentials From RECIPE JSON')
    # If not given in recipe, try "service" auth information from connection
    else:
      try:
        service_connection_extra = BaseHook.get_connection(CONNECTION_SERVICE).extra_dejson
        if service_connection_extra['extra__google_cloud_platform__key_path']:
          self.recipe['setup']['auth']['service'] = service_connection_extra[
            'extra__google_cloud_platform__key_path']
          print('Loaded Service Credentials From: %s, Keyfile Path' % CONNECTION_SERVICE)
        elif service_connection_extra[
          'extra__google_cloud_platform__keyfile_dict']:
          self.recipe['setup']['auth']['service'] = service_connection_extra[
            'extra__google_cloud_platform__keyfile_dict']
          print('Loaded Service Credentials From: %s, Keyfile JSON' % CONNECTION_SERVICE)
      except Exception as e:
        pass

    # If project id given in recipe, skip load from connection
    if self.recipe['setup'].get('project'):
      print('Loaded Project ID From: RECIPE JSON')
    # If not given in recipe, try project id fetch from connections
    else:
      # check user
      try:
        user_connection_extra = BaseHook.get_connection(CONNECTION_USER).extra_dejson
        self.recipe['setup']['project'] = user_connection_extra.get('extra__google_cloud_platform__project')
      except: pass

      if self.recipe['setup'].get('project'):
        print('Loaded Project ID From: %s, Project Id' % CONNECTION_USER)
      else:
        # check service
        try:

          service_connection_extra = BaseHook.get_connection(CONNECTION_SERVICE).extra_dejson
          self.recipe['setup']['project'] = service_connection_extra.get('extra__google_cloud_platform__project')

          # check service json
          if self.recipe['setup'].get('project'):
            print('Loaded Project ID From: %s, Project Id' % CONNECTION_SERVICE)
          else:
            self.recipe['setup']['project'] = json.loads(
              service_connection_extra['extra__google_cloud_platform__keyfile_dict']
            )['project_id']
            print('Loaded Project ID From: %s, Keyfile JSON' % CONNECTION_SERVICE)

        except: pass


  def python_task(self, function, instance, task):
    print('STARTHINKER TASK:', function, instance)

    PythonOperator(
        task_id='%s_%d' % (function, instance),
        python_callable=getattr(
            import_module('starthinker.task.%s.run' % function), function),
        op_kwargs={
            'config': Configuration(recipe=self.recipe),
            'task': task
        },
        dag=self.dag)

    return self


  def airflow_task(self, task, instance, parameters):
    print('STARTHINKER AIRFLOW TASK:', task, instance)

    def airflow_import_unroll(definition):
      return next(iter([i for i in definition.items() if i[0] != '__comment__']))

    af_path, af_module = airflow_import_unroll(parameters)
    af_module, af_operator = airflow_import_unroll(af_module)
    af_operator, af_parameters = airflow_import_unroll(af_operator)

    operator = getattr(import_module('%s.%s.%s' % (task, af_path, af_module)), af_operator)

    af_parameters['dag'] = self.dag
    af_parameters['task_id'] = '%s_%d' % (task, instance)

    operator(**af_parameters)

    return self


  def airflow_start(self):
    return datetime.now(self.recipe.get('setup', {}).get('timezone')) - timedelta(days=7)


  def airflow_schedule(self):
    recipe_day = self.recipe.get('setup', {}).get('day', [])
    recipe_hour = [str(h) for h in self.recipe.get('setup', {}).get('hour', [])]

    airflow_schedule = None
    if recipe_day or recipe_hour:
      airflow_schedule = '{minutes} {hours} {day_of_month} {month} {day_of_week}'.format(**{
        'minutes':randint(0, 15),
        'hours':','.join(recipe_hour) or '*',
        'day_of_month':'*',
        'month':'*',
        'day_of_week':','.join(recipe_day) or '*'
      })

    return airflow_schedule

  def generate(self):
    print('STARTHINKER DAG:', self.dag_name)

    self.dag = DAG(
        dag_id=self.dag_name,
        default_args={
            'owner': 'airflow',
            'start_date': self.airflow_start()
        },
        schedule_interval=self.airflow_schedule(),
        catchup=False)

    for instance, task in enumerate(self.recipe['tasks'], 1):
      function = next(iter(task.keys()))

      # if airflow function ( product )
      if function == 'airflow':
        self.airflow_task(function, instance, task[function])

      # if airflow function ( local )
      elif function == 'starthinker.airflow':
        self.airflow_task(function, instance, task[function])

      # if native python operator
      else:
        self.python_task(function, instance, task[function])

    return self.dag


  def print_commandline(self):

    print('')
    print('STARTHINKER COMMANDLINE: %s' % self.dag_name)
    print('')

    for instance, task in enumerate(self.recipe['tasks'], 1):
      function = next(iter(task.keys()))
      print('airflow tasks test "%s" %s_%d %s' %
            (self.dag_name, function, instance, str(date.today())))
    print('')
