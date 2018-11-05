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
# just some utility functions and constants

# constants
THIS_DIR="$( cd "$( dirname "$_" )" && pwd )"
CRON_DIRECTORY="${HOME}/starthinker_cron"
CLIENT_CREDENTIALS="${HOME}/starthinker_client.json"
SERVICE_CREDENTIALS="${HOME}/starthinker_service.json"
USER_CREDENTIALS="${HOME}/starthinker_user.json"
DATA_FILE="${HOME}/starthinker_cloud.txt"
CLOUD_PROJECT_ID=""

# stop if any part fails
set -e 
set -o pipefail

# read stored data ( right now only project id )
if [ -e "${DATA_FILE}" ];then
  CLOUD_PROJECT_ID=`cat "${DATA_FILE}"`
fi

# read_multiline 
# $1 = termination parameter ( optional )
# $read_multiline_return = global result return
read_multiline() {
  read_multiline_return=""
  printf ">"
  while IFS= read -e -r read_multiline_line
  do
    read_multiline_return="${read_multiline_return}${read_multiline_line}"
    if [ "${1}" ];then
      if [[ $read_multiline_line = *"${1}"* ]]; then
        break
      else
        read_multiline_return="${read_multiline_return} "
      fi
    fi
  done
}


################################################################################
#
# set project - in case service account operates on foreign project, used in menu below

setup_project() {

  echo ""
  echo "----------------------------------------"
  echo "Set Cloud Project - ${CLOUD_PROJECT_ID}"
  echo ""

  read -p "Cloud Project ID ( blank to skip ): " cloud_id

  if [ "${cloud_id}" ];then
    CLOUD_PROJECT_ID="${cloud_id}"
    echo $CLOUD_PROJECT_ID > "${DATA_FILE}"
    echo "Project ID Saved"
  else
    echo "Project ID Unchanged"
  fi
}


################################################################################
#
# download credentials - called by menu below

setup_credentials() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Credentials"
  echo ""

  # client
  echo "Retrieve OAuth Client ID credentials from: https://console.cloud.google.com/apis/credentials"
  echo "Application type: Other"
  echo "Paste in your client credentials here: ( CTRL+D to skip )"

  read_multiline "}}"

  if [ "${read_multiline_return}" ];then
    printf "%s" "$read_multiline_return" > "${CLIENT_CREDENTIALS}"
  fi

  # service
  echo ""
  echo "Retrieve Service account key credentials from: https://console.cloud.google.com/apis/credentials"
  echo "Key type: JSON"
  echo "Paste in your service credentials: ( CTRL+D to skip )"

  read_multiline "}"

  if [ "${read_multiline_return}" ];then
    printf "%s" "$read_multiline_return" > "${SERVICE_CREDENTIALS}"
  fi

  # user
  echo ""
  echo "Using client credentials to get user credentials..."

  python auth/helper.py -c "${CLIENT_CREDENTIALS}" -u "${USER_CREDENTIALS}"

  echo "Credentials Setup Finished"
  echo ""
}


################################################################################
#
# install dependencies - called by menu below

install_dependencies() {
  echo ""
  sudo easy_install pip
  sudo pip install --upgrade --quiet -r requirements.txt
  echo ""
  echo "Dependency Install Finished"
  echo ""
}


################################################################################
#
# set up paths for execution of cron jobs and create a cron directory - called by menu

setup_paths() {
  echo ""
  export PYTHONPATH="${PYTHONPATH}:${THIS_DIR}"
  export STARTHINKER_PATH=${THIS_DIR}
  echo "Path Setup Finished"
  echo ""
}


################################################################################
#
# start or stop cron command in screen for easier debug - called by menu

start_cron() {

  echo ""

  mkdir -p "${CRON_DIRECTORY}"

  CRON_COMMAND="source "${THIS_DIR}/setup.sh"; python "${THIS_DIR}/cron/run.py" "${CRON_DIRECTORY}/" -p "${CLOUD_PROJECT_ID}" -c "${CLIENT_CREDENTIALS}" -u "${USER_CREDENTIALS}" -s "${SERVICE_CREDENTIALS}" --verbose;"

  if ! screen -list | grep -q "starthinker"; then
    echo "Launching Screen Job"
    screen -dmS starthinker bash -c "${CRON_COMMAND}"
  else
    echo "Screen Job Exists"
  fi

  echo "Cron Setup Finished"
  echo ""
}

stop_cron() {

  echo ""

  if screen -list | grep -q "starthinker"; then
    screen -X -S "starthinker" quit
    echo "Cron Job Stopped"
  else
    echo "Cron Job Is Already Stopped"
  fi

  echo ""
}


################################################################################
#
# recipe functions for adding and removing recipes - called by menu below

list_recipes() {
  echo ""

  for entry in "${CRON_DIRECTORY}"/*.json
  do
    echo "${entry##*/}"
  done

  echo ""
}

delete_recipe() {

  delete_recipe_done=0
  while (( !delete_recipe_done ))
  do
    echo ""
    echo "----------------------------------------"
    echo "Delete Recipe"
    echo ""
  
    files=("${CRON_DIRECTORY}"/*.json)
  
    PS3='Your Choice: '
    select file in "${files[@]##*/}" "Quit"
    do
     case ${file} in 
      "Quit") delete_recipe_done=1; break;;
      *)
        if [ "${file}" ]
        then
          echo ""
          echo "Removing: ${file}"
          rm "${CRON_DIRECTORY}/${file}"
          break
        else
          echo "Please choose a number from 1 to $((${#files[@]}+1))"
        fi;;
      esac
    done
  done
}

run_recipe() {

  run_recipe_done=0
  while (( !run_recipe_done ))
  do
    echo ""
    echo "----------------------------------------"
    echo "Run Recipe"
    echo ""
  
    files=("${CRON_DIRECTORY}"/*.json)
  
    PS3='Your Choice: '
    select file in "${files[@]##*/}" "Quit"
    do
     case ${file} in 
      "Quit") run_recipe_done=1; break;;
      *)
        if [ "${file}" ]
        then
          echo ""
          source "${THIS_DIR}/setup.sh" 
          python "${THIS_DIR}/all/run.py" "${CRON_DIRECTORY}/${file}" -p "${CLOUD_PROJECT_ID}" -c "${CLIENT_CREDENTIALS}" -u "${USER_CREDENTIALS}" -s "${SERVICE_CREDENTIALS}" --verbose --force
          break
        else
          echo "Please choose a number from 1 to $((${#files[@]}+1))"
        fi;;
      esac
    done
  done
}


add_recipe() {
  echo ""
  echo "----------------------------------------"
  echo "Add Recipe"
  echo ""

  read -p "Name Of Recipe ( do not include .json ): " recipe_name

  echo ""

  if [ "${recipe_name}" ];then
    recipe_file="${CRON_DIRECTORY}/${recipe_name}.json"

    if [ -e "${recipe_file}" ];then
      echo "Error: ${recipe_file} Already Exists"
    else
      echo "Paste in your recipe json: ( CTRL+D after paste )"
      read_multiline ""
      if [ "${read_multiline_return}" ];then
        printf "%s" "$read_multiline_return" > "${recipe_file}"
        echo "${recipe_file} Created"
      else
        echo "Error: No JSON To Write"
      fi
    fi
  else
    echo "Error: No Recipe Name Given"
  fi

  echo ""
}


################################################################################
#
# instructions - technical description of what this script does

instructions() {
  echo ""
  echo "----------------------------------------"
  echo "StarThinker Instructions"
  echo ""
  echo "This script sets up a basic screen based cron job that will read recipes"
  echo "from a directory and execute them on the schedule defined in each file."
  echo ""
  echo "Quick Start:"
  echo "  1 - Choose Full Setup from the main menu and follow all instructions."
  echo "  2 - Choose Add Recipe from the main menu and add a recipe."
  echo ""
  echo "Effects Of This Script"
  echo "  1 - Files Created"
  echo "        ~/starthinker_client.json"
  echo "        ~/starthinker_service.json"
  echo "        ~/starthinker_user.json"
  echo "        ~/starthinker_cloud.txt"
  echo "        ~/starthinker_cron/*"
  echo "  2 - Processes Started"
  echo "        screen -S starthinker"
  echo ""
  echo "Cron Operation"
  echo "  1 - Long running screen job checks the cron directory every hour for json files."
  echo "  2 - If the json has an hour and day entry it is checked, otherwise the task is executed every hour."
  echo "  3 - The uploaded credentials are used to execute the recipe, even if the recipe has its own credentials."
  echo "  3 - To execute the recipe, the cron launches a new non-blocking process for the entire json using run/all.py."
  echo "  4 - Each all/run.py launches a blocking process for each task in the recipe."
  echo ""
  echo "Possible Optimizations"
  echo "  Memory - In setup.py there is a BUFFER_SCALE parameter, setting it to 1 maxes out memory per process at 1 about GB."
  echo "  Processes - Recipes run concurrently, for a large number of processes consider an instance with more memory."
  echo "  CPU - Most task execute work using cloud resources, memory is more important than CPUs."
  echo "  Disk - 99% of tasks do not use disk, our goal is 100%." 
  echo "  Caching - Setting up a disk cache for memory may prevent many memory limit failures."
  echo "  Scaling - To scale to a larger instance, create an image of this one, then launch it as a larger one."
  echo "  Logs - To enable logging to a Google Cloud Storage Bucket, configure UI_PROJECT, UI_SERVICE, UI_BUCKET_LOG in setup.py."
  echo ""
  echo "Thank You For Using StarThinker"
  echo "  - Paul Kenjora @ Google gTech"
  echo "  - Mauricio Desiderio @ Google gTech"
  echo ""
}


################################################################################
#
# main - root menu of all actions

echo ""
echo "Welcome To StarThinker ( Google gTech )"
echo ""
echo "This utility will help you set up and manage long running recipes."
echo "If this is your first time running this script, select Full Setup."
echo ""

setup_paths;

main_done=0
options=("Full Setup" "Install Dependencies" "Set Cloud Project" "Set Credentials" "Start Cron" "Stop Cron" "List Recipes" "Add Recipe" "Run Recipe" "Delete Recipe" "Instructions" "Quit")

while (( !main_done ))
do
  echo "----------------------------------------------------------------------"
  echo "Main Menu"
  echo ""

  PS3='Your Choice: '
  select option in "${options[@]}"; do
    case $REPLY in
      1) install_dependencies; setup_project; setup_credentials; start_cron; break ;;
      2) install_dependencies; break ;;
      3) setup_project; break ;;
      4) setup_credentials; break ;;
      5) start_cron; break ;;
      6) stop_cron; break ;;
      7) list_recipes; break ;;
      8) add_recipe; break ;;
      9) run_recipe; break ;;
      10) delete_recipe; break ;;
      11) instructions; break ;;
      12) main_done=1; break;;
      *) echo "What's that?" ;;
    esac
  done
done
