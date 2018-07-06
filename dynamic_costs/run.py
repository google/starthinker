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


from util.project import project 
from util.bigquery import rows_to_table, query_to_view
from util.sheets import sheets_tab_copy, sheets_read
from util.dcm import report_build, report_file, report_to_rows, report_clean, report_schema, DCM_CHUNK_SIZE


def write_report(report, dataset, table):
  # turn report file into rows
  rows = report_to_rows(report)
  rows = report_clean(rows)

  if rows:
    if project.verbose: print "DYNAMIC COSTS WRITTEN:", table

    # pull DCM schema automatically
    schema = report_schema(rows.next())

    # write report to bigquery
    rows_to_table(
      project.task['out']["auth"],
      project.id,
      project.task['out']["dataset"],
      table,
      rows,
      schema,
      0
    )

  else:
    if project.verbose: print "DYNAMIC COSTS REPORT NOT READY:", table



def report_combos(name, startDate, endDate, advertiser, campaign, dynamicProfile):
  if project.verbose: print "DYNAMIC COSTS COMBOS:", name

  # create the report if it does not exist
  report = report_build(
    project.task["auth"],
    project.task["account"],
    {
      "kind": "dfareporting#report",
      "type": "STANDARD",
      "name": "Dynamic Costs %s - Dynamic Combos ( StarThinker )" % name,
      "criteria": {
        "dateRange": {
          "kind": "dfareporting#dateRange",
          "startDate": str(startDate),
          "endDate": str(endDate),
        },
        "dimensionFilters": [
          {
            "kind": "dfareporting#dimensionValue",
            "dimensionName": "dfa:dynamicProfile",
            "id": dynamicProfile,
            "matchType": "EXACT"
          },
          {
            "kind": "dfareporting#dimensionValue",
            "dimensionName": "dfa:advertiser",
            "id": advertiser,
            "matchType": "EXACT"},
          {
            "kind": "dfareporting#dimensionValue",
            "dimensionName": "dfa:campaign",
            "id": campaign,
            "matchType": "EXACT"
          }
        ],
        "dimensions": [
          {"kind": "dfareporting#sortedDimension", "name": "dfa:placement"},
          {"kind": "dfareporting#sortedDimension", "name": "dfa:placementId"},
          {"kind": "dfareporting#sortedDimension", "name": "dfa:dynamicElement1Value"},
          {"kind": "dfareporting#sortedDimension", "name": "dfa:dynamicElement1Field1Value"},
          {"kind": "dfareporting#sortedDimension", "name": "dfa:dynamicElement1Field2Value"}
        ],
        "metricNames": [
          "dfa:impressions",
          "dfa:clicks",
          "dfa:totalConversions"
        ]
      }
    }
  )

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, filedata = report_file(
    project.task["auth"],
    project.task["account"],
    report["id"],
    None,
    0,
    DCM_CHUNK_SIZE
  )

  # write report to a table ( avoid collisions as best as possible )
  table_name = "Dynamic_Costs_%s_Dynamic_Combos" % name
  write_report(
    filedata,
    project.task["out"]["dataset"],
    table_name
  )

  return table_name


def report_main(name, startDate, endDate, advertiser, campaign):
  if project.verbose: print "DYNAMIC COSTS MAIN:", name

  # create the report if it does not exist
  report = report_build(
    project.task["auth"],
    project.task["account"],
    {
      "kind": "dfareporting#report",
      "type": "STANDARD",
      "name": "Dynamic Costs %s - Main Advertiser ( StarThinker )" % name,
      "criteria": {
        "dateRange": {
          "kind": "dfareporting#dateRange",
          "startDate": str(startDate),
          "endDate": str(endDate),
        },
        "dimensionFilters": [
          {
            "kind": "dfareporting#dimensionValue",
            "dimensionName": "dfa:advertiser",
            "id": advertiser,
            "matchType": "EXACT"
          },
          {
            "kind": "dfareporting#dimensionValue",
            "dimensionName": "dfa:campaign",
            "id": campaign,
            "matchType": "EXACT"
          }
        ],
        "dimensions": [
          {"kind": "dfareporting#sortedDimension", "name": "dfa:placement"},
          {"kind": "dfareporting#sortedDimension", "name": "dfa:placementId"}
        ],
        "metricNames": [
          "dfa:impressions", 
          "dfa:clicks"
        ]
      }
    }
  )

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, filedata = report_file(
    project.task["auth"],
    project.task["account"],
    report["id"],
    None,
    0,
    DCM_CHUNK_SIZE
  )

  # write report to a table ( avoid collisions as best as possible )
  table_name = "Dynamic_Costs_%s_Main_Advertiser" % name
  write_report(
    filedata,
    project.task["out"]["dataset"],
    table_name
  )

  return table_name


def report_shadow(name, startDate, endDate, advertiser, campaign):
  if project.verbose: print "DYNAMIC COSTS SHADOW:", name

  # create the report if it does not exist
  report = report_build(
    project.task["auth"],
    project.task["account"],
    {
      "kind": "dfareporting#report",
      "type": "STANDARD",
      "name": "Dynamic Costs %s - Shadow Advertiser ( StarThinker )" % name,
      "criteria": {
        "dateRange": {
          "kind": "dfareporting#dateRange",
          "startDate": str(startDate),
          "endDate": str(endDate),
        },
        "dimensionFilters": [
          {
            "dimensionName": "dfa:advertiser",
            "id": advertiser,
            "kind": "dfareporting#dimensionValue",
            "matchType": "EXACT"},
          {
            "dimensionName": "dfa:campaign",
            "id": campaign,
            "kind": "dfareporting#dimensionValue",
            "matchType": "EXACT"
          }
        ],
        "dimensions": [
          {"kind": "dfareporting#sortedDimension", "name": "dfa:placement"},
          {"kind": "dfareporting#sortedDimension", "name": "dfa:placementId"}
        ],
        "metricNames": [
          "dfa:dbmCost"
        ]
      }
    }
  )

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, filedata = report_file(
    project.task["auth"],
    project.task["account"],
    report["id"],
  )

  # write report to a table ( avoid collisions as best as possible )
  table_name = "Dynamic_Costs_%s_Shadow_Advertiser" % name
  write_report(
    filedata,
    project.task["out"]["dataset"],
    table_name
  )

  return table_name


def view_combine(name, combos_table, main_table, shadow_table):
  if project.verbose: print "DYNAMIC COSTS VIEW:", name

  query = """
    SELECT
      combos.*,
      (combos.Impressions / main.Impressions) * shadow.Dbm_Cost_Account_Currency AS Scaled_Dbm_Cost_Account_Currency
    FROM `%(project)s.%(dataset)s.%(combos_table)s` combos
    JOIN `%(project)s.%(dataset)s.%(main_table)s` main
    ON combos.Placement_Id = main.Placement_Id
    JOIN `%(project)s.%(dataset)s.%(shadow_table)s` shadow
    ON STARTS_WITH(shadow.Placement, combos.Placement)
    """ % {
      "project":project.id,
      "dataset":project.task['out']['dataset'],
      "combos_table":combos_table,
      "main_table":main_table,
      "shadow_table":shadow_table
    }

  query_to_view(
    project.task['out']['auth'],
    project.id,
    project.task['out']['dataset'],
    'Dynamic_Costs_%s_Analysis' % name,
    query,
    False
  )


def dynamic_costs():

  # make sure tab exists in sheet
  sheets_tab_copy(
    project.task['auth'],
    project.task['sheet']['template']['url'],
    project.task['sheet']['template']['tab'],
    project.task['sheet']['url'],
    project.task['sheet']['tab']
  )

  # read configuration from sheet
  inputs = sheets_read(project.task['auth'],
    project.task['sheet']['url'],
    project.task['sheet']['tab'],
    project.task['sheet']['range']
  )

  # convert inputs into dictionary
  inputs = dict(inputs)

  if project.verbose: print "DYNAMIC COSTS PARAMETERS", inputs

  # allows each advertiser to run multiple reports ( somewhat collision avoidance )
  unique_name = inputs['Dynamic Profile ID']

  combos_table = report_combos(
    unique_name,
    inputs['Start Date'],
    inputs['End Date'],
    inputs['Main Advertiser ID'],
    inputs['Main Campaign ID'],
    inputs['Dynamic Profile ID'],
  )

  main_table = report_main(
    unique_name,
    inputs['Start Date'],
    inputs['End Date'],
    inputs['Main Advertiser ID'],
    inputs['Main Campaign ID'],
  )

  shadow_table = report_shadow(
    unique_name,
    inputs['Start Date'],
    inputs['End Date'],
    inputs['Shadow Advertiser ID'],
    inputs['Shadow Campaign ID'],
  )

  view_combine(
    unique_name,
    combos_table, 
    main_table, 
    shadow_table
  )


if __name__ == "__main__":
  project.load("dynamic_costs")
  dynamic_costs()
