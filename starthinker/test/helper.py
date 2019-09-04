###########################################################################
# 
#  Copyright 2018 Google Inc.
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


"""Command line to run all tests or list all runnable tests.

Meant to speed up an automate testing of StarThinker.

To get list: python test/helper.py --list -u [credentials] -s [credentials] -p [project_id]

"""
import os
import sys
import re
import argparse
import subprocess
import json
import datetime
from shutil import copyfile


from starthinker.config import UI_ROOT, UI_SERVICE, UI_PROJECT
from starthinker.script.parse import json_get_fields, json_set_fields
from starthinker.script.run import script_read
from starthinker.util.sheets import sheets_create


UI_CLIENT = os.environ.get('STARTHINKER_CLIENT_INSTALLED', 'MISSING RUN deploy.sh TO SET')
UI_USER = os.environ.get('STARTHINKER_USER', 'MISSING RUN deploy.sh TO SET')
CONFIG_FILE_PATH = UI_ROOT + '/starthinker/test/config.json'
LOG_FILE_PATH = UI_ROOT + '/starthinker/test/log.txt'
TEST_DIRECTORY_PATH = UI_ROOT + '/starthinker/test/test_recipes/'
AUTO_GEN_TEST_FILES = UI_ROOT + '/starthinker/test/auto_gen_test_recipes/'

RE_TEST = re.compile(r'test.*\.json')


def tests():
  parser = argparse.ArgumentParser()
  parser.add_argument('--init', '-init', help='Flag for if you want to only initialize tests and not run tests. set = true')

  args = parser.parse_args()

  if args.init == 'true':
    initialize_tests()
  else:
    run_tests()

def run_tests():
  config_fields = initialize_tests()
  create_auto_gen_test_recipes(config_fields)

  # Write to logging file
  f = open(LOG_FILE_PATH, "w+")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("Testing Run - %s \n" % datetime.datetime.now())
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.write("*\n")
  f.close()

  for root, dirs, files in os.walk(AUTO_GEN_TEST_FILES):
    for filename in files:
      has_test = False
      script = script_read(AUTO_GEN_TEST_FILES + filename)

      # Check if the script has a test associated with it
      for tasks in script['tasks']:
        for key,value in tasks.iteritems():
          if key == 'test':
            has_test = True
            break

      if not has_test:
        continue

      # Run the test script
      command = 'python %s/starthinker/all/run.py %s/%s -c %s -u %s -s %s -p %s --force' % (
        UI_ROOT,
        root,
        filename,
        UI_CLIENT,
        UI_USER,
        UI_SERVICE,
        UI_PROJECT
      )

      print ''
      print ''
      print '----------------------------------------'
      print ' TEST: ', command
      print '----------------------------------------'
      print ''    

      #std_out, std_err = subprocess.call(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()

      std_out, std_err = subprocess.Popen(command, shell=True, cwd=UI_ROOT, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
      # Write to log file   
      f = open(LOG_FILE_PATH, "a")
      f.write('\n')
      f.write('\n')
      f.write('----------------------------------------\n')
      f.write('Test: %s \n' % filename)
      f.write('Command: ' + command + '\n')
      f.write('\n')
      f.write('Standard Out=======\n')
      f.write('\n')
      f.write(std_out)
      f.write('\n')
      f.write('Standard Error=======\n')
      f.write('\n')
      f.write(std_err)
      f.write('\n')
      f.close()

  f = open(LOG_FILE_PATH, "a")
  f.write('\n')
  f.write('\n')
  f.write('\n')
  f.write('\n')
  f.write('Testing Completed\n')
  f.write('\n')
  f.write('\n')
  f.close()


"""Initialize all the necessary test files for Starthinker

Args:

Returns:
  * {
      "script_name": {
        "field_name": default_value
      }
    }
"""
def initialize_tests():
  # Get all necessary fields from Gtech scripts
  gtech_fields = get_fields_from_gtech_folder()

  # Get fields from the config file
  config_fields = {}
  if (os.path.exists(CONFIG_FILE_PATH)):
    config_fields = get_config_fields()

  # Update the config fields with any new scripts or fields 
  updated_config_fields,is_updated = update_config_fields(config_fields, gtech_fields)

  # Update the config file with any new values
  if(is_updated):
    update_config_file(updated_config_fields)

  print "All Starthinker files successfully updated."
  print ""
  print "------"
  print "------------"
  print "------------------------"
  print "Please visit " + CONFIG_FILE_PATH + " to go through and update the necessary fields for the tests you wish to run."
  print "Please visit the Google Sheet \"Starthinker Test Sheet\" to input values for the necessary tests you would like to run."
  print "------------------------"
  print "------------"
  print "------"
  print ""

  return updated_config_fields


""" Create test recipes to run, this method inputs the settings in config.json into the test recipes

Args:
  * config_fields -> the json object from config.json

Returns:
"""
def create_auto_gen_test_recipes(config_fields):
  for root, dirs, files in os.walk(TEST_DIRECTORY_PATH):
    for filename in files:
      script_json = {}
      with open(TEST_DIRECTORY_PATH + filename, 'r') as f:
        script_json = json.load(f)

      # Set cal config field values into the script
      json_set_fields(script_json, config_fields[filename.split('.')[0]])

      script = json.dumps(script_json, sort_keys=True, indent=2)
      f = open(AUTO_GEN_TEST_FILES + filename,"w")
      f.write(script)
      f.close()  


"""Read all the required fields from the gtech folder

Args:

Returns:
  * {
      "script_name": {
        "field_name": default_value
      }
    }
"""
def get_fields_from_gtech_folder():
  # Get all the necessary fields from the gtech scripts
  fields = {}
  for root, dirs, files in os.walk(TEST_DIRECTORY_PATH):
    for filename in files:
      path = TEST_DIRECTORY_PATH + filename
      script = script_read(path)
      script_fields = json_get_fields(script)
      
      for field in script_fields:
        script_name = filename.split('.')[0]
        if script_name not in fields:
          fields[script_name] = {}
        fields[script_name][field["name"]] = field["default"] if 'default' in field else ''
  return fields


"""Read the test config file into a json object

Args:

Returns:
  * Json object representing the current test config settings
    {
      "script_name": {
        "field_name": default_value
      }
    }
"""
def get_config_fields():
  with open(CONFIG_FILE_PATH, 'r') as f:
    fields = json.load(f)

  return fields


""" Goes through the current config fields and the gtech fields 
    adds any missing values to the config fields

Args:
  * config_fields -> fields object for what is currently in the config file 
  * gtech_fields -> fields object for what gtech is looking for

Returns:
  * Json object representing the current test config settings
    {
      "script_name": {
        "field_name": default_value
      }
    }
"""
def update_config_fields(config_fields, gtech_fields):
  is_updated = False

  for script_name,fields in gtech_fields.iteritems():
    for field_name,default_value in fields.iteritems():
      # Check if the script is in the config fields already
      if script_name not in config_fields:
        config_fields[script_name] = {}
        is_updated = True

      # Check if the field is in the config for the script
      if field_name not in config_fields[script_name]:
        config_fields[script_name][field_name] = default_value
        is_updated = True

  return config_fields,is_updated


""" Overwrites the current config file with the new values

Args:
  * config_fields -> fields object for what needs to be written to the
      config file

Returns:
  * None
"""
def update_config_file(config_fields):
  field_json = json.dumps(config_fields, sort_keys=True, indent=2)
  f = open(CONFIG_FILE_PATH,"w+")
  f.write(field_json)
  f.close()  


if __name__ == "__main__":
  tests()
