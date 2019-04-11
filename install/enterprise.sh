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


setup_sql() {
  echo ""
  echo "----------------------------------------"
  echo "Set Up Cloud SQL Database"
  echo "----------------------------------------"
  echo ""

  gcloud sql instances create $STARTHINKER_UI_DATABASE_NAME --tier=db-n1-standard-2 --region=$STARTHINKER_REGION
  gcloud sql databases create $STARTHINKER_UI_DATABASE_NAME --instance=$STARTHINKER_UI_DATABASE_NAME 
  gcloud sql users create $STARTHINKER_UI_DATABASE_USER --host=% --instance=$STARTHINKER_UI_DATABASE_NAME --password=$STARTHINKER_UI_DATABASE_PASSWORD

  echo "Done"
  echo ""
}


start_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Start Cloud Proxy"
  echo "----------------------------------------"
  echo ""

  case "$OSTYPE" in
    linux*)   wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O $STARTHINKER_ASSETS/cloud_sql_proxy ;;
    darwin*)  curl -o $STARTHINKER_ASSETS/cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64 ;;
    win*)     echo "For $OSTYPE Visit: https://cloud.google.com/sql/docs/mysql/sql-proxy for instructions." ;;
    msys*)    echo "For $OSTYPE Visit: https://cloud.google.com/sql/docs/mysql/sql-proxy for instructons." ;;
    cygwin*)  echo "For $OSTYPE Visit: https://cloud.google.com/sql/docs/mysql/sql-proxy for instructons." ;;
    bsd*)     echo "For $OSTYPE Visit: https://cloud.google.com/sql/docs/mysql/sql-proxy for instructons." ;;
    solaris*) echo "For $OSTYPE Visit: https://cloud.google.com/sql/docs/mysql/sql-proxy for instructons." ;;
    *)        echo "For $OSTYPE Visit: https://cloud.google.com/sql/docs/mysql/sql-proxy for instructons." ;;
  esac
  chmod +x $STARTHINKER_ASSETS/cloud_sql_proxy;
  $STARTHINKER_ASSETS/cloud_sql_proxy -instances="$STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_DATABASE_NAME"=tcp:3306 -credential_file $STARTHINKER_SERVICE &

  echo "Done"
  echo ""
}


stop_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Stop Cloud Proxy"
  echo "----------------------------------------"
  echo ""

  kill -9 $(jobs -pr)

  echo "Done"
  echo ""
}


migrate_proxy_database() {
  echo ""
  echo "----------------------------------------"
  echo "Setup Database"
  echo "----------------------------------------"
  echo ""

  (
    start_proxy;
    source "${STARTHINKER_CONFIG}" --load;
    export STARTHINKER_UI_DATABASE_ENGINE="django.db.backends.mysql"
    export STARTHINKER_UI_DATABASE_HOST="127.0.0.1"
    export STARTHINKER_UI_DATABASE_PORT="3306"
    export STARTHINKER_UI_DATABASE_NAME="$STARTHINKER_UI_DATABASE_NAME"
    export STARTHINKER_UI_DATABASE_USER="$STARTHINKER_UI_DATABASE_USER"
    export STARTHINKER_UI_DATABASE_PASSWORD="$STARTHINKER_UI_DATABASE_PASSWORD"
    python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" makemigrations;
    python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" migrate;
    deactivate
    stop_proxy;
  )

  echo "Done"
  echo ""
}


deploy_appengine() {
  echo ""
  echo "----------------------------------------"
  echo "Deploy AppEngine"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_CONFIG}" --load;
  python starthinker_ui/recipe/scripts.py
  pip install -t lib -r requirements.txt --quiet
  gcloud app deploy app.yaml --stop-previous-version
  deactivate

  echo "Done"
  echo ""
}


configure_yaml() {
  yaml_Target=$1

  echo ""
  echo "----------------------------------------"
  echo "Configure StarThinker App"
  echo "----------------------------------------"
  echo ""
  echo "Copy settings from $STARTHINKER_CONFIG and adjust for App Engine deployment."
  echo ""

  appengine_client=$(cat "$STARTHINKER_CLIENT" | tr '\n' ' ')
  appengine_service=$(cat "$STARTHINKER_SERVICE" | tr '\n' ' ')

  appengine_recipe_project="${STARTHINKER_RECIPE_PROJECT:-$STARTHINKER_PROJECT}"
  appengine_recipe_service="${STARTHINKER_RECIPE_SERVICE:-$STARTHINKER_SERVICE}"
  appengine_recipe_service=$(cat "$appengine_recipe_service" | tr '\n' ' ')

  if [ "$yaml_Target" == "app" ]; then
    appengine_development="0"
    appengine_domain="https://$STARTHINKER_PROJECT.appspot.com"
    appengine_database_engine="django.db.backends.mysql"
    appengine_database_host="/cloudsql/$STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_DATABASE_NAME"
    appengine_database_port=""
  else
    appengine_development="1"
    appengine_domain="http://localhost:8080"
    appengine_database_engine="django.db.backends.mysql"
    appengine_database_host="127.0.0.1"
    appengine_database_port="3306"
  fi

  bash -c "cat > $STARTHINKER_ROOT/$yaml_Target.yaml" << EOL
runtime: python27
api_version: 1
threadsafe: yes

handlers:
- url: .*
  script: starthinker_ui.ui.wsgi.application

libraries:
- name: django
  version: 1.11
- name: MySQLdb
  version: 1.2.5
- name: ssl
  version: latest

skip_files:
- ^(.*/)?.*~$
- ^(.*/)?.*\.pyc$
- ^(.*/)?\..*$
- ^starthinker_assets/.*$
- ^.git/.*$

env_variables:
  STARTHINKER_SCALE: '1'
  STARTHINKER_WORKERS: '$STARTHINKER_WORKERS'
  STARTHINKER_MANAGERS: '$STARTHINKER_MANAGERS'
  STARTHINKER_PROJECT: '$STARTHINKER_PROJECT'
  STARTHINKER_ZONE: '$STARTHINKER_ZONE'
  STARTHINKER_TOPIC: '$STARTHINKER_TOPIC'
  STARTHINKER_CLIENT: '$appengine_client'
  STARTHINKER_SERVICE: '$appengine_service'
  STARTHINKER_DEVELOPMENT: '$appengine_development'
  STARTHINKER_UI_DOMAIN: '$appengine_domain' 
  STARTHINKER_UI_SECRET: '$STARTHINKER_UI_SECRET'
  STARTHINKER_UI_DATABASE_ENGINE: '$appengine_database_engine'
  STARTHINKER_UI_DATABASE_HOST: '$appengine_database_host'
  STARTHINKER_UI_DATABASE_PORT: '$appengine_database_port'
  STARTHINKER_UI_DATABASE_NAME: "$STARTHINKER_UI_DATABASE_NAME"
  STARTHINKER_UI_DATABASE_USER: "$STARTHINKER_UI_DATABASE_USER"
  STARTHINKER_UI_DATABASE_PASSWORD: "$STARTHINKER_UI_DATABASE_PASSWORD"
  STARTHINKER_RECIPE_PROJECT: '$appengine_recipe_project'
  STARTHINKER_RECIPE_SERVICE: '$appengine_recipe_service'
EOL

  echo "Done"
  echo ""
}


setup_appengine() {

  echo ""
  echo "----------------------------------------"
  echo "Setup UI Instance On App Engine"
  echo "----------------------------------------"
  echo "This will create a StarThinker UI instances in Google Cloud project $STARTHINKER_PROJECT."
  echo ""
  read -p "Do you wish to proceed (y/n)? " -n 1 -r
  echo ""
  echo ""
  
  setup_project "optional";
  setup_credentials "optional";
  setup_domain "optional";
  setup_database "optional" "optional" "optional";
  save_config;

  install_virtualenv;
  install_requirements;
  setup_sql;
  migrate_proxy_database; 
  configure_yaml "app"; 
  deploy_appengine; 

  echo "Done"
  echo ""
}


test_appengine() {
  echo ""
  echo "----------------------------------------"
  echo "Deploying Test Server Using test.yaml"
  echo "----------------------------------------"
  echo ""
  echo "Configuring and running: dev_appserver.py test.yaml" 
  echo ""

  configure_yaml "test"; 

  (
    start_proxy;
    source "${STARTHINKER_CONFIG}" --load;
    dev_appserver.py test.yaml 
    deactivate
    stop_proxy;
  )

  echo "Done"
  echo ""
}

setup_enterprise() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Enterprise Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "StartThinker provides a Django powered Browser UI for multi user enterprise teams."
  echo "The UI works best with a Worker Setup and Docker Build. We suggest running those as well."
  echo ""
  echo "------------------------------------------------------------------------------"
  echo "This script will set up a public HTTPS server on an linux Instance or App Engine."
  echo "For instances you must enable the HTTP/HTTPS ports and add firewall restrictions on your own."
  echo ""
  echo ""

  enterprise_done=0
  enterprise_options=("Deploy UI On App Engine ( All Steps )" "Deploy UI On Linux Instance ( All Steps )" "Deploy Workers ( All Steps )" "Change Domain ( Requires UI Re-Deploy )" "Change Project ( Requires UI And Worker Re-Deploy )" "Change Credentials ( Requires UI And Worker Re-Deply )" "Change Database ( Requires UI And Worker Re-Deply )" "Test User" "Test App Engine Deployment" "Docker Image Build ( Will Run Jobs On Current Code )" "Quit")

  while (( !enterprise_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Enterprise Menu"
    echo "----------------------------------------------------------------------"
    echo ""

    PS3='Your Choice: '
    select enterprise_option in "${enterprise_options[@]}"; do
      case $REPLY in
        1) setup_appengine; break ;;
        2) setup_linux; break ;;
        3) setup_worker; break ;;
        4) setup_domain; save_config; break ;;
        5) setup_project; save_config; break ;;
        6) setup_credentials; save_config; break ;;
        7) setup_database; save_config; break ;;
        8) setup_user; break ;;
        9) test_appengine; break ;;
        10) build_docker; break ;;
        11) enterprise_done=1; break;;
        *) echo "What's that?" ;;
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
    source ${THIS_DIR}/install/worker.sh
    source ${THIS_DIR}/install/alternate.sh

    setup_enterprise;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the directory containing the starthinker directory."
    echo "Please change directories and try again."
    echo ""

  fi

fi

