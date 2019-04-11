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


################################################################################
#
# start or stop cron command in screen for easier debug - called by menu
#
make_cron() {
  mkdir -p "${STARTHINKER_CRON}"
}


################################################################################
#
# start or stop cron command in screen for easier debug - called by menu
#
start_cron() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo "Start Cron"
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "This will start a screen process running in the background to run recipes."
  echo "The recipe folder is $STARTHINKER_CRON.  The cron job will run once per hour."
  echo "It will check if {{ "setup":"day":{...}, "hour":{...}}} is set and current."
  echo "It uses the timezone specified in the recipe to determine the proper hour."
  echo ""
  echo "To check if the screen job is running run 'screen -ls' from command line."
  echo "You should see a job with the label xxxxxx.starthinker (Detached)."
  echo "Detached is OK, to learn about screen type 'man screen'."
  echo ""

  make_cron;

  CRON_COMMAND="source ${STARTHINKER_ENV}/bin/activate; python "${THIS_DIR}/starthinker/cron/run.py" "${STARTHINKER_CRON}/" -p "${STARTHINKER_PROJECT}" -c "${STARTHINKER_CLIENT}" -u "${STARTHINKER_USER}" -s "${STARTHINKER_SERVICE}" --verbose;"

  if ! screen -list | grep -q "starthinker"; then
    echo "Launching Screen Job"
   screen -dmS starthinker bash -c "$CRON_COMMAND"
   screen -ls
  else
    echo "Screen Job Exists"
  fi

  echo "Done"
  echo ""
}

stop_cron() {

  echo ""

  make_cron;

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

  make_cron;

  for entry in "${STARTHINKER_CRON}"/*.json
  do
    echo "${entry##*/}"
  done

  echo ""
}

delete_recipe() {

  make_cron;

  delete_recipe_done=0
  while (( !delete_recipe_done ))
  do
    echo ""
    echo "----------------------------------------"
    echo "Delete Recipe"
    echo ""
  
    files=("${STARTHINKER_CRON}"/*.json)
  
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
          rm "${STARTHINKER_CRON}/${file}"
          break
        else
          echo "Please choose a number from 1 to $((${#files[@]}+1))"
        fi;;
      esac
    done
  done
}


run_recipe() {

  make_cron;

  run_recipe_done=0
  while (( !run_recipe_done ))
  do
    echo ""
    echo "----------------------------------------"
    echo "Run Recipe"
    echo ""
  
    files=("${STARTHINKER_CRON}"/*.json)
  
    PS3='Your Choice: '
    select file in "${files[@]##*/}" "Quit"
    do
     case ${file} in 
      "Quit") run_recipe_done=1; break;;
      *)
        if [ "${file}" ]
        then
          echo ""
          source ${STARTHINKER_ENV}/bin/activate;
          python "${STARTHINKER_CODE}/all/run.py" "${STARTHINKER_CRON}/${file}" -p "${STARTHINKER_PROJECT}" -c "${STARTHINKER_CLIENT}" -u "${STARTHINKER_USER}" -s "${STARTHINKER_SERVICE}" --force --verbose;
          deactivate;
          break
        else
          echo "Please choose a number from 1 to $((${#files[@]}+1))"
        fi;;
      esac
    done
  done
}


generate_recipe() {

  make_cron;

  generate_recipe_done=0
  while (( !generate_recipe_done ))
  do
    echo ""
    echo "----------------------------------------"
    echo "Add Recipe"
    echo ""

    files=("${THIS_DIR}"/starthinker/gtech/script_*.json)

    PS3='Your Recipe Choice: '
    select file in "${files[@]##*/}" "Quit"
    do
     case ${file} in
      "Quit") generate_recipe_done=1; break;;
      *)
        if [ "${file}" ]
        then
          echo ""
          read -p "Name Of Recipe ( do not include .json ): " recipe_name
          source ${STARTHINKER_ENV}/bin/activate;
          python "${THIS_DIR}/starthinker/script/run.py" "${THIS_DIR}/starthinker/gtech/${file}" "${STARTHINKER_CRON}/${recipe_name}.json"
          deactivate;
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
  echo "Paste Recipe"
  echo ""

  make_cron;

  read -p "Name Of Recipe ( do not include .json ): " recipe_name

  echo ""

  if [ "${recipe_name}" ];then
    recipe_file="${STARTHINKER_CRON}/${recipe_name}.json"

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

setup_scientist() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Data Scientist Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "This script will set up a cron job on this machine to execute recipes on a schedule."
  echo "Logging out of the machine will keep the jobs running, however if the machine goes to sleep, jobs will stop."
  echo ""
  echo "Cron Operation"
  echo "  1 - Long running screen job checks the $STARTHINKER_CRON directory every hour for recipe json files."
  echo "  2 - If the recipe has an hour and day entry it is checked, otherwise the recipe is executed every hour."
  echo "  3 - The uploaded credentials are used to execute the recipe, even if the recipe has its own credentials."
  echo "  4 - The all/run.py script will launch a process for each task in the recipe and wait for it to complete."
  echo ""
  echo "Files Created"
  echo "  - $STARTHINKER_CONFIG"
  echo "  - $STARTHINKER_ENV"
  echo "  - $STARTHINKER_CLIENT"
  echo "  - $STARTHINKER_SERVICE"
  echo "  - $STARTHINKER_USER"
  echo "  - $STARTHINKER_CRON"
  echo ""
  echo "Processes Started"
  echo "  - screen -S starthinker"
  echo ""
  echo "You can also upload recipes for exectution to:"
  echo "  - $STARTHINKER_CRON"
  echo ""

  scientist_done=0
  scientist_options=("Install ( All Steps )" "Change Project" "Change Credentials" "Change User" "Start Cron" "Stop Cron" "List Recipes" "Add Recipe" "Generate Recipe" "Run Recipe" "Delete Recipe" "Quit")
 
  while (( !scientist_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Data Scientist Menu"
    echo "----------------------------------------------------------------------"
    echo ""
 
    PS3='Your Choice: '
    select scientist_option in "${scientist_options[@]}"; do
      case $REPLY in
        1) install_virtualenv; install_requirements; setup_project "optional"; setup_credentials "optional"; setup_user; save_config; start_cron; break;;
        2) setup_project; save_config; break ;;
        3) setup_credentials; save_config; break ;;
        4) setup_user; save_config; break ;;
        5) start_cron; break ;;
        6) stop_cron; break ;;
        7) list_recipes; break ;;
        8) add_recipe; break ;;
        9) generate_recipe; break ;;
        10) run_recipe; break ;;
        11) delete_recipe; break ;;
        12) scientist_done=1; break;;
        *) echo "What's that?" ;;
      esac
    done
    echo ""
  done
}

if [ "$1" == '--instance' ];then
  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh

    setup_scientist;

  fi
fi
