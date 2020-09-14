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
"""--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

cTV Inventory Availability Dashboard

The cTV Audience Affinity dashboard is designed to give clients insights into
which cTV apps their audiences have a high affinity for using.  The goal of this
dashboard is to provide some assistance with the lack of audience targeting for
cTV within DV360.

Find instructions and recommendations for this dashboard <a
href="https://docs.google.com/document/d/120kcR9OrS4hGdTxRK0Ig2koNmm6Gl7sH0L6U56N0SAM/view?usp=sharing"
target="_blank">here</a>

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'recipe_project': '',  # Project where BigQuery dataset will be created.
    'dataset': '',  # Place where tables will be written in BigQuery.
    'auth_read': 'user',  # Credentials used for reading data.
    'partner_id': '',  # DV360 Partner id.
    'auth_write': 'service',  # Credentials used for writing data.
    'recipe_name': '',  # Name of document to deploy to.
    'audience_ids': '',  # Comma separated list of Audience Ids
}

TASKS = [{
    'drive': {
        'auth': 'user',
        'copy': {
            'source':
                'https://docs.google.com/spreadsheets/d/1PPPk2b4gGJHNgQ4hXLiTKzH8pRIdlF5fNy9VCw1v7tM/',
            'destination': {
                'field': {
                    'name': 'recipe_name',
                    'default': '',
                    'description': 'Name of document to deploy to.',
                    'prefix': 'cTV App Match Table ',
                    'kind': 'string',
                    'order': 1
                }
            }
        }
    }
}, {
    'dataset': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'dataset': {
            'field': {
                'description': 'BigQuery Dataset where all data will live.',
                'name': 'dataset',
                'default': '',
                'kind': 'string',
                'order': 3
            }
        }
    }
}, {
    'dbm': {
        'auth': 'user',
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery Dataset where all data will live.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            3
                    }
                },
                'schema': [{
                    'name': 'app_url',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'impressions',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'uniques',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }],
                'table': 'us_country_app'
            }
        },
        'report': {
            'body': {
                'params': {
                    'filters': [{
                        'value': {
                            'field': {
                                'description': 'DV360 Partner id.',
                                'name': 'partner_id',
                                'kind': 'integer',
                                'order': 1
                            }
                        },
                        'type': 'FILTER_PARTNER'
                    }, {
                        'value': 'VIDEO',
                        'type': 'FILTER_INVENTORY_FORMAT'
                    }, {
                        'value': 'US',
                        'type': 'FILTER_COUNTRY'
                    }],
                    'includeInviteData': True,
                    'type': 'TYPE_INVENTORY_AVAILABILITY',
                    'metrics': [
                        'METRIC_BID_REQUESTS', 'METRIC_UNIQUE_VISITORS_COOKIES'
                    ],
                    'groupBys': ['FILTER_APP_URL']
                },
                'metadata': {
                    'dataRange': 'LAST_30_DAYS',
                    'sendNotification': False,
                    'title': {
                        'field': {
                            'prefix': 'us_country_app_',
                            'name': 'recipe_name',
                            'kind': 'string'
                        }
                    },
                    'format': 'CSV'
                },
                'timezoneCode': 'America/Los_Angeles',
                'schedule': {
                    'nextRunTimezoneCode': 'America/Los_Angeles',
                    'frequency': 'DAILY',
                    'endTimeMs': 7983727200000,
                    'nextRunMinuteOfDay': 0
                },
                'kind': 'doubleclickbidmanager#query'
            }
        }
    }
}, {
    'dbm': {
        'auth': 'user',
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery Dataset where all data will live.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            3
                    }
                },
                'schema': [{
                    'name': 'impressions',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'uniques',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }],
                'table': 'us_country_baseline'
            }
        },
        'report': {
            'body': {
                'params': {
                    'filters': [{
                        'value': {
                            'field': {
                                'description': 'DV360 Partner id.',
                                'name': 'partner_id',
                                'kind': 'integer',
                                'order': 1
                            }
                        },
                        'type': 'FILTER_PARTNER'
                    }, {
                        'value': 'US',
                        'type': 'FILTER_COUNTRY'
                    }],
                    'includeInviteData':
                        True,
                    'type':
                        'TYPE_INVENTORY_AVAILABILITY',
                    'metrics': [
                        'METRIC_BID_REQUESTS', 'METRIC_UNIQUE_VISITORS_COOKIES'
                    ]
                },
                'metadata': {
                    'dataRange': 'LAST_30_DAYS',
                    'sendNotification': False,
                    'title': {
                        'field': {
                            'prefix': 'us_country_baseline_',
                            'name': 'recipe_name',
                            'kind': 'string'
                        }
                    },
                    'format': 'CSV'
                },
                'timezoneCode': 'America/Los_Angeles',
                'schedule': {
                    'nextRunTimezoneCode': 'America/Los_Angeles',
                    'frequency': 'DAILY',
                    'endTimeMs': 7983727200000,
                    'nextRunMinuteOfDay': 0
                },
                'kind': 'doubleclickbidmanager#query'
            }
        }
    }
}, {
    'dbm': {
        'auth': 'user',
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery Dataset where all data will live.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            3
                    }
                },
                'schema': [{
                    'name': 'user_list',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'impressions',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'uniques',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }],
                'table': 'us_audience_baseline'
            }
        },
        'report': {
            'filters': {
                'FILTER_USER_LIST': {
                    'single_cell': True,
                    'values': {
                        'field': {
                            'description':
                                'Comma separated list of Audience Ids',
                            'name':
                                'audience_ids',
                            'kind':
                                'integer_list',
                            'order':
                                2
                        }
                    }
                }
            },
            'body': {
                'params': {
                    'filters': [{
                        'value': {
                            'field': {
                                'description': 'DV360 Partner id.',
                                'name': 'partner_id',
                                'kind': 'integer',
                                'order': 1
                            }
                        },
                        'type': 'FILTER_PARTNER'
                    }, {
                        'value': 'US',
                        'type': 'FILTER_COUNTRY'
                    }],
                    'includeInviteData': True,
                    'type': 'TYPE_INVENTORY_AVAILABILITY',
                    'metrics': [
                        'METRIC_BID_REQUESTS', 'METRIC_UNIQUE_VISITORS_COOKIES'
                    ],
                    'groupBys': ['FILTER_AUDIENCE_LIST']
                },
                'metadata': {
                    'dataRange': 'LAST_30_DAYS',
                    'sendNotification': False,
                    'title': {
                        'field': {
                            'prefix': 'us_audience_baseline_',
                            'name': 'recipe_name',
                            'kind': 'string'
                        }
                    },
                    'format': 'CSV'
                },
                'timezoneCode': 'America/Los_Angeles',
                'schedule': {
                    'nextRunTimezoneCode': 'America/Los_Angeles',
                    'frequency': 'DAILY',
                    'endTimeMs': 7983727200000,
                    'nextRunMinuteOfDay': 0
                },
                'kind': 'doubleclickbidmanager#query'
            }
        }
    }
}, {
    'dbm': {
        'auth': 'user',
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery Dataset where all data will live.',
                        'name':
                            'dataset',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            3
                    }
                },
                'schema': [{
                    'name': 'app_url',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'user_list',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'impressions',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'uniques',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }],
                'table': 'us_audience_app'
            }
        },
        'report': {
            'filters': {
                'FILTER_USER_LIST': {
                    'single_cell': True,
                    'values': {
                        'field': {
                            'description':
                                'Comma separated list of Audience Ids',
                            'name':
                                'audience_ids',
                            'kind':
                                'integer_list',
                            'order':
                                2
                        }
                    }
                }
            },
            'body': {
                'params': {
                    'filters': [{
                        'value': {
                            'field': {
                                'description': 'DV360 Partner id.',
                                'name': 'partner_id',
                                'kind': 'integer',
                                'order': 1
                            }
                        },
                        'type': 'FILTER_PARTNER'
                    }, {
                        'value': 'VIDEO',
                        'type': 'FILTER_INVENTORY_FORMAT'
                    }, {
                        'value': 'US',
                        'type': 'FILTER_COUNTRY'
                    }],
                    'includeInviteData': True,
                    'type': 'TYPE_INVENTORY_AVAILABILITY',
                    'metrics': [
                        'METRIC_BID_REQUESTS', 'METRIC_UNIQUE_VISITORS_COOKIES'
                    ],
                    'groupBys': ['FILTER_APP_URL', 'FILTER_AUDIENCE_LIST']
                },
                'metadata': {
                    'dataRange': 'LAST_30_DAYS',
                    'sendNotification': False,
                    'title': {
                        'field': {
                            'prefix': 'us_audience_app_',
                            'name': 'recipe_name',
                            'kind': 'string'
                        }
                    },
                    'format': 'CSV'
                },
                'timezoneCode': 'America/Los_Angeles',
                'schedule': {
                    'nextRunTimezoneCode': 'America/Los_Angeles',
                    'frequency': 'DAILY',
                    'endTimeMs': 7983727200000,
                    'nextRunMinuteOfDay': 0
                },
                'kind': 'doubleclickbidmanager#query'
            }
        }
    }
}, {
    'sheets': {
        'header': True,
        'sheet': {
            'field': {
                'name': 'recipe_name',
                'default': '',
                'description': 'Name of document to deploy to.',
                'prefix': 'cTV App Match Table ',
                'kind': 'string',
                'order': 1
            }
        },
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'tab': 'data',
        'out': {
            'auth': {
                'field': {
                    'description': 'Credentials used for writing data.',
                    'name': 'auth_write',
                    'default': 'service',
                    'kind': 'authentication',
                    'order': 1
                }
            },
            'bigquery': {
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery Dataset where all data will live.',
                        'name':
                            'dataset',
                        'kind':
                            'string'
                    }
                },
                'schema': [{
                    'name': 'Publisher_Name',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'CTV_App_name',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }],
                'table': 'CTV_App_Lookup'
            }
        },
        'range': 'A:Z'
    }
}, {
    'bigquery': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'description':
            'The query to join all the IAR reports into an Affinity Index.',
        'to': {
            'dataset': {
                'field': {
                    'description': 'BigQuery Dataset where all data will live.',
                    'name': 'dataset',
                    'kind': 'string'
                }
            },
            'table': 'final_table'
        },
        'from': {
            'query':
                "SELECT    audience_app.app_url,    audience_app.ctv_app_name,"
                "  IF    (audience_app.app_url LIKE '%Android%'      OR "
                "audience_app.app_url LIKE '%iOS',      'App',      'Domain') "
                "AS app_or_domain,    audience_app.user_list AS audience_list,"
                "    audience_app.Potential_Impressions AS "
                "audience_app_impressions,    "
                "audience_app.Unique_Cookies_With_Impressions AS "
                "audience_app_uniques,    "
                "audience_baseline.Potential_Impressions AS "
                "audience_baseline_impressions,    "
                "audience_baseline.Unique_Cookies_With_Impressions AS "
                "audience_baseline_uniques,    "
                "country_app.Potential_Impressions AS country_app_impressions,"
                "    country_app.Unique_Cookies_With_Impressions AS "
                "country_app_uniques,    "
                "country_baseline.Potential_Impressions AS "
                "country_baseline_impressions,    "
                "country_baseline.Unique_Cookies_With_Impressions AS "
                "country_baseline_uniques,    "
                "((audience_app.Unique_Cookies_With_Impressions/NULLIF(audience_baseline.Unique_Cookies_With_Impressions,"
                "          "
                "0))/NULLIF((country_app.Unique_Cookies_With_Impressions/NULLIF(CAST(country_baseline.Unique_Cookies_With_Impressions"
                " AS int64),            0)),        0))*100 AS affinity_index"
                "  FROM (    SELECT      user_list,      CAST(      IF        "
                "(impressions LIKE '%< 1000%',          0,          "
                "CAST(impressions AS int64)) AS int64) AS "
                "potential_impressions,      CAST(      IF        (uniques "
                "LIKE '%< 100%',          0,          CAST(uniques AS int64)) "
                "AS int64) AS unique_cookies_with_impressions    FROM      "
                "`[PARAMETER].[PARAMETER].us_audience_baseline` ) AS "
                "audience_baseline  JOIN (    SELECT      ctv_app.CTV_App_name"
                " AS ctv_app_name,      user_list,      app_url,      CAST("
                "      IF        (impressions LIKE '%< 1000%',          0,"
                "          CAST(impressions AS int64)) AS int64) AS "
                "potential_impressions,      CAST(      IF        (uniques "
                "LIKE '%< 1000%',          0,          CAST(uniques AS int64))"
                " AS int64) AS unique_cookies_with_impressions    FROM      "
                "`[PARAMETER].[PARAMETER].us_audience_app` AS a    LEFT JOIN"
                "      `[PARAMETER].[PARAMETER].CTV_App_Lookup` AS ctv_app    "
                "ON      a.app_url = ctv_app.Publisher_Name ) AS audience_app"
                "  ON    audience_baseline.user_list = audience_app.user_list"
                "  LEFT JOIN (    SELECT      app_url,      CAST(      IF"
                "        (CAST(impressions AS STRING) LIKE '%< 1000%',"
                "          0,          CAST(impressions AS int64)) AS int64) "
                "AS Potential_Impressions,      CAST(      IF        "
                "(CAST(uniques AS STRING) LIKE '%< 1000%',          0,"
                "          CAST(uniques AS int64)) AS int64) AS "
                "Unique_Cookies_With_Impressions    FROM      "
                "`[PARAMETER].[PARAMETER].us_country_app` ) AS country_app  ON"
                "    country_app.app_url = audience_app.app_url  CROSS JOIN ("
                "    SELECT      CAST(      IF        (CAST(impressions AS "
                "STRING) LIKE '%< 1000%',          0,          "
                "CAST(impressions AS int64)) AS int64) AS "
                "Potential_Impressions,      CAST(      IF        "
                "(CAST(uniques AS STRING) LIKE '%< 1000%',          0,"
                "          CAST(uniques AS int64)) AS int64) AS "
                "Unique_Cookies_With_Impressions    FROM      "
                "`[PARAMETER].[PARAMETER].us_country_baseline` ) AS "
                "country_baseline",
            'legacy':
                False,
            'parameters': [{
                'field': {
                    'description':
                        'Project where BigQuery dataset will be created.',
                    'name':
                        'recipe_project',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'dataset',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Project where BigQuery dataset will be created.',
                    'name':
                        'recipe_project',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'dataset',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Project where BigQuery dataset will be created.',
                    'name':
                        'recipe_project',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'dataset',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Project where BigQuery dataset will be created.',
                    'name':
                        'recipe_project',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'dataset',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Project where BigQuery dataset will be created.',
                    'name':
                        'recipe_project',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'dataset',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Project where BigQuery dataset will be created.',
                    'name':
                        'recipe_project',
                    'kind':
                        'string'
                }
            }, {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'dataset',
                    'kind':
                        'string'
                }
            }]
        }
    }
}]

DAG_FACTORY = DAG_Factory('ctv_audience_affinity', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
