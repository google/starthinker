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


################################################################################
#
# constats used by all the scripts
#
STARTHINKER_SCALE=1
STARTHINKER_DEVELOPMENT=0
STARTHINKER_GSUITE=1

STARTHINKER_WORKER_MAX=10
STARTHINKER_WORKER_INSTANCE="e2-highmem-4"
STARTHINKER_WORKER_JOBS=4

STARTHINKER_ANALYTICS="UA-167283455-2"

STARTHINKER_PROJECT=""
STARTHINKER_ZONE=""
STARTHINKER_DEVELOPER_TOKEN=""
STARTHINKER_API_KEY=""

STARTHINKER_UI_PRODUCTION_DOMAIN=""
STARTHINKER_UI_PRODUCTION_SECRET=""
STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE="django.db.backends.postgresql"
STARTHINKER_UI_PRODUCTION_DATABASE_HOST="127.0.0.1"
STARTHINKER_UI_PRODUCTION_DATABASE_PORT="5432"
STARTHINKER_UI_PRODUCTION_DATABASE_NAME="starthinker"
STARTHINKER_UI_PRODUCTION_DATABASE_USER="starthinker_user"
STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD="starthinker_password"

STARTHINKER_UI_DEVELOPMENT_DOMAIN="http://localhost:8000";
STARTHINKER_UI_DEVELOPMENT_SECRET="fordevelomentthisisokbutproductionneedsa50characterrandomsecret";
STARTHINKER_UI_DEVELOPMENT_DATABASE_ENGINE="django.db.backends.sqlite3";
STARTHINKER_UI_DEVELOPMENT_DATABASE_HOST="";
STARTHINKER_UI_DEVELOPMENT_DATABASE_PORT="";
STARTHINKER_UI_DEVELOPMENT_DATABASE_NAME="";
STARTHINKER_UI_DEVELOPMENT_DATABASE_USER="";
STARTHINKER_UI_DEVELOPMENT_DATABASE_PASSWORD="";

check_billing() {
  if [[ $(gcloud alpha billing projects describe "$STARTHINKER_PROJECT" --format='value(billingEnabled)') == "True" ]]; then
    STARTHINKER_BILLING=1
  else
    STARTHINKER_BILLING=0
  fi
}

check_gsuite() {
  if [[ $(curl -s -X GET https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="$(gcloud auth print-identity-token)") == *"\"hd\": "* ]]; then
    STARTHINKER_GSUITE=1
  else
    STARTHINKER_GSUITE=0
  fi
}

derive_config() {

  STARTHINKER_REGION=$(echo "$STARTHINKER_ZONE" | sed -e "s/\-[a-z]$//")

  STARTHINKER_ROOT="${THIS_DIR}"

  STARTHINKER_CLIENT_WEB="${THIS_DIR}/starthinker_assets/client_web.json"
  STARTHINKER_CLIENT_INSTALLED="${THIS_DIR}/starthinker_assets/client_installed.json"
  STARTHINKER_SERVICE="${THIS_DIR}/starthinker_assets/service.json"
  STARTHINKER_USER="${THIS_DIR}/starthinker_assets/user.json"
  STARTHINKER_CONFIG="${THIS_DIR}/starthinker_assets/config.sh"

  STARTHINKER_CRON="${THIS_DIR}/starthinker_cron"
  STARTHINKER_ENV="${THIS_DIR}/starthinker_virtualenv"

  if [ -z "${STARTHINKER_UI_PRODUCTION_SECRET}" ]; then
    STARTHINKER_UI_PRODUCTION_SECRET=$(openssl rand -base64 48)
  fi

  STARTHINKER_UI_DEVELOPMENT_DATABASE_NAME="${STARTHINKER_ROOT}/starthinker_assets/database.sqlite";

}


load_config() {
  echo ""
  echo "----------------------------------------"
  echo "Loading Configuration"
  echo "----------------------------------------"
  echo ""
  echo " - ${THIS_DIR}/starthinker_assets/config.sh"
  echo ""

  if [ -e "${THIS_DIR}/starthinker_assets/config.sh" ]; then
    source "${THIS_DIR}/starthinker_assets/config.sh";
  fi

  derive_config;

  echo "Done"
}


save_config() {

  derive_config;

  echo ""
  echo "----------------------------------------"
  echo "Saving Configuration"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_CONFIG}"
  echo ""

  echo "export STARTHINKER_SCALE=$STARTHINKER_SCALE;" > "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_DEVELOPMENT=$STARTHINKER_DEVELOPMENT;" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_WORKER_MAX=$STARTHINKER_WORKER_MAX;" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_WORKER_INSTANCE=\"$STARTHINKER_WORKER_INSTANCE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_WORKER_JOBS=$STARTHINKER_WORKER_JOBS;" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_ANALYTICS=\"$STARTHINKER_ANALYTICS\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_PROJECT=\"$STARTHINKER_PROJECT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ZONE=\"$STARTHINKER_ZONE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_DEVELOPER_TOKEN=\"$STARTHINKER_DEVELOPER_TOKEN\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_API_KEY=\"$STARTHINKER_API_KEY\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_ROOT=\"$STARTHINKER_ROOT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CLIENT_WEB=\"$STARTHINKER_CLIENT_WEB\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CLIENT_INSTALLED=\"$STARTHINKER_CLIENT_INSTALLED\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_SERVICE=\"$STARTHINKER_SERVICE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_USER=\"$STARTHINKER_USER\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CONFIG=\"$STARTHINKER_CONFIG\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CRON=\"$STARTHINKER_CRON\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ENV=\"$STARTHINKER_ENV\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_UI_PRODUCTION_DOMAIN=\"$STARTHINKER_UI_PRODUCTION_DOMAIN\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_SECRET=\"$STARTHINKER_UI_PRODUCTION_SECRET\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE=\"$STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_DATABASE_HOST=\"$STARTHINKER_UI_PRODUCTION_DATABASE_HOST\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_DATABASE_PORT=\"$STARTHINKER_UI_PRODUCTION_DATABASE_PORT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_DATABASE_NAME=\"$STARTHINKER_UI_PRODUCTION_DATABASE_NAME\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_DATABASE_USER=\"$STARTHINKER_UI_PRODUCTION_DATABASE_USER\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD=\"$STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_UI_DEVELOPMENT_DOMAIN=\"$STARTHINKER_UI_DEVELOPMENT_DOMAIN\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_SECRET=\"$STARTHINKER_UI_DEVELOPMENT_SECRET\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_DATABASE_ENGINE=\"$STARTHINKER_UI_DEVELOPMENT_DATABASE_ENGINE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_DATABASE_HOST=\"$STARTHINKER_UI_DEVELOPMENT_DATABASE_HOST\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_DATABASE_PORT=\"$STARTHINKER_UI_DEVELOPMENT_DATABASE_PORT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_DATABASE_NAME=\"$STARTHINKER_UI_DEVELOPMENT_DATABASE_NAME\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_DATABASE_USER=\"$STARTHINKER_UI_DEVELOPMENT_DATABASE_USER\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DEVELOPMENT_DATABASE_PASSWORD=\"$STARTHINKER_UI_DEVELOPMENT_DATABASE_PASSWORD\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "if [[ "\$PYTHONPATH" != *\"\${STARTHINKER_ROOT}\"* ]]; then" >> "${STARTHINKER_CONFIG}"
  echo "  export PYTHONPATH=\"\${PYTHONPATH}:\${STARTHINKER_ROOT}\"" >> "${STARTHINKER_CONFIG}"
  echo "fi" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "if [ -d \"\${STARTHINKER_ROOT}/starthinker_virtualenv\" ]; then" >> "${STARTHINKER_CONFIG}"
  echo "  source \"\${STARTHINKER_ROOT}/starthinker_virtualenv/bin/activate\";" >> "${STARTHINKER_CONFIG}"
  echo "fi" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "Done"
}


################################################################################
#
#  read multiline example
#
#  read_multiline "}}"
#  if [ "${read_multiline_return}" ];then
#    printf "%s" "$read_multiline_return" > "${STARTHINKER_CLIENT_WEB}"
#  fi
#
read_multiline() {
  read_multiline_return=""
  printf ">"
  while IFS= read -e -r read_multiline_line
  do
    read_multiline_return="${read_multiline_return}${read_multiline_line}"
    if [ "${1}" ];then
      if [[ $read_multiline_line = *"${1}"* ]]; then
        break
      else
        read_multiline_return="${read_multiline_return} "
      fi
    fi
  done
}


setup_gcloud() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set gCloud User"
  echo "----------------------------------------"
  echo ""
  echo "This command line is used to administer your Google Cloud Project."
  echo ""
  echo "CAUTION: THIS MUST BE SET TO A USER NOT A SERVICE."
  echo "  - Deploying App Engine instances requires gcloud to be administered by a user."
  echo "  - The user will have to have at least editor on the chosen Google Cloud Project."
  echo ""

  if [ "$(command -v gcloud)" == "" ]; then

    echo "Please install gcloud command using: https://cloud.google.com/sdk/install"
    echo "Then run the StarThinker deployment again."
    echo ""
    exit 1;

  else

    if [ "$forced" == "forced" ]; then

      echo "Changing gcloud account, please log in."
      gcloud auth login --no-launch-browser --brief
      echo ""

     else

       error=$(gcloud auth print-identity-token 2>&1 > /dev/null)

       if [[ ! -z $error ]]; then

         echo "No gcloud account detected, please log in."
         echo ""
         gcloud auth login --no-launch-browser --brief
         echo ""

       else

         account=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
         echo "Using gCloud Account: $account"
         echo ""

       fi
    fi
  fi
}


setup_database() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set Cloud Database Parameters"
  echo "----------------------------------------"
  echo ""

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_UI_PRODUCTION_DATABASE_NAME}" == "" ]; then
    read -p "Database Name - ${STARTHINKER_UI_PRODUCTION_DATABASE_NAME} ( blank to skip ): " database_name
    if [ "${database_name}" ]; then
      STARTHINKER_UI_PRODUCTION_DATABASE_NAME="${database_name}"
    else
      echo "Database Name Unchanged"
    fi
  else
    echo "Using Existing Database Name: ${STARTHINKER_UI_PRODUCTION_DATABASE_NAME}"
  fi

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_UI_PRODUCTION_DATABASE_USER}" == "" ]; then
    read -p "Database User - ${STARTHINKER_UI_PRODUCTION_DATABASE_USER} ( blank to skip ): " database_user
    if [ "${database_user}" ]; then
      STARTHINKER_UI_PRODUCTION_DATABASE_USER="${database_user}"
    else
      echo "Database User Unchanged"
    fi
  else
    echo "Using Existing Database User: ${STARTHINKER_UI_PRODUCTION_DATABASE_USER}"
  fi

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD}" == "" ]; then
    read -p "Database Password - ${STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD} ( blank to skip ): " database_password
    if [ "${database_password}" ]; then
      STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD="${database_password}"
    else
      echo "Database Password Unchanged"
    fi
  else
    echo "Using Existing Database Password: NOT SHOWN"
  fi
}


setup_analytics() {

  echo ""
  echo "----------------------------------------"
  echo "Set Analytics Tracking"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_ANALYTICS}"
  echo ""

  echo "All data collected is anonymous and never shared outside of the StarThinker team."
  echo "Leaving the tracking in place helps us continue supporting StarThinker by showing it is useful."
  echo "To opt out simply enter a blank or type in your own."
  echo ""

  read -p "Google Analytics Token ( blank to leave unchanged or OFF to remove): " analytics

  if [ "$analytics" == "OFF" ]; then
    STARTHINKER_ANALYTICS="";
  elif [ ! -z "${analytics}" ]; then
    STARTHINKER_ANALYTICS=$analytics;
  fi

}


setup_project() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set gCloud Project"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_PROJECT}"
  echo ""

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_PROJECT}" == "" ]; then

    echo "Retrieve Project ID from: https://console.cloud.google.com"
    echo ""
    echo "IMPORTANT SETUP NOTES"
    echo ""
    echo " * The Project ID is in a drop down at the top of your Google Cloud Console."
    echo " * Use the Project ID not the Name."
    echo " * Include the organization if it is part of the Project ID."
    echo ""

    read -p "Cloud Project ID ( blank to keep existing ): " cloud_id

    if [ "${cloud_id}" ]; then
      STARTHINKER_PROJECT="${cloud_id}"
      save_config;
    else
      echo "Project ID Unchanged"
      echo ""
    fi
  else
    echo "Using Existing Project ID: ${STARTHINKER_PROJECT}"
    echo ""
  fi

  gcloud config set project "${STARTHINKER_PROJECT}" --no-user-output-enabled;
}


setup_region_and_zone() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set gCloud Default Region And Zone"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_ZONE}"
  echo " - https://cloud.google.com/compute/docs/regions-zones#available"
  echo ""

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_ZONE}" == "" ]; then

    echo "Retrieve Zone from:  https://cloud.google.com/compute/docs/regions-zones#available"
    echo ""
    echo "IMPORTANT SETUP NOTES"
    echo ""
    echo " * Ensure the zone supports N1 and N2 compue types."
    echo " * For the UI: SQL and AppEngine require the zone to be the same and remain unchanged once deployed."
    echo " * Enter the full zone name, for example: us-central1-a"
    echo ""

    read -p "Full zone name ( blank to keep existing ): " zone_id

    if [ "${zone_id}" ]; then
      STARTHINKER_ZONE="${zone_id}"
      save_config;
    else
      echo "Project ID Unchanged"
      echo ""
    fi
  else
    echo "Using Existing Zone: ${STARTHINKER_ZONE}"
    echo ""
  fi
}

setup_developer_token() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set Developer Token"
  echo "----------------------------------------"
  echo ""
  echo " - https://developers.google.com/google-ads/api/docs/first-call/dev-token"
  echo ""

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_DEVELOPER_TOKEN}" == "" ]; then

    echo "Used for Adwords APIs only. Otherwise leave blank."
    echo "Retrieve Developer Token from: https://developers.google.com/google-ads/api/docs/first-call/dev-token"
    echo ""

    read -p "Developer Token ( blank to keep existing ): " developer_token

    if [ "${developer_token}" ]; then
      STARTHINKER_DEVELOPER_TOKEN="${developer_token}"
      save_config;
    else
      echo "Developer Token Unchanged"
      echo ""
    fi
  else
    echo "Using Existing Developer Token: ${STARTHINKER_DEVELOPER_TOKEN}"
    echo ""
  fi
}


setup_api_key() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set API Key"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_API_KEY}"
  echo ""

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_API_KEY}" == "" ]; then

    echo "Used when API endpoint requires special approval from Google, typically betas. Otherwise leave blank."
    echo "Retrieve API Key from: https://cloud.google.com/docs/authentication/api-keys"
    echo ""

    read -p "API Key ( blank to keep existing ): " api_key

    if [ "${api_key}" ]; then
      STARTHINKER_API_KEY="${api_key}"
      save_config;
    else
      echo "Api Key Unchanged"
      echo ""
    fi
  else
    echo "Using Existing API Key: ${STARTHINKER_API_KEY}"
    echo ""
  fi
}


setup_credentials_commandline() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup Command Line Credentials For User"
  echo "----------------------------------------"
  echo ""

  if [ "$forced" == "forced" ] || [ ! -f "$STARTHINKER_CLIENT_INSTALLED" ]; then

    echo "Step 1: Configure Consent Screen ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials/consent"

    if [[ $STARTHINKER_GSUITE == 1 ]]; then
      echo "  B. Choose Internal."
    else
      echo "  B. Choose External."
    fi

    echo "  C. For Application Name enter: StarThinker"
    echo "  D. All other fields are optional, click Save."
    echo ""

    echo "Step 2: Setup Credentials ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials/oauthclient"
    echo "  B. Choose Desktop."
    echo "  C. For Name enter: StarThinker."
    echo "  D. Click Create and ignore the confirmation pop-up."
    echo ""

    echo "Step 3: Enter Credentials ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials"
    echo "  B. Find your key under OAuth 2.0 Client IDs and click download arrow."
    echo "  C. Paste credentials JSON below, then press return ( if return does not work press CTRL + D ):"
    echo ""

    read_multiline "}}"

    if [ "${read_multiline_return}" ];then
      printf "%s" "$read_multiline_return" > "${STARTHINKER_CLIENT_INSTALLED}"
    fi

  else
    echo "Using Existing Client Credentials: ${STARTHINKER_CLIENT_INSTALLED}"
  fi

  if ! [ -s "${STARTHINKER_ROOT}/starthinker_assets/client_installed.json" ]; then
    rm "${STARTHINKER_ROOT}/starthinker_assets/client_installed.json"
    echo "Failed To Create Client Desktop Credentials, Fix Then Run This Script Again"
    echo " 1. Check permissions of gcloud user."
    echo " 2. Check if client accounts are enabled for the project."
    echo " 3. Manually paste client JSON credentials into: starthinker_assets/client_installed.json"
    exit 1;
  fi
}


setup_credentials_ui() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup UI Credentials"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_CLIENT_WEB}"
  echo ""

  if [ "$forced" == "forced" ] || [ ! -f "$STARTHINKER_CLIENT_WEB" ]; then

    echo "Step 1: Configure Consent Screen ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials/consent"

    if [[ $STARTHINKER_GSUITE == 1 ]]; then
      echo "  B. Choose Internal."
    else
      echo "  B. Choose External."
    fi

    echo "  C. For Application Name enter: StarThinker"
    echo "  D. In Authorized domains, type $(gcloud app browse --no-launch-browser), without http://, and press Enter."
    echo "  E. All other fields are optional, click Save."
    echo ""

    echo "Step 2: Setup Credentials ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials/oauthclient"
    echo "  B. Choose Web Application."
    echo "  C. For Name enter: StarThinker."
    echo "  D. For Authorized redirect URIs enter:"
    echo "       $(gcloud app browse --no-launch-browser)/oauth_callback/"
    echo "  F. Click Create and ignore the confirmation pop-up."
    echo ""

    echo "Step 3: Enter Credentials ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials"
    echo "  B. Find your key under OAuth 2.0 Client IDs and click download arrow."
    echo "  C. Paste credentials JSON below, then press return ( if return does not work press CTRL + D ):"
    echo ""

    read_multiline "}}"

    if [ "${read_multiline_return}" ];then
      printf "%s" "$read_multiline_return" > "${STARTHINKER_CLIENT_WEB}"
    fi
  else
    echo "Using Existing Client Credentials"
  fi

  if ! [ -s "${STARTHINKER_ROOT}/starthinker_assets/client_web.json" ]; then
     rm "${STARTHINKER_ROOT}/starthinker_assets/client_web.json"
     echo "Failed To Create Client Web Credentials, Fix Then Run This Script Again"
     echo " 1. Check permissions of gcloud user."
     echo " 2. Check if client accounts are enabled for the project."
     echo " 3. Manually paste client JSON credentials into: starthinker_assets/client_web.json"
     exit 1;
  fi
}


get_service_email() {
  echo $(echo "starthinker@${STARTHINKER_PROJECT}.iam.gserviceaccount.com" | sed -r "s/(google.com):(.*)/\2.\1/g")
}

get_cloudbuild_email() {
  project_number=$(gcloud projects describe $STARTHINKER_PROJECT --format="value(projectNumber)")
  echo "${project_number}@cloudbuild.gserviceaccount.com"
}

setup_credentials_service() {
  echo ""
  echo "----------------------------------------"
  echo "Setup Service Credentials - NO KEY DOWNLOAD"
  echo "----------------------------------------"
  echo ""
  echo " - starthinker@${STARTHINKER_PROJECT}.iam.gserviceaccount.com"
  echo ""

  gcloud alpha iam service-accounts create "starthinker" \
  --display-name="StarThinker (Service Account)" \
  --description="This service account is used by the StarThinker framework." \
  --verbosity=critical

  if [ !$? ]; then

    gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role='roles/secretmanager.admin'

    gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role='roles/secretmanager.secretAccessor'

    gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role='roles/cloudsql.editor'

    gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role='roles/iam.serviceAccountUser'

    gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role='roles/compute.admin'

    gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
    --member=serviceAccount:$(get_service_email) \
    --role='roles/cloudsql.client'

  else
    echo "WARNING: Failed to create service account.  You may not be able to deploy workers."
    exit
  fi
}

setup_credentials_user() {
  echo ""
  echo "----------------------------------------"
  echo "Update User Credentials"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_USER}"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";
  python3 "${THIS_DIR}/starthinker/tool/auth.py" -c "${STARTHINKER_CLIENT_INSTALLED}" -u "${STARTHINKER_USER}"
  deactivate

  echo ""
  echo "Done"
  echo ""
}


update_apt() {
  echo ""
  echo "----------------------------------------"
  echo "Update Debian Installer ( Uses Sudo )"
  echo "----------------------------------------"
  echo ""

  if [ "$(uname -s)" == "Linux" ]; then
    sudo apt-get update -qq > /dev/null
  fi

  echo ""
  echo "Done"
  echo ""
}


install_virtualenv_darwin() {

  if [ "$(command -v python3)" == "" ]; then
    echo ""
    echo "----------------------------------------"
    echo "MISSING python3"
    echo "----------------------------------------"
    echo ""
    echo "Please install: https://www.python.org/downloads/release/python-380/"
    echo "Then run the install again."
    echo ""
    return
  fi

  if [ "$(command -v pip3)" == "" ]; then
    echo ""
    echo "----------------------------------------"
    echo "MISSING pip3"
    echo "----------------------------------------"
    echo ""
    echo "Please install: https://evansdianga.com/install-pip-osx/"
    echo "Then run the install again."
    echo ""
    return
  else
    if [[ -z $VIRTUAL_ENV ]]; then
      python3 -m pip install pip --upgrade --quiet --user;
    fi
  fi

  if [ "$(command -v virtualenv)" == "" ]; then
    python3 -m pip install virtualenv --quiet --user;
  fi

}


install_virtualenv_linux() {
  if [ "$(command -v lsb_release)" == "" ]; then
    echo "Install not supported.  Please use a Debian based Linux instance."
  else
    sudo apt-get install gcc python3-dev python3-pip wget -qq;
    if [ "$(command -v virtualenv)" == "" ]; then
      sudo apt-get install virtualenv -qq
    fi
  fi
}


install_virtualenv() {

  echo ""
  echo "----------------------------------------"
  echo "Install Virtual Environment ( Uses Sudo )"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_ENV}"
  echo ""

  case "$(uname -s)" in
    Darwin) install_virtualenv_darwin ;;
    Linux)  install_virtualenv_linux ;;
    *) echo "ERROR: Please install pip manually."
  esac

  if [ ! -d "${STARTHINKER_ENV}" ]; then

    PYTHON3=$(which python3);
    virtualenv --python=${PYTHON3} ${STARTHINKER_ENV}

  fi

  echo "Done"
}


install_requirements() {
  echo ""
  echo "----------------------------------------"
  echo "Install Python Packages - ${STARTHINKER_ROOT}/starthinker/requirements.txt"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ENV}/bin/activate"
  python3 -m pip install --upgrade pip
  python3 -m pip install install -r ${STARTHINKER_ROOT}/requirements.txt --quiet
  deactivate

  echo ""
  echo "Done"
}


setup_swap() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Swap ( Uses Sudo )"
  echo "----------------------------------------"
  echo ""

  if [ -e "/swapfile" ]; then
    sudo swapoff /swapfile;
    sudo rm /swapfile;
  fi

  sudo fallocate -l 10G /swapfile;
  sudo chmod 600 /swapfile;
  sudo mkswap /swapfile;
  sudo swapon /swapfile;
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab;

  echo ""
  echo "Done"
}


setup_domain() {

  echo ""
  echo "----------------------------------------"
  echo "Set UI Domain"
  echo "----------------------------------------"
  echo ""
  echo " - $STARTHINKER_UI_PRODUCTION_DOMAIN"
  echo ""
  echo "If you DO NOT HAVE A DOMAIN then LEAVE IT BLANK."
  echo "If left blank, the default domain of [project].[appengine URL] will be used."
  echo "The script will use whatever defaults necessary to get things working."
  echo ""

  if [ "${STARTHINKER_UI_PRODUCTION_DOMAIN}" == "" ]; then

    read -p "Domain Name ( blank to skip ): " domain_name

    if [ "${domain_name}" ];then
      STARTHINKER_UI_PRODUCTION_DOMAIN="${domain_name}"
    else
      echo "Domain Name Unchanged"
    fi
  else
    echo "Using Existing Domain"
  fi

  echo ""
  echo "Done"
}


make_cron() {
  if [ "${STARTHINKER_CRON}" ]; then
    if [ ! -d "${STARTHINKER_CRON}" ]; then

      echo ""
      echo "----------------------------------------"
      echo " Create Cron Directory - ${STARTHINKER_CRON}"
      echo "----------------------------------------"
      echo ""

      mkdir -p "${STARTHINKER_CRON}"

      echo "Done"
      echo ""

    fi
  fi
}


install_proxy_darwin() {
  if [ "$(uname -m)" == "x86_64" ]; then
    curl -o "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy" https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
  else
    curl -o "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy" https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.386
  fi
}


install_proxy_linux() {
  if [ "$(uname -m)" == "x86_64" ]; then
    wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy"
  else
    wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.386 -O "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy"
  fi
}


generate_translations() {
  echo ""
  echo "----------------------------------------"
  echo "Generate Translations"
  echo "----------------------------------------"
  echo ""
  echo " - https://docs.djangoproject.com/en/4.0/topics/i18n/translation/"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/production.sh";
  cd "${STARTHINKER_ROOT}/starthinker_ui"
  python3 manage.py makemessages -a;
  python3 manage.py compilemessages;
  cd "${STARTHINKER_ROOT}"
  deactivate

  echo "Done"
}


install_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Install Cloud Proxy ( Uses Sudo )"
  echo "----------------------------------------"
  echo ""
  echo " - ${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy"
  echo " - https://cloud.google.com/sql/docs/mysql/sql-proxy"
  echo ""

  case "$(uname -s)" in
    Darwin) echo "Skipping Postgres, not required for local development: https://www.postgresql.org/download/macosx/";;
    Linux)  sudo apt-get install gcc python3-dev python3-pip libpq-dev postgresql-client python3-psycopg2 wget -qq;;
    *) echo "ERROR: Unknown Postgres install, visit http://postgresguide.com/setup/install.html" ;;
  esac

  if [ ! -f "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy" ]; then

    case "$(uname -s)" in
      Darwin) install_proxy_darwin;;
      Linux)  install_proxy_linux;;
      *) echo "ERROR: Unknown OS, Visit https://cloud.google.com/sql/docs/postgres/sql-proxy" ;;
    esac

    chmod +x "${STARTHINKER_ROOT}/starthinker_assets/cloud_sql_proxy";
  fi

  echo ""
  echo "Done"
}


################################################################################
#
#  load variables or reset paths - when copying assets paths need to be realigned to new destination
#
load_config;

if [ "$1" = "--no_user" ];then
  shift
  setup_gcloud;
  setup_project;
else
  setup_gcloud;
  setup_project;
  setup_region_and_zone;
  check_gsuite;
fi

save_config;
