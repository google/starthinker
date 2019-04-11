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


gcloud_service() {
  gcloud auth activate-service-account --project=$STARTHINKER_PROJECT --key-file=$STARTHINKER_SERVICE
}


gcloud_topic() {
  topic_Name=$1
  gcloud pubsub topics create $topic_Name --project=$STARTHINKER_PROJECT
}


gcloud_subscription() {
  subscription_Topic=$1
  subscription_Name=$2
  gcloud pubsub subscriptions create $subscription_Name --project=$STARTHINKER_PROJECT --topic=$subscription_Topic --topic-project=$STARTHINKER_PROJECT --message-retention-duration=24h
}


gcloud_firewall_ssh()
{
  gcloud compute firewall-rules create default-allow-ssh --allow tcp:22
}


gcloud_firewall_https()
{
  gcloud compute firewall-rules create default-allow-https --allow tcp:443
}


instance_create()
{
  create_INSTANCE=$1
  gcloud compute instances create $create_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --machine-type=g1-small --boot-disk-size=200GB --scopes https://www.googleapis.com/auth/cloud-platform
}


instance_start()
{
  start_INSTANCE=$1
  gcloud compute instances start $start_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE
}


instance_describe()
{
  describe_INSTANCE=$1
  gcloud compute instances describe $describe_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --format=list
}


instance_metadata()
{
  metadata_INSTANCE=$1
  metadata_KEY=$2
  metadata_VALUE=$3
  gcloud compute instances add-metadata $metadata_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --metadata=$metadata_KEY=$metadata_VALUE
}


instance_command()
{
  command_INSTANCE=$1
  command_COMMAND=$2
  gcloud compute ssh $command_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --command="$command_COMMAND"
}


instance_copy()
{
  copy_INSTANCE=$1
  copy_SOURCE_FILENAME=$2
  copy_DESTINATION_FILENAME=$3
  instance_command $copy_INSTANCE "rm -rf $copy_DESTINATION_FILENAME"
  gcloud compute scp $copy_SOURCE_FILENAME $copy_INSTANCE:$copy_DESTINATION_FILENAME --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --recurse --compress --scp-flag="-o ServerAliveInterval=30"
}


configure_worker() {

  STARTHINKER_SCALE=6
  STARTHINKER_MANAGERS=1
  STARTHINKER_WORKERS=6
  STARTHINKER_DEVELOPMENT=0
  save_config; 

  echo "Done"
  echo ""
}


start_worker() {

  sudo bash -c "cat > /etc/systemd/system/starthinker.service" << EOL
[Unit]
Description=Starthinker Worker Service
After=multi-user.target

[Service]
Type=simple
Environment=STARTHINKER_SCALE=$STARTHINKER_SCALE
Environment=STARTHINKER_WORKERS=$STARTHINKER_WORKERS
Environment=STARTHINKER_PROJECT=$STARTHINKER_PROJECT
Environment=STARTHINKER_ZONE=$STARTHINKER_ZONE
Environment=STARTHINKER_TOPIC=$STARTHINKER_TOPIC
Environment=STARTHINKER_CLIENT=$STARTHINKER_CLIENT
Environment=STARTHINKER_SERVICE=$STARTHINKER_SERVICE
Environment=STARTHINKER_USER=$STARTHINKER_USER
Environment=STARTHINKER_CRON=$STARTHINKER_CRON
Environment=STARTHINKER_ENV=$STARTHINKER_ENV
Environment=STARTHINKER_CODE=$STARTHINKER_CODE
Environment=STARTHINKER_ASSETS=$STARTHINKER_ASSETS
Environment=PYTHONPATH=$STARTHINKER_ROOT
WorkingDirectory=$THIS_DIR
ExecStart=$STARTHINKER_ENV/bin/python $STARTHINKER_CODE/manager/manager.py

[Install]
WantedBy=multi-user.target
EOL
  sudo systemctl daemon-reload
  sudo systemctl start starthinker
  sudo systemctl enable starthinker
}


setup_worker() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Worker"
  echo "----------------------------------------"
  echo "This will create $STARTHINKER_MANAGERS recipe manager instances in Google Cloud project $STARTHINKER_PROJECT."
  echo ""
  read -p "Do you wish to proceed (y/n)? " -n 1 -r
  echo ""
  echo ""

  setup_project "optional";
  setup_credentials "optional";
  save_config;

  setup_gcloud;

  gcloud_service;
  gcloud_firewall_ssh;

  gcloud_topic "${STARTHINKER_TOPIC}_worker"
  gcloud_topic "${STARTHINKER_TOPIC}_maintenance"
  gcloud_subscription "${STARTHINKER_TOPIC}_worker" "${STARTHINKER_TOPIC}"

  for ((instance=1;instance<=STARTHINKER_MANAGERS;instance++)); do
    echo ""
    echo "INSTANCE: starthinker-worker-$instance" 

    instance_create "starthinker-worker-$instance"
    instance_start "starthinker-worker-$instance"

    instance_command "starthinker-worker-$instance" "mkdir -p starthinker_assets"

    instance_copy "starthinker-worker-$instance" $STARTHINKER_CLIENT starthinker_assets/client.json
    instance_copy "starthinker-worker-$instance" $STARTHINKER_SERVICE starthinker_assets/service.json
    instance_copy "starthinker-worker-$instance" $STARTHINKER_CONFIG starthinker_assets/config.sh
    instance_copy "starthinker-worker-$instance" $STARTHINKER_CODE starthinker/

    instance_command "starthinker-worker-$instance" "source starthinker/install/worker.sh --instance"
  done

  echo "Done"
  echo ""
}


if [ "$1" == '--instance' ];then

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh

    update_apt;
    install_docker;
    install_virtualenv;

    configure_worker;

    install_requirements;
    setup_swap;
    start_worker;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the directory containing the starthinker directory."
    echo "Please change directories and try again."
    echo ""

  fi

fi
