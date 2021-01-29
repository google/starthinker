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

import json

from starthinker.util.project import project
from starthinker.util.bigquery import rows_to_table, query_to_view
from starthinker.util.dcm import report_build, report_file, report_to_rows, report_clean, report_schema, DCM_CHUNK_SIZE


def write_report(report, dataset, table):
  # turn report file into rows
  rows = report_to_rows(report)
  rows = report_clean(rows)

  if rows:
    if project.verbose:
      print('DYNAMIC COSTS WRITTEN:', table)

    # pull DCM schema automatically
    try:
      schema = report_schema(next(rows))
    except StopIteration:  # report is empty
      raise ValueError('REPORT DID NOT RUN')

    # write report to bigquery
    rows_to_table(project.task['out']['auth'], project.id,
                  project.task['out']['dataset'], table, rows, schema, 0)

  else:
    if project.verbose:
      print('DYNAMIC COSTS REPORT NOT READY:', table)


def report_combos(name, dateRange, schedule, advertiser, campaign,
                  dynamicProfile):
  if project.verbose:
    print('DYNAMIC COSTS COMBOS:', name)

  # basic report schema, with no dynamic elements
  schema = {
      'kind': 'dfareporting#report',
      'type': 'STANDARD',
      'name': 'Dynamic Costs %s - Dynamic Combos ( StarThinker )' % name,
      'schedule': schedule,
      'criteria': {
          'dateRange':
              dateRange,
          'dimensionFilters': [{
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'dfa:dynamicProfile',
              'id': dynamicProfile,
              'matchType': 'EXACT'
          }, {
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'dfa:advertiser',
              'id': advertiser,
              'matchType': 'EXACT'
          }, {
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'dfa:campaign',
              'id': campaign,
              'matchType': 'EXACT'
          }],
          'dimensions': [{
              'kind': 'dfareporting#sortedDimension',
              'name': 'dfa:placement'
          }, {
              'kind': 'dfareporting#sortedDimension',
              'name': 'dfa:placementId'
          }, {
              'kind': 'dfareporting#sortedDimension',
              'name': 'dfa:activity'
          }, {
              'kind': 'dfareporting#sortedDimension',
              'name': 'dfa:activityId'
          }],
          'metricNames': [
              'dfa:impressions', 'dfa:clicks', 'dfa:totalConversions'
          ]
      }
  }

  # add in all reasonable dynamic elements
  for i in range(1, 5 + 1):  # 5 elements/feeds
    for j in range(1, 6 + 1):  # 6 fields per element
      schema['criteria']['dimensions'].append({
          'kind': 'dfareporting#sortedDimension',
          'name': 'dfa:dynamicElement%iField%iValue' % (i, j)
      })

  print(json.dumps(schema, indent=2))

  # create the report if it does not exist
  report = report_build(project.task['auth'], project.task['account'], schema)

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, filedata = report_file(project.task['auth'],
                                   project.task['account'], report['id'], None,
                                   60, DCM_CHUNK_SIZE)

  # write report to a table ( avoid collisions as best as possible )
  table_name = 'Dynamic_Costs_%s_Dynamic_Combos' % name
  write_report(filedata, project.task['out']['dataset'], table_name)

  return table_name


def report_main(name, dateRange, schedule, advertiser, campaign, shadow=True):
  if project.verbose:
    print('DYNAMIC COSTS MAIN:', name)

  # base report schema
  schema = {
      'kind': 'dfareporting#report',
      'type': 'STANDARD',
      'name': 'Dynamic Costs %s - Main Advertiser ( StarThinker )' % name,
      'schedule': schedule,
      'criteria': {
          'dateRange': dateRange,
          'dimensionFilters': [{
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'dfa:advertiser',
              'id': advertiser,
              'matchType': 'EXACT'
          }, {
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'dfa:campaign',
              'id': campaign,
              'matchType': 'EXACT'
          }],
          'dimensions': [{
              'kind': 'dfareporting#sortedDimension',
              'name': 'dfa:placement'
          }, {
              'kind': 'dfareporting#sortedDimension',
              'name': 'dfa:placementId'
          }],
          'metricNames': ['dfa:impressions', 'dfa:clicks']
      }
  }

  # if not using shadow advertiser, pull DBM cost here
  if not shadow:
    schema['criteria']['metricNames'].append('dfa:dbmCost')

  # create the report if it does not exist
  report = report_build(project.task['auth'], project.task['account'], schema)

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, filedata = report_file(project.task['auth'],
                                   project.task['account'], report['id'], None,
                                   60, DCM_CHUNK_SIZE)

  # write report to a table ( avoid collisions as best as possible )
  table_name = 'Dynamic_Costs_%s_Main_Advertiser' % name
  write_report(filedata, project.task['out']['dataset'], table_name)

  return table_name


def report_shadow(name, dateRange, schedule, advertiser, campaign):
  if project.verbose:
    print('DYNAMIC COSTS SHADOW:', name)

  # create the report if it does not exist
  report = report_build(
      project.task['auth'], project.task['account'], {
          'kind': 'dfareporting#report',
          'type': 'STANDARD',
          'name': 'Dynamic Costs %s - Shadow Advertiser ( StarThinker )' % name,
          'schedule': schedule,
          'criteria': {
              'dateRange': dateRange,
              'dimensionFilters': [{
                  'dimensionName': 'dfa:advertiser',
                  'id': advertiser,
                  'kind': 'dfareporting#dimensionValue',
                  'matchType': 'EXACT'
              }, {
                  'dimensionName': 'dfa:campaign',
                  'id': campaign,
                  'kind': 'dfareporting#dimensionValue',
                  'matchType': 'EXACT'
              }],
              'dimensions': [{
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:placement'
              }, {
                  'kind': 'dfareporting#sortedDimension',
                  'name': 'dfa:placementId'
              }],
              'metricNames': ['dfa:dbmCost']
          }
      })

  # fetch report file if it exists ( timeout = 0 means grab most reent ready )
  filename, filedata = report_file(project.task['auth'],
                                   project.task['account'], report['id'])

  # write report to a table ( avoid collisions as best as possible )
  table_name = 'Dynamic_Costs_%s_Shadow_Advertiser' % name
  write_report(filedata, project.task['out']['dataset'], table_name)

  return table_name


def view_combine(name, combos_table, main_table, shadow_table):
  if project.verbose:
    print('DYNAMIC COSTS VIEW:', name)

  if shadow_table:
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
          'project': project.id,
          'dataset': project.task['out']['dataset'],
          'combos_table': combos_table,
          'main_table': main_table,
          'shadow_table': shadow_table
      }
  else:
    query = """
      SELECT
        combos.*,
        (combos.Impressions / main.Impressions) * main.Dbm_Cost_Account_Currency AS Scaled_Dbm_Cost_Account_Currency
      FROM `%(project)s.%(dataset)s.%(combos_table)s` combos
      JOIN `%(project)s.%(dataset)s.%(main_table)s` main
      ON combos.Placement_Id = main.Placement_Id
      """ % {
          'project': project.id,
          'dataset': project.task['out']['dataset'],
          'combos_table': combos_table,
          'main_table': main_table
      }

  query_to_view(project.task['out']['auth'], project.id,
                project.task['out']['dataset'],
                'Dynamic_Costs_%s_Analysis' % name, query, False)


@project.from_parameters
def dynamic_costs():

  if project.verbose:
    print('DYNAMIC COSTS PARAMETERS', project.task)

  # allows each advertiser to run multiple reports ( somewhat collision avoidance )
  unique_name = project.task['dynamic_profile_id']

  # check if using wrapped tags
  shadow = project.task['shadow_advertiser_id'] and project.task[
      'shadow_campaign_id']

  # parse date range
  if project.task.get('date_start') and project.task.get('date_end'):
    date_range = {
        'kind': 'dfareporting#dateRange',
        'startDate': project.task['date_start'],
        'endDate': project.task['date_end'],
    }
    schedule = {'active': False, 'repeats': 'DAILY', 'every': 1}
  else:
    date_range = {
        'kind': 'dfareporting#dateRange',
        'relativeDateRange': project.task.get('date_relative', 'YESTERDAY')
    }
    schedule = {'active': True, 'repeats': 'DAILY', 'every': 1}

  combos_table = report_combos(unique_name, date_range, schedule,
                               project.task['main_advertiser_id'],
                               project.task['main_campaign_id'],
                               project.task['dynamic_profile_id'])

  main_table = report_main(unique_name, date_range, schedule,
                           project.task['main_advertiser_id'],
                           project.task['main_campaign_id'], shadow)

  if shadow:
    shadow_table = report_shadow(
        unique_name,
        date_range,
        project.task['shadow_advertiser_id'],
        project.task['shadow_campaign_id'],
    )
  else:
    shadow_table = None

  view_combine(unique_name, combos_table, main_table, shadow_table)


if __name__ == '__main__':
  dynamic_costs()
