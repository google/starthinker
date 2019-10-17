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


test_ui() {

  install_virtualenv; 
  install_requirements; 
  setup_project "optional"; 
  setup_credentials_service "optional"; 
  setup_credentials_commandline "optional"; 
  save_config;

  echo ""
  echo "----------------------------------------"
  echo "Load Development Settings - ${STARTHINKER_ROOT}/starthinker_assets/development.sh"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";

  echo ""
  echo "----------------------------------------"
  echo "Run UI Tests - python ${STARTHINKER_ROOT}/starthinker_ui/manage.py test"
  echo "----------------------------------------"
  echo ""

  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" test account -v 2;
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" test website -v 2;
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" test recipe -v 2;

  deactivate

  echo "Done"
  echo ""
}

test_tasks() {

  install_virtualenv; 
  install_requirements; 
  setup_project "optional"; 
  setup_credentials_service "optional"; 
  setup_credentials_commandline "optional"; 
  save_config;

  echo ""
  echo "----------------------------------------"
  echo "Load Development Settings - ${STARTHINKER_ROOT}/starthinker_assets/development.sh"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";

  echo ""
  echo "----------------------------------------"
  echo "Run Task Tests - python ${STARTHINKER_ROOT}/starthinker/test/helper.py"
  echo "----------------------------------------"
  echo ""

  python "${STARTHINKER_ROOT}/starthinker/test/helper.py";

  deactivate

  echo "Done"
  echo ""
}


launch_developer_ui() {

  install_virtualenv; 
  install_requirements; 
  setup_project "optional"; 
  setup_credentials_service "optional"; 
  setup_credentials_ui "optional"; 
  save_config;
  make_cron;

  echo ""
  echo "----------------------------------------"
  echo "Load Development Settings - ${STARTHINKER_ROOT}/starthinker_assets/development.sh"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";

  echo ""
  echo "----------------------------------------"
  echo "Configure Development Database - ${STARTHINKER_ROOT}/starthinker_database/database.sqlite"
  echo "----------------------------------------"
  echo ""

  mkdir -p "${STARTHINKER_ROOT}/starthinker_database/"
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" makemigrations;
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" migrate;

  echo "----------------------------------------"
  echo "Launch Developer UI - python ${STARTHINKER_ROOT}/starthinker_ui/manage.py runserver localhost:8000"
  echo "----------------------------------------"
  echo ""

  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" runserver localhost:8000;
  deactivate

  echo ""
  echo "Done"
  echo ""
}

launch_developer_worker() {
  options=$1

  echo "----------------------------------------"
  echo "Launch Developer Worker - python ${STARTHINKER_ROOT}/starthinker_ui/manage.py job_worker --verbose ${options}"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" job_worker --verbose ${options}
  deactivate

  echo ""
  echo "Done"
  echo ""
}


install_developer() {
  install_virtualenv; 
  install_requirements; 
  setup_project "optional"; 
  setup_credentials_service "optional"; 
  setup_credentials_commandline "optional"; 
  setup_credentials_user; 
  save_config;
  make_cron;
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
  echo "  - $STARTHINKER_CLIENT_INSTALLED"
  echo "  - $STARTHINKER_CLIENT_WEB"
  echo "  - $STARTHINKER_SERVICE"
  echo "  - $STARTHINKER_USER"
  echo "  - $STARTHINKER_ENV"
  echo "  - $STARTHINKER_ROOT/starthinker_database/database.sqlite"
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
  developer_options=("Install Developer StarThinker" "Launch Developer UI" "Developer Worker - Single" "Developer Worker - Peristent" "Test UI" "Test Tasks" "Quit")
 
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
        3) launch_developer_worker "--test"; break;;
        4) launch_developer_worker ""; break;;
        5) test_ui; break;;
        6) test_tasks; break;;
        7) developer_done=1; break;;
        *) echo "What's that?";;
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

    setup_developer;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi
fi
