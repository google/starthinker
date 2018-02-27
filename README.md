# StarThinker Workflow Framework From Google

StarThinker is a Google built python framework for creating and sharing re-usable workflow components.
This document has everything you need to use existing solutions and launch new ones.  Its a tutorial by example.

## What is it?

A collection of libraries, scripts, and json workflow definitions that allow you to define shareable workflows.

*Directory structure:*

``` shell
util/ - holds all the python libraries used by the framework.
projects/ - holds custom workflow json used to define and exectute tasks.
solutions/ - holds workflow templates that can be re-used using solution/run.py.
script_[name].json - holds the json that can be used with that script.
```

## How do I use it?

1. Check out a copy of the code.

``` shell
git clone https://github.com/google/starthinker
```

3. Install Dependencies

``` shell
sudo apt-get install python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install --upgrade google-cloud
sudo pip install --upgrade google-api-python-client
```

4. Load Environment Variables

``` shell
source setup.sh
```

5. Run Hello World

``` shell
python all/run.py project/sample/say_hello.json
```

6. Configure project variables.

``` shell
vi setup.sh
```

## Different Ways Of Running A Script

Run all tasks sequentially.
``` shell
python all/run.py project/sample/say_hello.json --verbose --force
```

Run a specific task instance ( 2nd one ).
``` shell
python hello/run.py project/sample/say_hello.json --verbose -i 2 --force
```

Kick of a cron to to run projects by schedule in directory.
``` shell
python cron/run.py project/sample
```

## Using Solutions Templates

1. First define a solution.

``` shell
cp project/sample/solution.json project/[your folder]/[project name].json
vi project/[your folder]/[project name].json
```

2. After editing run the solution script to generate workflow scripts for each template.

``` shell
python solution/run.py project/[your folder]/[project name].json [folder to put scripts]
```

3. Then run each solution workflow like a project.

``` shell
python all/run.py [folder to put scripts]/[project name]_[solution].json --verbose --force
```

## Where can I learn more?

Run the sample code, it explains in detail the structure of worklows and how they map to code.

``` shell
python all/run.py project/sample/say_hello.json --verbose --force
```

For additional help email: starthinker-help@google.com
