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


def creative_clear():
  table_create(
    project.task["auth_bigquery"],
    project.id,
    project.task["dataset"],
    "DV_Creatives",
    Discovery_To_BigQuery(
      "displayvideo",
      "v1"
    ).method_schema("advertisers.creatives.list"),
  )

  sheets_clear(project.task["auth_sheets"], project.task["sheet"], "Creatives", "B2:Z")


def creative_load():

  # load multiple partners from user defined sheet
  def creative_load_multiple():
    rows = get_rows(
      project.task["auth_sheets"], {
        "sheets": {
          "sheet": project.task["sheet"],
          "tab": "Advertisers",
          "range": "A2:A"
        }
    })

    for row in rows:
      yield from API_DV360(
        project.task["auth_dv"], iterate=True).advertisers().creatives().list(
          advertiserId=lookup_id(row[0])
        ).execute()

  # write creatives to database and sheet
  put_rows(
    project.task["auth_bigquery"], {
      "bigquery": {
        "dataset":project.task["dataset"],
        "table":"DV_Creatives",
        "schema":Discovery_To_BigQuery(
          "displayvideo",
          "v1"
        ).method_schema("advertisers.creatives.list"),
        "format": "JSON"
      }
    }, creative_load_multiple()
  )

  # write creatives to sheet
  rows = get_rows(
    project.task["auth_bigquery"], {
      "bigquery": {
        "dataset":project.task["dataset"],
        "query":"""SELECT
          CONCAT(P.displayName, ' - ', P.partnerId),
          CONCAT(A.displayName, ' - ', A.advertiserId),
          CONCAT(C.displayName, ' - ', C.creativeId),
          C.entityStatus,
          C.creativeType,
          C.dimensions.widthPixels,
          C.dimensions.heightPixels,
          C.reviewStatus.approvalStatus,
          C.reviewStatus.creativeAndLandingPageReviewStatus,
          C.reviewStatus.contentAndPolicyReviewStatus,
          COUNTIF(RS.status='REVIEW_STATUS_UNSPECIFIED') OVER() AS Exchanges_Unspecified,
          COUNTIF(RS.status='REVIEW_STATUS_PENDING') OVER() AS Exchanges_Pending,
          COUNTIF(RS.status='REVIEW_STATUS_REJECTED') OVER() AS Exchanges_Rejected,
          COUNTIF(RS.status='REVIEW_STATUS_APPROVED') OVER() AS Exchanges_Approved,
          COUNTIF(RP.status='REVIEW_STATUS_UNSPECIFIED') OVER() AS Publishers_Unspecified,
          COUNTIF(RP.status='REVIEW_STATUS_PENDING') OVER() AS Publishers_Pending,
          COUNTIF(RP.status='REVIEW_STATUS_REJECTED') OVER() AS Publishers_Rejected,
          COUNTIF(RP.status='REVIEW_STATUS_APPROVED') OVER() AS Publishers_Approved,
          FROM `{dataset}.DV_Creatives` AS C, UNNEST(reviewStatus.exchangeReviewStatuses) AS RS, UNNEST(reviewStatus.publisherReviewStatuses) AS RP
          LEFT JOIN `{dataset}.DV_Advertisers` AS A
          ON C.advertiserId=A.advertiserId
          LEFT JOIN `{dataset}.DV_Partners` AS P
          ON A.partnerId=P.partnerId
        """.format(**project.task),
        "legacy":False
      }
    }
  )

  put_rows(
    project.task["auth_sheets"],
    {
      "sheets": {
        "sheet": project.task["sheet"],
        "tab": "Creatives",
        "range": "B2"
      }
    },
    rows
  )
