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

if [ -z "${STARTHINKER_ROOT}" ]; then
  echo "Checking directory...."
  if [ -d "${PWD}/install" ]; then
    echo "Setting root path..."
    STARTHINKER_ROOT=$PWD
  else
    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the directory containing the starthinker directory."
    echo "Please change directories and try again."
    echo ""
  fi
fi

if [ ! -z "${STARTHINKER_ROOT}" ]; then
  echo "Setting development variables..."

  source "${STARTHINKER_ROOT}/starthinker_assets/production.sh";

  export STARTHINKER_SCALE=1;
  export STARTHINKER_DEVELOPMENT=1;

  export STARTHINKER_UI_DOMAIN="http://localhost:8000";
  export STARTHINKER_UI_SECRET="fordevelomentthisisokbutproductionneedsa50characterrandomsecret";
  export STARTHINKER_UI_DATABASE_ENGINE="django.db.backends.sqlite3";
  export STARTHINKER_UI_DATABASE_HOST="";
  export STARTHINKER_UI_DATABASE_PORT="";
  export STARTHINKER_UI_DATABASE_NAME="${STARTHINKER_ROOT}/starthinker_database/database.sqlite";
  export STARTHINKER_UI_DATABASE_USER="";
  export STARTHINKER_UI_DATABASE_PASSWORD="";

fi
