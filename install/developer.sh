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


setup_developer_database() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Local UI And Database"
  echo "----------------------------------------"
  echo ""
  echo "Activating: $STARTHINKER_ASSETS/database.sqlite"
  echo ""

  STARTHINKER_DEVELOPMENT=1
  STARTHINKER_UI_DATABASE_ENGINE="django.db.backends.sqlite3"
  STARTHINKER_UI_DATABASE_HOST=""
  STARTHINKER_UI_DATABASE_PORT=""
  STARTHINKER_UI_DATABASE_NAME="$STARTHINKER_ASSETS/database.sqlite"
  STARTHINKER_UI_DATABASE_USER=""
  STARTHINKER_UI_DATABASE_PASSWORD=""

  echo "Done"
  echo ""
}


setup_developer() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Developer Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Configure a basic development environment for StarThinker."
  echo ""
  echo "This script may create or modify:"
  echo "  - $STARTHINKER_CONFIG"
  echo "  - $STARTHINKER_ENV"
  echo "  - $STARTHINKER_CLIENT"
  echo "  - $STARTHINKER_SERVICE"
  echo "  - $STARTHINKER_USER"
  echo "  - $STARTHINKER_ASSETS/database.sqlite"
  echo ""
  echo "After running this script once, activate StarThinker virtual environment and config using:"
  echo " - source $STARTHINKER_CONFIG"
  echo ""
  echo "After activating StarThinker run the sample code:"
  echo " - python all/run.py gtech/say_hello.json -u \$STARTHINKER_USER -s \$STARTHINKER_SERVICE -p \$STARTHINKER_PROJECT"
  echo ""
  echo "After activating StarThinker run the UI:"
  echo " - python starthinker_ui/manage.py runserver localhost:8000"
  echo ""
  echo "Deactivate the virtual environment:"
  echo " - deactivate"
  echo ""

  developer_done=0
  developer_options=("Install ( All Steps )" "Change Project" "Change Credentials" "Change User" "Setup Local UI + Database" "Re-Load Configuration" "Quit")
 
  while (( !developer_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Developer Menu"
    echo "----------------------------------------------------------------------"
    echo ""
   
    PS3='Your Choice: '
    select developer_option in "${developer_options[@]}"; do
      case $REPLY in
        1) install_virtualenv; install_requirements; setup_project "optional"; setup_credentials "optional"; setup_user; setup_developer_database; save_config; migrate_database; break;;
        2) setup_project; save_config; break;;
        3) setup_credentials; save_config; break;;
        4) setup_user; save_config; break;;
        5) setup_developer_database; save_config; migrate_database; break;;
        6) load_config; break;;
        7) developer_done=1; break;;
        *) echo "What's that?";;
      esac
    done
    echo ""
  done
}

if [ "$1" == '--instance' ];then
  shift;

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh

    setup_developer;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the directory containing the starthinker directory."
    echo "Please change directories and try again."
    echo ""

  fi
fi
