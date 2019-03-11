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

source starthinker/install/config.sh

install_dependencies() {
  echo "----------------------------------------"
  echo "Installing StarThinker UI On Debian"
  echo "- Update Debian Installer"
  echo "- Set Production Mode"
  echo "- Install Postgre SQL Database"
  echo "- Install Git And Clone Repository"
  echo "- Install Virtual Environment"
  echo "- Install StarThinker Requirements"
  echo "- Configure StarThinker: starthinker/config.py"
  echo "- Configure StarThinker: starthinker/ui/ui/settings_open.py"
  echo "- Configure uWSGI"
  echo "- Configure Nginx"
  
  echo ""
  echo "----------------------------------------"
  echo "Update Debian Installer"
  sudo apt-get update -qq > /dev/null
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Set Production Mode"
  sudo touch /mnt/SERVER
  sudo chmod 777 /mnt/SERVER
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Install Postgre SQL Database"
  sudo apt-get install python-dev libpq-dev postgresql postgresql-contrib -qq > /dev/null
  sudo -u postgres bash -c "psql -c \"CREATE USER starthinker_user WITH PASSWORD 'starthinker_password';\""
  sudo -u postgres bash -c "psql -c \"CREATE DATABASE starthinker;\""
  sudo -u postgres bash -c "psql -c \"ALTER ROLE starthinker_user SET default_transaction_isolation TO 'read committed';\""
  sudo -u postgres bash -c "psql -c \"ALTER ROLE starthinker_user SET timezone TO 'UTC';\""
  sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE starthinker TO starthinker_user;\""
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Install Git And Clone Repository"
  sudo apt install git
  git clone https://github.com/google/starthinker
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Install Virtual Environment"
  sudo apt-get install python-pip -qq > /dev/null
  sudo -H pip install --quiet --upgrade pip
  sudo -H pip install --quiet virtualenv
  virtualenv env
  source env/bin/activate
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Install StarThinker Requirements"
  pip install --quiet -r starthinker/requirements.txt
  pip install --quiet -r starthinker/ui/requirements.txt
  cd starthinker
  source setup.sh
  python ui/manage.py makemigrations --settings=ui.settings_open
  python ui/manage.py migrate --settings=ui.settings_open
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Configure StarThinker: starthinker/config.py"
  setup_project
  sed -i "s|UI CLOUD PROJECT|$CLOUD_PROJECT_ID|" config.py
  setup_credentials
  sed -i "s|UI CLIENT CREDENTIALS PATH|$CLIENT_CREDENTIALS|" config.py
  sed -i "s|UI SERVICE CREDENTIALS PATH|$SERVICE_CREDENTIALS|" config.py
  sed -i "s|CRON DIRECTORY|$CRON_DIRECTORY|" config.py
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "Configure StarThinker: starthinker/ui/ui/settings_open.py"
  sed -i "s|RECIPE STORAGE PROJECT|$CLOUD_PROJECT_ID|" ui/ui/settings_open.py
  sed -i "s|RECIPE STORAGE SERVICE CREDENTIALS PATH|$SERVICE_CREDENTIALS|" ui/ui/settings_open.py
  SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
  sed -i "s|THIS MUST BE A 50 CHARACTER RANDOM ALPHA NUMERIC STRING YOU GENERATE|$SECRET_KEY|" ui/ui/settings_open.py
  ALLOWED_HOST=$(curl -s -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
  sed -i "s|DOMAIN OR IP ADDRESS|$ALLOWED_HOST|g" ui/ui/settings_open.py
  RANDOM_HASH=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1)
  sed -i "s|RECIPE BUCKET PREFIX|starthinker-recipes-$RANDOM_HASH-|" ui/ui/settings_open.py
  sed -i "s|USER TOKEN STORAGE BUCKET|starthinker-users-$RANDOM_HASH-|" ui/ui/settings_open.py
  deactivate
  cd ..
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "- Configure uWSGI"
  sudo pip install --quiet uwsgi
  sudo mkdir -p /etc/uwsgi/sites
  sudo bash -c "cat > /etc/uwsgi/sites/starthinker.ini" << EOL
[uwsgi]
plugin = python
uid = $USER
gid = www-data
project = starthinker
base = /home/$USER
pythonpath = %(base) 
chdir = %(base)/%(project)
home = %(base)/env
module = %(project).ui.ui.wsgi_open:application
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
  echo "Done"
  
  echo ""
  echo "----------------------------------------"
  echo "- Configure Nginx"
  Configure Nginx
  sudo apt-get install nginx -qq > /dev/null
  sudo bash -c "cat > /etc/nginx/sites-available/starthinker" << EOL
server {
  listen 80;
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
  sudo systemctl start nginx
  sudo systemctl enable nginx
  echo "Done"
  
  echo ""
  echo "------------------------------------------------------------------------------"
  echo "The StarThinker Reference UI Is Ready"
  echo ""
  echo "- Review all configurations, Google does not warranty this install in any way."
  echo "- Visit: http://$ALLOWED_HOST"
  echo ""
  echo "- StarThinker settings:"
  echo "  - starthinker/config.py"
  echo "  - starthinker/ui/ui/settings_open.py"
  echo ""
  echo "- Web server settings:"
  echo "  - /etc/uwsgi/sites/starthinker.ini"
  echo "  - /etc/systemd/system/uwsgi.service" 
  echo "  - /etc/nginx/sites-available/starthinker"
  echo "  - /etc/nginx/nginx.conf" 
}

echo ""
echo "------------------------------------------------------------------------------"
echo "This is a reference implementation only and not warrantied by Google."
echo ""

read -p "Do you wish to proceed (y/n)? " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then

  echo ""
  echo "------------------------------------------------------------------------------"
  echo "This script will set up a public HTTP server on this machine."
  echo ""

  echo "This script will also modify the following files:"
  echo "  - starthinker/config.py"
  echo "  - starthinker/ui/ui/settings_open.py"
  echo ""

  echo "This script will also overwrite the following files:"
  echo "  - /etc/uwsgi/sites/starthinker.ini"
  echo "  - /etc/systemd/system/uwsgi.service" 
  echo "  - /etc/nginx/sites-available/starthinker"
  echo "  - /etc/nginx/nginx.conf" 
  echo ""

  read -p "Do you wish to proceed (y/n)? " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    install_dependencies
  fi

fi
