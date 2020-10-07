# Using StarThinker On The Command Line

This deployment is for non-developers who simply wish to use StarThinker to
execute a recipe.

## Install StarThinker

To run StarThinker you will need the folowing:

1. A unix / linux command line.
2. A version of Python 3.7 or greater.

From the command line on any unix/linux machine install StarThinker.  All following examples begin with this step.

```
pip3 install git+https://github.com/google/starthinker
```

- If you get a permission error add: ```--user``` to the above command.
- If you get a PATH WARNING:
  1. Copy the new command PATH from the warning.
  1. Activate the new command path now, run: ```export PATH="[PASTE THE PATH HERE]":$PATH;```
  1. Activate for all future logins, run: ```echo 'export PATH="[PASTE THE PATH HERE]":$PATH;' >> ~/.bash_profile;```

## Optional Setup User Credentials

To run some recipes, functions, or helpers, user credentials are required.  To acquire user credentials run the
following utility and follow instructions on screen:

```
st_auth -h
```

## Run A Helper

There are several [command line helpers](helpers.md) packaged in StarThinker, simply PIP install it and use the comands.

## Run A Script

A script is a template for a recipe, usually downloaded from the [recipe
gallery](https://google.github.io/starthinker/).  A script can be identified by
the presence of **{ 'field': ... }*** entries in the source JOSN.

Before running a script, convert it to a recipe... this will create a new json
file which is the recipe.

```
python st_script [SCRIPT JOSN FILE]
```

## Run A Recipe

Often you will receive a recipe, via email for example, that is ready to be executed.
If your recipe requires [User Credentials](#Optional-Setup-User-Credentials) or [Service Credentials](cloud_service.md) please generate both first.
All parameters are optional:

```
python st_run -h
python st_run [RECIPE JSON FILE] -u [SERVICE JSON PATH] -s [SERVICE JSON PATH] -p [GCP PROJECT ID]
```

You should see each step of your your recipe executing on the command line.

## Additional Resources

There are several [command line helpers](helpers.md) packaged in StarThinker, simply PIP install it and use the comands.

[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_commandline.md)

Next, review list of available tasks in the [Recipe Gallery](https://google.github.io/starthinker/) or [GIT Scripts Folder](../scripts/).


---
&copy; 2019 Google LLC - Apache License, Version 2.0
