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

from starthinker.util.bigquery import query_to_view
from starthinker.util.bigquery import table_create
from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.google_api import API_DV360
from starthinker.util.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.regexp import lookup_id
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_targeter.edit import edit_log
from starthinker.task.dv_targeter.edit import edit_preview

from starthinker.util.dv_targeting import Assigned_Targeting


TARGETING_TYPES = [
  'TARGETING_TYPE_EXCHANGE',
  'TARGETING_TYPE_SUB_EXCHANGE',
  'TARGETING_TYPE_BROWSER',
  'TARGETING_TYPE_LANGUAGE',
  'TARGETING_TYPE_DEVICE_MAKE_MODEL',
  'TARGETING_TYPE_OPERATING_SYSTEM',
  'TARGETING_TYPE_LANGUAGE',
  'TARGETING_TYPE_CARRIER_AND_ISP',
  'TARGETING_TYPE_CATEGORY',
  'TARGETING_TYPE_APP_CATEGORY',
]


def targeting_clear(config, task):
  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Targeting_Options',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).resource_schema(
      'TargetingOption'
    )
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Targeting Options',
    'A2:Q'
  )

  table_create(
    config,
    task['auth_bigquery'],
    config.project,
    task['dataset'],
    'DV_Targeting_Assigned',
    Discovery_To_BigQuery(
      'displayvideo',
      'v1'
    ).resource_schema(
      'AssignedTargetingOption'
    )
  )


def targeting_clear_changes(config, task):
  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Destination Targeting',
    'A2:Z'
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Brand Safety Targeting',
    'A2:Z'
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Demographic Targeting',
    'A2:Z'
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Audience Targeting',
    'A2:Z'
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Device Targeting',
    'A2:Z'
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Geography Targeting',
    'A2:Z'
  )

  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Viewability Targeting',
    'A2:Z'
  )


def targeting_load(config, task):

  # load multiple from user defined sheet
  def load_multiple():
    advertisers = get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'Advertisers',
        "header":False,
        'range': 'A2:A'
      }}
    )

    for advertiser in advertisers:
      for targeting_type in TARGETING_TYPES:
        yield from API_DV360(
          config,
          task['auth_dv'],
          iterate=True
        ).targetingTypes().targetingOptions().list(
          advertiserId=str(lookup_id(advertiser[0])),
          targetingType=targeting_type
        ).execute()

  targeting_clear(config, task)

  # write to database
  put_rows(
    config,
    task['auth_bigquery'],
    { 'bigquery': {
      'dataset': task['dataset'],
      'table': 'DV_Targeting_Options',
      'schema': Discovery_To_BigQuery(
        'displayvideo',
        'v1'
      ).method_schema(
        'targetingTypes.targetingOptions.list'
      ),
      'format': 'JSON'
    }},
    load_multiple()
  )

  # write app category
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'A2:A'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(appCategoryDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write exchange
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'B2:B'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(subExchangeDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write browser
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'C2:C'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(browserDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write make / model
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'D2:D'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(deviceMakeModelDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write category
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'E2:E'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(categoryDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write language
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'F2:F'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(languageDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write operating system
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'G2:G'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           DISTINCT(operatingSystemDetails.displayName)
           FROM `{dataset}.DV_Targeting_Options`
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )

  # write carrier and isp
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Targeting Options',
      "header":False,
      'range': 'H2:H'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT
           CONCAT(carrierAndIspDetails.displayName, ' - ', SUBSTR(carrierAndIspDetails.type, 22))
           FROM `{dataset}.DV_Targeting_Options`
           GROUP BY 1
           ORDER BY 1
        """.format(**task),
        'legacy': False
      }}
    )
  )


def targeting_combine(config, task):

  # read destination targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Destination_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Authorized_Seller", "type": "STRING" },
        { "name": "User_Rewarded_Content", "type": "STRING" },
        { "name": "Exchange", "type": "STRING" },
        { "name": "Sub_Exchange", "type": "STRING" },
        { "name": "Channel", "type": "STRING" },
        { "name": "Channel_Negative", "type": "BOOLEAN" },
        { "name": "Inventory_Source", "type": "STRING" },
        { "name": "Inventory_Group", "type": "STRING" },
        { "name": "URL", "type": "STRING" },
        { "name": "URL_Negative", "type": "BOOLEAN" },
        { "name": "App", "type": "STRING" },
        { "name": "App_Negative", "type": "BOOLEAN" },
        { "name": "App_Category", "type": "STRING" },
        { "name": "App_Category_Negative", "type": "BOOLEAN" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Destination Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  # read brand safety targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Brand_Safety_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Content_Label", "type": "STRING" },
        { "name": "Sensitive_Category", "type": "STRING" },
        { "name": "Negative_Keyword_List", "type": "STRING" },
        { "name": "Category", "type": "STRING" },
        { "name": "Category_Negative", "type": "BOOLEAN" },
        { "name": "Keyword", "type": "STRING" },
        { "name": "Keyword_Negative", "type": "BOOLEAN" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Brand Safety Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  # read demographic targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Demographic_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Age_Range", "type": "STRING" },
        { "name": "Gender", "type": "STRING" },
        { "name": "Parental_Status", "type": "STRING" },
        { "name": "Household_Income", "type": "STRING" },
        { "name": "Language", "type": "STRING" },
        { "name": "Language_Negative", "type": "BOOLEAN" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Demographic Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  # read audience targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Audience_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Included_1P_And_3P_Group", "type": "INTEGER" },
        { "name": "Included_1P_And_3P", "type": "STRING" },
        { "name": "Included_1P_And_3P_Recency", "type": "STRING" },
        { "name": "Excluded_1P_And_3P", "type": "STRING" },
        { "name": "Excluded_1P_And_3P_Recency", "type": "STRING" },
        { "name": "Included_Google", "type": "STRING" },
        { "name": "Excluded_Google", "type": "STRING" },
        { "name": "Included_Custom", "type": "STRING" },
        { "name": "Included_Combined", "type": "STRING" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Audience Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  # read device targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Device_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Device_Type", "type": "STRING" },
        { "name": "Make_Model", "type": "STRING" },
        { "name": "Make_Model_Negative", "type": "BOOLEAN" },
        { "name": "Operating_System", "type": "STRING" },
        { "name": "Operating_System_Negative", "type": "BOOLEAN" },
        { "name": "Browser", "type": "STRING" },
        { "name": "Browser_Negative", "type": "BOOLEAN" },
        { "name": "Environment", "type": "STRING" },
        { "name": "Carrier_And_ISP", "type": "STRING" },
        { "name": "Carrier_And_ISP_Negative", "type": "BOOLEAN" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Device Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  # read geography targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Geography_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Day_Of_Week", "type": "STRING" },
        { "name": "Hour_Start", "type": "INTEGER" },
        { "name": "Hour_End", "type": "INTEGER" },
        { "name": "Timezone", "type": "STRING" },
        { "name": "Geo_Region", "type": "STRING" },
        { "name": "Geo_Region_Type", "type": "STRING" },
        { "name": "Geo_Region_Negative", "type": "BOOLEAN" },
        { "name": "Proximity_Location_List", "type": "STRING" },
        { "name": "Proximity_Location_List_Radius_Range", "type": "STRING" },
        { "name": "Regional_Location_List", "type": "STRING" },
        { "name": "Regional_Location_List_Negative", "type": "BOOLEAN" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Geography Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  # read viewability targeting
  put_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table": "SHEET_Viewability_Targeting",
      "schema": [
        { "name": "Action", "type": "STRING" },
        { "name": "Partner", "type": "STRING" },
        { "name": "Advertiser", "type": "STRING" },
        { "name": "LineItem", "type": "STRING" },
        { "name": "Video_Player_Size", "type": "STRING" },
        { "name": "In_Stream_Position", "type": "STRING" },
        { "name": "Out_Stream_Position", "type": "BOOLEAN" },
        { "name": "On_Screen_Position", "type": "STRING" },
        { "name": "Viewability", "type": "STRING" },
      ],
      "format": "CSV"
    }},
    get_rows(
      config,
      task["auth_sheets"],
      { "sheets": {
        "sheet": task["sheet"],
        "tab": "Viewability Targeting",
        "header":False,
        "range": "A2:Z"
      }}
    )
  )

  query_to_view(
    config,
    task["auth_bigquery"],
    config.project,
    task["dataset"],
    "SHEET_Combined_Targeting",
    """SELECT
        COALESCE(
          L.advertiserId,
          A.advertiserId,
          CAST(REGEXP_EXTRACT(Advertiser, r' - (\d+)$') AS INT64)
        ) AS Advertiser_Lookup,
        T.*
      FROM (
        SELECT
          COALESCE(A.Action,B.Action,C.Action,D.Action,E.Action,F.Action,G.Action) AS Action,
          COALESCE(A.partner,B.Partner,C.Partner,D.partner,E.Partner,F.Partner,G.Partner) AS Partner,
          COALESCE(A.Advertiser,B.Advertiser,C.Advertiser,D.Advertiser,E.Advertiser,F.Advertiser,G.Advertiser) AS Advertiser,
          COALESCE(A.LineItem,B.LineItem,C.LineItem,D.LineItem,E.LineItem,F.LineItem,G.LineItem) AS LineItem,
          * EXCEPT (Action, Partner, Advertiser, LineItem)
        FROM `{dataset}.SHEET_Destination_Targeting` AS A
        FULL OUTER JOIN `{dataset}.SHEET_Brand_Safety_Targeting` AS B
        ON A.Action=B.Action
        AND A.Partner=B.Partner
        AND A.Advertiser=B.Advertiser
        AND A.LineItem=B.LineItem
        FULL OUTER JOIN `{dataset}.SHEET_Demographic_Targeting` AS C
        ON A.Action=C.Action
        AND A.Partner=C.Partner
        AND A.Advertiser=C.Advertiser
        AND A.LineItem=C.LineItem
        FULL OUTER JOIN `{dataset}.SHEET_Audience_Targeting` AS D
        ON A.Action=D.Action
        AND A.Partner=D.Partner
        AND A.Advertiser=D.Advertiser
        AND A.LineItem=D.LineItem
        FULL OUTER JOIN `{dataset}.SHEET_Device_Targeting` AS E
        ON A.Action=E.Action
        AND A.Partner=E.Partner
        AND A.Advertiser=E.Advertiser
        AND A.LineItem=E.LineItem
        FULL OUTER JOIN `{dataset}.SHEET_Geography_Targeting` AS F
        ON A.Action=F.Action
        AND A.Partner=F.Partner
        AND A.Advertiser=F.Advertiser
        AND A.LineItem=F.LineItem
        FULL OUTER JOIN `{dataset}.SHEET_Viewability_Targeting` AS G
        ON A.Action=G.Action
        AND A.Partner=G.Partner
        AND A.Advertiser=G.Advertiser
        AND A.LineItem=G.LineItem
      ) AS T
      LEFT JOIN `{dataset}.DV_LineItems` AS L
      ON CAST(REGEXP_EXTRACT(T.LineItem, r' - (\d+)$') AS INT64)=L.lineItemId
      LEFT JOIN (
        SELECT partnerId, advertiserId
        FROM `{dataset}.DV_Advertisers`
        GROUP BY 1,2
      ) AS A
      ON CAST(REGEXP_EXTRACT(T.Partner, r' - (\d+)$') AS INT64)=A.partnerId
    """.format(**task),
    legacy=False
  )


def targeting_edit(config, task, commit=False):
  edits = []
  targetings = {}

  targeting_combine(config, task)

  for row in get_rows(
    config,
    task["auth_bigquery"],
    { "bigquery": {
      "dataset": task["dataset"],
      "table":"SHEET_Combined_Targeting",
    }},
    as_object=True
  ):

    # check if settings are applied at this layer
    if not row['Action']: continue

    # create new batch of candidates
    candidates = []

    # check partner ID from sheet
    if row['Partner']:

      # if action is at Advertiser layer, translate partner into list of advertisers
      if 'ADVERTISERS' in row['Action'].upper():
        for advertiserId in get_rows(
          config,
          task['auth_bigquery'],
          { 'bigquery': {
            'dataset': task['dataset'],
            'query': "SELECT advertiserId FROM `{dataset}.DV_Advertisers` WHERE partnerId={partnerId};".format(
              dataset=task['dataset'],
              partnerId=lookup_id(row['Partner'])
            ),
            'legacy': False
          }},
          unnest=True
        ):
          candidates.append(
            targetings.setdefault(
              ('Advertiser', 'Partner {0} : {1}'.format(row['Partner'], advertiserId)),
              Assigned_Targeting(
                config,
                task["auth_dv"],
                None,
                advertiserId,
                None
              )
            )
          )

      # if action is at LineItem layer, translate partner into list of lineitems
      elif 'LINEITEMS' in row['Action'].upper():
        print("NOT IMPLEMENTED UNTIL FURTHER EVALUATION")

      # if action is directly on Partner, only add it to the list
      else:
        candidates.append(
          targetings.setdefault(
            ('Partner', row['Partner']),
            Assigned_Targeting(
              config,
              task["auth_dv"],
              lookup_id(row['Partner']),
              row['Advertiser_Lookup'], # required by API for lookup of values ( not for targeting )
              None
            )
          )
        )

    # check advertiser ID from sheet
    if row['Advertiser']:

      # if action is at LineItem layer, translate advertiser into list of lineitems
      if 'LINEITEMS' in row['Action'].upper():
        for lineItemId in get_rows(
          config,
          task['auth_bigquery'],
          { 'bigquery': {
            'dataset': task['dataset'],
            'query': "SELECT lineItemId FROM `{dataset}.DV_LineItems` WHERE advertiserId={advertiserId};".format(
              dataset=task['dataset'],
              advertiserId=lookup_id(row['Advertiser'])
            ),
            'legacy': False
          }},
          unnest=True
        ):
          candidates.append(
            targetings.setdefault(
              ('LineItem', 'Advertiser {0} : {1}'.format(row['Advertiser'], lineItemId)),
              Assigned_Targeting(
                config,
                task["auth_dv"],
                None,
                lookup_id(row['Advertiser']),
                lineItemId
              )
            )
          )

      # if action is directly on Advertiser, only add it to the list
      else:
        candidates.append(
          targetings.setdefault(
            ('Advertiser', row['Advertiser']),
            Assigned_Targeting(
              config,
              task["auth_dv"],
              None,
              lookup_id(row['Advertiser']),
              None
            )
          )
        )

    # check lineitem ID from sheet
    if row['LineItem']:
      candidates.append(
        targetings.setdefault(
          ('LineItem', row['LineItem']),
          Assigned_Targeting(
            config,
            task["auth_dv"],
            None,
            row['Advertiser_Lookup'],
            lookup_id(row['LineItem'])
          )
        )
      )

    # attempt targeting changes for each candidate
    for targeting in candidates:
      if row['Authorized_Seller']:
        if 'ADD' in row['Action'].upper():
          targeting.add_authorized_seller(row['Authorized_Seller'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_authorized_seller(row['Authorized_Seller'])

      if row['User_Rewarded_Content']:
        if 'ADD' in row['Action'].upper():
          targeting.add_user_rewarded_content(row['User_Rewarded_Content'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_user_rewarded_content(row['User_Rewarded_Content'])

      if row['Exchange']:
        if 'ADD' in row['Action'].upper():
          targeting.add_exchange(row['Exchange'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_exchange(row['Exchange'])

      if row['Sub_Exchange']:
        if 'ADD' in row['Action'].upper():
          targeting.add_sub_exchange(row['Sub_Exchange'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_sub_exchange(row['Sub_Exchange'])

      if row['Channel']:
        identifier = lookup_id(row['Channel'])
        if 'ADD' in row['Action'].upper():
          targeting.add_channel(identifier, row['Channel_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_channel(identifier)

      if row['Inventory_Source']:
        identifier = lookup_id(row['Inventory_Source'])
        if 'ADD' in row['Action'].upper():
          targeting.add_inventory_source(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_inventory_source(identifier)

      if row['Inventory_Group']:
        identifier = lookup_id(row['Inventory_Group'])
        if 'ADD' in row['Action'].upper():
          targeting.add_inventory_source_group(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_inventory_source_group(identifier)

      if row['URL']:
        if 'ADD' in row['Action'].upper():
          targeting.add_url(row['URL'], row['URL_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_url(row['URL'])

      if row['App']:
        identifier = lookup_id(row['App'])
        if 'ADD' in row['Action'].upper():
          targeting.add_app(identifier, row['App_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_app(identifier)

      if row['App_Category']:
        if 'ADD' in row['Action'].upper():
          targeting.add_app_category(row['App_Category'], row['App_Category_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_app_category(row['App_Category'])

      if row['Content_Label']:
        if 'ADD' in row['Action'].upper():
          targeting.add_content_label(row['Content_Label'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_content_label(row['Content_Label'])

      if row['Sensitive_Category']:
        if 'ADD' in row['Action'].upper():
          targeting.add_sensitive_category(row['Sensitive_Category'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_sensitive_category(row['Sensitive_Category'])

      if row['Negative_Keyword_List']:
        identifier = lookup_id(row['Negative_Keyword_List'])
        if 'ADD' in row['Action'].upper():
          targeting.add_negative_keyword_list(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_negative_keyword_list(identifier)

      if row['Keyword']:
        if 'ADD' in row['Action'].upper():
          targeting.add_keyword(row['Keyword'], row['Keyword_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_keyword(row['Keyword'])

      if row['Category']:
        if 'ADD' in row['Action'].upper():
          targeting.add_category(row['Category'], row['Category_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_category(row['Category'])

      if row['Age_Range']:
        if 'ADD' in row['Action'].upper():
          targeting.add_age_range(row['Age_Range'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_age_range(row['Age_Range'])

      if row['Gender']:
        if 'ADD' in row['Action'].upper():
          targeting.add_gender(row['Gender'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_gender(row['Gender'])

      if row['Parental_Status']:
        if 'ADD' in row['Action'].upper():
          targeting.add_parental_status(row['Parental_Status'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_parental_status(row['Parental_Status'])

      if row['Geo_Region']:
        if 'ADD' in row['Action'].upper():
          targeting.add_geo_region(row['Geo_Region'], row['Geo_Region_Type'], row['Geo_Region_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_geo_region(row['Geo_Region'])

      if row['Proximity_Location_List']:
        if 'ADD' in row['Action'].upper():
          targeting.add_proximity_location_list(row['Proximity_Location_List'], row['Proximity_Location_List_Radius_Range'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_proximity_location_list(row['Proximity_Location_List'])

      if row['Regional_Location_List']:
        identifier = lookup_id(row['Regional_Location_List'])
        if 'ADD' in row['Action'].upper():
          targeting.add_regional_location_list(identifier, row['Regional_Location_List_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_regional_location_list(identifier)

      if row['Household_Income']:
        if 'ADD' in row['Action'].upper():
          targeting.add_household_income(row['Household_Income'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_household_income(row['Household_Income'])

      if row['Language']:
        if 'ADD' in row['Action'].upper():
          targeting.add_language(row['Language'], row['Language_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_language(row['Language'])

      if row['Included_1P_And_3P']:
        identifier = lookup_id(row['Included_1P_And_3P'])
        if 'ADD' in row['Action'].upper():
          targeting.add_included_1p_and_3p_audience(identifier, row['Included_1P_And_3P_Recency'], row['Included_1P_And_3P_Group'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_included_1p_and_3p_audience(identifier, row['Included_1P_And_3P_Recency'], row['Included_1P_And_3P_Group'])

      if row['Excluded_1P_And_3P']:
        identifier = lookup_id(row['Excluded_1P_And_3P'])
        if 'ADD' in row['Action'].upper():
          targeting.add_excluded_1p_and_3p_audience(identifier, row['Excluded_1P_And_3P_Recency'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_excluded_1p_and_3p_audience(identifier, row['Excluded_1P_And_3P_Recency'])

      if row['Included_Google']:
        identifier = lookup_id(row['Included_Google'])
        if 'ADD' in row['Action'].upper():
          targeting.add_included_google_audience(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_included_google_audience(identifier)

      if row['Excluded_Google']:
        identifier = lookup_id(row['Excluded_Google'])
        if 'ADD' in row['Action'].upper():
          targeting.add_excluded_google_audience(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_excluded_google_audience(identifier)

      if row['Included_Custom']:
        identifier = lookup_id(row['Included_Custom'])
        if 'ADD' in row['Action'].upper():
          targeting.add_included_custom_audience(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_included_custom_audience(identifier)

      if row['Included_Combined']:
        identifier = lookup_id(row['Included_Combined'])
        if 'ADD' in row['Action'].upper():
          targeting.add_included_combined_audience(identifier)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_included_combined_audience(identifier)

      if row['Device_Type']:
        if 'ADD' in row['Action'].upper():
          targeting.add_device_type(row['Device_Type'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_device_type(row['Device_Type'])

      if row['Make_Model']:
        if 'ADD' in row['Action'].upper():
          targeting.add_make_model(row['Make_Model'], row['Make_Model_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_make_model(row['Make_Model'])

      if row['Operating_System']:
        if 'ADD' in row['Action'].upper():
          targeting.add_operating_system(row['Operating_System'], row['Operating_System_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_operating_system(row['Operating_System'])

      if row['Browser']:
        if 'ADD' in row['Action'].upper():
          targeting.add_browser(row['Browser'], row['Browser_Negative'] or False)
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_browser(row['Browser'])

      if row['Environment']:
        if 'ADD' in row['Action'].upper():
          targeting.add_environment(row['Environment'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_environment(row['Environment'])

      if row['Carrier_And_ISP']:
        if 'ADD' in row['Action'].upper():
          targeting.add_carrier_and_isp(row['Carrier_And_ISP'], row['Carrier_And_ISP_Negative'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_carrier_and_isp(row['Carrier_And_ISP'])

      if row['Day_Of_Week']:
        if 'ADD' in row['Action'].upper():
          targeting.add_day_and_time(row['Day_Of_Week'], row['Hour_Start'], row['Hour_End'], row['Timezone'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_day_and_time(row['Day_Of_Week'], row['Hour_Start'], row['Hour_End'], row['Timezone'])

      if row['Video_Player_Size']:
        if 'ADD' in row['Action'].upper():
          targeting.add_video_player_size(row['Video_Player_Size'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_video_player_size(row['Video_Player_Size'])

      if row['In_Stream_Position']:
        if 'ADD' in row['Action'].upper():
          targeting.add_instream_position(row['In_Stream_Position'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_instream_position(row['In_Stream_Position'])

      if row['Out_Stream_Position']:
        if 'ADD' in row['Action'].upper():
          targeting.add_outstream_position(row['Out_Stream_Position'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_outstream_position()

      if row['On_Screen_Position']:
        if 'ADD' in row['Action'].upper():
          targeting.add_on_screen_position(row['On_Screen_Position'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_on_screen_position(row['On_Screen_Position'])

      if row['Viewability']:
        if 'ADD' in row['Action'].upper():
          targeting.add_viewability(row['Viewability'])
        elif 'DELETE' in row['Action'].upper():
          targeting.delete_viewability(row['Viewability'])


  for layer_and_name, targeting in targetings.items():
    layer, name = layer_and_name
    body = targeting.get_body()
    warnings = targeting.get_warnings()

    if body:
      parameters = {'body':body}

      if layer == 'Partner':
        parameters['partnerId'] = str(targeting.partner)
      elif layer == 'Advertiser':
        parameters['advertiserId'] = str(targeting.advertiser)
      elif layer == 'LineItem':
        parameters['advertiserId'] = str(targeting.advertiser)
        parameters['lineItemId'] = str(targeting.lineitem)

      edits.append({
        "layer": layer,
        "partner": name if layer == 'Partner' else '',
        "advertiser": name if layer == 'Advertiser' else '',
        "line_item": name if layer == 'LineItem' else '',
        "parameters": parameters
      })

    if warnings:
      edit_log(config, task, {
        "layer": layer,
        "partner": name if layer == 'Partner' else '',
        "advertiser": name if layer == 'Advertiser' else '',
        "line_item": name if layer == 'LineItem' else '',
        "warning": "\n".join(warnings)
     })

  edit_preview(config, task, edits)

  if commit:
    targeting_commit(config, task, edits)


def targeting_commit(config, task, edits):
  for edit in edits:
    try:
      if edit.get("line_item"):
        print("API LINE ITEM:", edit["line_item"])
        response = API_DV360(
          config,
          task["auth_dv"]
        ).advertisers().lineItems().bulkEditLineItemAssignedTargetingOptions(
          **edit["parameters"]
        ).execute()
        edit["success"] = len(response.get("createdAssignedTargetingOptions", []))
      elif edit.get("advertiser"):
        print("API ADVERTISER:", edit["advertiser"])
        response = API_DV360(
          config,
          task["auth_dv"]
        ).advertisers().bulkEditAdvertiserAssignedTargetingOptions(
          **edit["parameters"]
        ).execute()
        edit["success"] = len(response.get("createdAssignedTargetingOptions", []))
      elif edit.get("partner"):
        print("API PARTNER:", edit["partner"])
        response = API_DV360(
          config,
          task["auth_dv"]
        ).partners().bulkEditPartnerAssignedTargetingOptions(
          **edit["parameters"]
        ).execute()
        edit["success"] = len(response.get("createdAssignedTargetingOptions", []))
    except Exception as e:
      edit["error"] = str(e)
    finally:
      edit_log(config, task, edit)
  edit_log(config, task)
