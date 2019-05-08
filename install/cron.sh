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

# Wrapper for crontab to execute python commands in the virtualenv.
# Assumes StarThinker directory structure. Not for use outside of StarThinker.
# Writes to a log file for easier debugging of cron, log file is overwritten each time to keep it small.
# Deploy cron using install/deploy.sh
#
# For Example: 0/3 * * * * /home/starthinker/install/cron recipe_log python starthinker_ui/manage.py recipe_log

THIS_DIR="$(dirname $0)/.."

source "${THIS_DIR}/starthinker_assets/production.sh"
$2 "${THIS_DIR}/${@:3}" 2>&1 | tee "${THIS_DIR}/starthinker_assets/cron/cron_$1.log"
deactivate
