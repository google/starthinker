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
STARTHINKER_GSUITE=0

STARTHINKER_WORKER_MAX=10
STARTHINKER_WORKER_INSTANCE="e2-highmem-4"
STARTHINKER_WORKER_JOBS=4

STARTHINKER_ANALYTICS="UA-167283455-2"

STARTHINKER_PROJECT=""
STARTHINKER_ZONE="us-west2-b"

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

  if [ -z "${STARTHINKER_UI_DEVELOPMENT_DATABASE_NAME}" ]; then
    STARTHINKER_UI_DEVELOPMENT_DATABASE_NAME="${STARTHINKER_ROOT}/starthinker_database/database.sqlite";
  fi
}


load_config() {
  echo ""
  echo "----------------------------------------"
  echo "Loading Configuration - ${THIS_DIR}/starthinker_assets/config.sh"
  echo "----------------------------------------"
  echo ""

  if [ -e "${THIS_DIR}/starthinker_assets/config.sh" ]; then
    source "${THIS_DIR}/starthinker_assets/config.sh";
  fi

  derive_config;

  echo "Done"
  echo ""
}


save_config() {

  derive_config;

  echo ""
  echo "----------------------------------------"
  echo "Saving Configuration - ${STARTHINKER_CONFIG}"
  echo "----------------------------------------"
  echo ""

  echo "export STARTHINKER_SCALE=$STARTHINKER_SCALE;" > "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_DEVELOPMENT=$STARTHINKER_DEVELOPMENT;" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_WORKER_MAX=$STARTHINKER_WORKER_MAX;" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_WORKER_INSTANCE=\"$STARTHINKER_WORKER_INSTANCE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_WORKER_JOBS=$STARTHINKER_WORKER_JOBS;" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_ANALYTICS=$STARTHINKER_ANALYTICS;" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_PROJECT=\"$STARTHINKER_PROJECT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ZONE=\"$STARTHINKER_ZONE\";" >> "${STARTHINKER_CONFIG}"
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
  echo ""
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
    echo "Using Existing Database Name"
  fi

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_UI_PRODUCTION_DATABASE_USER}" == "" ]; then
    read -p "Database User - ${STARTHINKER_UI_PRODUCTION_DATABASE_USER} ( blank to skip ): " database_user
    if [ "${database_user}" ]; then
      STARTHINKER_UI_PRODUCTION_DATABASE_USER="${database_user}"
    else
      echo "Database User Unchanged"
    fi
  else
    echo "Using Existing Database User"
  fi

  if [ "$forced" == "forced" ] || [ "${STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD}" == "" ]; then
    read -p "Database Password - ${STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD} ( blank to skip ): " database_password
    if [ "${database_password}" ]; then
      STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD="${database_password}"
    else
      echo "Database Password Unchanged"
    fi
  else
    echo "Using Existing Database Password"
  fi

  echo ""
  echo "Done"
  echo ""
}


setup_analytics() {

  echo ""
  echo "----------------------------------------"
  echo "Set Analytics Tracking - ${STARTHINKER_ANALYTICS}"
  echo "----------------------------------------"
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

  echo ""
  echo "Done"
  echo ""
}


setup_project() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Set gCloud Project - ${STARTHINKER_PROJECT}"
  echo "----------------------------------------"
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
    echo "Using Existing Project ID"
    echo ""
  fi

  gcloud config set project "${STARTHINKER_PROJECT}" --no-user-output-enabled;
}


setup_credentials_commandline() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup Command Line Credentials For User - ${STARTHINKER_CLIENT_INSTALLED}"
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
    echo "Using Existing Client Credentials"
  fi

  echo "Done"
  echo ""
}


setup_credentials_ui() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup UI Credentials - ${STARTHINKER_CLIENT_WEB}"
  echo "----------------------------------------"
  echo ""

  if [ "$forced" == "forced" ] || [ ! -f "$STARTHINKER_CLIENT_WEB" ]; then

    values=$(gcloud app describe --format="value(name)" --verbosity=none)
    if [ -z "${values}" ]; then
      gcloud app create --region "${STARTHINKER_REGION}"
    fi

    echo "Step 1: Configure Consent Screen ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials/consent"

    if [[ $STARTHINKER_GSUITE == 1 ]]; then
      echo "  B. Choose Internal."
    else
      echo "  B. Choose External."
    fi

    echo "  C. For Application Name enter: StarThinker"
    echo "  D. In Authorized domains, type $(gcloud app browse --no-launch-browser) and press Enter."
    echo "  E. All other fields are optional, click Save."
    echo ""

    echo "Step 2: Setup Credentials ( do only once )"
    echo "----------------------------------------"
    echo "  A. Visit: https://console.developers.google.com/apis/credentials/oauthclient"
    echo "  B. Choose Web Application."
    echo "  C. For Name enter: StarThinker."
    echo "  D. For Authorized redirect URIs enter:"
    echo "       http://localhost:8000/oauth_callback/"
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

  echo "Done"
  echo ""
}

setup_credentials_service() {
  forced=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup Service Credentials - ${STARTHINKER_SERVICE}"
  echo "----------------------------------------"
  echo ""

  if [ "$forced" == "forced" ] || [ ! -f "$STARTHINKER_SERVICE" ]; then

    echo "Retrieve Service Account Key Credentials from: https://console.cloud.google.com/apis/credentials"
    echo ""

    gcloud alpha iam service-accounts create "starthinker" \
    --display-name="StarThinker (Service Account)" \
    --description="This service account is used by the StarThinker framework." \
    --verbosity=critical

    return_code=$?
    if [ !$return_code ]; then

      gcloud projects add-iam-policy-binding "${STARTHINKER_PROJECT}" \
      --member=serviceAccount:starthinker@${STARTHINKER_PROJECT}.iam.gserviceaccount.com \
      --role='roles/editor'

      return_code=$?
      if [ !$return_code ]; then

        gcloud iam service-accounts keys create ${STARTHINKER_ROOT}/starthinker_assets/service.json \
        --iam-account=starthinker@${STARTHINKER_PROJECT}.iam.gserviceaccount.com \
        --key-file-type=json

      else

        echo "Failed to create keys."
        return

      fi

    else
      echo "Failed to create file."
      return

    fi

  else
    echo "Using Existing Service Credentials"
  fi

  echo ""
  echo "Done"
  echo ""
}

setup_credentials_user() {
  echo ""
  echo "----------------------------------------"
  echo "Update User Credentials - ${STARTHINKER_USER}"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ROOT}/starthinker_assets/development.sh";
  python3 "${THIS_DIR}/starthinker/auth/helper.py" -c "${STARTHINKER_CLIENT_INSTALLED}" -u "${STARTHINKER_USER}"
  deactivate

  echo ""
  echo "Done"
  echo ""
}


update_apt() {
  echo ""
  echo "----------------------------------------"
  echo "Update Debian Installer"
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
  echo "Install Virtual Environment - ${STARTHINKER_ENV}"
  echo "----------------------------------------"
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
  echo ""
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
  echo ""
}


setup_swap() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Swap"
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
  echo ""
}


setup_domain() {

  echo ""
  echo "----------------------------------------"
  echo "Set UI Domain - $STARTHINKER_UI_PRODUCTION_DOMAIN"
  echo "----------------------------------------"
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
  echo ""
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
    curl -o "${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy" https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
  else
    curl -o "${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy" https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.386
  fi
}


install_proxy_linux() {
  if [ "$(uname -m)" == "x86_64" ]; then
    wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O "${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy"
  else
    wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.386 -O "${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy"
  fi
}


install_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Install Cloud Proxy - ${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy"
  echo "----------------------------------------"
  echo ""

  if [ "$(command -v psql)" == "" ]; then
    case "$(uname -s)" in
      Darwin) echo "Skipping Postgres, not required for local development: https://www.postgresql.org/download/macosx/";;
      Linux)  sudo apt-get install gcc python3-dev python3-pip libpq-dev postgresql-client python-psycopg2 wget -qq;;
      *) echo "ERROR: Unknown Postgres install, visit http://postgresguide.com/setup/install.html" ;;
    esac
  fi

  if [ ! -f "${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy" ]; then

    mkdir -p "${STARTHINKER_ROOT}/starthinker_database/"

    case "$(uname -s)" in
      Darwin) install_proxy_darwin;;
      Linux)  install_proxy_linux;;
      *) echo "ERROR: Unknown OS, Visit https://cloud.google.com/sql/docs/postgres/sql-proxy" ;;
    esac

    chmod +x "${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy";
  fi

  echo ""
  echo "Done"
  echo ""
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
  check_gsuite;
fi

save_config;
