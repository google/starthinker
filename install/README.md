# StarThinker Reference Installations

StarThinker is fully configured from environmental variables.
A deployment script is provided to help with the configuration.
It provides reference examples for how to deploy to:

 - Local Machine ( Developer / Data Scientist )
 - Google App Engine ( Enterprise )
 - Debian Linux Server ( Alternative )
 - Debian Pub/Sub ( Enterprise )

All actions are more fully documented in the deploy script.

## Quick Start

To deploy a configuration for local development run:

```source install/deploy.sh```

Select: Developer Menu -> Install ( All Steps ) -> Quit

To activate the new StarThinker configuration and environment run:

```source starthinker_assets/config.sh```

You are now ready to run and develop StarThinker recipes.
For documentation on all other confogutrations see the deployment script.

## Environmental Variables

All environmental variables are controlled by install/deploy.sh.
The deploy script simply manages all the variables in starthinker_assets/config.sh.
You can edit these variables using deplloy.sh, config.sh, or just set them on the command line.

 - STARTHINKER_SCALE - ( int ) scales all iternal buffers by a multiplier, used to adjust memory allocation.
 - STARTHINKER_MANAGERS - ( int ) number of machines to deploy to handle recipe processing.
 - STARTHINKER_WORKERS - ( int ) number of processes to start on each machine.
 - STARTHINKER_PROJECT - ( string ) Google Cloud project identifier to run local recipes or UI in.
 - STARTHINKER_ZONE - ( string ) Zone and region to set up all assets in, for example: us-central1-a.
 - STARTHINKER_TOPIC - ( string ) Should be set to just "starthinker", used to create pub/sub topics for processing recipes.
 - STARTHINKER_ASSETS - ( path ) Directory where deploy script stores assets, needs to be sibling of starthinker code directory.
 - STARTHINKER_CLIENT - ( path or json ) Google Cloud client json that allows OAuth. Needed to create user json.
 - STARTHINKER_SERVICE - ( path or json ) Google Cloud service account that is used by recipes or UI.
 - STARTHINKER_USER - ( path or json ) Google Cloud user account that is used by recipes. Denerated from STARTHINKER_CLIENT by deploy script.
 - STARTHINKER_CRON - ( path ) Directory where recipes are stored whn run by cron job, optional Data Scientist deploy option.
 - STARTHINKER_ENV - ( path ) Directory where virtual environment is created for StarThinker and all python dependencies installed.
 - STARTHINKER_CRT - ( path ) File where SSL certificate is stored, used by Alternate deploy option.
 - STARTHINKER_KEY - ( path ) File where SSL key is stored, used by Alternate deploy option.
 - STARTHINKER_CSR - ( path ) File where SSL certificate signing request is stored, used by Alternate deploy option.
 - STARTHINKER_CONFIG - ( path ) File that stores all StarThinker ENV ( these ) variables. Launch Starthinker by sourcing this file.
 - STARTHINKER_CODE - ( path ) Directory that has all the starthinekr code in it.
 - STARTHINKER_ASSETS - ( path ) Directory that has all the starthinekr configuration in it.
 - STARTHINKER_ROOT - ( path ) Directory containing both STARTHINKER_CODE and STARTHINKER_ASSETS.

 - STARTHINKER_UI_DEVELOPMENT ( 1 or 0 ) - Maps to Django DEVELOPMENT_MODE.
 - STARTHINKER_UI_DOMAIN - ( string ) Maps to Django ALLOWED_HOSTS.
 - STARTHINKER_UI_SECRET - ( string ) Maps to Django SECRET_KEY.
 - STARTHINKER_UI_DATABASE_ENGINE - ( string ) Maps to Django DATABASES - ENGINE.
 - STARTHINKER_UI_DATABASE_HOST - ( string ) Maps to Django DATABASES - HOST.
 - STARTHINKER_UI_DATABASE_NAME - ( string ) Maps to Django DATABASES - NAME.
 - STARTHINKER_UI_DATABASE_USER - ( string ) Maps to Django DATABASES - USER.
 - STARTHINKER_UI_DATABASE_PASSWORD - ( string ) Maps to Django DATABASES - PASSWORD.
 - STARTHINKER_UI_DATABASE_PORT - ( int ) Maps to Django DATABASES - PORT.

 - STARTHINKER_INTERNAL - ( 1 or 0 ) Internal to Google, activates parts of API not avilable externally.

 - STARTHINKER_RECIPE_PROJECT - Google Cloud project where UI will store recipes.
 - STARTHINKER_RECIPE_SERVICE= Google Cloud service account used by UI to store recipes.

# The Rest Of This Document Is Pulled From Code Comments
