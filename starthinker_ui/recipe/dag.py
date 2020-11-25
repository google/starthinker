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

from starthinker_ui.recipe.scripts import Script
from starthinker.script.parse import json_get_fields, dict_to_string, fields_to_string

AIRFLOW_TEMPLATE = """###########################################################################
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

\'\'\'
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer:

    From Open Source: pip install git+https://github.com/google/starthinker
    From Release: pip install starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

{title}

{description}

{instructions}

\'\'\'

from starthinker.airflow.factory import DAG_Factory

# If the recipe has "auth" set to "user" add user credentials:
#  1. Alternatively change all "user" values to "service" and set USER_CONN_ID = None.
#  2. Visit Airflow UI > Admin > Connections.
#  3. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
#    - Conn Type: Google Cloud Platform
#    - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
#    - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials
USER_CONN_ID = "starthinker_user"

# If the recipe has "auth" set to "service" add service credentials:
#  1. Visit Airflow UI > Admin > Connections.
#  2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
#    - Conn Type: Google Cloud Platform
#    - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
#    - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md
SERVICE_CONN_ID = "starthinker_service"

INPUTS = {inputs}

RECIPE = {recipe}

DAG_FACTORY = DAG_Factory('{dag}', RECIPE, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, SERVICE_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
"""


def script_to_dag(dag_name,
                  title,
                  description,
                  instructions,
                  script,
                  parameters={}):
  return AIRFLOW_TEMPLATE.format(**{
    'title':title,
    'description':description,
    'instructions':'\n'.join(instructions),
    'inputs':fields_to_string(
      json_get_fields(script),
      parameters
    ),
    'recipe':dict_to_string(
      script,
      skip=('fields',)
    ),
    'dag':dag_name
  })
