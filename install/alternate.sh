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


install_postgress() {
  echo ""
  echo "----------------------------------------"
  echo "Install Postgre SQL Database"
  echo "----------------------------------------"
  echo ""

  sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib -qq > /dev/null
  sudo -u postgres bash -c "psql -c \"CREATE USER starthinker_user WITH PASSWORD 'starthinker_password';\""
  sudo -u postgres bash -c "psql -c \"CREATE DATABASE starthinker;\""
  sudo -u postgres bash -c "psql -c \"ALTER ROLE starthinker_user SET default_transaction_isolation TO 'read committed';\""
  sudo -u postgres bash -c "psql -c \"ALTER ROLE starthinker_user SET timezone TO 'UTC';\""
  sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE starthinker TO starthinker_user;\""

  echo "Done"
  echo ""
}


configure_linux_ui() {

  echo ""
  echo "----------------------------------------"
  echo "Configure StarThinker UI"
  echo "----------------------------------------"
  echo ""

  STARTHINKER_SCALE=1
  STARTHINKER_MANAGERS=1
  STARTHINKER_WORKERS=6
  STARTHINKER_DEVELOPMENT=0

  STARTHINKER_UI_DATABASE_ENGINE="django.db.backends.postgresql";
  STARTHINKER_UI_DATABASE_HOST="localhost";
  STARTHINKER_UI_DATABASE_NAME="starthinker";
  STARTHINKER_UI_DATABASE_USER="starthinker_user";
  STARTHINKER_UI_DATABASE_PASSWORD="starthinker_password";
  STARTHINKER_UI_DATABASE_PORT="";

  if [ "$STARTHINKER_UI_DOMAIN" == "" ]; then
    STARTHINKER_UI_DOMAIN=$(curl -s -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
  fi

  echo ""
  echo "CAUTION: Configures UI credentials and recipe buckets in same cloud projec."
  echo "CAUTION: For added security please edit STARTHINKER_RECIPE_PROJECT in config to be dofferent."
  echo ""
  STARTHINKER_RECIPE_PROJECT=$STARTHINKER_PROJECT
  STARTHINKER_RECIPE_SERVICE=$STARTHINKER_SERVICE
  save_config;

  echo "Done"
  echo ""
}


install_ssl() {
  echo ""
  echo "----------------------------------------"
  echo "Configure SSL"
  echo "----------------------------------------"
  echo ""

  openssl genrsa -out ${STARTHINKER_KEY} 2048
  openssl req -new -key ${STARTHINKER_KEY} -out ${STARTHINKER_CSR} -subj "/C=US/ST=California/L=San 
Francisco/O=Google gTEch/OU=IT Department/CN=ssl.google.com"
  openssl x509 -req -days 365 -in ${STARTHINKER_CSR} -signkey ${STARTHINKER_KEY} -out ${STARTHINKER_CRT}

  echo "Done"
  echo ""
}


install_uwsgi() {
  echo ""
  echo "----------------------------------------"
  echo "Configure uWSGI"
  echo "----------------------------------------"
  echo ""

  sudo pip2 install --quiet uwsgi
  sudo mkdir -p /etc/uwsgi/sites
  sudo bash -c "cat > /etc/uwsgi/sites/starthinker.ini" << EOL
[uwsgi]
plugin = python
uid = $USER
gid = www-data
project = starthinker
base = ${THIS_DIR}
pythonpath = %(base) 
chdir = %(base)/%(project)
home = %(base)/starthinker_assets/env
virtualenv = %(base)/starthinker_assets/env
env = STARTHINKER_SCALE=$STARTHINKER_SCALE
env = STARTHINKER_WORKERS=$STARTHINKER_WORKERS
env = STARTHINKER_MANAGERS=$STARTHINKER_MANAGERS
env = STARTHINKER_PROJECT=$STARTHINKER_PROJECT
env = STARTHINKER_ZONE=$STARTHINKER_ZONE
env = STARTHINKER_TOPIC=$STARTHINKER_TOPIC
env = STARTHINKER_CLIENT=$STARTHINKER_CLIENT
env = STARTHINKER_SERVICE=$STARTHINKER_SERVICE
env = STARTHINKER_USER=$STARTHINKER_USER
env = STARTHINKER_CRON=$STARTHINKER_CRON
env = STARTHINKER_ENV=$STARTHINKER_ENV
env = STARTHINKER_CRT=$STARTHINKER_CRT
env = STARTHINKER_KEY=$STARTHINKER_KEY
env = STARTHINKER_CSR=$STARTHINKER_CSR
env = STARTHINKER_CONFIG=$STARTHINKER_CONFIG
env = STARTHINKER_CODE=$STARTHINKER_CODE
env = STARTHINKER_ROOT=$STARTHINKER_ROOT
env = STARTHINKER_UI_DEVELOPMENT=True
env = STARTHINKER_UI_DOMAIN=$STARTHINKER_UI_DOMAIN
env = STARTHINKER_UI_SECRET=$STARTHINKER_UI_SECRET
env = STARTHINKER_UI_DATABASE_ENGINE=$STARTHINKER_UI_DATABASE_ENGINE
env = STARTHINKER_UI_DATABASE_HOST=$STARTHINKER_UI_DATABASE_HOST
env = STARTHINKER_UI_DATABASE_NAME=$STARTHINKER_UI_DATABASE_NAME
env = STARTHINKER_UI_DATABASE_USER=$STARTHINKER_UI_DATABASE_USER
env = STARTHINKER_UI_DATABASE_PASSWORD=$STARTHINKER_UI_DATABASE_PASSWORD
env = STARTHINKER_UI_DATABASE_PORT=$STARTHINKER_UI_DATABASE_PORT
env = STARTHINKER_RECIPE_PROJECT=$STARTHINKER_RECIPE_PROJECT
env = STARTHINKER_RECIPE_SERVICE=$STARTHINKER_RECIPE_SERVICE
module = %(project).ui.ui.wsgi:application
master = true
processes = 2
chown-socket = %(uid):%(gid)
chmod-socket = 664
socket = /run/uwsgi/%(project).sock
vacuum = true
EOL
  sudo bash -c "cat > /etc/systemd/system/uwsgi.service" << EOL
[Unit]
Description=uWSGI Emperor service
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
EOL
  sudo mkdir -p /run/uwsgi
  sudo chown $USER:www-data /run/uwsgi/
  sudo chown $USER:www-data starthinker/
  sudo systemctl daemon-reload
  sudo systemctl start uwsgi
  sudo systemctl enable uwsgi
  sleep 15
  echo "Done"
  echo ""
}
  

install_nginx() {
  echo ""
  echo "----------------------------------------"
  echo "Configure Nginx"
  echo "----------------------------------------"
  echo ""
  sudo apt-get install nginx -qq > /dev/null
  sudo bash -c "cat > /etc/nginx/sites-available/starthinker" << EOL
server {
  listen 80 default_server;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;

  server_name _;

  ssl_certificate "$STARTHINKER_UI_CRT";
  ssl_certificate_key "$STARTHINKER_UI_KEY";

  location = /favicon.ico { access_log off; log_not_found off; }
  location / {
    include uwsgi_params;
    uwsgi_pass unix:/run/uwsgi/starthinker.sock;
  }
}
EOL
  sudo bash -c "cat > /etc/nginx/nginx.conf" << EOL
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
events {
  worker_connections 768;
  # multi_accept on;
}
http {

  ##
  # Basic Settings
  ##
  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  # server_tokens off;
  # server_names_hash_bucket_size 64;
  # server_name_in_redirect off;
  include /etc/nginx/mime.types;
  default_type application/octet-stream;

  ##
  # SSL Settings
  ##
  ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
  ssl_prefer_server_ciphers on;

  ##
  # Logging Settings
  ##
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;

  ##
  # Gzip Settings
  ##
  gzip on;
  gzip_disable "msie6";
  # gzip_vary on;
  # gzip_proxied any;
  # gzip_comp_level 6;
  # gzip_buffers 16 8k;
  # gzip_http_version 1.1;
  # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

  ##
  # Virtual Host Configs
  ##
  include /etc/nginx/conf.d/*.conf;
  include /etc/nginx/sites-enabled/*;
}
EOL
  sudo rm /etc/nginx/sites-available/default 
  sudo ln -s /etc/nginx/sites-available/starthinker /etc/nginx/sites-enabled/starthinker
  sudo nginx -t
  sudo systemctl daemon-reload
  sudo systemctl restart nginx
  sudo systemctl enable nginx
  echo "Done"
  
  echo ""
  echo "------------------------------------------------------------------------------"
  echo "The StarThinker Reference UI Is Ready"
  echo ""
  echo "- Review all configurations, Google does not warranty this install in any way."
  echo "- Visit By IP: https://$INSTANCE_IP"
  if [ "$STARTHINKER_UI_DOMAIN" ];then
    echo "- Visit By Domain: https://$STARTHINKER_UI_DOMAIN"
  fi
  echo ""
  echo "- StarThinker settings:"
  echo "  - starthinker/config.py"
  echo "  - starthinker_ui/ui/settings_open.py"
  echo ""
  echo "- Web server settings:"
  echo "  - /etc/uwsgi/sites/starthinker.ini"
  echo "  - /etc/systemd/system/uwsgi.service" 
  echo "  - /etc/nginx/sites-available/starthinker"
  echo "  - /etc/nginx/nginx.conf" 
  echo ""
  echo "- Useful commands:"
  echo "  - sudo systemctl status uwsgi"
  echo "  - sudo systemctl restart uwsgi"
  echo "  - sudo systemctl restart nginx"
}


setup_linux() {

  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "Linux Setup - Instance Called stathinker_ui"
  echo ""
  echo "------------------------------------------------------------------------------"
  echo ""
  echo "StartThinker provides a full stack Nginx / Postgress / Django powered server for customzable deployments."
  echo "The UI works best with a Worker Setup and Docker Build. We suggest running those as well."
  echo ""
  echo "------------------------------------------------------------------------------"
  echo "This script will set up a public HTTPS server on a cloud instance machine running StarThinker UI."
  echo "You must enable the HTTP/HTTPS ports and add firewall restrictions on your own."
  echo ""
  echo "This script will create the following files on the remote server."
  echo "  - $STARTHINKER_CONFIG"
  echo "  - $STARTHINKER_ENV"
  echo "  - $STARTHINKER_CLIENT"
  echo "  - $STARTHINKER_SERVICE"
  echo "  - $STARTHINKER_USER"
  echo "  - $STARTHINKER_CRT"
  echo "  - $STARTHINKER_KEY"
  echo "  - $STARTHINKER_CSR"
  echo ""
  echo "This script will overwrite the following remote server files:"
  echo "  - /etc/uwsgi/sites/starthinker.ini"
  echo "  - /etc/systemd/system/uwsgi.service" 
  echo "  - /etc/nginx/sites-available/starthinker"
  echo "  - /etc/nginx/nginx.conf" 
  echo ""
  echo ""
  echo "This will create a StarThinker UI instances in Google Cloud project $STARTHINKER_PROJECT."
  echo ""
  read -p "Do you wish to proceed (y/n)? " -n 1 -r
  echo ""
  echo ""
  
  setup_project "optional";
  setup_credentials "optional";
  setup_domain "optional";
  setup_database "optional" "optional" "optional";
  save_config;

  setup_gcloud;

  gcloud_service;
  gcloud_firewall_ssh;
  gcloud_firewall_https;

  echo ""
  echo "INSTANCE: starthinker-ui" 

  instance_create "starthinker-ui"
  instance_start "starthinker-ui"

  instance_copy "starthinker-ui" $STARTHINKER_CLIENT starthinker_assets/client.json
  instance_copy "starthinker-ui" $STARTHINKER_SERVICE starthinker_assets/service.json
  instance_copy "starthinker-ui" $STARTHINKER_CONFIG starthinker_assets/config.sh
  instance_copy "starthinker-ui" $STARTHINKER_CODE starthinker/

  instance_command "starthinker-ui" "source install/alternate.sh --instance"

  echo "Done"
  echo ""
}


if [ "$1" == '--instance' ];then

  if [ -d "${PWD}/install" ]; then

    THIS_DIR=$PWD
    source ${THIS_DIR}/install/config.sh
    source ${THIS_DIR}/install/worker.sh

    update_apt;
    install_virtualenv;
    install_postgress;

    configure_linux_ui;

    install_requirements;
    migrate_database;
    install_ssl;
    install_uwsgi;
    install_nginx;

  else

    echo ""
    echo "Directory starthinker not found."
    echo "This utility must be run from the directory containing the starthinker directory."
    echo "Please change directories and try again."
    echo ""

  fi

fi

