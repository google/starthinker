This code is an open source reference implementation and is not an officially supported Google product.

# StarThinker Workflow Framework For Google

StarThinker is a Google built python framework for creating and sharing re-usable workflow components. 
To make it easier for partners and clients to work with some of our solutions, the gTech team has
open sourced this framework as a reference implementation.  Our goal is to make managing data workflows
using Google Cloud as fast and re-usable as possible, allowing teams to focus on building solutions.

## Why Use The StarThinker Open Source Code?

1. The framework provides practical working examples of moving data using Google Cloud.
2. Google teams can hand over internally built solutions to your team on top of this framework.
3. The code is Apache Licensed and fully modifiable by your team.
4. The code has been stress tested internally across projects and includes many best practices.

## Where Is The Documentation?

The code is documented inline at core points, with documentation being added every day.  For a list
of how to use and deploy the code see:

[StarThinker GitHub Documentation Page](https://google.github.io/starthinker/)

## Whats The Most Basic Use?

The Say Hello workflow, is a basic example endpoint for running workflows from the comand line.  It
provides an explination of all the components of a workflow.  Run it first, look at the source of both
the JSON and say_hello/run.py to see how the two connect.  Then write your own.

python all/run.py project/sample/say_hello.json --verbose

## Where Do I Get Help?

Email: starthinker-help@google.com
