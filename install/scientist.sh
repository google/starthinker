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


start_cron() {

  echo ""
  echo "----------------------------------------"
  echo "Add Tasks To CronTab - crontab -l"
  echo "----------------------------------------"
  echo ""

  echo "* * * * * command to be executed"
  echo "- - - - -"
  echo "| | | | |"
  echo "| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)"
  echo "| | | ------- Month (1 - 12)"
  echo "| | --------- Day of month (1 - 31)"
  echo "| ----------- Hour (0 - 23)"
  echo "------------- Minute (0 - 59)"
  echo ""

  ( echo "" ) | crontab -

  if [ "${STARTHINKER_CRON}" ]; then
    (crontab -l ; echo "30 * * * * ${STARTHINKER_ROOT}/install/cron_recipe.sh ${STARTHINKER_ROOT}" ) | crontab -
  fi

  echo "Done"
  echo ""
}


stop_cron() {

  echo ""
  echo "----------------------------------------"
  echo "Clear All Tasks In CronTab - crontab -l"
  echo "----------------------------------------"
  echo ""

  ( echo "" ) | crontab -

  echo "Done"
  echo ""
}


list_recipes() {

  make_cron;

  echo ""
  echo "----------------------------------------"
  echo "List Recipes - ${STARTHINKER_CRON}"
  echo "----------------------------------------"
  echo ""

  for entry in "${STARTHINKER_CRON}"/*.json
  do
    echo "${entry##*/}"
  done

  echo "Done"
  echo ""
}


delete_recipe() {

  make_cron;

  delete_recipe_done=0
  while (( !delete_recipe_done ))
  do
    echo ""
    echo "----------------------------------------"
    echo "Delete Recipe - ${STARTHINKER_CRON}"
    echo "----------------------------------------"
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
    echo "----------------------------------------"
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
          python "${STARTHINKER_ROOT}/starthinker/all/run.py" "${STARTHINKER_CRON}/${file}" -p "${STARTHINKER_PROJECT}" -c "${STARTHINKER_CLIENT_INSTALLED}" -u "${STARTHINKER_USER}" -s "${STARTHINKER_SERVICE}" --force --verbose;
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
    echo "----------------------------------------"
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

  make_cron;

  echo ""
  echo "----------------------------------------"
  echo "Paste Recipe"
  echo "----------------------------------------"
  echo ""

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


install_scientist() {
  install_virtualenv;
  install_requirements;

  setup_project "optional";
  setup_credentials_service "optional";
  setup_credentials_commandline "optional";
  setup_credentials_user "optional";
  save_config;

  make_cron;
  start_cron;
}


setup_scientist() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Data Scientist Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "This script will set up a cron on this machine to execute recipes on a schedule."
  echo "Recipes are placed in a folder where the cron job will find and execute them once an hour."
  echo "Recipe credentials are ignored, all recipes are run with credentials set up using this script."
  echo ""
  echo "After running this script you can see and edit recipes using this menu or the command line:"
  echo " - $STARTHINKER_CRON"
  echo ""
  echo "Each run will store a log of the last execution in:"
  echo " - $STARTHINKER_CRON/cron_run.log"
  echo ""
  echo "You can see the scheduled tasks using:"
  echo " - crontab -l"
  echo ""

  scientist_done=0
  scientist_options=("Install Data Scientist StarThinker" "Start Cron" "Stop Cron" "List Recipes" "Add Recipe" "Generate Recipe" "Run Recipe" "Delete Recipe" "Quit")
 
  while (( !scientist_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Data Scientist Menu"
    echo "----------------------------------------------------------------------"
    echo ""
 
    PS3='Your Choice: '
    select scientist_option in "${scientist_options[@]}"; do
      case $REPLY in
        1) install_scientist; break;;
        2) start_cron; break ;;
        3) stop_cron; break ;;
        4) list_recipes; break ;;
        5) add_recipe; break ;;
        6) generate_recipe; break ;;
        7) run_recipe; break ;;
        8) delete_recipe; break ;;
        9) scientist_done=1; break;;
        *) echo "What's that?" ;;
      esac
    done
    echo ""
  done
}


if [ "$1" == '--instance' ];then
  shift

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh

    setup_scientist;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi
fi
