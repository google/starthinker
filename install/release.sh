#!/bin bash

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

# Push StarThinker code to PyPi and AppEngine.

if [ -d "${PWD}/install" ]; then
  THIS_DIR=$PWD

  echo ""
  echo "StarThinker Deployment ( Google gTech )"
  echo ""
  echo "This utility will help you deploy StarThinker to AppEngine and PyPi."
  echo ""

  if [ ! -z "${BASH}" ]; then

    read -p "Is the version in setup.py up to date (y/n)? " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then

      source ${THIS_DIR}/install/config.sh;
      source ${THIS_DIR}/install/worker.sh;
      source ${THIS_DIR}/install/developer.sh;
      source ${THIS_DIR}/install/enterprise.sh;

      source ${THIS_DIR}/starthinker_assets/production.sh

      generate_assets;
      setup_worker;
      setup_appengine;
      deploy_pypi --production;

    fi

  else

    echo ""
    echo "This script requires a bash shell."
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
