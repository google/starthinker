#!/bin/sh

###########################################################################
#
#  Copyright 2018 Google Inc.
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


################################################################################
#
# install dependencies


sudo easy_install pip
sudo pip install --upgrade --quiet -r requirements.txt
echo "Dependency Install Finished"
echo ""


################################################################################
#
# set up paths for execution of cron jobs
# create a cron directory


THIS_DIR="$( cd "$( dirname "$_" )" && pwd )"
export PYTHONPATH="${PYTHONPATH}:${THIS_DIR}"
export STARTHINKER_PATH=${THIS_DIR}
echo "Path Setup Finished"
echo ""


################################################################################
#
# run cron command in screen for easier debug


CRON_COMMAND="source ${THIS_DIR}/setup.sh; python ${THIS_DIR}/cron/run.py --path ${THIS_DIR}/project/cron/ --verbose;"
if ! screen -list | grep -q "starthinker"; then
  echo "Launching Screen Job"
  screen -dmS starthinker bash -c "${CRON_COMMAND}"
else
  echo "Screen Job Exists"
fi


echo ""
echo "Install Done, Cron Is Running"
echo ""
echo "The Install Script Can Be Run Multiple Times To Fix The Setup."
echo ""
echo "Add JSON Recipes To Be Run by Cron To: ${THIS_DIR}/project/cron/"
echo ""
echo "Confirm Screen Cron Is Running ( you will see starthinker listed ): screen -ls"
echo ""
echo "View Screen Cron ( exit safely using CTRL+A CTRL+D ): screen -r starthinker"
echo ""
echo "Stop Screen Cron: screen -S starthinker -X quit"
echo ""
