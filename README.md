This is not an officially supported Google product.  It is a reference implementation.

# StarThinker Workflow Framework For Google

StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components. 
To make it easier for partners and clients to work with some of our advertsing solutions, the gTech team has
open sourced this framework as a reference implementation.  Our goal is to make managing data workflows
using Google Cloud as fast and re-usable as possible, allowing teams to focus on building advertising solutions.

## Why Use The StarThinker Open Source Code?

- The framework provides practical working examples of moving data using Google Cloud.
- Google teams can hand over internally built solutions to your team on top of this framework.
- The code has been stress tested internally across projects and includes many best practices.
- The code runs at scale, allowing you to simply upgrade Cloud Machines to move larger data sets.
- The code is Apache Licensed and fully modifiable by your team.

## Where Is The Documentation?

Every directory contains a README.me file. These are instructions for how to use the code in that directory.
General structure ofthe code is:

- [/install](install/) - Scripts for installing and deploying StarThinker.
- [/starthinker/config.py](starthinker/config.py) - global settings covering buffer size, cloud credentials, and production vs debug.
- [/starthinker/util](starthinker/util/) - Low level library wrappers around Google API with helpers to handle common errors.
- [/starthinker/task](starthinker/task/) - Handlers for each task specified in a JSON recipe.
- [/starthinker/gtech](starthinker/gtech/) - complete solution templates provided by Google gTech, great starting point for ideas.
- [/starthinker/script](starthinker/script/) - command line for converting a recipe template into a client specific executable recipe
- [/starthinker/all](starthinker/all/) - command line for executing a recipe in its entirety
- [/starthinker/cron](starthinker/cron/) - command line for executing recipes on a schedule
- [/starthinker/auth](starthinker/auth/) - command line for testing user credential setup
- [/starthinker_ui](starthinker/starthinker_ui/) - browser based UI powered by Django

## What are some common terms?

StarThinker uses JSON configuration blocks that map to python run handlers.  When these JSON blocks
are assembled in sequence, a recipe is created that can execute complex workflows.  To make the JSON
configurations re-usable they are packaged as templates that can be populated with client specific
data on the command line ( or a UI ).

- recipe template - a JSON file with a structure script\*.json and { 'field':{...}} placeholders.
- recipe - a JSON file with all the { 'field':{...}} placeholders replaced with actual values.
- handler - any run.py script, its directory will map to a task JSON block in a recipe.

[StarThinker GitHub Documentation Page](https://google.github.io/starthinker/)

## Whats The Most Basic Use?


For a quick start that will do nothing other than show how to sucesfully run recipes, try:

```
git clone https://github.com/google/starthinker
cd starthinker
source install/developer.sh --instance
Choose Option 1) Full Install
python all/run.py gtech/say_hello.json --verbose
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2FREADME.md)

Read more at [all/README.md](all/README.md) under Useful Developer Features. 

## How Do I Turn A Recipe Template Into A Recipe?

To quickly use any one of the template to perform a task, moving a DCM report for example:

```
python script/run.py gtech/script_dcm_to_bigquery.json -h
python script/run.py gtech/script_dcm_to_bigquery.json 7880 1234567 "" "Test_Dataset" "Test_Table" --datastudio > test_recipe.json
python python all/run.py test_recipe.json
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_DEPLOY.txt&cloudshell_tutorial=%2FREADME.md)

Read more at [script/README.md](script/README.md).

## Whats The Easiest ( Non-Technical ) Way To Deploy Long Running Jobs?

To execute recipes on a regular schedule, for example moving a report every day. Find an always
on machine, like a Google Cloud Instance. Download the open source code, and execute the following

```
git clone https://github.com/google/starthinker
cd starthinker
source install/cron.sh --instance
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_DEPLOY.txt&cloudshell_tutorial=README.md)

## Using The Micro UI To Deploy Recipes...

```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh
```

A micro UI will activate ( no system changes are made unless you choose an option ), choose the 
appropriate option.  Full setup walks through everything, including credentials and install.  
The process is re-entrant so you can run it multiple times without corrupting the setup.  
Start with Option 11 to get an overview. Here is the main utility menu:

```
----------------------------------------------------------------------
gTech StarThinker
----------------------------------------------------------------------

Developer Menu
Sets up local environment to run StarThinker recipes from the command line. Most basic setup.


Data Scientist Menu
Sets up local job that will run recipes on a schedule persistently.  For long running custom jobs.


Enterprise Setup Menu
Sets up a Google App Engine Instance web UI for multiple users and disctributed jobs.  Highly scalable team wide deployment.


Alternate Setup Menu
Sets up a traditional full stack UI server on Google Cloud Instance for multiple users and disctributed jobs.  Highly customizable deployment.

----------------------------------------------------------------------
Main Menu
----------------------------------------------------------------------

1) Developer Menu
2) Data Scientist Menu
3) Enterprise Setup Menu
4) Quit
Your Choice: 
```

## Where Do I Get Help?

Email: starthinker-help@google.com

## Authors 

- Paul Kenjora ( kenjora@google.com ) - Google gTech
- Mauricio Desiderio ( mauriciod@google.com ) - Google gTech

Additional contributors to individual handlers and recipes are listed in each file.

# The Rest Of This Document Is Pulled From Code Comments

No code comments at this level.
