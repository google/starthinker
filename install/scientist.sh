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


setup_scientist() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Data Scientist Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "StartThinker provides a Django powered browser UI for a single user."
  echo "The UI will also require a deployment of worker machines to run jobs remotely."
  echo ""
  echo "- All deployments are re-entrant, you can run them multiple times."
  echo "- Set up the UI first, you will probably leave the domain blank."
  echo "- Workers deployments will create cloud instances.  You can delete them and run the script again."
  echo "- A Cloud SQL Postgres Database will be created for the UI and workers." 
  echo "- You need to manually delete and/or secure worker instances and database."
  echo ""
  echo "To edit production deployment parameters use this script or from the command line edit:"
  echo "- ${STARTHINKER_CONFIG}"
  echo ""

  scientist_done=0
  scientist_options=("Deploy Single User UI" "Deploy Job Workers" "Check Job Workers" "Deploy User Credentials" "Change Domain" "Change Database" "Migrate Database")

  while (( !scientist_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Scientist Menu"
    echo "----------------------------------------------------------------------"
    echo ""

    PS3='Your Choice ( q = Quit ): '
    select scientist_option in "${scientist_options[@]}"; do
      case $REPLY in
        1) setup_appengine "Scientist"; break ;;
        2) setup_worker; break ;;
        3) check_worker; break ;;
        4) setup_ui_account; break ;;
        5) setup_domain; save_config; break ;;
        6) setup_database; save_config; break ;;
        7) migrate_database_enterprise; break ;;
        q) scientist_done=1; break;;
        *) echo "What's that?" ;;
      esac
    done
    echo ""
  done
}

if [ "$1" = "--instance" ];then
  shift;

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh
    source ${THIS_DIR}/install/worker.sh
    source ${THIS_DIR}/install/enterprise.sh

    setup_scientist;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi

fi

