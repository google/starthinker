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
STARTHINKER_MANAGERS=1
STARTHINKER_WORKERS=6
STARTHINKER_PROJECT=""
STARTHINKER_ZONE="us-central1-a"
STARTHINKER_TOPIC="starthinker"
STARTHINKER_ASSETS="${THIS_DIR}/starthinker_assets"
STARTHINKER_CLIENT="${THIS_DIR}/starthinker_assets/client.json"
STARTHINKER_SERVICE="${THIS_DIR}/starthinker_assets/service.json"
STARTHINKER_USER="${THIS_DIR}/starthinker_assets/user.json"
STARTHINKER_CRON="${THIS_DIR}/starthinker_assets/cron"
STARTHINKER_ENV="${THIS_DIR}/starthinker_assets/env"
STARTHINKER_CRT="${THIS_DIR}/starthinker_assets/ssl.crt"
STARTHINKER_KEY="${THIS_DIR}/starthinker_assets/ssl.key"
STARTHINKER_CSR="${THIS_DIR}/starthinker_assets/ssl.csr"
STARTHINKER_CONFIG="${THIS_DIR}/starthinker_assets/config.sh"
STARTHINKER_CODE="${THIS_DIR}/starthinker"
STARTHINKER_ROOT="${THIS_DIR}"

STARTHINKER_DEVELOPMENT=0
STARTHINKER_INTERNAL=0

if [ "$STARTHINKER_UI_SECRET" == "" ]; then
  STARTHINKER_UI_SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
fi

STARTHINKER_UI_DOMAIN=""
STARTHINKER_UI_DATABASE_ENGINE=""
STARTHINKER_UI_DATABASE_HOST=""
STARTHINKER_UI_DATABASE_PORT=""
STARTHINKER_UI_DATABASE_NAME="starthinker-test"
STARTHINKER_UI_DATABASE_USER="starthinker_user"
STARTHINKER_UI_DATABASE_PASSWORD="starthinker_password"

STARTHINKER_RECIPE_PROJECT=""
STARTHINKER_RECIPE_SERVICE=""

# DO NOT SAVE THESE ( PURELY DERIVED VARIABLES )
STARTHINKER_REGION=$(echo "$STARTHINKER_ZONE" | sed -e "s/\-[a-z]$//")

################################################################################
#
# load project id from file between sessions ( only item in file )
#
load_config() {
  echo ""
  echo "----------------------------------------"
  echo "Loading Configuration - ${STARTHINKER_CONFIG}"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_CONFIG}" --load;

  echo "Done"
  echo ""
}


################################################################################
#
# save all variables to file for load at startup next time
#
save_config() {
  echo ""
  echo "----------------------------------------"
  echo "Saving Configuration - ${STARTHINKER_CONFIG}"
  echo "----------------------------------------"
  echo ""

  echo "export STARTHINKER_SCALE=$STARTHINKER_SCALE;" > "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_MANAGERS=$STARTHINKER_MANAGERS;" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_WORKERS=$STARTHINKER_WORKERS;" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_PROJECT=\"$STARTHINKER_PROJECT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ZONE=\"$STARTHINKER_ZONE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_TOPIC=\"$STARTHINKER_TOPIC\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ASSETS=\"$STARTHINKER_ASSETS\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CLIENT=\"$STARTHINKER_CLIENT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_SERVICE=\"$STARTHINKER_SERVICE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_USER=\"$STARTHINKER_USER\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CRON=\"$STARTHINKER_CRON\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ENV=\"$STARTHINKER_ENV\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CRT=\"$STARTHINKER_CRT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_KEY=\"$STARTHINKER_KEY\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CSR=\"$STARTHINKER_CSR\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CONFIG=\"$STARTHINKER_CONFIG\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_CODE=\"$STARTHINKER_CODE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_ROOT=\"$STARTHINKER_ROOT\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_DEVELOPMENT=$STARTHINKER_DEVELOPMENT;" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_INTERNAL=$STARTHINKER_INTERNAL;" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_UI_DOMAIN=\"$STARTHINKER_UI_DOMAIN\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_SECRET=\"$STARTHINKER_UI_SECRET\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_ENGINE=\"$STARTHINKER_UI_DATABASE_ENGINE\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_HOST=\"$STARTHINKER_UI_DATABASE_HOST\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_PORT=\"$STARTHINKER_UI_DATABASE_PORT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_NAME=\"$STARTHINKER_UI_DATABASE_NAME\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_USER=\"$STARTHINKER_UI_DATABASE_USER\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_UI_DATABASE_PASSWORD=\"$STARTHINKER_UI_DATABSE_PASSWORD\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "export STARTHINKER_RECIPE_PROJECT=\"$STARTHINKER_RECIPE_PROJECT\";" >> "${STARTHINKER_CONFIG}"
  echo "export STARTHINKER_RECIPE_SERVICE=\"$STARTHINKER_RECIPE_SERVICE\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "if [[ "\$PYTHONPATH" != *\"\${STARTHINKER_ROOT}\"* ]]; then" >> "${STARTHINKER_CONFIG}"
  echo "  export PYTHONPATH=\"\${PYTHONPATH}:\${STARTHINKER_ROOT}\"" >> "${STARTHINKER_CONFIG}"
  echo "fi" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "source \"\$STARTHINKER_ENV/bin/activate\";" >> "${STARTHINKER_CONFIG}"
  echo "" >> "${STARTHINKER_CONFIG}"

  echo "if [ \"\$1\" != '--load' ];then" >> "${STARTHINKER_CONFIG}"
  echo "  cd \$STARTHINKER_CODE" >> "${STARTHINKER_CONFIG}"
  echo "fi" >> "${STARTHINKER_CONFIG}"

  echo "Done"
  echo ""
}


################################################################################
#
#  read multiline example
#
#  read_multiline "}}"
#  if [ "${read_multiline_return}" ];then
#    printf "%s" "$read_multiline_return" > "${STARTHINKER_CLIENT}"
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


################################################################################
#
#  setup gcloud - Give the instance some overflow memory
#
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


################################################################################
#
#  set database parameters - name, user, and password
#
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
    read -p "Databse Name - ${STARTHINKER_UI_DATABASE_NAME} ( blank to skip ): " database_name
    if [ "${databse_name}" ]; then
      STARTHINKER_UI_DATABASE_NAME="${database_name}"
    else
      echo "Database Name Unchanged"
    fi
  else
    echo "Using Existing Database Name"
  fi

  if [ "$optional_user" != "optional" ] || [ "${STARTHINKER_UI_DATABASE_USER}" == "" ]; then
    read -p "Databse User - ${STARTHINKER_UI_DATABASE_USER} ( blank to skip ): " database_user
    if [ "${databse_user}" ]; then
      STARTHINKER_UI_DATABASE_USER="${database_user}"
    else
      echo "Database User Unchanged"
    fi
  else
    echo "Using Existing Database User"
  fi

  if [ "$optional_password" != "optional" ] || [ "${STARTHINKER_UI_DATABASE_PASSWORD}" == "" ]; then
    read -p "Databse Password - ${STARTHINKER_UI_DATABASE_PASSWORD} ( blank to skip ): " database_password
    if [ "${databse_password}" ]; then
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


################################################################################
#
#  make migrations for configured database
#
migrate_database() {
  echo ""
  echo "----------------------------------------"
  echo "Setup Database"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_CONFIG}" --load;
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" makemigrations;
  python "${STARTHINKER_ROOT}/starthinker_ui/manage.py" migrate;
  deactivate

  echo "Done"
  echo ""
}


################################################################################
#
#  set project id in data file and constant
#
setup_project() {
  optional_project=$1

  echo ""
  echo "----------------------------------------"
  echo "Set Cloud Project"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_project" != "optional" ] || [ "${STARTHINKER_PROJECT}" == "" ]; then

    read -p "Cloud Project ID - ${STARTHINKER_PROJECT} ( blank to skip ): " cloud_id

    if [ "${cloud_id}" ]; then
      STARTHINKER_PROJECT="${cloud_id}"
    else
      echo "Project ID Unchanged"
    fi
  else
    echo "Using Existing Project ID"
  fi

  echo "Done"
  echo ""
}


################################################################################
#
# download credentials - client and service, then generate user
#
setup_credentials() {
  optional_credentials=$1

  echo ""
  echo "----------------------------------------"
  echo "Setup Credentials"
  echo "----------------------------------------"
  echo ""

  if [ "$optional_credentials" != "optional" ] || [ ! -f "$STARTHINKER_CLIENT" ]; then

    # client
    echo "Retrieve OAuth Client ID credentials from: https://console.cloud.google.com/apis/credentials"
    echo "Application type: Other"
    echo "Paste in your client credentials here: ( CTRL+D to skip )"

    read_multiline "}}"

    if [ "${read_multiline_return}" ];then
      printf "%s" "$read_multiline_return" > "${STARTHINKER_CLIENT}"
    fi
  else
    echo "Using Existing Client Credentials"
  fi

  if [ "$optional_credentials" != "optional" ] || [ ! -f "$STARTHINKER_SERVICE" ]; then
    # service
    echo ""
    echo "Retrieve Service account key credentials from: https://console.cloud.google.com/apis/credentials"
    echo "Key type: JSON"
    echo "Paste in your service credentials: ( CTRL+D to skip )"

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

################################################################################
#
# download credentials - client and service, then generate user
#
setup_user() {
  echo ""
  echo "----------------------------------------"
  echo "Using client credentials to get user credentials..."
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ENV}/bin/activate"
  python "${THIS_DIR}/starthinker/auth/helper.py" -c "${STARTHINKER_CLIENT}" -u "${STARTHINKER_USER}"
  deactivate

  echo "Done"
  echo ""
}


################################################################################
#
# upgrade apt - allows safe pip install of requirements
#
update_apt() {
  echo ""
  echo "----------------------------------------"
  echo "Update Debian Installer"
  echo "----------------------------------------"
  echo ""

  sudo apt-get update -qq > /dev/null

  echo "Done"
  echo ""
}


################################################################################
#
# install virtualenv - allows safe pip install of requirements
#
install_virtualenv() {

  echo ""
  echo "----------------------------------------"
  echo "Install Virtual Environment"
  echo "----------------------------------------"
  echo ""

  if [ $(command -v pip) == "" ]; then
    sudo apt-get install python-pip -qq > /dev/null
  fi

  pip install --quiet --upgrade pip
  pip install --quiet virtualenv
  virtualenv ${STARTHINKER_ENV}

  echo "Done"
  echo ""
}


################################################################################
#
#  install requirements - leverage virtual env
#
install_requirements() {

  echo ""
  echo "----------------------------------------"
  echo "Install StarThinker Requirements"
  echo "----------------------------------------"
  echo ""

  source "${STARTHINKER_ENV}/bin/activate"
  pip install --quiet -r ${THIS_DIR}/requirements.txt
  pip install --quiet -r ${THIS_DIR}/starthinker_ui/requirements.txt
  deactivate

  echo "Done"
  echo ""
}


################################################################################
#
#  install repository - fetch starthinker code
#
install_repository() {

  echo ""
  echo "----------------------------------------"
  echo "Install Git And Clone Repository"
  echo "----------------------------------------"
  echo ""

  if [ $(command -v git) == "" ]; then
    sudo apt install git
  fi
  git clone https://github.com/google/starthinker

  echo "Done"
  echo ""
}


################################################################################
#
#  install docker - download and configure docker
#
install_docker() {

  echo ""
  echo "----------------------------------------"
  echo "Install Docker"
  echo "----------------------------------------"
  echo ""

  curl -fsSL get.docker.com -o get-docker.sh
  sh get-docker.sh
  sudo usermod -aG docker $USER
  sudo service docker start
}


################################################################################
#
#  setup docker - create an image with the latest docker tag
#
setup_docker() {
  docker --version

  if [ ! $? -eq 0 ]
  then
    echo ""
    echo -e "\e[31m[ERROR] \e[0mIt looks like docker isn't installed, please go to https://www.docker.com/get-started to install it "
    exit 1
  else
    echo ""
    echo "Docker is installed"
  fi
}

################################################################################
#
#  build docker - create an image with the latest docker tag
#
build_docker() {
  echo ""
  echo "----------------------------------------"
  echo "Build Docker Form Latest Tag"
  echo "----------------------------------------"
  echo ""
  echo "StarThinker allows versioned code to run, so you don't have to upgrade recipes as code changes."
  echo "To version code, simply tag it and create a docker image of the latest tag."
  echo ""
  echo "To create a <tag name>: ( Google tag StarThinker code prior to release: https://github.com/google/starthinker/tags )"
  echo "   - After the git commit and git push"
  echo "   - git tag <tag name>"
  echo "   - git push origin <tag name>"
  echo "   - source install/deploy.sh"
  echo "   - Select the docker deploy option, it will build and deploy a new docker image wiht the latest tag."
  echo "   - Your recipe deployed to workers can now use this version of the StarThinker code ( Setup Worker )."
  echo ""
  echo "To make a recipe use a version of StarThinker code:"
  echo "   - In a recipe include {\"setup\":{ \"version\":\"<tag name>\" }}"
  echo "   - That tag must exist otherwise you'll get an error in the logs."
  echo ""

  setup_gcloud;
  setup_docker;

  docker_Project=$(echo $STARTHINKER_PROJECT | tr : /)

  if [[ $# -eq 1 ]] ; then
    docker_Tag=$1
  else
    docker_Tag=$(git --git-dir=$STARTHINKER_ROOT/.git describe --tags)
  fi

  gcloud auth configure-docker --quiet

  echo "Creating docker image: gcr.io/$docker_Project/starthinker:$docker_Tag"
  cp $STARTHINKER_ROOT/.gitignore $STARTHINKER_ROOT/.dockerignore
  docker build --progress auto --no-cache -t "gcr.io/$docker_Project/starthinker:latest" -t "gcr.io/$docker_Project/starthinker:$docker_Tag" -f $STARTHINKER_CODE/install/Dockerfile $THIS_DIR
  docker push "gcr.io/$docker_Project/starthinker:latest"
  docker push "gcr.io/$docker_Project/starthinker:$docker_Tag"

  echo "Done"
  echo ""
}


################################################################################
#
#  setup swap - Give the instance some overflow memory
#
setup_swap() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Swap"
  echo "----------------------------------------"
  echo ""

  sudo swapoff /swapfile;
  sudo rm /swapfile;

  sudo fallocate -l 10G /swapfile;
  sudo chmod 600 /swapfile;
  sudo mkswap /swapfile;
  sudo swapon /swapfile;
  echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab;

}


################################################################################
#
#  set domain for UI deployment or default to instance IP
#
setup_domain() {
  optional_domain=$1

  echo ""
  echo "----------------------------------------"
  echo "Set UI Domain - $STARTHINKER_UI_DOMAIN"
  echo "----------------------------------------"
  echo ""
  echo "To deploy the webserver on an IP address, leave this blank."
  echo "The domain must be valid and pointed at the instance via registrar."
  echo "Leave Domain blank to defualt to IP or native domain of instance."
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


################################################################################
#
#  initialize variables - load configuration from file on load always
#
load_config;


################################################################################
#
#  reset paths - when copying assets paths need to be realigned to new destination
#
if [ "$1" == '--repath' ];then

  if [ -d "${PWD}/starthinker" ]; then
    THIS_DIR=$PWD
    save_config;
  fi

fi
