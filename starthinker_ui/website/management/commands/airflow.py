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

import os
import json
from random import choice

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker_ui.recipe.scripts import Script
from starthinker.script.parse import json_get_fields


AIRFLOW_TEMPLATE = '''###########################################################################
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

\'\'\'
%s

%s

%s

\'\'\'

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = %s

TASKS = %s

DAG_FACTORY = DAG_Factory('%s', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
'''


class Command(BaseCommand):
  help = 'Generate Templates For Airflow'

  def handle(self, *args, **kwargs):
     
    for script in Script.get_scripts():
      if script.get_open_source():

        inputs = '{'

        for field in json_get_fields(script.get_tasks()):

          if field['kind'] in ('string', 'email', 'text'):
            value = '"%s"' % field.get('default', '')
          elif field['kind'] in ('integer', 'boolean'):
            value = field.get('default', 'None')
          elif field['kind'] in ('choice', 'integer_list', 'string_list'):
            value = field.get('default', '[]')
          elif field['kind'] in ('json'):
            value = field.get('default', '{}')
          elif field['kind'] == 'timezone':
            value = field.get('default', 'America/Phoenix')
            field['description'] = '%s https://github.com/google/starthinker/blob/master/starthinker_ui/ui/timezones.py' % field.get('description', '')
          else:
            raise NotImplementedError("%s is not a suported field type" % field)

          if 'description' in field:
            inputs += '\n  "%s":%s, # %s' % (field['name'], value, field['description'])
          else:
            inputs += '\n  "%s":%s,' % (field['name'], value)

        inputs += '\n}'

        print('Writing: %s_dag.py' % script.get_tag())

        with open('%s/starthinker_airflow/dags/%s_dag.py' % (settings.UI_ROOT, script.get_tag()), 'w') as dag_file:
          dag_file.write(AIRFLOW_TEMPLATE % (
            script.get_name(),
            script.get_description(),
            '\n'.join(script.get_instructions()),
            inputs, 
            json.dumps(script.get_tasks(), indent=2), 
            script.get_tag())
          )
