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
  create_MACHINE=$2
  gcloud compute instances create $create_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --machine-type=$create_MACHINE --boot-disk-size=200GB --scopes https://www.googleapis.com/auth/cloud-platform
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
  copy_RECURSIVE=$4
  instance_command $copy_INSTANCE "rm -rf $copy_DESTINATION_FILENAME"
  gcloud compute scp $copy_SOURCE_FILENAME $copy_INSTANCE:$copy_DESTINATION_FILENAME --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE $copy_RECURSIVE --compress --scp-flag="-o ServerAliveInterval=30"
}


start_worker_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Start Worker Proxy"
  echo "----------------------------------------"
  echo ""

  sudo bash -c "cat > /etc/systemd/system/starthinker_proxy.service" << EOL
[Install]
WantedBy=multi-user.target

[Unit]
Description=Google Cloud Compute Engine SQL Proxy
Requires=networking.service
After=networking.service
StartLimitIntervalSec=0
StartLimitBurst=60

[Service]
Type=simple
Restart=always
RestartSec=5
TimeoutSec=10
WorkingDirectory=$STARTHINKER_ROOT/starthinker_assets
ExecStart="${STARTHINKER_ROOT}/starthinker_database/cloud_sql_proxy" -instances="$STARTHINKER_PROJECT:$STARTHINKER_REGION:$STARTHINKER_UI_PRODUCTION_DATABASE_NAME"=tcp:5432 -credential_file $STARTHINKER_SERVICE
StandardOutput=journal
User=root
EOL

  sudo systemctl daemon-reload
  sudo systemctl restart starthinker_proxy
  sudo systemctl enable starthinker_proxy

  echo ""
  echo "Check status using: sudo systemctl status starthinker_proxy"
  echo ""
  echo "Done"
  echo ""
}


start_worker() {
  worker_PARAMETERS=${@}

  echo ""
  echo "----------------------------------------"
  echo "Start Worker"
  echo "----------------------------------------"
  echo ""

  sudo bash -c "cat > /etc/systemd/system/starthinker.service" << EOL
[Unit]
Description=Starthinker Worker Service
After=multi-user.target starthinker_proxy.service
StartLimitIntervalSec=0
StartLimitBurst=60

[Service]
Type=simple
Restart=always
RestartSec=5
TimeoutSec=10
Environment=STARTHINKER_SCALE=$STARTHINKER_SCALE
Environment=STARTHINKER_DEVELOPMENT=$STARTHINKER_DEVELOPMENT
Environment=STARTHINKER_PROJECT=$STARTHINKER_PROJECT
Environment=STARTHINKER_ZONE=$STARTHINKER_ZONE
Environment=STARTHINKER_CLIENT_WEB=$STARTHINKER_CLIENT_WEB
Environment=STARTHINKER_SERVICE=$STARTHINKER_SERVICE
Environment=STARTHINKER_ROOT=$STARTHINKER_ROOT
Environment=STARTHINKER_CRON=$STARTHINKER_CRON
Environment=STARTHINKER_UI_DATABASE_ENGINE=$STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE
Environment=STARTHINKER_UI_DATABASE_HOST=$STARTHINKER_UI_PRODUCTION_DATABASE_HOST
Environment=STARTHINKER_UI_DATABASE_PORT=$STARTHINKER_UI_PRODUCTION_DATABASE_PORT
Environment=STARTHINKER_UI_DATABASE_NAME=$STARTHINKER_UI_PRODUCTION_DATABASE_NAME
Environment=STARTHINKER_UI_DATABASE_USER=$STARTHINKER_UI_PRODUCTION_DATABASE_USER
Environment=STARTHINKER_UI_DATABASE_PASSWORD=$STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD
Environment=STARTHINKER_UI_DOMAIN=$STARTHINKER_UI_PRODUCTION_DOMAIN
Environment=STARTHINKER_UI_SECRET=$STARTHINKER_UI_PRODUCTION_SECRET
Environment=PYTHONPATH=$STARTHINKER_ROOT
WorkingDirectory=$THIS_DIR
ExecStart=$STARTHINKER_ENV/bin/python $STARTHINKER_ROOT/starthinker_ui/manage.py job_worker $worker_PARAMETERS

[Install]
WantedBy=multi-user.target
EOL

  sudo systemctl daemon-reload
  sudo systemctl restart starthinker
  sudo systemctl enable starthinker

  echo ""
  echo "Check status using: sudo systemctl status starthinker"
  echo ""
  echo "Done"
  echo ""
}

deploy_worker() {
  instance_Label=$1
  instance_Type=$2
  instance_Workers=$3
  instance_Jobs=$4

  setup_project "optional";
  setup_credentials_service "optional";
  setup_credentials_ui "optional";
  save_config;

  echo ""
  echo "----------------------------------------"
  echo "Deploy Worker Instances - $instance_Label: $instance_Type ( $instance_Workers x $instance_Jobs )"
  echo "----------------------------------------"
  echo ""

  setup_gcloud;

  gcloud_service;
  gcloud_firewall_ssh;

  for ((instance=1;instance<=instance_Workers;instance++)); do
    instance_name="starthinker-${instance_Label}-${instance}"

    echo ""
    echo "----------------------------------------"
    echo "Deploy Instance: $instance_name" 
    echo "----------------------------------------"
    echo ""

    instance_create "$instance_name" "$instance_Type"
    instance_start "$instance_name"

    sleep 1m

    instance_command "$instance_name" "sudo systemctl stop starthinker"
    instance_command "$instance_name" "sudo systemctl stop starthinker_proxy"

    instance_copy "$instance_name" "${STARTHINKER_ROOT}/starthinker_assets" "starthinker_assets/" --recurse
    instance_copy "$instance_name" "${STARTHINKER_ROOT}/starthinker_ui" "starthinker_ui/" --recurse
    instance_copy "$instance_name" "${STARTHINKER_ROOT}/starthinker" "starthinker/" --recurse
    instance_copy "$instance_name" "${STARTHINKER_ROOT}/install" "install/" --recurse
    instance_copy "$instance_name" "${STARTHINKER_ROOT}/requirements.txt" "requirements.txt"

    instance_command "$instance_name" "source install/worker.sh --instance --jobs $instance_Jobs"
  done

  echo "Done"
  echo ""
}

setup_worker() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Worker"
  echo "----------------------------------------"
  echo ""
  echo "This will create Google Cloud Instances in project $STARTHINKER_PROJECT to run jobs."
  echo ""
  echo "Up To Date Pricing: https://cloud.google.com/compute/pricing"
  echo "Worker List: https:/console.cloud.google.com/compute/instances?project=$STARTHINKER_PROJECT"
  echo ""
  echo " - Pricing is subject to change, these estimates were roughly valid on Oct 2019 for US Central zone."
  echo " - StarThinker workers catch shutdown signals and attempt to gracefully finish jobs before shutdown."
  echo " - Its OK to simply terminate machines from the console."
  echo " - Deploying workers overwrites existing workers of the same kind."
  echo " - You will have to manually shutdown and delete any unused workers if you change configuration."
  echo ""

  worker_done=0
  worker_options=(
    "1   - 50 Recipes  = 1 x n1-highmem-4 x 2 jobs = 48 recipe hours  ( ~ \$37  / month )"
    "50  - 100 Recipes = 2 x n1-highmem-4 x 2 jobs = 96 recipe hours  ( ~ \$73  / month )"
    "100 - 200 Recipes = 3 x n1-highmem-4 x 2 jobs = 144 recipe hours ( ~ \$110 / month )"
    "200 - 300 Recipes = 4 x n1-highmem-4 x 2 jobs = 192 recipe hours ( ~ \$146 / month )"
    "300 - 400 Recipes = 5 x n1-highmem-4 x 2 jobs = 240 recipe hours ( ~ \$182 / month )"
    "400 - 500 Recipes = 4 x n1-highmem-8 x 3 jobs = 288 recipe hours ( ~ \$292 / month )"
    "500 - 600 Recipes = 5 x n1-highmem-8 x 3 jobs = 360 recipe hours ( ~ \$365 / month )"
    "600 - 700 Recipes = 6 x n1-highmem-8 x 3 jobs = 432 recipe hours ( ~ \$438 / month )"
  )

  while (( !worker_done ))
   do
    echo "----------------------------------------------------------------------"
    echo "Worker Deployment Menu"
    echo "----------------------------------------------------------------------"
    echo ""

    PS3='Your Choice ( q = Quit ): '
    select worker_option in "${worker_options[@]}"; do
      case $REPLY in
        1) deploy_worker "medium" "n1-highmem-4" 1 2; break ;;
        2) deploy_worker "medium" "n1-highmem-4" 2 2; break ;;
        3) deploy_worker "medium" "n1-highmem-4" 3 2; break ;;
        4) deploy_worker "medium" "n1-highmem-4" 4 2; break ;;
        5) deploy_worker "medium" "n1-highmem-4" 5 2; break ;;
        6) deploy_worker "large" "n1-highmem-8" 4 3; break ;;
        7) deploy_worker "large" "n1-highmem-8" 5 3; break ;;
        8) deploy_worker "large" "n1-highmem-8" 6 3; break ;;
        q) worker_done=1; break;;
        *) echo "What's that?" ;;
      esac
    done
    echo ""
  done
}

check_worker() {

  echo ""
  echo "----------------------------------------"
  echo "Check Workers"
  echo "----------------------------------------"

  for instance_name in $(gcloud compute instances list --filter="name~'^starthinker-.*'" --format="value(NAME)"); do

    echo ""
    echo "----------------------------------------"
    echo "INSTANCE PROXY: $instance_name"
    echo "----------------------------------------"
    instance_command "$instance_name" "sudo systemctl status starthinker_proxy"

    echo ""
    echo "----------------------------------------"
    echo "INSTANCE STARTHINKER: $instance_name"
    echo "----------------------------------------"
    instance_command "$instance_name" "sudo systemctl status starthinker"
    echo ""

  done

  echo "Done"
  echo ""
}


if [ "$1" = "--instance" ];then
  shift
  worker_PARAMETERS=${@}

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh

    export STARTHINKER_SCALE=5
    export STARTHINKER_DEVELOPMENT=0
    export STARTHINKER_UI_DATABASE_ENGINE="$STARTHINKER_UI_PRODUCTION_DATABASE_ENGINE"
    export STARTHINKER_UI_DATABASE_HOST="$STARTHINKER_UI_PRODUCTION_DATABASE_HOST"
    export STARTHINKER_UI_DATABASE_PORT="$STARTHINKER_UI_PRODUCTION_DATABASE_PORT"
    export STARTHINKER_UI_DATABASE_NAME="$STARTHINKER_UI_PRODUCTION_DATABASE_NAME"
    export STARTHINKER_UI_DATABASE_USER="$STARTHINKER_UI_PRODUCTION_DATABASE_USER"
    export STARTHINKER_UI_DATABASE_PASSWORD="$STARTHINKER_UI_PRODUCTION_DATABASE_PASSWORD"
    save_config; 

    make_cron;
    update_apt;
    install_proxy; # first so it installs psycopg dependencies
    install_virtualenv; # second because pip is here

    install_requirements; # second because pip is here
    install_requirements_ui; # second because pip is here

    setup_swap;
    start_worker_proxy;
    start_worker $worker_PARAMETERS;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the StarThinker directory containing the install folder."
    echo "Please change directories and try again."
    echo ""

  fi

fi
