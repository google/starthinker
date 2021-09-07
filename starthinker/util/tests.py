###########################################################################
#
#  Copyright 2021 Google LLC
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

import unittest
import io

from starthinker.config import UI_ROOT
from starthinker.util.csv import find_utf8_split, response_utf8_stream
from starthinker.util.recipe import get_recipe, recipe_includes, json_merge_field, json_merge_fields, json_set_fields


class TestCSV(unittest.TestCase):
  """Test the CSV module.  Currently only testing utf-8 function but WIP.
  """

  def test_find_utf8_split(self):
    """  Tests: find_utf8_split, response_utf8_stream

    Verify that encoding is an issue when not boundry aligned.
    Run boundary detection against 3 different UTF-8 encodings of different byte lengths.
    Pick 17 (prime) as a chunk size to ensure utf-8 byte boundary is hit.
    Run against multiple chunks to ensure test goes in and out of utf-8 alignement.

    """

    string_ascii = bytes('"#$%&()*+,-./0123456789:;<=>?@ABCDEF', 'utf-8')
    string_arabic = bytes('،؛؟ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلم', 'utf-8')
    string_misc = bytes('⌀⌂⌃⌄⌅⌆⌇⌈⌉⌊⌋⌌⌍⌎⌏⌐⌑⌒⌓⌔⌕⌖⌗⌘⌙⌚⌛⌜⌝⌞⌟⌠⌡⌢⌣', 'utf-8')
    string_cjk = bytes('豈更車勞擄櫓爐盧老蘆虜路露魯鷺碌祿綠菉錄縷陋勒諒量', 'utf-8')

    # verify raw split causes error
    try:
      string_ascii[:17].decode("utf-8")
    except UnicodeDecodeError:
      self.fail("ASCII bytes should fit within utf-8.")

    with self.assertRaises(UnicodeDecodeError):
      string_arabic[:17].decode("utf-8")

    with self.assertRaises(UnicodeDecodeError):
      string_misc[:17].decode("utf-8")

    with self.assertRaises(UnicodeDecodeError):
      string_cjk[:17].decode("utf-8")

    # verify various utf-8 lengths work
    self.assertEqual(next(response_utf8_stream(io.BytesIO(string_ascii), 17)), '"#$%&()*+,-./0123')
    self.assertEqual(next(response_utf8_stream(io.BytesIO(string_arabic), 17)), '،؛؟ءآأؤإ')
    self.assertEqual(next(response_utf8_stream(io.BytesIO(string_misc), 17)), '⌀⌂⌃⌄⌅')

    # verify middle and last parts of splits work
    chunks = response_utf8_stream(io.BytesIO(string_cjk), 17)
    self.assertEqual(next(chunks), '豈更車勞擄')
    self.assertEqual(next(chunks), '櫓爐盧老蘆虜')
    self.assertEqual(next(chunks), '路露魯鷺碌祿')
    self.assertEqual(next(chunks), '綠菉錄縷陋')
    self.assertEqual(next(chunks), '勒諒量')


class TestRecipe(unittest.TestCase):
  """Test the Recipe module.  Currently only testing recipe load and merge.
  """

  def test_recipe(self):
    """  Tests: get_recipe

    Verify that recipe is loaded correctly.
    Verify that an include is loaded correctly and parameters are expanded.

    """

    recipe = """
      {
        "setup":{
          "license":"Apache License, Version 2.0",
          "copyright":"Copyright 2020 Google LLC"
        },
        "tasks":[
          { "sample":{
            "query":"
              SELECT *
              FROM somwhere;
            ",
            "variable":{"field":{"name":"some_value", "kind":"string", "description":"Value for testing.", "prefix":"Before ", "suffix":" After", "default": "Yes"}},
            "constant":1234
          }}
        ]
      }
    """

    self.maxDiff = None
    self.assertEqual(get_recipe(stringcontent=recipe), {
      "setup":{
        "license":"Apache License, Version 2.0",
        "copyright":"Copyright 2020 Google LLC"
      },
      "tasks":[
        { "sample":{
          "query":"               SELECT *               FROM somwhere;             ",
          "variable":{"field":{"name":"some_value", "kind":"string", "description":"Value for testing.", "prefix":"Before ", "suffix":" After", "default": "Yes"}},
          "constant":1234
        }}
      ]
    })


  def test_merge_field(self):
    """  Tests: json_merge_field, json_merge_fields

    Name merges - from name must rename to.
    Suffix merges - to encompasses from so TFFT, hence suffix is FT, from + to.
    Prefix merges - to encompasses from so TFFT, hence suffix is TF, to + from.
    Default merges - from must overwirite to.

    """

    field_to = {"field":{"name":"some_value", "kind":"string", "description":"Value for testing.", "prefix":"Before ", "suffix":" After", "default": "Yes"}}
    field_from = {"field":{"name":"final_value", "kind":"string", "description":"Another for testing.", "prefix":"Pre ", "suffix":" Post", "default": "No"}}

    field_to = json_merge_field(field_to, field_from)

    self.maxDiff = None
    self.assertEqual(field_to, {"field":{
      "name":"final_value",
      "kind":"string",
      "description":"Another for testing.",
      "prefix":"Before Pre ",
      "suffix":" Post After",
      "default":"No"
    }})


  def test_merge_fields(self):
    """  Tests: json_merge_field, json_merge_fields

    Name merges - from name must rename to.
    Suffix merges - to encompasses from so TFFT, hence suffix is FT, from + to.
    Prefix merges - to encompasses from so TFFT, hence suffix is TF, to + from.
    Default merges - from must overwirite to.

    """

    parameters = {
      "field_merge":{"field":{"name":"final_value", "kind":"string", "description":"Another for testing.", "prefix":"Pre ", "suffix":" Post", "default": "No"}},
      "string_a": "Word",
      "int_1": 47,
      "bool_true": True
    }

    recipe = {
      "setup":{
        "license":"Apache License, Version 2.0",
        "copyright":"Copyright 2020 Google LLC"
      },
      "tasks":[
        { "sample":{
          "query":"SELECT * FROM somwhere;",
          "variable":{"field":{"name":"some_value", "kind":"string", "description":"Value for testing.", "prefix":"Before ", "suffix":" After", "default": "Yes"}},
          "constant":1234,
          "a":{"field":{"name":"field_merge", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
          "b":{"field":{"name":"field_merge", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
          "nested":{
            "a":{"field":{"name":"field_merge", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            "b":{"field":{"name":"field_merge", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            "c":{"field":{"name":"string_a", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            "d":{"field":{"name":"int_1", "kind":"integer", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            "e":{"field":{"name":"bool_true", "kind":"boolean", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            "f":'done'
          },
          "array":[
            {"field":{"name":"field_merge", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            {"field":{"name":"string_a", "kind":"string", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            {"field":{"name":"int_1", "kind":"integer", "description":"Gone.", "prefix":"Before ", "suffix":" After"}},
            "done"
          ]
        }}
      ]
    }

    recipe = json_merge_fields(recipe, parameters)

    self.maxDiff = None
    self.assertEqual(recipe, {
      "setup": {
        "license": "Apache License, Version 2.0",
        "copyright": "Copyright 2020 Google LLC"
     },
     "tasks": [
       {"sample": {
         "query": "SELECT * FROM somwhere;",
         "variable": {"field": {"name": "some_value", "kind": "string", "description": "Value for testing.", "prefix": "Before ", "suffix": " After", "default": "Yes"}},
         "constant": 1234,
         "a": {"field": {"name": "final_value", "kind": "string", "description": "Another for testing.", "prefix": "Before Pre ", "suffix": " Post After", "default": "No"}},
         "b": {"field": {"name": "final_value", "kind": "string", "description": "Another for testing.", "prefix": "Before Pre ", "suffix": " Post After", "default": "No"}},
         "nested": {
           "a": {"field": {"name": "final_value", "kind": "string", "description": "Another for testing.", "prefix": "Before Pre ", "suffix": " Post After", "default": "No"}},
           "b": {"field": {"name": "final_value", "kind": "string", "description": "Another for testing.", "prefix": "Before Pre ", "suffix": " Post After", "default": "No"}},
           "c": "Word",
           "d": 47,
           "e": True,
           "f": "done"
         },
         "array": [
           {"field": {"name": "final_value", "kind": "string", "description": "Another for testing.", "prefix": "Before Pre ", "suffix": " Post After", "default": "No"}},
           "Word",
           47,
           "done"
         ]
       }}
     ]
   })


  def test_includes(self):
    """  Tests: recipe_includes

    Requires scripts/hello.json recipe and UI_ROOT path set.
    Verify that script is included.
    Verify that remaining tasks as preserved.
    Verify that some fields are constants others fields.
    Verify that replace happens multiple times.

    """

    recipe = recipe_includes({
      "setup":{
        "license":"Apache License, Version 2.0",
        "copyright":"Copyright 2020 Google LLC"
      },
      "tasks":[
        { "include":{
          "script":"scripts/hello.json",
          "parameters":{
            "auth_read":"user",
            "say_first":"Hello",
            "say_second":{"field":{ "name":"field_two", "kind":"string", "description":"Type in a greeting." }},
            "error":{"field":{ "name":"field_three", "kind":"string", "description":"Optional error for testing." }},
            "sleep":{"field":{ "name":"sleep", "kind":"integer", "description":"Seconds to sleep." }}
          }
        }},
        { "sample":{}}
      ]},
      UI_ROOT
    )

    self.maxDiff = None
    self.assertEqual(recipe, {
      "setup": {
        "license": "Apache License, Version 2.0",
        "copyright": "Copyright 2020 Google LLC"
      },
      "tasks": [
        { "hello": {
          "auth": "user",
          "say": "Hello",
          "error":{"field":{ "name":"field_three", "kind":"string", "description":"Optional error for testing.", "order":3, "default":""}},
          "sleep":{"field":{ "name":"sleep", "kind":"integer", "description":"Seconds to sleep.", "order": 4, "default":0 }}
        }},
        { "hello": {
          "auth": "user",
          "say": {"field": {"name": "field_two", "kind": "string", "order": 1, "default": "Hello Twice", "description": "Type in a greeting."}},
          "sleep": {"field": {"name": "sleep", "kind": "integer", "order": 4, "default": 0, "description": "Seconds to sleep."}}
        }},
        { "sample":{}}
      ]
    })


  def test_set_fields(self):
    """  Tests: recipe_set_feilds

    Tests typical process of merge fields during include.
    Followed by application of constant parameters.
    Unlinke recipe_merge_fields this will set default values from a field.

    """

    original = {
      "first":{"field":{ "name":"recipe_name", "kind":"string", "prefix":"Twitter Targeting For ", "order":2, "description":"Name of sheet where Line Item settings will be read from.", "default":"" }},
      "another":{"field":{ "name":"another_name", "kind":"string", "description":"The sheet to use for the test.", "prefix":"StarThinker Test Twitter ", "default": "Also"}}
    }
    include = {
      "recipe_name":{"field":{ "name":"test_run_id", "kind":"string", "description":"The sheet to use for the test.", "prefix":"StarThinker Test Twitter ", "default": "Middle"}}
    }
    harness = { "test_run_id": "Manual" }

    self.maxDiff = None

    recipe = json_merge_fields(original, include)
    self.assertEqual(recipe, {
      "first": {"field": {"name": "test_run_id", "kind": "string", "prefix": "Twitter Targeting For StarThinker Test Twitter ", "order": 2, "description": "The sheet to use for the test.", "default": "Middle"}},
      "another":{"field":{ "name":"another_name", "kind":"string", "description":"The sheet to use for the test.", "prefix":"StarThinker Test Twitter ", "default": "Also"}}
    })

    recipe = json_set_fields(recipe, harness)
    self.assertEqual(recipe, {
      "first": "Twitter Targeting For StarThinker Test Twitter Manual",
      "another":"StarThinker Test Twitter Also"
    })


if __name__ == '__main__':
  unittest.main()
