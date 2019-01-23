This is not an officially supported Google product.  It is a reference implementation.

# StarThinker Workflow Framework For Google Solution Hand Over

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

- [/deploy.sh](/deploy.sh) - a micro UI for setting up credentials, and running recipes on a schedule
- [/setup.sh](setup.sh) - source this to set up python paths to run commands using this framework.
- [/setup.py](setup.py) - global settings covering buffer size, cloud paths, and production vs debug.
- [/util](util/) - Low level library wrappers around Google API with helpers to handle common errors.
- [/task](task/) - Handlers for each task specified in a JSON recipe.
- [/gtech](gtech/) - complete solution templates provided by Google gTech, great starting point for ideas.
- [/script](script/) - command line for converting a recipe template into a client specific executable recipe
- [/all](all/) - command line for executing a recipe in its entirety
- [/cron](cron/) - command line for executing recipes on a schedule
- [/auth](auth/) - command line for testing user credential setup

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
pip install -r requirements.txt
source setup.sh
python all/run.py gtech/say_hello.json --verbose
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=README.md)

Read more at [all/README.md](all/README.md) under Useful Developer Features. 

## How Do I Turn A Recipe Template Into A Recipe?

To quickly use any one of the template to perform a task, moving a DCM report for example:

```
python script/run.py dcm/script_dcm_to_bigquery.json -h
python script/run.py dcm/script_dcm_to_bigquery.json 7880 1234567 "" "Test_Dataset" "Test_Table" --datastudio > test_recipe.json
python python all/run.py test_recipe.json
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_DEPLOY.txt&cloudshell_tutorial=README.md)

Read more at [script/README.md](script/README.md).

## Whats The Easiest ( Non-Technical ) Way To Deploy Long Running Jobs?

To execute recipes on a regular schedule, for example moving a report every day. Find an always
on machine, like a Google Cloud Instance. Download the open source code, and execute the following

```
git clone https://github.com/google/starthinker
cd starthinker
pip install -r requirements.txt
source setup.sh
./deploy.sh
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_DEPLOY.txt&cloudshell_tutorial=README.md)

A micro UI will activate ( no system changes are made unless you choose an option ), choose the 
appropriate option.  Full setup walks through everything, including credentials and install.  
The process is re-entrant so you can run it multiple times without corrupting the setup.  
Start with Option 11 to get an overview. Here is the main utility menu:

```
Welcome To StarThinker ( Google gTech )

This utility will help you set up and manage long running recipes.
If this is your first time running this script, select Full Setup.


Path Setup Finished

----------------------------------------------------------------------
Main Menu

1) Full Setup		   5) Start Cron	     9) Run Recipe
2) Install Dependencies	   6) Stop Cron		    10) Delete Recipe
3) Set Cloud Project	   7) List Recipes	    11) Instructions
4) Set Credentials	   8) Add Recipe	    12) Quit
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
