#!/bin/bash
  
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

# Executes the starthinker cron command using virtualenv ( called from crontab -l )
# For Example: 0/3 * * * * /home/starthinker/install/cron_recipe.sh /home/starthinker

starthinker_ROOT=$1

source "${starthinker_ROOT}/starthinker_assets/production.sh"
python "${starthinker_ROOT}/starthinker/cron/run.py" ${STARTHINKER_CRON} -c ${STARTHINKER_CLIENT_INSTALLED} -u ${STARTHINKER_USER} -s ${STARTHINKER_SERVICE} -p ${STARTHINKER_PROJECT} 2>&1 | tee "${STARTHINKER_CRON}/cron_recipe.log"
deactivate
