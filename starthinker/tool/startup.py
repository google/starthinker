###########################################################################
#
#  Copyright 2020 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

import argparse
import subprocess
import sys
import textwrap
import os
import json
import concurrent.futures
from threading import current_thread
from typing import List

class Deployment:
    ''' Reads workflows from a directory and executes them.

        This class gathers all user input and executes DV360/CM360/SA360
        workflows to load reporting data to BigQuery.

    Attributes:
        directory - Parent directory where the workflow json files are
        debug - Instead of executing commands, print them.

    Typical Usage:
        deployment = Deployment(args.debug)
        deployment.execute_command('git clone https://github.com/google/starthinker.git', True)
        deployment.execute_command('pip install -r starthinker/starthinker/requirements.txt', True)
        directories = deployment.get_parent_workflow_directories('workflows')
        deployment.execute_workflows(directories)
    '''

    WORKFLOW_DIRECTORY = 'workflows'

    def __init__(self, debug: bool) -> None:
        '''Constructor loads all user provided values and initializes shared values.

        Args: See Attributes above.
        '''
        self.debug = debug

    def install_dependencies(package: str) -> None:
        '''Install Python dependencies

        Args:
            package (string): The package to install
        '''
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])

    def execute_command(self, command: str, read: bool = False) -> None:
        '''Helper function that either executes or prints each command.

        Args:
          command - a command line command, typically a gcloud command.
          read - if True, the commands output is passed back to the caller.

        Returns:
          Bool - if command value is not required, simply indicate successor failure.
          String - if read is specified, the command output or error is returned.
        '''
        if self.debug:
            print(command)
            return 'SIMULATING VALUE' if read else True
        else:
            print('\nCOMMAND\n', command, '\n' + '-' * 40)
            try:
                cmd = subprocess.run(
                    command, shell=True, capture_output=read, text=True, check=True)
                if read:
                    return cmd.stdout.strip()
                return True
            except subprocess.CalledProcessError as e:
                return False

    def execute_workflow(self, directory: str) -> None:
        '''Executes workflows in the provided directory, one per thread

        Args:
        - directory: (string) The directory with the workflow JSON files to execute
        '''
        thread = current_thread()
        print(f'Executing directory {directory} on thread {thread.name}...')
        # Iterate over directory ( will spawn a thread per directory to execute jobs in sequence )
        for path, subdirs, files in os.walk(directory):
            s = os.path.join(path, 'service.json')
            if os.path.isfile(s):
                project = self.get_project_from_service(s)
                service = s
            else:
                project = self.get_project_from_vm()
                service = 'DEFAULT'
            # Iterate over workflow JSON files only
            for filename in files:
                if filename != 'service.json':
                    workflow = os.path.join(path, filename)
                    # checking if it is a file
                    if os.path.isfile(workflow):
                        command = f'python3 starthinker/tool/recipe.py {workflow} -s {service} -p {project} --verbose'
                        self.execute_command(command)
        print(f'Finished executing workflows in directory {directory}.')

    def execute_workflows(self) -> None:
        '''Executes workflows in the provided directory, one per thread'''
        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            executor.map(self.execute_workflow, self.get_parent_workflow_directories())

    def get_project_from_service(self, service_path) -> str:
        '''Gets the project id from the service JSON file

        Args:
        - service_path: (list) The directory where the service JSON is

        Returns
            The project id in the service JSON file
        '''
        with open(service_path) as service_file:
            return json.load(service_file)['project_id']

    def get_project_from_vm(self) -> str:
        '''Gets the default/vm project id using gcloud commands

        Returns
            The default/vm project id
        '''
        return self.execute_command('gcloud config get-value project', read=True)

    def get_parent_workflow_directories(self) -> List[str]:
        '''Gets the workflow directories that are directly under the parent directory

        Returns
            A list of immediate directories under parent directory
        '''
        for path, subdirs, files in os.walk(Deployment.WORKFLOW_DIRECTORY):
            # Walk sub directories
            for s_dir in subdirs:
                yield os.path.join(path, s_dir)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
    Reads workflows from a directory and executes them.

    Directory Structure:

    root = dir, passed as parameter to this script
      - workflow_1 = dir, ran as a single sequence
        - service.json = file, optional service definition to run as, if not given uses VM default
        - workflow_a.json = file, the sequence of BQFlow steps to run
        - workflow_b.json = file, the sequence of BQFlow steps to run
        - ...
      - workflow_2 = dir, ran as a single sequence
        - service.json = file, optional service definition to run as, if not given uses VM default
        - workflow_a.json = file, the sequence of BQFlow steps to run
        - workflow_b.json = file, the sequence of BQFlow steps to run
        - ...

    Example:
      python3 runner.py [directory] --debug
  """))

    parser.add_argument(
        '--debug',
        '-d',
        help='Instead of executing commands, print them.',
        action='store_true'
    )

    args = parser.parse_args()

    # Execution order of functions is important
    # for debugging these are logical units than can be commented on or off
    deployment = Deployment(args.debug)
    #deployment.execute_command('git clone https://github.com/google/starthinker.git', True)
    #deployment.execute_command('pip install -r starthinker/starthinker/requirements.txt', True)
    deployment.execute_workflows()
