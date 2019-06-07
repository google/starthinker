# Deployment For Data Sciene Analysts

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
- Option 5) Add Recipe or Option 6) Generate Recipe
- Option 2) Start Cron


- Then activate StarThinker virtualenv...
```
source starthinker_assets/development.sh
```
- Finally run the sample aplication...
```
python starthinker/all/run.py starthinker/gtech/say_hello.json --verbose
```

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=README.md)
