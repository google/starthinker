# StarThinker Reference Installations

StarThinker is fully configured from environmental variables.
A deployment script is provided to help with the configuration.
To deploy a specific type of StarThinker setup see:

 - [Developer](../tutorials/deploy_developer.md) - Local machine, ideal for testing and development work.
 - [Data Scientist](../tutorials/deploy_scientist.md) - Single user recurring job running recipes.
 - [Enterprise](../tutorials/deploy_enterprise.md) - Google App Engine multi user web setup. 
 - [Package](../tutorials/deploy_package.md) - Workshop import and run instantly.

## Quick Start

To deploy StarThinker run and follow instructions within:

```source install/deploy.sh```

After deploy once, to use StarThinker for local development and testing, launch the saved configuration:

```source starthinker_assets/developer.sh```

Or if you are connecting to the production environment:

```source starthinker_assets/production.sh```

You are now ready to run and develop StarThinker recipes.

## Configuration Assets

The deploy script manages the following files and assets:

- starthinker_assets/production.sh - Parameters used for production deployments.
- starthinker_assets/developer.sh - Parameters used for local development.
- starthinker_assets/service.json - Google Cloud Service Credentials.
- starthinker_assets/client_web.json - Google Cloud Service Credentials used by UI.
- starthinker_assets/client_installed.json - Google Cloud Client Credentials used by command line.
- starthinker_assets/user.json - Google Cloud Service user ( generated from client_installed.json ).

The UI also creates a bucket with user credenentials when deployed.

## Environmental Variables

All environmental variables are controlled by install/deploy.sh.
The deploy script simply manages all the variables in starthinker_assets/production.sh.
You can edit these variables using deploy.sh, production.sh, or just set them on the command line.

 - STARTHINKER_SCALE - ( 1 - 5 ) scales all iternal buffers by a multiplier, used to adjust memory allocation.
 - STARTHINKER_DEVELOPMENT ( 1 or 0 ) - Maps to Django DEVELOPMENT_MODE.

 - STARTHINKER_PROJECT - ( string ) Google Cloud project identifier to run local recipes or UI in.
 - STARTHINKER_ZONE - ( string ) Zone and region to set up all assets in, for example: us-central1-a.

 - STARTHINKER_CLIENT_WEB - ( path or json ) Path to starthinker_assets/client_installed.json.
 - STARTHINKER_CLIENT_INSTALLED - ( path or json ) Path to starthinker_assets/client_web.json.
 - STARTHINKER_SERVICE - ( path or json ) Path to starthinker_assets/service.json.
 - STARTHINKER_USER - ( path or json ) Path to starthinker_assets/user.json.
 - STARTHINKER_ROOT - ( path ) Directory where root of starthinker is located.
 - STARTHINKER_CRON - ( path ) Directory used by cron job to store recipes, Data Scientist deploy option.
 - STARTHINKER_ENV - ( path ) Directory where virtual environment and all python dependencies are installed.
 - STARTHINKER_CRT - ( path ) File where SSL certificate is stored, used by Alternate deploy option.
 - STARTHINKER_KEY - ( path ) File where SSL key is stored, used by Alternate deploy option.
 - STARTHINKER_CSR - ( path ) File where SSL certificate signing request is stored, used by Alternate deploy option.
 - STARTHINKER_CONFIG - ( path ) Path to starthinker_assets/production.sh.

 - STARTHINKER_UI_DOMAIN - ( string ) Maps to Django ALLOWED_HOSTS.
 - STARTHINKER_UI_SECRET - ( string ) Maps to Django SECRET_KEY.
 - STARTHINKER_UI_DATABASE_ENGINE - ( string ) Maps to Django DATABASES - ENGINE.
 - STARTHINKER_UI_DATABASE_HOST - ( string ) Maps to Django DATABASES - HOST.
 - STARTHINKER_UI_DATABASE_PORT - ( int ) Maps to Django DATABASES - PORT.
 - STARTHINKER_UI_DATABASE_NAME - ( string ) Maps to Django DATABASES - NAME.
 - STARTHINKER_UI_DATABASE_USER - ( string ) Maps to Django DATABASES - USER.
 - STARTHINKER_UI_DATABASE_PASSWORD - ( string ) Maps to Django DATABASES - PASSWORD.

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
