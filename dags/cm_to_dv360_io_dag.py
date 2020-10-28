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

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

CM To BigQuery IO Synch

Migrate CM Placements to DV360 IO.

Fill in the CM accont information.
Fill in the DV360 accont information.
Click the 'Save' button to save configuration.
Click the 'Run Now' button to create the workflow.
Visit <b>BigQuery->UNDEFINED->UNDEFINED->DV360_IO_REVIEW</b> to check for updates.
Visit <b>BigQuery->UNDEFINED->UNDEFINED->DV360_IO_INSERT</b> to approve the updates.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'recipe_slug': '',  # Place where tables will be created in BigQuery.
  'dv360_advertisers': '',  # Comma seperated.
  'cm_account': '',  # Comma seperated.
  'cm_advertiser': '',  # Comma seperated.
  'dv360_advertiser': '',  # Comma seperated.
  'dv360_campaign': '',  # Comma seperated.
}

TASKS = [
  {
    'dataset': {
      'auth': 'service',
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
    'sheets': {
      'auth': 'user',
      'sheet': 'BB Demo',
      'tab': 'Rules',
      'range': 'A1:C',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          'table': 'Rules'
        }
      }
    }
  },
  {
    'dv360_api': {
      'auth': 'user',
      'endpoints': [
        'advertisers.insertionOrders'
      ],
      'advertisers': {
        'single_cell': True,
        'values': {
          'field': {
            'name': 'dv360_advertisers',
            'kind': 'integer_list',
            'description': 'Comma seperated.'
          }
        }
      },
      'out': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        }
      }
    }
  },
  {
    'dcm_api': {
      'auth': 'user',
      'endpoints': [
        'campaigns',
        'placements',
        'placementGroups'
      ],
      'accounts': {
        'values': {
          'field': {
            'name': 'cm_account',
            'kind': 'integer_list',
            'description': 'Comma seperated.'
          }
        }
      },
      'advertisers': {
        'values': {
          'field': {
            'name': 'cm_advertiser',
            'kind': 'integer_list',
            'description': 'Comma seperated.'
          }
        }
      },
      'out': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'auth': 'service',
      'from': {
        'legacy': False,
        'parameters': [
          {
            'field': {
              'name': 'dv360_advertiser',
              'kind': 'integer_list',
              'description': 'Comma seperated.'
            }
          },
          {
            'field': {
              'name': 'dv360_campaign',
              'kind': 'integer_list',
              'description': 'Comma seperated.'
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
              'name': 'recipe_slug',
              'kind': 'string',
              'description': 'Place where tables will be written in BigQuery.'
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
        'query': "SELECT   [PARAMETER] AS advertiserId,   [PARAMETER] AS campaignId,   REGEXP_REPLACE(CM_P.name, '_1X1.*', '') AS displayName,   'ENTITY_STATUS_DRAFT' AS entityStatus,   STRUCT(     'PACING_PERIOD_FLIGHT' AS pacingPeriod,     'PACING_TYPE_AHEAD' AS pacingType   ) AS pacing,   STRUCT(     false AS unlimited,     'TIME_UNIT_DAYS' AS timeUnit,     1 AS timeUnitCount,     CASE       WHEN CM_P.name LIKE '%FF%' AND CM_P.name LIKE '%PZN%'THEN 6       WHEN CM_P.name LIKE '%FF%' THEN 3       WHEN CM_P.name LIKE '%HOL%' THEN 6       WHEN CM_P.name LIKE '%BTC%' THEN 3     END AS maxImpressions   ) AS frequencyCap,   STRUCT(     'PERFORMANCE_GOAL_TYPE_CPM' AS performanceGoalType,     '10' AS performanceGoalAmountMicros   ) AS performanceGoal,   STRUCT(     'BUDGET_UNIT_CURRENCY' AS budgetUnit,     'INSERTION_ORDER_AUTOMATION_TYPE_BUDGET' AS automationType,     [       STRUCT(        '10000' AS budgetAmountMicros,        '' AS description,        STRUCT (          STRUCT (            EXTRACT(YEAR FROM GREATEST(CM_C.startDate, CURRENT_DATE())) AS year,            EXTRACT(MONTH FROM GREATEST(CM_C.startDate, CURRENT_DATE())) AS month,            EXTRACT(DAY FROM GREATEST(CM_C.startDate, CURRENT_DATE())) AS day          ) AS startDate,          STRUCT (            EXTRACT(YEAR FROM CM_C.endDate) AS year,            EXTRACT(MONTH FROM CM_C.endDate) AS month,            EXTRACT(DAY FROM CM_C.endDate) AS day          ) AS endDate        ) AS dateRange       )     ] AS budgetSegments   ) AS budget,   STRUCT(     STRUCT(       '10' AS bidAmountMicros     ) AS fixedBid   ) AS bidStrategy FROM `[PARAMETER].CM_placements` As CM_P LEFT JOIN `[PARAMETER].CM_campaigns` As CM_C ON CM_P.campaignId=CM_C.id LEFT JOIN `[PARAMETER].CM_placementGroups` As CM_G ON CM_P.placementGroupId=CM_G.id WHERE CM_P.advertiserID=4461789 AND CM_P.name LIKE 'PKG%' /*AND CM_G.placementGroupType = 'PACKAGE' */ ORDER BY displayName ;"
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        },
        'view': 'DV360_IO_LOGIC'
      }
    }
  },
  {
    'bigquery': {
      'auth': 'service',
      'from': {
        'legacy': False,
        'parameters': [
          {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'description': 'Place where tables will be written in BigQuery.'
            }
          }
        ],
        'query': 'SELECT STRUCT(   ROW_NUMBER() OVER() AS NUMBER,   displayName IN (SELECT displayName FROM `[PARAMETER].DV360_advertisers_insertionOrders`) AS DUPLICATE ) AS PREVIEW, * FROM `[PARAMETER].DV360_IO_LOGIC` ORDER BY displayName ;'
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        },
        'view': 'DV360_IO_PREVIEW'
      }
    }
  },
  {
    'bigquery': {
      'auth': 'service',
      'from': {
        'legacy': False,
        'parameters': [
          {
            'field': {
              'name': 'recipe_slug',
              'kind': 'string',
              'description': 'Place where tables will be written in BigQuery.'
            }
          }
        ],
        'query': ' SELECT * EXCEPT(PREVIEW) FROM `[PARAMETER].DV360_IO_PREVIEW` WHERE PREVIEW.NUMBER IN(0,0,0,0,0) AND PREVIEW.DUPLICATE=False LIMIT 1 ;'
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        },
        'view': 'DV360_IO_INSERT'
      }
    }
  },
  {
    'dv360_api': {
      'auth': 'user',
      'bigquery': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'recipe_slug',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        },
        'as_object': True,
        'table': 'DV360_IO_INSERT'
      },
      'insert': 'advertisers.insertionOrders'
    }
  }
]

DAG_FACTORY = DAG_Factory('cm_to_dv360_io', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
