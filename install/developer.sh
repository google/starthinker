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


launch_developer_ui() {

  echo ""
  echo "----------------------------------------"
  echo "Load Development Settings - ${STARTHINKER_ROOT}/starthinker_assets/development.sh"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";

  echo ""
  echo "----------------------------------------"
  echo "Configure Development Database - ${STARTHINKER_ROOT}/starthinker_assets/database.sqlite"
  echo "----------------------------------------"
  echo ""

  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" makemigrations;
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" migrate;

  echo "----------------------------------------"
  echo "Launch Developer UI python ${STARTHINKER_ROOT}/starthinker_ui/manage.py runserver localhost:8000"
  echo "----------------------------------------"
  echo ""

  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" runserver localhost:8000;

  deactivate

  echo "Done"
  echo ""
}


install_developer() {
  install_virtualenv; 
  setup_project "optional"; 
  setup_credentials "optional"; 
  setup_user; 
  save_config;
}


setup_developer() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Developer Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "This script manages environmental settings for StarThinker. you can edit them"
  echo "manually from the command line or use this script to manage them. All settings are in:"
  echo " - $STARTHINKER_CONFIG"
  echo ""
  echo "This script or you may create or modify:"
  echo "  - $STARTHINKER_CONFIG"
  echo "  - $STARTHINKER_ENV"
  echo "  - $STARTHINKER_CLIENT"
  echo "  - $STARTHINKER_SERVICE"
  echo "  - $STARTHINKER_USER"
  echo "  - $STARTHINKER_ROOT/starthinker_assets/database.sqlite"
  echo ""
  echo "After running this script once, activate StarThinker development settings from the command line:"
  echo " - source $STARTHINKER_ROOT/starthinker_assets/development.sh"
  echo ""
  echo "Or activate production settings from the command line:"
  echo " - source $STARTHINKER_CONFIG"
  echo ""
  echo "After activating StarThinker run the sample code:"
  echo " - python starthinker/all/run.py starthinker/gtech/say_hello.json -u \$STARTHINKER_USER -s \$STARTHINKER_SERVICE -p \$STARTHINKER_PROJECT"
  echo ""
  echo "After activating StarThinker run the UI from the menu below or from the command line:"
  echo " - source $STARTHINKER_ROOT/starthinker_assets/developmnet.sh"
  echo " - python starthinker_ui/manage.py runserver localhost:8000"
  echo ""
  echo "Deactivate the virtual environment:"
  echo " - deactivate"
  echo ""

  developer_done=0
  developer_options=("Install StarThinker" "Launch Developer UI" "Reset Root Path" "Quit")
 
  while (( !developer_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Developer Menu"
    echo "----------------------------------------------------------------------"
    echo ""
   
    PS3='Your Choice: '
    select developer_option in "${developer_options[@]}"; do
      case $REPLY in
        1) install_developer; break;;
        2) launch_developer_ui; break;;
        3) save_config; break;;
        4) developer_done=1; break;;
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
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi
fi
