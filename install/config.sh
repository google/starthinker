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
CLIENT_CREDENTIALS="${HOME}/starthinker_client.json"
SERVICE_CREDENTIALS="${HOME}/starthinker_service.json"
USER_CREDENTIALS="${HOME}/starthinker_user.json"
CRON_DIRECTORY="${HOME}/starthinker_cron"
DATA_FILE="${HOME}/starthinker.txt"
CLOUD_PROJECT_ID=""


################################################################################
#
# load project id from file between sessions ( only item in file )
#
if [ -e "${DATA_FILE}" ];then
  CLOUD_PROJECT_ID=`cat "${DATA_FILE}"`
fi


################################################################################
#
#  read multiline example
#
#  read_multiline "}}"
#  if [ "${read_multiline_return}" ];then
#    printf "%s" "$read_multiline_return" > "${CLIENT_CREDENTIALS}"
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
#  set project id in data file and constant
#
setup_project() {

  echo ""
  echo "----------------------------------------"
  echo "Set Cloud Project - ${CLOUD_PROJECT_ID}"
  echo ""

  read -p "Cloud Project ID ( blank to skip ): " cloud_id

  if [ "${cloud_id}" ];then
    CLOUD_PROJECT_ID="${cloud_id}"
    echo $CLOUD_PROJECT_ID > "${DATA_FILE}"
    echo "Project ID Saved"
  else
    echo "Project ID Unchanged"
  fi
}

################################################################################
#
# download credentials - client and service, then generate user
#
setup_credentials() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Credentials"
  echo ""

  # client
  echo "Retrieve OAuth Client ID credentials from: https://console.cloud.google.com/apis/credentials"
  echo "Application type: Other"
  echo "Paste in your client credentials here: ( CTRL+D to skip )"

  read_multiline "}}"

  if [ "${read_multiline_return}" ];then
    printf "%s" "$read_multiline_return" > "${CLIENT_CREDENTIALS}"
  fi

  # service
  echo ""
  echo "Retrieve Service account key credentials from: https://console.cloud.google.com/apis/credentials"
  echo "Key type: JSON"
  echo "Paste in your service credentials: ( CTRL+D to skip )"

  read_multiline "}"

  if [ "${read_multiline_return}" ];then
    printf "%s" "$read_multiline_return" > "${SERVICE_CREDENTIALS}"
  fi


  if [ "${read_multiline_return}" ];then
    printf "%s" "$read_multiline_return" > "${SERVICE_CREDENTIALS}"
  fi

  # user
  echo ""
  echo "Using client credentials to get user credentials..."

  python auth/helper.py -c "${CLIENT_CREDENTIALS}" -u "${USER_CREDENTIALS}"

  echo "Credentials Setup Finished"
  echo ""
}
