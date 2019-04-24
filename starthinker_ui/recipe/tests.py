###########################################################################
# 
#  Copyright 2019 Google Inc.
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

import time
import copy
from django.test import TestCase


TEST_TIMESTAMP = int(time.time()) # ensures unique recipe every run

TEST_RECIPE = {
  "script":{
    "license":"Apache License, Version 2.0",
    "copyright":"Copyright 2018 Google Inc.",
    "icon":"folder",
    "product":"gTech",
    "title":"Sample Recipe",
    "description":"Used for testing.",
    "instructions":[
      "Import this recipe.",
      "Pass it to a test.",
      "Make test pass."
    ],
    "authors":["kenjora@google.com"]
  },
  "setup":{
    "uuid":"RECIPE_UUID",
    "id": "cloud-project-id",
    "timezone": "America/Los_Angeles",
    "day":["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  },
  "tasks":[
    { "hello":{
        "auth":"user",
        "say":"Task One"
    }},
    { "hello":{
        "auth":"user",
        "say":"Task Two"
    }}
  ]
}


def uuid_timestamp(uid):
 return "%s_%d" % (uid, TEST_TIMESTAMP)


def recipe_create(uid, hour=[]):
  recipe = copy.deepcopy(TEST_RECIPE)
  recipe['setup']['uuid'] = uid
  if hour: recipe['setup']['hour'] = hour
  return recipe
 

def recipe_create_with_task_error(uid, hour=[]):
  recipe = recipe_create(uid)
  if hour: recipe['setup']['hour'] = hour
  recipe['tasks'].insert(1, { 
    "task_does_not_exist":{
      "auth":"user",
      "say":"Task Error"
  }})
  return recipe


def recipe_create_with_task_sleep(uid, hour=[]):
  recipe = recipe_create(uid)
  if hour: recipe['setup']['hour'] = hour
  recipe['tasks'][0]['hello']['sleep'] = 60 * 60 # 1 hour
  return recipe


class LogTest(TestCase):

  def test_log_limit(self):
    self.assertTrue(True)


class RecipeViewTest(TestCase):

  def test_recipe_list(self):
    resp = self.client.get('/')
    self.assertEqual(resp.status_code, 200)

  def test_recipe_edit(self):
    resp = self.client.get('/recipe/edit/')
    self.assertEqual(resp.status_code, 302)
