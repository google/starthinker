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


################################################################################
#
# constats used by all the debian scripts
#
STARTHINKER_SCALE=1
STARTHINKER_DEVELOPMENT=0

STARTHINKER_PROJECT=""
STARTHINKER_ZONE="us-west1-b"

STARTHINKER_UI_DOMAIN=""
STARTHINKER_UI_DATABASE_ENGINE="django.db.backends.postgresql"
STARTHINKER_UI_DATABASE_HOST="127.0.0.1"
STARTHINKER_UI_DATABASE_PORT="5432"
STARTHINKER_UI_DATABASE_NAME="starthinker-test"
STARTHINKER_UI_DATABASE_USER="starthinker_user"
STARTHINKER_UI_DATABASE_PASSWORD="starthinker_password"

derive_config() {

  STARTHINKER_REGION=$(echo "$STARTHINKER_ZONE" | sed -e "s/\-[a-z]$//")

  STARTHINKER_ROOT="${THIS_DIR}"

  STARTHINKER_CLIENT_WEB="${THIS_DIR}/starthinker_assets/client_web.json"
  STARTHINKER_CLIENT_INSTALLED="${THIS_DIR}/starthinker_assets/client_installed.json"
  STARTHINKER_SERVICE="${THIS_DIR}/starthinker_assets/service.json"
  STARTHINKER_USER="${THIS_DIR}/starthinker_assets/user.json"
  STARTHINKER_CONFIG="${THIS_DIR}/starthinker_assets/production.sh"
  STARTHINKER_CRT="${THIS_DIR}/starthinker_assets/ssl.crt"
  STARTHINKER_KEY="${THIS_DIR}/starthinker_assets/ssl.key"
  STARTHINKER_CSR="${THIS_DIR}/starthinker_assets/ssl.csr"

  STARTHINKER_CRON="${THIS_DIR}/starthinker_cron"
  STARTHINKER_ENV="${THIS_DIR}/starthinker_virtualenv"

  if [ -z "${STARTHINKER_UI_SECRET}" ]; then
    STARTHINKER_UI_SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
  fi

}


load_config() {
  echo ""
  echo "----------------------------------------"
  echo "Loading Configuration - ${THIS_DIR}/starthinker_assets/production.sh"
  echo "----------------------------------------"
  echo ""

  if [ -e "${THIS_DIR}/starthinker_assets/production.sh" ]; then
    source "${THIS_DIR}/starthinker_assets/production.sh";
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

  echo "export STARTHINKER_UI_DOMAIN=\"$STARTHINKER_UI_DOMAIN\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_SECRET=\"$STARTHINKER_UI_SECRET\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_ENGINE=\"$STARTHINKER_UI_DATABASE_ENGINE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_HOST=\"$STARTHINKER_UI_DATABASE_HOST\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_PORT=\"$STARTHINKER_UI_DATABASE_PORT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_NAME=\"$STARTHINKER_UI_DATABASE_NAME\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_USER=\"$STARTHINKER_UI_DATABASE_USER\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_PASSWORD=\"$STARTHINKER_UI_DATABASE_PASSWORD\";" >> "${STARTHINKER_CONFIG}"
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
  gcloud --version

  if [ ! $? -eq 0 ]
  then
    echo ""
    echo "\e[31m[ERROR] \e[0mIt looks like gcloud isn't installed, please go to https://cloud.google.com/sdk/install to install it"
    exit 1
  else
    gcloud config get-value account
    if [[ $? == *"ERROR"* ]]
    then
      echo ""
      echo "GCloud installed, authenticating"
      gcloud auth login
    fi
  fi
}


setup_database() {
  optional_name=$1
  optional_user=$2
  optional_password=$3

  echo ""
  echo "----------------------------------------"
  echo "Set Cloud Database Parameters"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_name" != "optional" ] || [ "${STARTHINKER_UI_DATABASE_NAME}" == "" ]; then
    read -p "Database Name - ${STARTHINKER_UI_DATABASE_NAME} ( blank to skip ): " database_name
    if [ "${database_name}" ]; then
      STARTHINKER_UI_DATABASE_NAME="${database_name}"
    else
      echo "Database Name Unchanged"
    fi
  else
    echo "Using Existing Database Name"
  fi

  if [ "$optional_user" != "optional" ] || [ "${STARTHINKER_UI_DATABASE_USER}" == "" ]; then
    read -p "Database User - ${STARTHINKER_UI_DATABASE_USER} ( blank to skip ): " database_user
    if [ "${database_user}" ]; then
      STARTHINKER_UI_DATABASE_USER="${database_user}"
    else
      echo "Database User Unchanged"
    fi
  else
    echo "Using Existing Database User"
  fi

  if [ "$optional_password" != "optional" ] || [ "${STARTHINKER_UI_DATABASE_PASSWORD}" == "" ]; then
    read -p "Database Password - ${STARTHINKER_UI_DATABASE_PASSWORD} ( blank to skip ): " database_password
    if [ "${database_password}" ]; then
      STARTHINKER_UI_DATABASE_PASSWORD="${database_password}"
    else
      echo "Database Password Unchanged"
    fi
  else
    echo "Using Existing Database Password"
  fi

  echo "Done"
  echo ""
}


setup_project() {
  optional_project=$1

  echo ""
  echo "----------------------------------------"
  echo "Set Cloud Project - ${STARTHINKER_PROJECT}"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_project" != "optional" ] || [ "${STARTHINKER_PROJECT}" == "" ]; then

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
    else
      echo "Project ID Unchanged"
    fi
  else
    echo "Using Existing Project ID"
  fi

  gcloud config set project "${STARTHINKER_PROJECT}";

  echo "Done"
  echo ""
}


setup_credentials_commandline() {
  optional_credentials=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup Command Line Credentials For User - ${STARTHINKER_CLIENT_INSTALLED}"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_credentials" != "optional" ] || [ ! -f "$STARTHINKER_CLIENT_INSTALLED" ]; then

    # client OTHER
    echo "Retrieve \"Other\" OAuth Client ID Credentials from: https://console.cloud.google.com/apis/credentials"
    echo "Google Cloud Console -> Services & APIs -> Create Credentials -> oAuth Credentials."
    echo ""

    echo "Paste credentials JSON here: ( CTRL+D to skip )"

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
  optional_credentials=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup UI Credentials - ${STARTHINKER_CLIENT_WEB}"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_credentials" != "optional" ] || [ ! -f "$STARTHINKER_CLIENT_WEB" ]; then

    # client OTHER
    echo "Retrieve \"Web\" OAuth Client ID Credentials from: https://console.cloud.google.com/apis/credentials"
    echo "Set up the \"Internal\" OAuth Consent Screen: https://pantheon.corp.google.com/apis/credentials/consent"
    echo "Google Cloud Console -> Services & APIs -> Create Credentials -> oAuth Credentials."
    echo ""

    echo "Paste credentials JSON here: ( CTRL+D to skip )"

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
  optional_credentials=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup Service Credentials - ${STARTHINKER_SERVICE}"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_credentials" != "optional" ] || [ ! -f "$STARTHINKER_SERVICE" ]; then

    echo "Retrieve Service Account Key Credentials from: https://console.cloud.google.com/apis/credentials"
    echo ""
    echo "IMPORTANT SETUP NOTES"
    echo ""
    echo " * In Google Cloud Console -> Services & APIs -> Create Credentials -> Service Credentials."
    echo " * Choose JSON format."
    echo " * Name the service 'starthinker' for ease of tracking later."
    echo " * Assign project editor role or restrict roles to BigQuery / Storage editors."
    echo " * Credentials will automatically download, open file and copy contents."
    echo ""

    echo "Paste credentials JSON here: ( CTRL+D to skip )"

    read_multiline "}"

    if [ "${read_multiline_return}" ];then
      printf "%s" "$read_multiline_return" > "${STARTHINKER_SERVICE}"
    fi

    if [ "${read_multiline_return}" ];then
      printf "%s" "$read_multiline_return" > "${STARTHINKER_SERVICE}"
    fi
  else
    echo "Using Existing Service Credentials"
  fi

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
  python "${THIS_DIR}/starthinker/auth/helper.py" -c "${STARTHINKER_CLIENT_INSTALLED}" -u "${STARTHINKER_USER}"
  deactivate

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

  echo "Done"
  echo ""
}


install_virtualenv_darwin() {

  if [ "$(command -v pip)" == "" ]; then
    sudo easy_install pip
    pip install pip --upgrade --quiet 
  fi

  if [ "$(command -v virtualenv)" == "" ]; then
    pip2 install virtualenv --quiet
  fi
}


install_virtualenv_linux() {

  if [ "$(command -v virtualenv)" == "" ]; then
    sudo apt-get install virtualenv -qq 
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

    PYTHON2=$(which python2);
    virtualenv --python=${PYTHON2} ${STARTHINKER_ENV}

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
  pip2 install -r ${STARTHINKER_ROOT}/starthinker/requirements.txt --quiet
  deactivate

  echo "Done"
  echo ""
}


install_requirements_ui() {
  echo ""
  echo "----------------------------------------"
  echo "Install Python Packages For UI - ${STARTHINKER_ROOT}/starthinker_ui/requirements.txt"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ENV}/bin/activate"
  pip2 install -r ${STARTHINKER_ROOT}/starthinker_ui/requirements.txt --quiet
  deactivate

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

  echo "Done"
  echo ""
}


setup_domain() {
  optional_domain=$1

  echo ""
  echo "----------------------------------------"
  echo "Set UI Domain - $STARTHINKER_UI_DOMAIN"
  echo "----------------------------------------"
  echo ""
  echo "If you DO NOT HAVE A DOMAIN then LEAVE IT BLANK."
  echo "The script will use whatever defaults necessay to get things working."
  echo ""

  if [ "$optional_domain" != "optional" ] || [ "${STARTHINKER_UI_DOMAIN}" == "" ]; then

    read -p "Domain Name ( blank to skip ): " domain_name

    if [ "${domain_name}" ];then
      STARTHINKER_UI_DOMAIN="${domain_name}"
    else
      echo "Domain Name Unchanged"
    fi
  else
    echo "Using Existing Domain"
  fi

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
      Darwin) brew install postgresql-client;;
      Linux)  sudo apt-get install gcc python-dev libpq-dev postgresql-client python-psycopg2 -qq;;
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

  echo "Done"
  echo ""
}


################################################################################
#
#  load variables or reset paths - when copying assets paths need to be realigned to new destination
#
load_config;
