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


from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_DV360
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.regexp import lookup_id


def insertion_order_clear(config, task):
  table_create(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "DV_InsertionOrders",
    Discovery_To_BigQuery(
      "displayvideo",
      "v1"
    ).method_schema(
      "advertisers.insertionOrders.list"
    )
  )


def insertion_order_load(config, task):

  # load multiple from user defined sheet
  def insertion_order_load_multiple():
    for row in get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Advertisers",
        "header":False,
        "range": "A2:A"
      }}
    ):
      if row:
        yield from API_DV360(
          config,
          task["auth_dv"],
          iterate=True
        ).advertisers().insertionOrders().list(
          advertiserId=lookup_id(row[0]),
          filter='entityStatus="ENTITY_STATUS_PAUSED" OR entityStatus="ENTITY_STATUS_ACTIVE" OR entityStatus="ENTITY_STATUS_DRAFT"'
        ).execute()

  insertion_order_clear(config, task)

  # write to database
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "DV_InsertionOrders",
      "schema": Discovery_To_BigQuery(
        "displayvideo",
        "v1"
      ).method_schema("advertisers.insertionOrders.list"),
      "format": "JSON"
    }},
    insertion_order_load_multiple()
  )
