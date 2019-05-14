This is not an officially supported Google product.  It is a reference implementation.

# gTech StarThinker Workflow Framework For Externalizing Solutions

StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components. 
To make it easier for partners and clients to work with some of our advertsing solutions, the gTech team has
open sourced this framework as a reference implementation.  Our goal is to make managing data workflows
using Google Cloud as fast and re-usable as possible, allowing teams to focus on building advertising solutions.



## Why Use The StarThinker Open Source Code?

- The framework provides practical working examples of moving data using Google Cloud.
- Google teams can hand over internally built solutions to your team on top of this framework.
- The code has been stress tested internally across projects and includes many best practices.
- The code runs at scale, allowing you to simply upgrade Cloud Machines to move larger data sets.
- There is an easily deployable UI that can be stood up within minutes on Google Cloud.
- The code is Apache Licensed and fully modifiable by your team.



## Where Is The Documentation?

Most directories contain a README.me file. These are instructions for how to use the code in that directory.
General structure ofthe code is:

- [/install](install/) - Scripts for installing and deploying StarThinker.
- [/starthinker_assets](starthinker_assets/) - Holds all configuration files when you launch StarThinker.
- [/starthinker/util](starthinker/util/) - Low level library wrappers around Google API with helpers to handle common errors.
- [/starthinker/task](starthinker/task/) - Handlers for each task specified in a JSON recipe.
- [/starthinker/gtech](starthinker/gtech/) - Complete solution templates provided by Google gTech that you can deploy.
- [/starthinker/script](starthinker/script/) - Command line for converting a recipe template into a client specific executable recipe
- [/starthinker/all](starthinker/all/) - Developer command line for executing a recipe in its entirety.
- [/starthinker/cron](starthinker/cron/) - Quick command line for executing recipes on a schedule.
- [/starthinker/auth](starthinker/auth/) - Developer command line for testing user credential setup.
- [/starthinker_ui](starthinker/starthinker_ui/) - UI deplyed on AppEngine powered by Django.



## What are some common terms?

StarThinker uses JSON configuration blocks that map to python run handlers.  When these JSON blocks
are assembled in sequence, a recipe is created that can execute complex workflows.  To make the JSON
configurations re-usable they are packaged as templates that can be populated with client specific
data on the command line or the UI.

- recipe template - a JSON file with a structure script\*.json and { 'field':{...}} placeholders.
- recipe - a JSON file with all the { 'field':{...}} placeholders replaced with actual values.
- handler - any run.py script, its directory will map to a task JSON block in a recipe.

[StarThinker GitHub Documentation Page](https://google.github.io/starthinker/)



## Whats The Most Basic Use?

For a quick start that will do nothing other than show how to sucesfully run a recipe:

- First configure StarThinker by running...
```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh 
```
- Option 1) Developer Menu
- Option 1) Install StarThinker
- Then activate StarThinker virtualenv...
```
source starthinker_assets/development.sh
```
- Finally run the sample aplication...
```
python starthinker/all/run.py starthinker/gtech/say_hello.json --verbose
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=%2FREADME.md)

Read more at [all/README.md](all/README.md) under Useful Developer Features. 



## How Do I Turn A Recipe Template Into A Recipe?

To quickly use any one of the template to perform a task, moving a DCM report for example:

```
python starthinker/script/run.py starthinker/gtech/script_dcm_to_bigquery.json -h
python starthinker/script/run.py starthinker/gtech/script_dcm_to_bigquery.json 7880 1234567 "" "Test_Dataset" "Test_Table" > test_recipe.json
python starthinker/all/run.py test_recipe.json
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=%2FREADME.md)

Read more at [script/README.md](script/README.md).



## Whats The Simplest ( Non-Technical ) Way To Deploy Long Running Jobs?

To execute recipes on a regular schedule, for example moving a report every day. Find an always
on machine, like a Google Cloud Instance. Download the open source code, and execute the following:

- First configure StarThinker by running...
```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh 
```
- Option 2) Data Scientist Menu
- Option 1) Install StarThinker
- Option 5) Add Recipe of 6) Generate Recipe
- Option 2) Start Cron


- Then activate StarThinker virtualenv...
```
source starthinker_assets/development.sh
```
- Finally run the sample aplication...
```
python starthinker/all/run.py starthinker/gtech/say_hello.json --verbose
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=%2FREADME.md)



## Deploying StarThinker UI For Enterprise Multi User 

When multiple users need to deploy and coordinate multiple reipces for multiple clients, stand up the UI.
The UI allows each user to authenticate and manage solutions leaving the development team free to create
and maintain the technical recipe scripts.  The UI deploys on AppEngine with a distributed worker back end
on Google Cloud Instances. Execute the following to stand up the UI:

```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh
```
- Option 3) Enterprise Setup Menu 
- Option 1) Deploy App Engine UI
- Option 2) Deploy Job Workers
- Option 1) Test - 1 Job



### When creating the oAuth Client:

- For credentials type choose: Web Application..
- For OAuth Consent Screen choose: Application Type Internal.
- Be sure to add callbacks to your OAuth Client:
```
http://localhost:8000/oauth_callback/	
https://[CLIENT_PROJECT_NAME].appspot.com/oauth_callback/	
```

If you DO NOT see Application Type Internal as an option, your project is not
a member of a [GSuite Organization](https://support.google.com/a/answer/6365252).
Having a GSuite Organization is the recommended setup, it provides additional
security and control over access to your cloud assets.  Alternatively you can
set up a verified domain and controll access using firewalls and other tools
available in Google Cloud.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=%2FREADME.md)



## Using StarThinker As A Python Package

You can use the starthinker module directly in any python project to run a recipe.

```
pip install git+https://github.com/google/starthinker
python
import starthinker
```

## Where Do I Get Help?

Email: starthinker-help@google.com



## Authors 

- Paul Kenjora ( kenjora@google.com ) - Google gTech
- Mauricio Desiderio ( mauriciod@google.com ) - Google gTech
- John Terwilleger ( terwilleger@google.com ) - Google gTech

Additional contributors to individual handlers and recipes are listed in each file.
