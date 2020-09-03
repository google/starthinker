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

# Environment setup configuration
GCP_PROJECT_ID=cse-cloud-composer-test
ENVIRONMENT=dev
COMPOSER_NAME=starthinker-on-composer-${ENVIRONMENT}

STARTHINKER_SERVICE_ACCOUNT=starthinker-on-composer

SERVICE_CREDENTIALS_JSON_NAME=service.json
USER_CREDENTIALS_JSON_NAME=user.json

COMPOSER_INSTANCE_DATA_FOLDER=/home/airflow/gcs/data
COMPOSER_LOCATION=us-east1
COMPOSER_ZONE=${COMPOSER_LOCATION}-d
COMPOSER_PYTHON_VERSION=2
COMPOSER_NODE_COUNT=3

# Environment variables values
VAR_STARTHINKER_ROOT=/home/airflow/gcs/plugins
VAR_STARTHINKER_ZONE=${COMPOSER_ZONE}
VAR_STARTHINKER_PROJECT=${GCP_PROJECT_ID}
VAR_STARTHINKER_SERVICE=${COMPOSER_INSTANCE_DATA_FOLDER}/data/${SERVICE_CREDENTIALS_JSON_NAME}

# Find the path to the current script
THIS_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

status_update(){
    local message=$1
    echo ""
    echo "----------------------------------------"
    echo ${message}
    echo "----------------------------------------"
    echo ""
}

if [ -d "${THIS_DIR}/install" ]; then
  echo ""
  echo "StarThinker directory not found."
  echo "This utility must be run from the directory containing the starthinker directory."
  echo "Please change directories and try again."
  echo ""

fi

status_update "Working from ${THIS_DIR}"

# Seetting the default project ID
status_update "Operating on environment ${COMPOSER_NAME} and GCP ID ${GCP_PROJECT_ID}"
gcloud config set project ${GCP_PROJECT_ID}

# Create the user credentials
status_update "Creating user credentials"
source ${THIS_DIR}/install/config.sh
install_virtualenv
install_requirements
save_config
source ${THIS_DIR}/starthinker_assets/development.sh
setup_credentials_commandline
touch ${THIS_DIR}/starthinker_assets/user.json
setup_credentials_user
deactivate
rm -R -f ${THIS_DIR}/starthinker_assets/config.sh
rm -R -f ${THIS_DIR}/starthinker_assets/client_installed.json

status_update "NOTE: The operations that follow do not require imput and wil take ~1-2 hour(s) to complete. Go get a coffee!"

# Enabling the necessary GCP APIs
status_update "Enabling the necessary GCP APIs"
gcloud services enable \
doubleclickbidmanager.googleapis.com \
dfareporting.googleapis.com \
doubleclicksearch.googleapis.com \
sheets.googleapis.com

# Create the composer environment
status_update "Creating the composer environment ${COMPOSER_NAME} in ${COMPOSER_ZONE}"
gcloud composer environments create ${COMPOSER_NAME} \
    --location=${COMPOSER_LOCATION} \
    --zone=${COMPOSER_ZONE} \
    --python-version=${COMPOSER_PYTHON_VERSION} \
    --node-count=${COMPOSER_NODE_COUNT}

# Get the GCS bucket information
COMPOSER_GCS_BUCKET=$(gcloud composer environments describe ${COMPOSER_NAME} --location ${COMPOSER_LOCATION} | grep 'dagGcsPrefix' | grep -Eo "\S+/")
echo "Storage bucket is ${COMPOSER_GCS_BUCKET}"
COMPOSER_GCS_BUCKET_DATA_FOLDER=${COMPOSER_GCS_BUCKET}data
echo "Data folder is ${COMPOSER_GCS_BUCKET_DATA_FOLDER}"
COMPOSER_GCS_BUCKET_PLUGINS_FOLDER=${COMPOSER_GCS_BUCKET}plugins
echo "Data folder is ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}"

# Set-up a StarThinker service account
status_update "Setting up the StarThinker service account (${STARTHINKER_SERVICE_ACCOUNT})"
gcloud alpha iam service-accounts create ${STARTHINKER_SERVICE_ACCOUNT} \
--display-name="StarThinker on Composer (Service Account)" \
--description="This service account is used by the StarThinker on Composer environment."
gcloud projects add-iam-policy-binding ${GCP_PROJECT_ID} \
--member=serviceAccount:${STARTHINKER_SERVICE_ACCOUNT}@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
--role='roles/editor'

# Store the StarThinker Service Account credentials in the cloud bucket
status_update "Creating service account keys and storing them in the Composer environment"
gcloud iam service-accounts keys create ${THIS_DIR}/starthinker_assets/${SERVICE_CREDENTIALS_JSON_NAME} \
--iam-account=${STARTHINKER_SERVICE_ACCOUNT}@${GCP_PROJECT_ID}.iam.gserviceaccount.com \
--key-file-type=json
gsutil cp ${THIS_DIR}/starthinker_assets/${SERVICE_CREDENTIALS_JSON_NAME} ${COMPOSER_GCS_BUCKET_DATA_FOLDER}
rm -f ${THIS_DIR}/starthinker_assets/${SERVICE_CREDENTIALS_JSON_NAME}

# Store the StarThinker User credentials in the cloud bucket
gsutil cp starthinker_assets/user.json ${COMPOSER_GCS_BUCKET_DATA_FOLDER}
rm -R -f ${THIS_DIR}/starthinker_assets/user.json

# Install PyPi packages from file and configure environment variables
status_update "Installing pypi packages from requirements.txt and setting up environment variables"

# Clean up requirements.txt: lowercase and remove comments
sed -e "/#/d; s/./\L&/g" \
${THIS_DIR}/starthinker/requirements.txt > /tmp/requirements.txt
echo "----------------------------------------"
cat /tmp/requirements.txt
echo ""
echo "----------------------------------------"

# Install requirements and clean up
gcloud composer environments update ${COMPOSER_NAME} \
    --location ${COMPOSER_LOCATION} \
    --update-pypi-packages-from-file=/tmp/requirements.txt
 rm -f /tmp/requirements.txt

# Set-up environment variables
status_update "Setting up StarThinker environment variables"
gcloud composer environments update ${COMPOSER_NAME} \
    --location ${COMPOSER_LOCATION} \
    --update-env-variables=\
STARTHINKER_ROOT=${VAR_STARTHINKER_ROOT},\
STARTHINKER_ZONE=${VAR_STARTHINKER_ZONE},\
STARTHINKER_PROJECT=${VAR_STARTHINKER_PROJECT},\
STARTHINKER_SERVICE=${VAR_STARTHINKER_SERVICE}

status_update "Creating StarThinker connections"
gcloud composer environments run ${COMPOSER_NAME} \
    --location ${COMPOSER_LOCATION} connections -- --add \
    --conn_id=starthinker_service --conn_type=google_cloud_platform \
    --conn_extra <<EXTRA "{\"extra__google_cloud_platform__project\": \"${GCP_PROJECT_ID}\",
\"extra__google_cloud_platform__key_path\": \"${COMPOSER_INSTANCE_DATA_FOLDER}/data/${SERVICE_CREDENTIALS_JSON_NAME}\"}"
EXTRA
gcloud composer environments run ${COMPOSER_NAME} \
    --location ${COMPOSER_LOCATION} connections -- --add \
    --conn_id=starthinker_user --conn_type=google_cloud_platform \
    --conn_extra <<EXTRA "{\"extra__google_cloud_platform__project\": \"${GCP_PROJECT_ID}\",
\"extra__google_cloud_platform__key_path\": \"${COMPOSER_INSTANCE_DATA_FOLDER}/data/${USER_CREDENTIALS_JSON_NAME}\",
\"extra__google_cloud_platform__scope\": \"https://www.googleapis.com/auth/bigquery,https://www.googleapis.com/auth/cloud-platform\"}"
EXTRA
echo "Done"

status_update "Copying StarThinker code to ${COMPOSER_GCS_BUCKET}/plugins"
# Clean up *.pyc files before uploading to the GCS bucket
find ${THIS_DIR}/starthinker -type f -name '*.pyc' -delete
gsutil -m cp ${THIS_DIR}/starthinker/__init__.py ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker/__init__.py
gsutil -m cp ${THIS_DIR}/starthinker/config.py ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker/config.py
gsutil -m cp -r ${THIS_DIR}/starthinker/script ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker
gsutil -m cp -r ${THIS_DIR}/starthinker/task ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker
gsutil -m cp -r ${THIS_DIR}/starthinker/util ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}/starthinker
gsutil -m cp -r ${THIS_DIR}/starthinker_airflow/starthinker ${COMPOSER_GCS_BUCKET_PLUGINS_FOLDER}