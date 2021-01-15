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
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.project import project
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear


def line_item_clear():
  table_create(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "DV_LineItems",
    Discovery_To_BigQuery(
      "displayvideo",
      "v1"
    ).method_schema(
      "advertisers.lineItems.list"
    )
  )

  sheets_clear(
    project.task["auth_sheets"],
    project.task["sheet"],
    "Line Items",
    "B2:Z"
  )


def line_item_load():

  # load multiple partners from user defined sheet
  def load_multiple():
    rows = get_rows(
      project.task["auth_sheets"],
      { "sheets": {
        "sheet": project.task["sheet"],
        "tab": "Advertisers",
        "range": "A2:A"
      }}
    )

    for row in rows:
      yield from API_DV360(
        project.task["auth_dv"],
        iterate=True
      ).advertisers().lineItems().list(
        advertiserId=lookup_id(row[0])
      ).execute()

  # write line_items to database
  put_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "table": "DV_LineItems",
      "schema": Discovery_To_BigQuery(
        "displayvideo",
        "v1"
      ).method_schema(
        "advertisers.lineItems.list"
      ),
      "format":"JSON"
    }},
    load_multiple()
  )

  # write line items to sheet
  rows = get_rows(
    project.task["auth_bigquery"],
    { "bigquery": {
      "dataset": project.task["dataset"],
      "query": """SELECT
        CONCAT(P.displayName, ' - ', P.partnerId),
        CONCAT(A.displayName, ' - ', A.advertiserId),
        CONCAT(C.displayName, ' - ', C.campaignId),
        CONCAT(I.displayName, ' - ', I.insertionOrderId),
        CONCAT(L.displayName, ' - ', L.lineItemId),
        L.entityStatus,
        ARRAY_TO_STRING(L.warningMessages, '\\n'),
        FROM `{dataset}.DV_LineItems` AS L
        LEFT JOIN `{dataset}.DV_Advertisers` AS A
        ON L.advertiserId=A.advertiserId
        LEFT JOIN `{dataset}.DV_Campaigns` AS C
        ON L.advertiserId=C.advertiserId
        LEFT JOIN `{dataset}.DV_InsertionOrders` AS I
        ON L.insertionOrderId=I.insertionOrderId
        LEFT JOIN `{dataset}.DV_Partners` AS P
        ON A.partnerId=P.partnerId
      """.format(**project.task),
      "legacy": False
    }}
  )

  put_rows(
    project.task["auth_sheets"],
    { "sheets": {
      "sheet": project.task["sheet"],
      "tab": "Line Items",
      "range": "B2"
    }},
    rows
  )


def line_item_load_targeting():

  def load_bulk():
    # TODO: incorporate filters into line item fetch
    line_items = [lookup_id(p[0]) for p in get_rows(
      project.task['auth_sheets'],
      { 'sheets': {
        'sheet': project.task['sheet'],
        'tab': 'Line Items',
        'range': 'A2:A'
      }}
    )]

    parameters = get_rows(
      project.task["auth_bigquery"],
      { "bigquery": {
        "dataset": project.task["dataset"],
        "query":"SELECT advertiserId, lineItemId FROM `{dataset}.DV_LineItems`".format(**project.task)
      }},
      as_object=True
    )

    for parameter in parameters:
      yield from API_DV360(
        project.task["auth_dv"],
        iterate=True
      ).advertisers().lineItems().bulkListLineItemAssignedTargetingOptions(
        advertiserId=str(parameter['advertiserId']),
        lineItemId=str(parameter['lineItemId']),
      ).execute()

  put_rows(
    project.task['auth_bigquery'],
    { 'bigquery': {
      'dataset': project.task['dataset'],
      'table': 'DV_Targeting',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).resource_schema(
        'AssignedTargetingOption'
      ),
      'disposition':'WRITE_APPEND',
      'format': 'JSON'
    }},
    load_bulk()
  )
