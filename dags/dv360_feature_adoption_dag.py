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

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

DV360 Feature Adoption Dashboard

Tracks revenue spent on various DV360 features and compares to performance metrics.

  - IMPORTANT: You must add Advertiser IDS, we're still working on a partner level report.
  - Wait for <b>BigQuery->->->DV360_Feature_Analysis</b> dataset to be created.
  - Join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a> to access the following assets
  - Copy <a href='https://datastudio.google.com/c/u/0/datasources/1IPh_zqjFeZTemq6iTUvc3JvZqD0Frneo' target='_blank'>Sample DV360 Feature Adoption Analysis</a>.
  - Click Edit Connection, find above dataset, and choose <b>Sample DV360 Feature Adoption Analysis</b>.
  - Copy <a href='https://datastudio.google.com/c/u/0/datasources/1vQMz7O05gaXRX_8ZF7kKXmfaBLjVv07H' target='_blank'>Sample DV360 Feature Adoption Environment</a>.
  - Click Edit Connection, find above dataset, and choose <b>Sample DV360 Feature Adoption Environment</b>.  This report takes a long time to run, on your first setup you may have to wait a few hours for this step to complete.
  - Copy <a href='https://datastudio.google.com/open/1uZ4WtxiRsBu54gxFdYAzPfW2yGRZlWn0?usp=sharing' target='_blank'>Sample DV360 Feature Adoption Report</a>.
  - When prompted choose the new data source you just created.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug': '',  # Place where tables will be created in BigQuery.
  'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
  'recipe_name': '',  # Name of report in DV360, should be unique.
  'partners': [],  # DV360 partner id.
  'advertisers': [],  # Comma delimited list of DV360 advertiser ids.
  'recipe_project': '',  # Google Cloud Project Id.
}

RECIPE = {
  'setup': {
    'day': [
      'Mon',
      'Tue',
      'Wed',
      'Thu',
      'Fri',
      'Sat',
      'Sun'
    ],
    'hour': [
      2,
      4,
      6
    ]
  },
  'tasks': [
    {
      'dataset': {
        'hour': [
          1
        ],
        'auth': 'service',
        'description': 'Create a dataset for bigquery tables.',
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        }
      }
    },
    {
      'dbm': {
        'hour': [
          2
        ],
        'auth': 'user',
        'report': {
          'filters': {
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'name': 'partners',
                  'kind': 'integer_list',
                  'order': 5,
                  'default': [
                  ],
                  'description': 'DV360 partner id.'
                }
              }
            },
            'FILTER_ADVERTISER': {
              'values': {
                'field': {
                  'name': 'advertisers',
                  'kind': 'integer_list',
                  'order': 6,
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.'
                }
              }
            }
          },
          'body': {
            'timezoneCode': {
              'field': {
                'name': 'recipe_timezone',
                'kind': 'timezone',
                'description': 'Timezone for report dates.',
                'default': 'America/Los_Angeles'
              }
            },
            'metadata': {
              'dataRange': 'LAST_30_DAYS',
              'format': 'CSV',
              'title': {
                'field': {
                  'name': 'recipe_name',
                  'kind': 'string',
                  'prefix': 'Feature Adoption Spend For ',
                  'description': 'Name of report in DV360, should be unique.'
                }
              }
            },
            'params': {
              'type': 'TYPE_GENERAL',
              'groupBys': [
                'FILTER_ADVERTISER',
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_INSERTION_ORDER',
                'FILTER_INSERTION_ORDER_NAME',
                'FILTER_LINE_ITEM',
                'FILTER_LINE_ITEM_NAME',
                'FILTER_DATE'
              ],
              'metrics': [
                'METRIC_IMPRESSIONS',
                'METRIC_BILLABLE_IMPRESSIONS',
                'METRIC_CLICKS',
                'METRIC_CTR',
                'METRIC_TOTAL_CONVERSIONS',
                'METRIC_LAST_CLICKS',
                'METRIC_LAST_IMPRESSIONS',
                'METRIC_REVENUE_ADVERTISER',
                'METRIC_MEDIA_COST_ADVERTISER',
                'METRIC_RICH_MEDIA_VIDEO_COMPLETIONS',
                'METRIC_RICH_MEDIA_VIDEO_PLAYS',
                'METRIC_CM_POST_CLICK_REVENUE',
                'METRIC_CM_POST_VIEW_REVENUE'
              ]
            }
          }
        }
      }
    },
    {
      'dbm': {
        'hour': [
          2
        ],
        'auth': 'user',
        'report': {
          'filters': {
            'FILTER_PARTNER': {
              'values': {
                'field': {
                  'name': 'partners',
                  'kind': 'integer_list',
                  'order': 5,
                  'default': [
                  ],
                  'description': 'DV360 partner id.'
                }
              }
            },
            'FILTER_ADVERTISER': {
              'values': {
                'field': {
                  'name': 'advertisers',
                  'kind': 'integer_list',
                  'order': 6,
                  'default': [
                  ],
                  'description': 'Comma delimited list of DV360 advertiser ids.'
                }
              }
            }
          },
          'body': {
            'timezoneCode': {
              'field': {
                'name': 'recipe_timezone',
                'kind': 'timezone',
                'description': 'Timezone for report dates.',
                'default': 'America/Los_Angeles'
              }
            },
            'metadata': {
              'dataRange': 'LAST_30_DAYS',
              'format': 'CSV',
              'title': {
                'field': {
                  'name': 'recipe_name',
                  'kind': 'string',
                  'prefix': 'Feature Adoption Environment For ',
                  'description': 'Name of report in DV360, should be unique.'
                }
              }
            },
            'params': {
              'type': 'TYPE_GENERAL',
              'groupBys': [
                'FILTER_ADVERTISER',
                'FILTER_ADVERTISER_NAME',
                'FILTER_ADVERTISER_CURRENCY',
                'FILTER_INSERTION_ORDER',
                'FILTER_INSERTION_ORDER_NAME',
                'FILTER_LINE_ITEM',
                'FILTER_LINE_ITEM_NAME',
                'FILTER_DEVICE_TYPE',
                'FILTER_PAGE_LAYOUT',
                'FILTER_DATE'
              ],
              'metrics': [
                'METRIC_IMPRESSIONS',
                'METRIC_BILLABLE_IMPRESSIONS',
                'METRIC_CLICKS',
                'METRIC_TOTAL_CONVERSIONS',
                'METRIC_LAST_CLICKS',
                'METRIC_LAST_IMPRESSIONS',
                'METRIC_REVENUE_ADVERTISER',
                'METRIC_MEDIA_COST_ADVERTISER'
              ]
            }
          }
        }
      }
    },
    {
      'dbm': {
        'hour': [
          6
        ],
        'auth': 'user',
        'report': {
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'prefix': 'Feature Adoption Spend For ',
              'description': 'Name of report in DV360, should be unique.'
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            },
            'table': 'DV360_Feature_Spend',
            'is_incremental_load': True,
            'header': True,
            'schema': [
              {
                'name': 'Advertiser_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Advertiser',
                'type': 'STRING'
              },
              {
                'name': 'Advertiser_Currency',
                'type': 'STRING'
              },
              {
                'name': 'Insertion_Order_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Insertion_Order',
                'type': 'STRING'
              },
              {
                'name': 'Line_Item_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Line_Item',
                'type': 'STRING'
              },
              {
                'name': 'Report_Day',
                'type': 'DATE'
              },
              {
                'name': 'Impressions',
                'type': 'INTEGER'
              },
              {
                'name': 'Billable_Impressions',
                'type': 'FLOAT'
              },
              {
                'name': 'Clicks',
                'type': 'INTEGER'
              },
              {
                'name': 'Click_Rate_Ctr',
                'type': 'STRING'
              },
              {
                'name': 'Total_Conversions',
                'type': 'FLOAT'
              },
              {
                'name': 'Post_Click_Conversions',
                'type': 'FLOAT'
              },
              {
                'name': 'Post_View_Conversions',
                'type': 'FLOAT'
              },
              {
                'name': 'Revenue_Adv_Currency',
                'type': 'FLOAT'
              },
              {
                'name': 'Media_Cost_Advertiser_Currency',
                'type': 'FLOAT'
              },
              {
                'name': 'Complete_Views_Video',
                'type': 'INTEGER'
              },
              {
                'name': 'Starts_Video',
                'type': 'INTEGER'
              },
              {
                'name': 'Cm_Post_Click_Revenue',
                'type': 'FLOAT'
              },
              {
                'name': 'Cm_Post_View_Revenue',
                'type': 'FLOAT'
              }
            ]
          }
        }
      }
    },
    {
      'dbm': {
        'hour': [
          6
        ],
        'auth': 'user',
        'report': {
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'prefix': 'Feature Adoption Environment For ',
              'description': 'Name of report in DV360, should be unique.'
            }
          }
        },
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            },
            'table': 'DV360_Feature_Environment',
            'is_incremental_load': True,
            'header': True,
            'schema': [
              {
                'name': 'Advertiser_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Advertiser',
                'type': 'STRING'
              },
              {
                'name': 'Advertiser_Currency',
                'type': 'STRING'
              },
              {
                'name': 'Insertion_Order_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Insertion_Order',
                'type': 'STRING'
              },
              {
                'name': 'Line_Item_Id',
                'type': 'INTEGER'
              },
              {
                'name': 'Line_Item',
                'type': 'STRING'
              },
              {
                'name': 'Device_Type',
                'type': 'STRING'
              },
              {
                'name': 'Environment',
                'type': 'STRING'
              },
              {
                'name': 'Report_Day',
                'type': 'DATE'
              },
              {
                'name': 'Impressions',
                'type': 'INTEGER'
              },
              {
                'name': 'Billable_Impressions',
                'type': 'FLOAT'
              },
              {
                'name': 'Clicks',
                'type': 'INTEGER'
              },
              {
                'name': 'Total_Conversions',
                'type': 'FLOAT'
              },
              {
                'name': 'Post_Click_Conversions',
                'type': 'FLOAT'
              },
              {
                'name': 'Post_View_Conversions',
                'type': 'FLOAT'
              },
              {
                'name': 'Revenue_Adv_Currency',
                'type': 'FLOAT'
              },
              {
                'name': 'Media_Cost_Advertiser_Currency',
                'type': 'FLOAT'
              }
            ]
          }
        }
      }
    },
    {
      'sdf_legacy': {
        'hour': [
          4
        ],
        'auth': 'user',
        'version': '5',
        'file_types': [
          'LINE_ITEM'
        ],
        'filter_type': 'ADVERTISER_ID',
        'read': {
          'filter_ids': {
            'values': {
              'field': {
                'name': 'advertisers',
                'kind': 'integer_list',
                'order': 6,
                'default': [
                ],
                'description': 'Comma delimited list of DV360 advertiser ids.'
              }
            }
          }
        },
        'daily': True,
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            }
          }
        }
      }
    },
    {
      'sdf_legacy': {
        'hour': [
          4
        ],
        'auth': 'user',
        'version': '5',
        'file_types': [
          'INSERTION_ORDER'
        ],
        'filter_type': 'ADVERTISER_ID',
        'read': {
          'filter_ids': {
            'values': {
              'field': {
                'name': 'advertisers',
                'kind': 'integer_list',
                'order': 6,
                'default': [
                ],
                'description': 'Comma delimited list of DV360 advertiser ids.'
              }
            }
          }
        },
        'daily': True,
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            }
          }
        }
      }
    },
    {
      'bigquery': {
        'hour': [
          6
        ],
        'auth': 'service',
        'from': {
          'query': " SELECT   Report_Day,   Advertiser,   Advertiser_Id,   Advertiser_Currency,   Insertion_Order AS Insertion_Order_Name,   Insertion_Order_Id AS Insertion_Order_ID,   CONCAT(Insertion_Order,' (',CAST(Insertion_Order_ID AS STRING),')') AS Insertion_Order,   Line_Item AS LI_Name,   b.Line_Item_Id AS LI_ID,   CONCAT(Line_Item,' (',CAST(b.Line_Item_Id AS STRING),')') AS Line_Item,   IF(MAX(SDF_Day) OVER () = SDF_Day, 'True', 'False') AS Max_Date,   a.*,   IF(Bid_Strategy_Type = 'Fixed', 'Fixed', CONCAT(Bid_Strategy_Type, ' ', Bid_Strategy_Unit)) AS Bid_Strategy,   IF(Bid_Strategy_Type = 'Fixed', 'Fixed', 'Autobidding') AS Autobidding_Overall,   CONCAT(Pacing, ' ', Pacing_Rate) AS Pacing_Overall,   IF(Affinity_In_Market_Targeting_Include IS NULL, 'False', 'True') AS Affinity_In_Market_TF,   IF(Affinity_In_Market_Targeting_Exclude IS NULL, 'False', 'True') AS Affinity_In_Market_Exclude_TF,   IF(Custom_List_Targeting IS NULL, 'False', 'True') AS Custom_List_TF,   IF(Audience_Targeting_Include IS NULL     AND Affinity_In_Market_Targeting_Include IS NULL     AND Custom_List_Targeting IS NULL     AND Audience_Targeting_Similar_Audiences = 'False' , 'False', 'True') AS Audience_Targeting_TF,   IF(Keyword_Targeting_Exclude IS NULL     AND Keyword_List_Targeting_Exclude IS NULL, 'False', 'True') AS Keyword_Exclusions_TF,   IF(Position_Targeting_On_Screen IS NULL     AND Position_Targeting_Display_Position_In_Content IS NULL     AND Position_Targeting_Video_Position_In_Content IS NULL     AND Position_Targeting_Audio_Position_In_Content IS NULL, 'False', 'True') AS Position_Targeting_TF,   IF((Geography_Targeting_Include IS NULL       AND Geography_Regional_Location_List_Targeting_Include IS NULL), 'False', 'True') AS Geography_Targeting_TF,   IF(Language_Targeting_Include IS NULL, 'False', 'True') AS Language_Targeting_TF,   IF(Site_Targeting_Exclude IS NULL     AND Site_Targeting_Include IS NULL, 'False', 'True') AS Site_List_TF,   Impressions AS Impressions,   Billable_Impressions AS Billable_Impressions,   Clicks AS Clicks,   Total_Conversions AS Total_Conversions,   Post_Click_Conversions AS Post_Click_Conversions,   Post_View_Conversions AS Post_View_Conversions,   Revenue_Adv_Currency AS Rev_Adv_Currency,   Media_Cost_Advertiser_Currency AS Media_Cost_Adv_Currency,   Cm_Post_Click_Revenue AS CM_Post_Click_Revenue,   Cm_Post_View_Revenue AS CM_Post_View_Revenue,   (Cm_Post_Click_Revenue+Cm_Post_View_Revenue) AS CM_Total_Revenue,   IF (Bid_Strategy_Type = 'Fixed', 0, Revenue_Adv_Currency) AS Autobid_Rev,   IF (Type = 'Display', Revenue_Adv_Currency, 0) AS Display_Rev,   IF (Type = 'Video', Revenue_Adv_Currency, 0) AS Video_Rev,   IF (Type = 'TrueView', Revenue_Adv_Currency, 0) AS TrueView_Rev,   IF (Type = 'Audio', Revenue_Adv_Currency, 0) AS Audio_Rev,   IF ((STRPOS(Environment_Targeting, 'Desktop')>0), Revenue_Adv_Currency, 0) AS Desktop_Rev   FROM `[PARAMETER].[PARAMETER].SDF_LINE_ITEM` AS a   LEFT JOIN `[PARAMETER].[PARAMETER].DV360_Feature_Spend` AS b     ON DATE_SUB(a.SDF_Day, INTERVAL 1 DAY) = b.Report_Day     AND a.Line_Item_Id = b.Line_Item_Id   WHERE b.Report_Day IS NOT NULL ",
          'parameters': [
            {
              'field': {
                'name': 'recipe_project',
                'kind': 'string',
                'order': 6,
                'default': '',
                'description': 'Google Cloud Project Id.'
              }
            },
            {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            },
            {
              'field': {
                'name': 'recipe_project',
                'kind': 'string',
                'order': 6,
                'default': '',
                'description': 'Google Cloud Project Id.'
              }
            },
            {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            }
          ],
          'legacy': False
        },
        'to': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          'view': 'DV360_Feature_Adoption_Analysis'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('dv360_feature_adoption', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
