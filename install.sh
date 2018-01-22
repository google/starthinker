#!/bin/bash

###########################################################################
#
#  Copyright 2017 Google Inc.
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

if [ "$1" = "ubuntu" ]
then
  echo "Ubuntu Install"

  sudo apt-get update
  sudo apt-get install python-setuptools python-dev build-essential
  sudo apt-get install python-pip

  # https://cloud.google.com/sdk/downloads#apt-get
  export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"
  echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo apt-get update 
  sudo apt-get install google-cloud-sdk

  sudo apt-get install git
  git clone sso://team/cse-dclk/starthinker_opensource

  sudo pip install google-api-python-client

elif [ "$1" = "google_ubuntu" ]
then
  echo "Google Ubuntu Install"

  sudo apt-get update
  sudo apt-get install python-setuptools python-dev build-essential
  sudo apt-get install python-pip

  gcert
  glogin

  # https://g3doc.corp.google.com/cloud/sdk/g3doc/index.md?cl=head#installing-and-using-the-cloud-sdk
  sudo goobuntu-add-repo -e cloud-sdk-trusty
  sudo apt-get update
  sudo apt-get install google-cloud-sdk

  sudo apt-get install uwsgi uwsgi-plugin-python
  git clone sso://team/cse-dclk/starthinker

  sudo pip install google-api-python-client
  sudo pip install google-cloud

elif [ "$1" = "osx" ]
then
  echo "OSX Install"
  # incomplete - please fill in

  sudo easy_install pip
  sudo pip install --upgrade google-cloud
  sudo pip install --upgrade google-api-python-client
  sudo pip install --upgrade requests

else
   echo "Unknown OS"
fi
