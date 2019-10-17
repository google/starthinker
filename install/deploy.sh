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


if [ -d "${PWD}/install" ]; then
  THIS_DIR=$PWD

  source ${THIS_DIR}/install/config.sh;
  source ${THIS_DIR}/install/worker.sh;
  source ${THIS_DIR}/install/developer.sh;
  source ${THIS_DIR}/install/scientist.sh;
  source ${THIS_DIR}/install/enterprise.sh;
  source ${THIS_DIR}/install/composer.sh;

  echo ""
  echo "Welcome To StarThinker ( Google gTech )"
  echo ""
  echo "This utility will help you set up and manage long running recipes."
  echo "If this is your first time running this script, select Full Setup."
  echo ""
  
  if [ ! -z "${BASH}" ]; then

    echo ""
    echo "------------------------------------------------------------------------------"
    echo "This is a reference implementation only and not warrantied by Google."
    echo ""
  
    read -p "Do you acknowledge and wish to proceed (y/n)? " -n 1 -r
    echo ""
    echo ""
  
    if [[ $REPLY =~ ^[Yy]$ ]]; then

      echo "----------------------------------------------------------------------"
      echo "gTech StarThinker"
      echo "----------------------------------------------------------------------"
      echo ""
      echo "Developer Menu"
      echo "Sets up local environment to run StarThinker recipes from the command line. Most basic setup."
      echo ""
      echo ""
      echo "Data Scientist Menu"
      echo "Sets up local job that will run recipes on a schedule persistently.  For long running custom jobs."
      echo ""
      echo ""
      echo "Enterprise Setup Menu"
      echo "Sets up a Google App Engine Instance web UI for multiple users and disctributed jobs.  Highly scalable team wide deployment."
      echo ""
      echo ""
    
      main_done=0
      main_options=("Developer Menu" "Data Scientist Menu" "Enterprise Menu" "Composer Menu" "Change Project" "Change Service Credentials" "Change User Credentials" "Change UI Credentials" "Quit")
    
      while (( !main_done ))
      do
        echo "----------------------------------------------------------------------"
        echo "Main Menu"
        echo "----------------------------------------------------------------------"
        echo ""
      
        PS3='Your Choice: '
        select main_option in "${main_options[@]}"; do
          case $REPLY in
            1) setup_developer; break ;;
            2) setup_scientist; break ;;
            3) setup_enterprise; break ;;
            4) setup_composer; break ;;
            5) setup_project; save_config; break ;;
            6) setup_credentials_service; save_config; break ;;
            7) setup_credentials_commandline; setup_credentials_user; save_config; break ;;
            8) setup_credentials_ui; save_config; break ;;
            9) main_done=1; break;;
            *) echo "What's that?" ;;
          esac
        done
        echo ""
      done
    
    fi

  else

    echo ""
    echo "This script require a bash shell."
    echo "Run: /bin/bash"
    echo "Then run this script again." 
  echo ""
  
  fi

else

  echo ""
  echo "Directory starthinker not found."
  echo "This utility must be run from the directory containing the starthinker directory."
  echo "Please change directories and try again."
  echo ""

fi
