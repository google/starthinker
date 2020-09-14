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

Segmentology DV360

DV360 funnel analysis using Census data.

Wait for <b>BigQuery->UNDEFINED->UNDEFINED->Census_Pivot</b> to be created.
Join the <a hre='https://groups.google.com/d/forum/starthinker-assets'
target='_blank'>StarThinker Assets Group</a> to access the following assets
Copy <a
href='https://datastudio.google.com/c/u/0/reporting/4a908845-fdba-4023-9bb7-68666202bafb/page/K15YB/'
target='_blank'>DV360 Segmentology</a>. Leave the Data Source as is, you will
change it in the next step.
Click Edit Connection, and change to
<b>BigQuery->UNDEFINED->(field:recipe_slug}->Census_Pivot</b>.
Or give these intructions to the client.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth_read': 'user',  # Credentials used for reading data.
    'recipe_project': '',  # Project ID hosting dataset.
    'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
    'auth_write': 'service',  # Authorization used for writing data.
    'recipe_name': '',  # Name of report, not needed if ID used.
    'recipe_slug': '',  # Name of Google BigQuery dataset to create.
    'partners': [],  # DV360 partner id.
    'advertisers': [],  # Comma delimited list of DV360 advertiser ids.
}

TASKS = [{
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
        'description': 'Create a dataset for bigquery tables.',
        'dataset': {
            'field': {
                'description':
                    'Place where tables will be created in BigQuery.',
                'name':
                    'recipe_slug',
                'kind':
                    'string'
            }
        },
        'hour': [4]
    }
}, {
    'bigquery': {
        'auth': {
            'field': {
                'description': 'Credentials used for writing function.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'to': {
            'dataset': {
                'field': {
                    'description': 'Name of Google BigQuery dataset to create.',
                    'name': 'recipe_slug',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            }
        },
        'function': 'pearson_significance_test'
    }
}, {
    'dbm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 0
            }
        },
        'report': {
            'filters': {
                'FILTER_PARTNER': {
                    'values': {
                        'field': {
                            'description': 'DV360 partner id.',
                            'name': 'partners',
                            'default': [],
                            'kind': 'integer_list',
                            'order': 5
                        }
                    }
                },
                'FILTER_ADVERTISER': {
                    'values': {
                        'field': {
                            'description':
                                'Comma delimited list of DV360 advertiser ids.',
                            'name':
                                'advertisers',
                            'default': [],
                            'kind':
                                'integer_list',
                            'order':
                                6
                        }
                    }
                }
            },
            'body': {
                'params': {
                    'type':
                        'TYPE_CROSS_PARTNER',
                    'metrics': [
                        'METRIC_BILLABLE_IMPRESSIONS', 'METRIC_CLICKS',
                        'METRIC_TOTAL_CONVERSIONS'
                    ],
                    'groupBys': [
                        'FILTER_PARTNER', 'FILTER_PARTNER_NAME',
                        'FILTER_ADVERTISER', 'FILTER_ADVERTISER_NAME',
                        'FILTER_MEDIA_PLAN', 'FILTER_MEDIA_PLAN_NAME',
                        'FILTER_ZIP_POSTAL_CODE'
                    ]
                },
                'metadata': {
                    'dataRange': 'LAST_30_DAYS',
                    'title': {
                        'field': {
                            'name':
                                'recipe_name',
                            'default':
                                '',
                            'prefix':
                                'Segmentology ',
                            'description':
                                'Name of report, not needed if ID used.',
                            'kind':
                                'string',
                            'order':
                                3
                        }
                    },
                    'format': 'CSV'
                },
                'timezoneCode': {
                    'field': {
                        'description': 'Timezone for report dates.',
                        'name': 'recipe_timezone',
                        'default': 'America/Los_Angeles',
                        'kind': 'timezone'
                    }
                },
                'schedule': {
                    'frequency': 'WEEKLY'
                }
            }
        }
    }
}, {
    'dbm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 0
            }
        },
        'out': {
            'bigquery': {
                'auth': {
                    'field': {
                        'description': 'Authorization used for writing data.',
                        'name': 'auth_write',
                        'default': 'service',
                        'kind': 'authentication',
                        'order': 1
                    }
                },
                'dataset': {
                    'field': {
                        'description':
                            'Name of Google BigQuery dataset to create.',
                        'name':
                            'recipe_slug',
                        'default':
                            '',
                        'kind':
                            'string',
                        'order':
                            4
                    }
                },
                'schema': [{
                    'name': 'Partner_Id',
                    'type': 'INTEGER',
                    'mode': 'REQUIRED'
                }, {
                    'name': 'Partner',
                    'type': 'STRING',
                    'mode': 'REQUIRED'
                }, {
                    'name': 'Advertiser_Id',
                    'type': 'INTEGER',
                    'mode': 'REQUIRED'
                }, {
                    'name': 'Advertiser',
                    'type': 'STRING',
                    'mode': 'REQUIRED'
                }, {
                    'name': 'Campaign_Id',
                    'type': 'INTEGER',
                    'mode': 'REQUIRED'
                }, {
                    'name': 'Campaign',
                    'type': 'STRING',
                    'mode': 'REQUIRED'
                }, {
                    'name': 'Zip',
                    'type': 'STRING',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'Impressions',
                    'type': 'FLOAT',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'Clicks',
                    'type': 'INTEGER',
                    'mode': 'NULLABLE'
                }, {
                    'name': 'Conversions',
                    'type': 'FLOAT',
                    'mode': 'NULLABLE'
                }],
                'table': 'DV360_KPI'
            }
        },
        'report': {
            'name': {
                'field': {
                    'name': 'recipe_name',
                    'default': '',
                    'prefix': 'Segmentology ',
                    'description': 'Name of report, not needed if ID used.',
                    'kind': 'string',
                    'order': 3
                }
            }
        }
    }
}, {
    'bigquery': {
        'auth': {
            'field': {
                'description': 'Authorization used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'to': {
            'view': 'DV360_KPI_Normalized',
            'dataset': {
                'field': {
                    'description':
                        'Place where tables will be written in BigQuery.',
                    'name':
                        'recipe_slug',
                    'kind':
                        'string'
                }
            }
        },
        'from': {
            'query':
                'SELECT            Partner_Id,            Partner,            '
                'Advertiser_Id,            Advertiser,            Campaign_Id,'
                '            Campaign,            Zip,            '
                'SAFE_DIVIDE(Impressions, SUM(Impressions) OVER(PARTITION BY '
                'Advertiser_Id)) AS Impression_Percent,            '
                'SAFE_DIVIDE(Clicks, Impressions) AS Click_Percent,'
                '            SAFE_DIVIDE(Conversions, Impressions) AS '
                'Conversion_Percent,            Impressions AS Impressions'
                '          FROM            `{project}.{dataset}.DV360_KPI`;'
                '        ',
            'legacy':
                False,
            'parameters': {
                'project': {
                    'field': {
                        'description': 'Project ID hosting dataset.',
                        'name': 'recipe_project',
                        'kind': 'string'
                    }
                },
                'dataset': {
                    'field': {
                        'description':
                            'Place where tables will be created in BigQuery.',
                        'name':
                            'recipe_slug',
                        'kind':
                            'string'
                    }
                }
            }
        }
    }
}, {
    'census': {
        'auth': {
            'field': {
                'description': 'Authorization used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'to': {
            'dataset': {
                'field': {
                    'description': 'Name of Google BigQuery dataset to create.',
                    'name': 'recipe_slug',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            },
            'type': 'view'
        },
        'normalize': {
            'census_geography': 'zip_codes',
            'census_span': '5yr',
            'census_year': '2018'
        }
    }
}, {
    'census': {
        'auth': {
            'field': {
                'description': 'Authorization used for writing data.',
                'name': 'auth_write',
                'default': 'service',
                'kind': 'authentication',
                'order': 1
            }
        },
        'correlate': {
            'significance': 80,
            'correlate': [
                'Impression_Percent', 'Click_Percent', 'Conversion_Percent'
            ],
            'join': 'Zip',
            'pass': [
                'Partner_Id', 'Partner', 'Advertiser_Id', 'Advertiser',
                'Campaign_Id', 'Campaign'
            ],
            'sum': ['Impressions'],
            'dataset': {
                'field': {
                    'description': 'Name of Google BigQuery dataset to create.',
                    'name': 'recipe_slug',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            },
            'table': 'DV360_KPI_Normalized'
        },
        'to': {
            'dataset': {
                'field': {
                    'description': 'Name of Google BigQuery dataset to create.',
                    'name': 'recipe_slug',
                    'default': '',
                    'kind': 'string',
                    'order': 4
                }
            },
            'type': 'view'
        }
    }
}]

DAG_FACTORY = DAG_Factory('segmentology_dv360', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
