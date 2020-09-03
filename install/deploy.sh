#!/bin/bash

###########################################################################
#
#  Copyright 2020 Google LLC
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

    if [[ $REPLY =~ ^[Yy]$ ]]; then

      source ${THIS_DIR}/install/config.sh;
      source ${THIS_DIR}/install/worker.sh;
      source ${THIS_DIR}/install/developer.sh;
      source ${THIS_DIR}/install/enterprise.sh;
      source ${THIS_DIR}/install/composer.sh;

      echo ""
      echo "----------------------------------------------------------------------"
      echo "gTech StarThinker"
      echo "----------------------------------------------------------------------"
      echo ""
      echo "Developer Menu"
      echo "Sets up local environment to run StarThinker recipes from the command line. Most basic setup."
      echo ""
      echo ""
      echo "Enterprise Setup Menu"
      echo "Sets up a Google App Engine Instance web UI for multiple users and distributed jobs.  Highly scalable team wide deployment."
      echo ""
      echo ""
      echo "Composer Setup Menu"
      echo "Sets up a Google Cloud Composer Instance for distributed jobs.  Alternate scalable team wide deployment."
      echo ""
      echo ""
      echo "Change Analytics Token"
      echo "The UI deployment will track anonymous usage data, to disable, adjust the Google Analytics Token."
      echo ""

      main_done=0
      main_options=("Developer Menu" "Enterprise Menu" "Composer Setup Menu" "Change gCloud User" "Change gCloud Project" "Change Service Credentials" "Change User Credentials" "Change UI Credentials" "Change Analytics Token")

      while (( !main_done ))
      do
        echo "----------------------------------------------------------------------"
        echo "Main Menu"
        echo "----------------------------------------------------------------------"
        echo ""

        PS3='Your Choice ( q = Quit ): '
        select main_option in "${main_options[@]}"; do
          case $REPLY in
            1) setup_developer; break ;;
            2) setup_enterprise; break ;;
            3) setup_composer; break ;;
            4) setup_gcloud "forced"; save_config; break ;;
            5) setup_project "forced"; save_config; break ;;
            6) setup_credentials_service "forced"; save_config; break ;;
            7) setup_credentials_commandline "forced"; setup_credentials_user "forced"; save_config; break ;;
            8) setup_credentials_ui "forced"; save_config; break ;;
            9) setup_analytics "forced"; save_config; break ;;
            q) main_done=1; break;;
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
