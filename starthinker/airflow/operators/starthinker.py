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
"""A set of operators to facilitate StarThinker integration with AirFlow.

The operators are meant to facilitate the reuse of StarThinker code inside an
AirFlow workflow, for example being able to reuse a StarThinker task without
having to specify the entire recipe.
"""

import importlib
import json

from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults


class StarThinkerTaskOperator(PythonOperator):
  """Runs a StarThinker task.

  This operator takes care of the creation of a valid StarThinker recipe JSON
  containing a single task and its parameters, as well as valid authentication
  information.

  Attributes:
    starthinker_task: A string identifying the StarThinker task to be called.
    starthinker_task_config: A dictionary containing the StarThinker task
      configuration. (templated) Can receive a json string representing the task
      configuration or reference to a template file. Template references are
      recognized by a string ending in '.json'.
    user_conn_id: The connection to use for user authentication.
    gcp_conn_id: The connection to use for service authentication.
    delegate_to: The account to impersonate, if any. Currently ignored.
  """

  template_fields = ['starthinker_task_config']
  template_ext = ['.json']
  ui_color = '#C4C4C4'

  @apply_defaults
  def __init__(self,
               starthinker_task,
               starthinker_task_config,
               user_conn_id=None,
               gcp_conn_id='google_cloud_default',
               delegate_to=None,
               *args,
               **kwargs):
    # Generate the correct callable for the task, based on the assumption that
    # StarThinker tasks are located under plugins/starthinker/task
    starthinker_callable = getattr(
        importlib.import_module('starthinker.task.%s.run' % starthinker_task),
        starthinker_task)

    super(StarThinkerTaskOperator, self).__init__(
        python_callable=starthinker_callable, *args, **kwargs)
    self.starthinker_task = starthinker_task
    self.starthinker_task_config = starthinker_task_config
    self.user_conn_id = user_conn_id
    self.gcp_conn_id = gcp_conn_id
    self.delegate_to = delegate_to

    # A baseline recipe that will have only one task
    self.recipe = {
        'setup': {
            'auth': {
                'user': '',
                'service': ''
            }
        },
        'tasks': [{
            starthinker_task: starthinker_task_config
        }]
    }

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

    self.log.info('The compiled recipe is the following:\n\n%s' %
                  json.dumps(self.recipe))

    self.op_kwargs = {'recipe': self.recipe, 'instance': 1}
