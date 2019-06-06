# StarThinker Reference Installations

StarThinker is fully configured from environmental variables.
A deployment script is provided to help with the configuration.
It provides reference examples for how to deploy to:

 - Local Machine ( Developer / Data Scientist )
 - Google App Engine ( Enterprise )

All actions are more fully documented in the deploy script.



## Quick Start

To deploy StarThinker run and follow instructions:

```source install/deploy.sh```

The deploy script simply edits starthinker_assets/production.sh. You
can edit it manually for a custom configuration or use the deploy script
to manage it.  Once you configure StarThinker once, you no longer need
to run the deply scripts.  

After the first deploy, to use StarThinker localy simply launch the saved configuration:

```source starthinker_assets/developer.sh```

Or if you are connecting to the production environment:

```source starthinker_assets/production.sh```

You are now ready to run and develop StarThinker recipes.



## Environmental Variables

All environmental variables are controlled by install/deploy.sh.
The deploy script simply manages all the variables in starthinker_assets/production.sh.
You can edit these variables using deploy.sh, production.sh, or just set them on the command line.

 - STARTHINKER_SCALE - ( int ) scales all iternal buffers by a multiplier, used to adjust memory allocation.
 - STARTHINKER_DEVELOPMENT ( 1 or 0 ) - Maps to Django DEVELOPMENT_MODE.

 - STARTHINKER_PROJECT - ( string ) Google Cloud project identifier to run local recipes or UI in.
 - STARTHINKER_ZONE - ( string ) Zone and region to set up all assets in, for example: us-central1-a.

 - STARTHINKER_CLIENT - ( path or json ) Google Cloud client json that allows OAuth. Needed to create user json.
 - STARTHINKER_SERVICE - ( path or json ) Google Cloud service account that is used by recipes or UI.
 - STARTHINKER_USER - ( path or json ) Google Cloud user account that is used by recipes. Denerated from STARTHINKER_CLIENT by deploy script.
 - STARTHINKER_ROOT - ( path ) Directory where root of starthinker is located.
 - STARTHINKER_CRON - ( path ) Directory where recipes are stored whn run by cron job, optional Data Scientist deploy option.
 - STARTHINKER_ENV - ( path ) Directory where virtual environment is created for StarThinker and all python dependencies installed.
 - STARTHINKER_CRT - ( path ) File where SSL certificate is stored, used by Alternate deploy option.
 - STARTHINKER_KEY - ( path ) File where SSL key is stored, used by Alternate deploy option.
 - STARTHINKER_CSR - ( path ) File where SSL certificate signing request is stored, used by Alternate deploy option.
 - STARTHINKER_CONFIG - ( path ) File that stores all StarThinker ENV ( these ) variables. Launch Starthinker by sourcing this file.

 - STARTHINKER_UI_DOMAIN - ( string ) Maps to Django ALLOWED_HOSTS.
 - STARTHINKER_UI_SECRET - ( string ) Maps to Django SECRET_KEY.
 - STARTHINKER_UI_DATABASE_ENGINE - ( string ) Maps to Django DATABASES - ENGINE.
 - STARTHINKER_UI_DATABASE_HOST - ( string ) Maps to Django DATABASES - HOST.
 - STARTHINKER_UI_DATABASE_PORT - ( int ) Maps to Django DATABASES - PORT.
 - STARTHINKER_UI_DATABASE_NAME - ( string ) Maps to Django DATABASES - NAME.
 - STARTHINKER_UI_DATABASE_USER - ( string ) Maps to Django DATABASES - USER.
 - STARTHINKER_UI_DATABASE_PASSWORD - ( string ) Maps to Django DATABASES - PASSWORD.
