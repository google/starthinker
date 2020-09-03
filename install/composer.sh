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

COMPOSER_NAME="starthinker-on-composer"
COMPOSER_SERVICE_ACCOUNT=starthinker-on-composer
COMPOSER_INSTANCE_DATA_FOLDER=/home/airflow/gcs/data
COMPOSER_PYTHON_VERSION=3
COMPOSER_NODE_COUNT=3

composer_activate() {

  echo ""
  echo "----------------------------------------"
  echo "Enabling GCP APIs"
  echo "----------------------------------------"
  echo ""
  echo " - doubleclickbidmanager.googleapis.com"
  echo " - dfareporting.googleapis.com"
  echo " - doubleclicksearch.googleapis.com"
  echo " - sheets.googleapis.com"
  echo " - "
  echo ""

  gcloud services enable doubleclickbidmanager.googleapis.com dfareporting.googleapis.com doubleclicksearch.googleapis.com sheets.googleapis.com

  echo ""
  echo "----------------------------------------"
  echo "Creating The Composer Environment ${COMPOSER_NAME} In ${STARTHINKER_ZONE}"
  echo "----------------------------------------"
  echo ""
  echo " This may take an hour or two, go get some coffee...."
  echo ""

  gcloud composer environments create ${COMPOSER_NAME} --location=${STARTHINKER_REGION} --zone=${STARTHINKER_ZONE} --python-version=${COMPOSER_PYTHON_VERSION} --node-count=${COMPOSER_NODE_COUNT}
}

composer_credentials() {

  install_virtualenv;
  install_requirements;

  setup_credentials_service;
  setup_credentials_commandline;
  setup_credentials_user;
  save_config;

  echo ""
  echo "----------------------------------------"
  echo "Install Kebernetes"
  echo "----------------------------------------"
  echo ""
  gcloud components install kubectl

  echo ""
  echo "----------------------------------------"
  echo "Uploading Credentials To Composer"
  echo "----------------------------------------"
  echo ""

  # Get the GCS bucket information
  COMPOSER_GCS_BUCKET=$(gcloud composer environments describe ${COMPOSER_NAME} --location ${STARTHINKER_REGION} | grep 'dagGcsPrefix' | grep -Eo "\S+/")
  echo "Storage bucket is ${COMPOSER_GCS_BUCKET}"
  COMPOSER_GCS_BUCKET_DATA_FOLDER=${COMPOSER_GCS_BUCKET}data
  echo "Data folder is ${COMPOSER_GCS_BUCKET_DATA_FOLDER}"
  COMPOSER_GCS_BUCKET_PLUGINS_FOLDER=${COMPOSER_GCS_BUCKET}plugins
  echo "Data folder is ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}"

  # Store the StarThinker Service credentials in the cloud bucket
  gsutil cp ${THIS_DIR}/starthinker_assets/service.json ${COMPOSER_GCS_BUCKET_DATA_FOLDER}

  # Store the StarThinker User credentials in the cloud bucket
  gsutil cp starthinker_assets/user.json ${COMPOSER_GCS_BUCKET_DATA_FOLDER}
}

composer_environment() {
  # Install PyPi packages from file and configure environment variables
  echo "Installing pypi packages from requirements.txt and setting up environment variables"

  # Clean up requirements.txt: lowercase and remove comments ( awk is more platform compatible because of lack of regexp )
  awk '!/^ *#/ && NF {print tolower($0)}' starthinker/requirements.txt > /tmp/requirements.txt

  echo "----------------------------------------"
  cat /tmp/requirements.txt
  echo ""
  echo "----------------------------------------"

  # Install requirements and clean up
  echo " gcloud composer environments update ${COMPOSER_NAME} --location ${STARTHINKER_REGION} --update-pypi-packages-from-file=/tmp/requirements.txt"

  gcloud composer environments update ${COMPOSER_NAME} --location ${STARTHINKER_REGION} --update-pypi-packages-from-file=/tmp/requirements.txt
  rm -f /tmp/requirements.txt

  # Set-up environment variables
  echo "Setting up StarThinker environment variables"
  gcloud composer environments update ${COMPOSER_NAME} --location ${STARTHINKER_REGION} --update-env-variables=\
  STARTHINKER_ROOT=${STARTHINKER_ROOT},\
  STARTHINKER_ZONE=${STARTHINKER_ZONE},\
  STARTHINKER_PROJECT=${STARTHINKER_PROJECT},\
  STARTHINKER_SERVICE=${STARTHINKER_SERVICE}

  echo "Creating StarThinker connections"
  gcloud composer environments run ${COMPOSER_NAME} \
      --location ${STARTHINKER_REGION} connections -- --add \
      --conn_id=starthinker_service --conn_type=google_cloud_platform \
      --conn_extra <<EXTRA "{\"extra__google_cloud_platform__project\": \"${STARTHINKER_PROJECT}\",
  \"extra__google_cloud_platform__key_path\": \"${COMPOSER_INSTANCE_DATA_FOLDER}/data/service.json\"}"
EXTRA

  gcloud composer environments run ${COMPOSER_NAME} \
      --location ${STARTHINKER_REGION} connections -- --add \
      --conn_id=starthinker_user --conn_type=google_cloud_platform \
      --conn_extra <<EXTRA "{\"extra__google_cloud_platform__project\": \"${STARTHINKER_PROJECT}\",
  \"extra__google_cloud_platform__key_path\": \"${COMPOSER_INSTANCE_DATA_FOLDER}/data/user.json\",
  \"extra__google_cloud_platform__scope\": \"https://www.googleapis.com/auth/bigquery,https://www.googleapis.com/auth/cloud-platform\"}"
EXTRA

  echo "Done"
}

composer_code() {
  echo "Copying StarThinker code to ${COMPOSER_GCS_BUCKET}/plugins"
  # Clean up *.pyc files before uploading to the GCS bucket
  find ${THIS_DIR}/starthinker -type f -name '*.pyc' -delete
  gsutil -m cp ${THIS_DIR}/starthinker/__init__.py ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker/__init__.py
  gsutil -m cp ${THIS_DIR}/starthinker/config.py ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker/config.py
  gsutil -m cp -r ${THIS_DIR}/starthinker/script ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker
  gsutil -m cp -r ${THIS_DIR}/starthinker/task ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker
  gsutil -m cp -r ${THIS_DIR}/starthinker/util ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker
  gsutil -m cp -r ${THIS_DIR}/starthinker_airflow ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}

  echo "Done"
}

composer_all() {
  composer_activate;
  composer_credentials;
  composer_code;
  composer_environment;
}

setup_composer() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Composer Setup"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "StartThinker provides a Cloud Composer integration for teams running Airflow."
  echo ""
  echo "- All deployments are re-entrant, you can run them multiple times."
  echo "- You can manage the credentials, code, and dags individually."
  echo "- Currently this deployment ONLY deploys one user credential."
  echo "- You need to manually delete and/or secure all Cloud Composer assets."
  echo ""
  echo "To edit deployment parameters use this script or from the command line edit:"
  echo "- ${STARTHINKER_CONFIG}"
  echo ""

  composer_done=0
  composer_options=("Deploy All" "Deploy Credentials" "Deploy Dags" "Deploy Code" "Deploy Environment")

  while (( !composer_done ))
  do
    echo "----------------------------------------------------------------------"
    echo "Cloud Composer Menu"
    echo "----------------------------------------------------------------------"
    echo ""

    PS3='Your Choice ( q = Quit ): '
    select composer_option in "${composer_options[@]}"; do
      case $REPLY in
        1) composer_all; break ;;
        2) composer_credentials; break ;;
        3) composer_dags; break ;;
        4) composer_code; break ;;
        5) composer_environment; break ;;
        q) composer_done=1; break;;
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

    setup_composer;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi

fi
