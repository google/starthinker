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

CM360 Domain And App Transparency

Reports the percentage of CM impressions that can be attributed to a specific domain or application.  Allows diagnostic of which domains and apps are misconfigured by publisher resulting in underreporting.

  - Wait for <a href='https://console.cloud.google.com/bigquery?project=&d=' target='_blank'>BigQuery : </a> :  : </a> to be created.
  - Copy DataStudio <a href='https://datastudio.google.com/c/u/0/datasources/1Az6d9loAHo69GSIyKUfusrtyf_IDqTVs' target='_blank'>Transparency Combined KPI</a> and connect.
  - Copy DataStudio <a href='https://datastudio.google.com/c/u/0/reporting/1foircGRxgYCL_PR8gfdmYOleBacnPKwB/page/QCXj' target='_blank'>Transparency Breakdown</a>.
  - When prompted choose the new data source you just created.
  - Or give these intructions to the client, they will have to join the <a hre='https://groups.google.com/d/forum/starthinker-assets' target='_blank'>StarThinker Assets Group</a>.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'recipe_slug': '',  # Place where tables will be written in BigQuery.
  'recipe_name': '',  # Name of report in CM, should be unique.
  'recipe_project': '',  # Project where BigQuery dataset will be created.
  'dcm_account': '',  # CM account id of client.
  'dcm_advertisers': '',  # Comma delimited list of CM advertiser ids.
}

RECIPE = {
  'tasks': [
    {
      'dataset': {
        'hour': [
          1
        ],
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Name of Google BigQuery dataset to create.'
          }
        }
      }
    },
    {
      'dcm': {
        'hour': [
          2
        ],
        'auth': 'user',
        'report': {
          'account': {
            'field': {
              'name': 'dcm_account',
              'kind': 'integer',
              'order': 2,
              'default': '',
              'description': 'CM account id of client.'
            }
          },
          'filters': {
            'dfa:advertiser': {
              'values': {
                'field': {
                  'name': 'dcm_advertisers',
                  'kind': 'integer_list',
                  'order': 3,
                  'description': 'Comma delimited list of CM advertiser ids.'
                }
              }
            }
          },
          'body': {
            'type': 'STANDARD',
            'format': 'CSV',
            'name': {
              'field': {
                'name': 'recipe_name',
                'kind': 'string',
                'prefix': 'Transparency App For ',
                'description': 'Name of report in CM, unique.'
              }
            },
            'criteria': {
              'dateRange': {
                'relativeDateRange': 'PREVIOUS_MONTH'
              },
              'dimensions': [
                {
                  'name': 'dfa:advertiser'
                },
                {
                  'name': 'dfa:advertiserId'
                },
                {
                  'name': 'dfa:campaign'
                },
                {
                  'name': 'dfa:campaignId'
                },
                {
                  'name': 'dfa:siteId'
                },
                {
                  'name': 'dfa:site'
                },
                {
                  'name': 'dfa:adType'
                },
                {
                  'name': 'dfa:environment'
                },
                {
                  'name': 'dfa:appId'
                },
                {
                  'name': 'dfa:app'
                }
              ],
              'metricNames': [
                'dfa:impressions'
              ]
            },
            'schedule': {
              'active': True,
              'every': 1,
              'repeats': 'MONTHLY',
              'runsOnDayOfMonth': 'DAY_OF_MONTH'
            }
          }
        }
      }
    },
    {
      'dcm': {
        'hour': [
          2
        ],
        'auth': 'user',
        'report': {
          'account': {
            'field': {
              'name': 'dcm_account',
              'kind': 'integer',
              'order': 2,
              'default': '',
              'description': 'CM account id of client.'
            }
          },
          'filters': {
            'dfa:advertiser': {
              'values': {
                'field': {
                  'name': 'dcm_advertisers',
                  'kind': 'integer_list',
                  'order': 3,
                  'description': 'Comma delimited list of CM advertiser ids.'
                }
              }
            }
          },
          'body': {
            'type': 'STANDARD',
            'format': 'CSV',
            'name': {
              'field': {
                'name': 'recipe_name',
                'kind': 'string',
                'prefix': 'Transparency Domain For ',
                'description': 'Name of report in CM, unique.'
              }
            },
            'criteria': {
              'dateRange': {
                'relativeDateRange': 'PREVIOUS_MONTH'
              },
              'dimensions': [
                {
                  'name': 'dfa:advertiser'
                },
                {
                  'name': 'dfa:advertiserId'
                },
                {
                  'name': 'dfa:campaign'
                },
                {
                  'name': 'dfa:campaignId'
                },
                {
                  'name': 'dfa:site'
                },
                {
                  'name': 'dfa:siteId'
                },
                {
                  'name': 'dfa:adType'
                },
                {
                  'name': 'dfa:domain'
                }
              ],
              'metricNames': [
                'dfa:verificationVerifiableImpressions'
              ]
            },
            'schedule': {
              'active': True,
              'every': 1,
              'repeats': 'MONTHLY',
              'runsOnDayOfMonth': 'DAY_OF_MONTH'
            }
          }
        }
      }
    },
    {
      'dcm': {
        'hour': [
          4
        ],
        'auth': 'user',
        'report': {
          'account': {
            'field': {
              'name': 'dcm_account',
              'kind': 'integer',
              'order': 2,
              'default': '',
              'description': 'CM account id of client.'
            }
          },
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'prefix': 'Transparency Domain For ',
              'description': 'Name of report in CM, should be unique.'
            }
          }
        },
        'out': {
          'bigquery': {
            'auth': 'service',
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': '',
                'description': 'Name of Google BigQuery dataset to create.'
              }
            },
            'table': 'Transparency_Domain_KPI'
          }
        }
      }
    },
    {
      'dcm': {
        'hour': [
          4
        ],
        'auth': 'user',
        'report': {
          'account': {
            'field': {
              'name': 'dcm_account',
              'kind': 'integer',
              'order': 2,
              'default': '',
              'description': 'CM account id of client.'
            }
          },
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'prefix': 'Transparency App For ',
              'description': 'Name of report in CM, should be unique.'
            }
          }
        },
        'out': {
          'bigquery': {
            'auth': 'service',
            'dataset': {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'order': 1,
                'default': '',
                'description': 'Name of Google BigQuery dataset to create.'
              }
            },
            'table': 'Transparency_App_KPI'
          }
        }
      }
    },
    {
      'bigquery': {
        'hour': [
          5
        ],
        'auth': 'user',
        'to': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'order': 1,
              'default': '',
              'description': 'Name of Google BigQuery dataset to create.'
            }
          },
          'view': 'Transparency_Combined_KPI'
        },
        'from': {
          'query': "With \r\nTransparent_Domains AS ( \r\n  SELECT\r\n    CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,\r\n    CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,\r\n    CONCAT(Site_Dcm, ' - ', CAST(Site_Id_Dcm AS STRING)) AS Site,\r\n    Domain,\r\n    Ad_Type,\r\n    Verifiable_Impressions AS Impressions,\r\n    IF(Domain IS NOT NULL, Verifiable_Impressions, 0) AS Visible_Impressions,\r\n    IF(Domain IS NULL, Verifiable_Impressions, 0) AS Null_Impressions\r\n  FROM `[PARAMETER].[PARAMETER].Transparency_Domain_KPI`\r\n),\r\nTransparent_Apps AS ( \r\n  SELECT\r\n    CONCAT(Advertiser, ' - ', CAST(Advertiser_Id AS STRING)) AS Advertiser,\r\n    CONCAT(Campaign, ' - ', CAST(Campaign_Id AS STRING)) AS Campaign,\r\n    CONCAT(Site_Dcm, ' - ', CAST(Site_Id_Dcm AS STRING)) AS Site,\r\n    /*If(App IS NOT NULL, CONCAT(App, ' - ', CAST(App_Id AS STRING)), App_Id) AS App, */\r\n    CASE \r\n      WHEN App IS NOT NULL THEN CONCAT(App, ' - ', CAST(App_Id AS STRING))\r\n      WHEN App_Id IS NOT NULL THEN App_Id\r\n      ELSE NULL\r\n    END AS App,\r\n    Ad_Type,\r\n    Impressions,\r\n    IF(App IS NOT NULL OR App_ID IS NOT NULL, Impressions, 0) AS Visible_Impressions,\r\n    IF(App IS NULL AND App_Id IS NULL, Impressions, 0) AS Null_Impressions\r\n  FROM `[PARAMETER].[PARAMETER].Transparency_App_KPI`\r\n  WHERE Environment = 'App'\r\n),\r\nDomains_And_Apps AS (\r\n  SELECT \r\n    TD.Advertiser,\r\n    TD.Campaign,\r\n    TD.Site,\r\n    TD.Ad_Type,\r\n    TD.Domain,\r\n    TD.Impressions AS Domain_Impressions,\r\n    TD.Visible_Impressions AS Domain_Visible_Impressions,\r\n    TD.Null_Impressions AS Domain_Null_Impressions,\r\n    NULL AS App,\r\n    0 AS App_Impressions,\r\n    0 AS App_Visible_Impressions,\r\n    0 AS App_Null_Impressions\r\n  FROM Transparent_Domains AS TD\r\n  UNION ALL\r\n  SELECT \r\n    TA.Advertiser,\r\n    TA.Campaign,\r\n    TA.Site,\r\n    TA.Ad_Type,\r\n    NULL AS Domain,\r\n    0 AS Domain_Impressions,\r\n    0 AS Domain_Visible_Impressions,\r\n    0 AS Domain_Null_Impressions,\r\n    TA.App,\r\n    TA.Impressions AS App_Impressions,\r\n    TA.Visible_Impressions AS App_Visible_Impressions,\r\n    TA.Null_Impressions AS App_Null_Impressions\r\n  FROM Transparent_Apps AS TA\r\n)\r\n\r\n  SELECT\r\n    Advertiser,\r\n    Campaign,\r\n    Site,\r\n    COALESCE(Domain, App, '') AS Domain_Or_App,\r\n    Ad_Type,\r\n    CASE\r\n      WHEN App IS NOT NULL AND Domain IS NOT NULL THEN 'Both' /* SHOULD NOT HAPPEN */\r\n      WHEN App IS NOT NULL THEN 'App'\r\n      WHEN Domain IS NOT NULL Then 'Domain'\r\n      ELSE 'Neither'\r\n    END AS Category,\r\n\r\n    SUM(Domain_Impressions) AS Domain_Impressions,\r\n    SUM(Domain_Visible_Impressions) AS Domain_Visible_Impressions,\r\n    SUM(Domain_Null_Impressions) AS Domain_Null_Impressions,\r\n\r\n    SUM(App_Impressions) AS App_Impressions,\r\n    SUM(App_Visible_Impressions) AS App_Visible_Impressions,\r\n    SUM(App_Null_Impressions) AS App_Null_Impressions,\r\n\r\n    SUM(App_Impressions + Domain_Impressions) AS Impressions /* Could also be MAX as its always one or the other*/\r\n\r\n  FROM Domains_And_Apps\r\n  GROUP By 1,2,3,4,5,6",
          'parameters': [
            {
              'field': {
                'name': 'recipe_project',
                'kind': 'string',
                'description': 'Project where BigQuery dataset will be created.'
              }
            },
            {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be written in BigQuery.'
              }
            },
            {
              'field': {
                'name': 'recipe_project',
                'kind': 'string',
                'description': 'Project where BigQuery dataset will be created.'
              }
            },
            {
              'field': {
                'name': 'recipe_slug',
                'kind': 'string',
                'description': 'Place where tables will be written in BigQuery.'
              }
            }
          ],
          'legacy': False
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('transparency', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
