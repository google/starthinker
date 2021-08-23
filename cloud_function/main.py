###########################################################################
#
#  Copyright 2021 Google LLC
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

""" Typically called by Cloud Scheduler with recipe JSON payload.

  Sample JSON POST payload:
    {
      "setup":{
        "id":"", #string - Cloud Project ID for billing.
        "auth":{
          "service":{}, #dict - Optional Cloud Service JSON credentials when task uses service.
          "user":{} #dict - Optional Cloud User JSON credentials when task uses user.
        }
      },
      "tasks":[ # list of recipe tasks to execute, see StarThinker scripts for examples.
        { "hello":{
          "auth":"user", # not used in demo, for display purposes only.
          "say":"Hello World"
        }}
      ]
    }

  Documentation: https://github.com/google/starthinker/blob/master/tutorials/deploy_cloudfunction.md

"""

from starthinker.util.configuration import Configuration
from starthinker.util.configuration import execute

def run(request):
  recipe = request.get_json(force=True)
  execute(Configuration(recipe=recipe, verbose=True), recipe.get('tasks', []), force=True)
  return 'DONE'
