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


setup_sql() {
  echo ""
  echo "----------------------------------------"
  echo "Set Up Cloud SQL Database"
  echo "----------------------------------------"
  echo ""
  echo " - https://cloud.google.com/endpoints/docs/openapi/enable-api"
  echo " - https://cloud.google.com/sql/docs/mysql/create-instance"
  echo " - https://cloud.google.com/sdk/gcloud/reference/sql/databases/create"
  echo " - https://cloud.google.com/sdk/gcloud/reference/sql/users/create"
  echo ""

  gcloud services enable sqladmin.googleapis.com
  gcloud services enable sql-component.googleapis.com
  gcloud services enable serviceusage.googleapis.com

  values=$(gcloud sql instances list --filter="name=$STARTHINKER_UI_PRODUCTION_DATABASE_NAME" --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud sql instances create $STARTHINKER_UI_PRODUCTION_DATABASE_NAME --database-version=POSTGRES_9_6 --cpu=2 --memory=7680MiB --region=$STARTHINKER_REGION
  else
    echo "Instance already exists."
  fi

  values=$(gcloud sql databases list --instance=$STARTHINKER_UI_PRODUCTION_DATABASE_NAME --filter="name=$STARTHINKER_UI_PRODUCTION_DATABASE_NAME" --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud sql databases create $STARTHINKER_UI_PRODUCTION_DATABASE_NAME --instance=$STARTHINKER_UI_PRODUCTION_DATABASE_NAME
  else
    echo "Database already exists."
  fi

  gcloud sql users create $STARTHINKER_UI_PRODUCTION_DATABASE_USER --host=% --instance=$STARTHINKER_UI_PRODUCTION_DATABASE_NAME --password=$STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD

  echo "Done"
}


start_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Start Cloud Proxy"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy -instances=$STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_PRODUCTION_DATABASE_NAME=tcp:5432"
  echo " - https://cloud.google.com/sql/docs/mysql/connect-admin-proxy"
  echo ""

  "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy" -instances="$STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_PRODUCTION_DATABASE_NAME"=tcp:5432 &
  sleep 15

  echo "Done"
}


stop_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Stop Cloud Proxy - ${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy"
  echo "----------------------------------------"
  echo ""

  kill -9 $(jobs -p "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy")

  echo "Done"
}


migrate_database_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Migrate Database"
  echo "----------------------------------------"
  echo ""
  echo " - https://docs.djangoproject.com/en/4.0/topics/migrations/"
  echo ""

  start_proxy;

  export STARTHINKER_UI_DOMAIN="${STARTHINKER_UI_PRODUCTION_DOMAIN}";
  export STARTHINKER_UI_SECRET="${STARTHINKER_UI_PRODUCTION_SECRET}";
  export STARTHINKER_UI_DATABASE_ENGINE="${STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE}";
  export STARTHINKER_UI_DATABASE_HOST="${STARTHINKER_UI_PRODUCTION_DATABASE_HOST}";
  export STARTHINKER_UI_DATABASE_PORT="${STARTHINKER_UI_PRODUCTION_DATABASE_PORT}";
  export STARTHINKER_UI_DATABASE_NAME="${STARTHINKER_UI_PRODUCTION_DATABASE_NAME}";
  export STARTHINKER_UI_DATABASE_USER="${STARTHINKER_UI_PRODUCTION_DATABASE_USER}";
  export STARTHINKER_UI_DATABASE_PASSWORD="${STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD}";

  source "${STARTHINKER_ROOT}/starthinker_virtualenv/bin/activate"
  python3 "${STARTHINKER_ROOT}/starthinker_ui/manage.py" makemigrations;
  python3 "${STARTHINKER_ROOT}/starthinker_ui/manage.py" migrate;
  deactivate

  stop_proxy;

  echo "Done"
}


deploy_appengine() {
  echo ""
  echo "----------------------------------------"
  echo "Deploy AppEngine"
  echo "----------------------------------------"
  echo ""
  echo " - https://cloud.google.com/endpoints/docs/openapi/enable-api"
  echo " - https://cloud.google.com/build/docs/securing-builds/configure-access-for-cloud-build-service-account"
  echo " - https://cloud.google.com/sdk/gcloud/reference/app/create"
  echo " - https://cloud.google.com/sdk/gcloud/reference/app/deploy"
  echo ""

  gcloud services enable cloudbuild.googleapis.com
  gcloud services enable appengine.googleapis.com

  sleep 10

  gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_cloudbuild_email) \
    --role='roles/appengine.appAdmin'

  # create recipe scripts python file for App Engine ( buffers scripts avoiding complex disk lookup )
  source "${STARTHINKER_ROOT}/starthinker_assets/production.sh";
  python3 "${STARTHINKER_ROOT}/starthinker_ui/recipe/scripts.py";

  values=$(gcloud app describe --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud app create --region "${STARTHINKER_REGION}"
  fi

  gcloud app deploy $STARTHINKER_ROOT/app.yaml --stop-previous-version --service-account=$(get_service_email)
  gcloud app deploy $STARTHINKER_ROOT/cron.yaml --stop-previous-version --service-account=$(get_service_email)

  # delete the recipe scripts python file for App Engine ( easy to forget and waste time debugging )
  rm "${STARTHINKER_ROOT}/starthinker_ui/recipe/scripts_lookup.py"*

  deactivate

  echo "Done"
}


configure_yaml() {
  deploy_Type=$1

  echo ""
  echo "----------------------------------------"
  echo "Configure StarThinker App"
  echo "----------------------------------------"
  echo ""
  echo " - $STARTHINKER_CONFIG"
  echo " - https://cloud.google.com/appengine/docs/standard/python/config/appref"
  echo " - https://cloud.google.com/appengine/docs/standard/python3/runtime#python-3.7"
  echo ""

  appengine_client=$(cat "$STARTHINKER_CLIENT_WEB" | tr '\n' ' ')

  if [ -z "${STARTHINKER_UI_PRODUCTION_DOMAIN}" ]; then
    appengine_domain=$(gcloud app browse --no-launch-browser)
  else
    appengine_domain=$STARTHINKER_UI_PRODUCTION_DOMAIN;
  fi

  appengine_database_engine="${STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE}"
  appengine_database_host="/cloudsql/$STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_PRODUCTION_DATABASE_NAME"
  appengine_database_port="${STARTHINKER_UI_PRODUCTION_DATABASE_PORT}"

  bash -c "cat > $STARTHINKER_ROOT/app.yaml" << EOL
runtime: python37
env: standard
entrypoint: gunicorn -b :\$PORT starthinker_ui.ui.wsgi

instance_class: F4_HIGHMEM

runtime_config:
  python_version: 37

beta_settings:
  cloud_sql_instances: $STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_PRODUCTION_DATABASE_NAME

env_variables:
  STARTHINKER_SCALE: '1'
  STARTHINKER_DEVELOPMENT: '$STARTHINKER_DEVELOPMENT'
  STARTHINKER_WORKER_MAX: '$STARTHINKER_WORKER_MAX'
  STARTHINKER_WORKER_JOBS: '$STARTHINKER_WORKER_JOBS'
  STARTHINKER_ANALYTICS: '$STARTHINKER_ANALYTICS'
  STARTHINKER_PROJECT: '$STARTHINKER_PROJECT'
  STARTHINKER_ZONE: '$STARTHINKER_ZONE'
  STARTHINKER_CLIENT: '$appengine_client'
  STARTHINKER_SERVICE: 'DEFAULT'
  STARTHINKER_UI_DOMAIN: '$appengine_domain'
  STARTHINKER_UI_SECRET: '$STARTHINKER_UI_PRODUCTION_SECRET'
  STARTHINKER_UI_DATABASE_ENGINE: '$appengine_database_engine'
  STARTHINKER_UI_DATABASE_HOST: '$appengine_database_host'
  STARTHINKER_UI_DATABASE_PORT: '$appengine_database_port'
  STARTHINKER_UI_DATABASE_NAME: '$STARTHINKER_UI_PRODUCTION_DATABASE_NAME'
  STARTHINKER_UI_DATABASE_USER: '$STARTHINKER_UI_PRODUCTION_DATABASE_USER'
  STARTHINKER_UI_DATABASE_PASSWORD: '$STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD'

handlers:
  - url: /static
    static_dir: starthinker_ui/static
  - url: /.*
    secure: always
    redirect_http_response_code: 301
    script: auto
EOL

  echo "Done"
}


setup_appengine() {
  echo ""
  echo "----------------------------------------"
  echo "Setup Enterprise UI Instance On App Engine"
  echo "----------------------------------------"
  echo ""
  echo "This will create a StarThinker UI instance in Google Cloud project $STARTHINKER_PROJECT."
  echo ""

  setup_credentials_service;
  setup_database;
  save_config;

  gcloud services enable doubleclickbidmanager.googleapis.com
  gcloud services enable storage-api.googleapis.com
  gcloud services enable bigquery-json.googleapis.com
  gcloud services enable dfareporting.googleapis.com
  gcloud services enable drive.googleapis.com
  gcloud services enable sheets.googleapis.com
  gcloud services enable doubleclicksearch.googleapis.com
  gcloud services enable secretmanager.googleapis.com

  install_proxy; # first so it install dependencies
  install_virtualenv; # second because pip is here
  install_requirements; # second because pip is here

  setup_sql;
  migrate_database_proxy;

  setup_credentials_ui;
  save_config;

  generate_translations;

  configure_yaml $deploy_Type;

  deploy_appengine;

  echo ""
  echo "----------------------------------------"
  echo ""
  echo "Access Your StarThinker UI At: $(gcloud app browse --no-launch-browser)"
  echo ""


  if [[ !$STARTHINKER_GSUITE ]]; then
    echo ""
    echo "----------------------------------------"
    echo "The application may show a security warning: https://github.com/google/starthinker/raw/master/tutorials/images/verification.png"
    echo "The warning is only showed when logging in."
    echo "Bypass it by clicking Advnaced and Go To StarThinker."
    echo ""
    echo "To remove the above warning:"
    echo "  A. Verify your domian and switch to internal application."
    echo "  B. Enroll in gSuite and switch to internal application."
    echo "  C. Submit your application for verification to Google ( 6+ weeks )."
    echo ""
  fi

  echo ""
  echo "----------------------------------------"
  echo "HIGHY SUGGESTED IAP SECURITY: https://console.cloud.google.com/security/iap?project=$STARTHINKER_PROJECT"
  echo "This allows you to conrol access to the UI on a per user basis."
  echo " 1. Enable IAP."
  echo " 2. Add members with access to the role: Cloud IAP > IAP-secured Web App User"
  echo " 3. Or use a firewall: https://cloud.google.com/appengine/docs/standard/python/application-security"
  echo ""

  echo ""
  echo "Done"
}


migrate_database_enterprise() {
  echo ""
  echo "----------------------------------------"
  echo "Migrate Database To Latest Version"
  echo "----------------------------------------"
  echo ""

  setup_credentials_service;
  setup_database;
  save_config;

  install_proxy; # first so it install dependencies
  install_virtualenv; # second because pip is here

  install_requirements; # second because pip is here

  setup_sql;
  migrate_database_proxy;

  echo "Done"
  echo ""
}


setup_cloud_function() {

  gcloud services enable cloudbuild.googleapis.com
  gcloud services enable cloudfunctions.googleapis.com
  gcloud services enable cloudscheduler.googleapis.com
  gcloud services enable appengine.googleapis.com

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Cloud Function Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo " - A sample cloud scheduler job is deploying: https://console.cloud.google.com/cloudscheduler"
  echo " - It will run a simple hello world task: https://github.com/google/starthinker/tree/master/starthinker/task/hello"
  echo " - Invoke the hello world task using the parameters file: https://github.com/google/starthinker/blob/master/scripts/hello.json"
  echo " - Extend the sample with scripts from: https://github.com/google/starthinker/tree/master/scripts"
  echo ' - Convert a script to a recipe, replaces {"field":{...}} with values: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#run-a-script'
  echo " - If you need service cerdentials see: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md"
  echo " - If you need user cerdentials see: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials"
  echo " - A single cloud function can run all StarThinker recipes, simply pass a different JSON in the request."
  echo ""
  echo "Setting up cloud function..."
  echo ""

  service=$(get_service_email);

  gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role=roles/cloudfunctions.invoker

  # BUFFER_SCALE=1 minimizes memory ( should it be lower still )?
  gcloud alpha functions deploy starthinker --entry-point run --runtime python39 \
     --trigger-http \
     --security-level secure-always \
     --service-account "${service}" \
     --memory 4096MB \
     --source "$STARTHINKER_ROOT/cloud_function" \
     --set-env-vars "BUFFER_SCALE=1, UI_SERVICE=DEFAULT" \
     --timeout 540s --quiet

  echo ""
  echo "Deploying sample scheduled job..."
  echo ""

  # 0 3 * * * = 3 AM Daily (can be adjusted by user from UI)
  trigger=$(gcloud functions describe starthinker --format 'value(httpsTrigger.url)')
  gcloud scheduler jobs create http starthinker_sample --schedule "0 3 * * *" --uri "${trigger}" --http-method POST --message-body='{ "setup":{ "id":"${STARTHINKER_PROJECT}" }, "tasks":[ { "hello":{ "auth":"user", "say":"Hello World" }} ] }' --oidc-token-audience "${trigger}" --oidc-service-account-email "${service}" --time-zone "Etc/UTC" --location=$STARTHINKER_REGION

  echo ""
  echo "View the function at: https://pantheon.corp.google.com/functions/list"
  echo "Run the scheduled task at: https://console.cloud.google.com/cloudscheduler"
  echo "The function trigger URL is: ${trigger}"
}


setup_enterprise() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Enterprise Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "StartThinker provides a Django powered browser UI for multi user enterprise teams."
  echo "The UI will also require a deployment of worker machines to run jobs remotely."
  echo ""
  echo "- All deployments are re-entrant, you can run them multiple times."
  echo "- Set up the UI first, you will probably leave the domain blank."
  echo "- Workers deployments will create cloud instances.  You can delete them and run the script again."
  echo "- A Cloud SQL Postgres Database will be created for the UI and workers."
  echo "- You need to manually delete and/or secure worker instances and database."
  echo ""
  echo "To edit deployment parameters use this script or from the command line edit:"
  echo "- ${STARTHINKER_CONFIG}"
  echo ""

  enterprise_done=0
  enterprise_options=("Deploy UI & Workers" "Deploy UI" "Deploy Workers" "Change Domain" "Change Database" "Migrate Database" "Start Datbase Proxy")

  while (( !enterprise_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Enterprise Menu"
    echo "----------------------------------------------------------------------"
    echo ""

    PS3='Your Choice ( q = Quit ): '
    select enterprise_option in "${enterprise_options[@]}"; do
      case $REPLY in
        1) setup_worker; setup_appengine; break ;;
        2) setup_appengine; break ;;
        3) setup_worker; break ;;
        4) setup_domain; save_config; break ;;
        5) setup_database; save_config; break ;;
        6) migrate_database_enterprise; break ;;
        7) start_proxy; break ;;
        q) enterprise_done=1; break;;
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

    setup_enterprise;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi

fi
