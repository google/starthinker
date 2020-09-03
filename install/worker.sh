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


firewall_create()
{
  values=$(gcloud compute firewall-rules list --filter="name=default-allow-ssh" --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud compute firewall-rules create default-allow-ssh --allow tcp:22
  else
    echo "Firewall rule already exists."
  fi
}


instance_create()
{
  create_INSTANCE=$1
  create_MACHINE=$2

  values=$(gcloud compute instances list --filter="name=$create_INSTANCE" --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud compute instances create $create_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE --machine-type=$create_MACHINE --boot-disk-size=200GB --scopes https://www.googleapis.com/auth/cloud-platform
  else
    gcloud compute instances start $create_INSTANCE --zone=$STARTHINKER_ZONE
    echo "Instance already exists."
  fi
}


instance_start()
{
  start_INSTANCE=$1
  values=$(gcloud compute instances list --filter="status=RUNNING name=$start_INSTANCE" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud compute instances start $start_INSTANCE --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE
  else
    echo "Instance already running."
  fi
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
  instance_command $copy_INSTANCE "sudo rm -rf $copy_DESTINATION_FILENAME"
  gcloud compute scp $copy_SOURCE_FILENAME $copy_INSTANCE:$copy_DESTINATION_FILENAME --project=$STARTHINKER_PROJECT --zone=$STARTHINKER_ZONE $copy_RECURSIVE --compress --scp-flag="-o ServerAliveInterval=30"
}


start_worker_proxy() {
  echo ""
  echo "----------------------------------------"
  echo "Start Worker Proxy - sudo systemctl status starthinker_proxy"
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
  sudo systemctl enable starthinker_proxy
  #sudo systemctl restart starthinker_proxy

  echo ""
  echo "Done"
  echo ""
}


start_worker() {
  worker_PARAMETERS=${@}

  echo ""
  echo "----------------------------------------"
  echo "Start Worker - sudo systemctl status starthinker"
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
Environment=STARTHINKER_WORKER_MAX=$STARTHINKER_WORKER_MAX
Environment=STARTHINKER_WORKER_JOBS=$STARTHINKER_WORKER_JOBS
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
ExecStart=$STARTHINKER_ENV/bin/python3 $STARTHINKER_ROOT/starthinker_ui/manage.py job_worker $worker_PARAMETERS

[Install]
WantedBy=multi-user.target
EOL

  sudo systemctl daemon-reload
  sudo systemctl enable starthinker
  #sudo systemctl restart starthinker

  echo ""
  echo "Done"
  echo ""
}


setup_worker() {

  echo ""
  echo "----------------------------------------"
  echo "Setup Worker"
  echo "----------------------------------------"
  echo ""
  echo "This will create Google Cloud VM Instances in project $STARTHINKER_PROJECT to run jobs."
  echo ""
  echo "Up To Date Pricing: https://cloud.google.com/compute/pricing"
  echo "Worker List: https:/console.cloud.google.com/compute/instances?project=$STARTHINKER_PROJECT"
  echo ""
  echo " - Pricing is subject to change, these estimates were roughly valid on Oct 2019 for US Central zone."
  echo " - StarThinker workers catch shutdown signals and attempt to gracefully finish jobs before shutdown."
  echo ""
  echo "WARNING: Your zone is set to $STARTHINKER_ZONE, you must delete any StarThinker workers outside this zone before launching new ones."
  echo ""

  setup_credentials_service;
  setup_credentials_ui;
  save_config;
  firewall_create;

  instance_name="starthinker-worker-instance"
  instance_image="starthinker-worker-image-$(date '+%Y-%m-%d-%H-%M-%S')"

  echo ""
  echo "----------------------------------------"
  echo "Configure Worker Instance - $instance_name: $STARTHINKER_WORKER_INSTANCE x $STARTHINKER_WORKER_JOBS job handlers"
  echo "----------------------------------------"
  echo ""

  instance_create $instance_name "${STARTHINKER_WORKER_INSTANCE}"

  sleep 60s

  instance_command "$instance_name" "sudo systemctl stop starthinker"
  instance_command "$instance_name" "sudo systemctl stop starthinker_proxy"

  find . -name '*.pyc' -delete

  instance_copy "$instance_name" "${STARTHINKER_ROOT}/starthinker_assets" "~/starthinker_assets/" --recurse
  instance_copy "$instance_name" "${STARTHINKER_ROOT}/starthinker_ui" "~/starthinker_ui/" --recurse
  instance_copy "$instance_name" "${STARTHINKER_ROOT}/scripts" "~/scripts/" --recurse
  instance_copy "$instance_name" "${STARTHINKER_ROOT}/starthinker" "~/starthinker/" --recurse
  instance_copy "$instance_name" "${STARTHINKER_ROOT}/install" "~/install/" --recurse
  instance_copy "$instance_name" "${STARTHINKER_ROOT}/requirements.txt" "~/requirements.txt"

  instance_command "$instance_name" "source install/worker.sh --instance --jobs $STARTHINKER_WORKER_JOBS"

  gcloud compute instances stop "$instance_name" --zone=$STARTHINKER_ZONE

  echo ""
  echo "----------------------------------------"
  echo "Create Image - starthinker-worker-family"
  echo "----------------------------------------"
  echo ""

  gcloud compute images create $instance_image --project=$STARTHINKER_PROJECT --description="Worker configuration." --family=starthinker-worker-family --source-disk=$instance_name --source-disk-zone=$STARTHINKER_ZONE

  echo ""
  echo "----------------------------------------"
  echo "Create Template - starthinker-worker-template"
  echo "----------------------------------------"
  echo ""

  values=$(gcloud compute instance-templates list --filter="name=starthinker-worker-template" --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud compute --project=$STARTHINKER_PROJECT instance-templates create starthinker-worker-template --machine-type=$STARTHINKER_WORKER_INSTANCE --network=projects/$STARTHINKER_PROJECT/global/networks/default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=default --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --image-family=starthinker-worker-family --image-project=$STARTHINKER_PROJECT --boot-disk-size=200GB --boot-disk-type=pd-standard --boot-disk-device-name=starthinker-worker-template --reservation-affinity=any
  else
    echo "Template already exists."
  fi

  echo ""
  echo "----------------------------------------"
  echo "Create Managed Instance Group - starthinker-worker-group"
  echo "----------------------------------------"
  echo ""

  values=$(gcloud compute instance-groups managed list --filter="name=starthinker-worker-group" --format="value(name)" --verbosity=none)
  if [ -z "${values}" ]; then
    gcloud compute --project=$STARTHINKER_PROJECT instance-groups managed create starthinker-worker-group --base-instance-name=$instance_name --template=starthinker-worker-template --size=0 --description="Worker auto scaling group" --zone=$STARTHINKER_ZONE
  else
    echo "Group already exists."
  fi

  echo ""
  echo "----------------------------------------"
  echo "Roll Managed Instance Group  Workers - custom.googleapis.com/starthinker/worker/usage"
  echo "----------------------------------------"
  echo ""

  gcloud compute instance-groups managed rolling-action replace starthinker-worker-group --max-surge="0" --max-unavailable="100%" --zone=$STARTHINKER_ZONE

  echo "Done"
  echo ""
}

if [ "$1" = "--instance" ];then
  shift
  worker_PARAMETERS=${@}

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh --no_user

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
