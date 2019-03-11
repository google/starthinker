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

echo ""
echo "----------------------------------------"
echo "Installing StarThinker UI On Debian"
echo "- Update Debian Installer"
echo "- Set Production Mode"
echo "- Install Postgre SQL Database"
echo "- Install Git And Clone Repository"
echo "- Install Virtual Environment"
echo "- Install StarThinker Requirements"
echo "- Configure uWSGI"
echo "- Configure Nginx"

echo ""
echo "----------------------------------------"
echo "Update Debian Installer"
sudo apt-get -qq update
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
sudo apt-get -qq install python-dev libpq-dev postgresql postgresql-contrib
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
sudo apt-get -qq install python-pip
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
SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
sed -i "s/THIS_MUST_BE_A_RANDOM_ALPHA_NUMERIC_STRING_YOU_GENERATE/$SECRET_KEY/" ui/ui/settings_open.py
ALLOWED_HOST=$(curl -s -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
sed -i "s/DOMAINS OR IP ADDRESS/$ALLOWED_HOST/" ui/ui/settings_open.py
BUCKET_PREFIX=starthinker_ui_users_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 24 | head -n 1)
sed -i "s/BUCKET_PREFIX/$BUCKET_PREFIX/" ui/ui/settings_open.py
echo "Done"

echo ""
echo "----------------------------------------"
echo "- Configure uWSGI"
sudo mkdir -p /etc/uwsgi/sites
sudo cat > /etc/uwsgi/sites/starthinker.ini << EOL
[uwsgi]
plugin = python
uid = $USER
gid = www-data
project = starthinker
base = /home/$USER
pythonpath = %(base) 
chdir = %(base)/%(project)
home = %(base)/%(project)/env
module = %(project).ui.ui.wsgi_open:application
master = true
processes = 2
chown-socket = %(uid):%(gid)
chmod-socket = 664
socket = /run/uwsgi/%(project).sock
vacuum = true
EOL
sudo mkdir /run/uwsgi
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
sudo apt-get -qq install nginx
sudo cat > /etc/nginx/sites-available/starthinker << EOL
server {
  listen 80;
  location = /favicon.ico { access_log off; log_not_found off; }
  location / {
    include uwsgi_params;
    uwsgi_pass unix:/run/uwsgi/starthinker.sock;
  }
}
EOL
sudo cat > /etc/nginx/nginx.conf << EOL
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

# Exit Virtual Environment
deactivate

echo ""
echo "----------------------------------------"
echo "The StarThinker Reference UI Is Ready"
echo "- Review configuration, Google does not warranty this install in any way."
echo "- Visit: http://$ALLOWED_HOST"
echo "- To change domain edit:"
echo "  - starthinker/ui/ui/settings_open.py"
echo "  - /etc/nginx/sites-available/starthinker"
