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

ITP Audit Dashboard ( 2020 )

Dashboard that shows performance metrics across browser to see the impact of
ITP.

Follow the instructions from <a
href="https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/edit?usp=sharing"
target="_blank">this document</a>

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'recipe_timezone': 'America/Los_Angeles',  # Timezone for report dates.
    'auth_read': 'user',  # Credentials used for reading data.
    'recipe_name': '',  # Name of document to deploy to.
    'recipe_slug':
        'ITP_Audit_Dashboard',  # BigQuery dataset for store dashboard tables.
    'auth_write': 'service',  # Credentials used for writing data.
    'cm_account_id': '',  # Campaign Manager Account Id.
    'cm_advertiser_ids':
        '',  # Optional: Comma delimited list of CM advertiser ids.
    'floodlight_configuration_id':
        '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
    'dv360_partner_ids': '',  # Comma delimited list of DV360 Partner ids.
    'dv360_advertiser_ids':
        '',  # Optional: Comma delimited list of DV360 Advertiser ids.
}

TASKS = [{
    'drive': {
        'auth': 'user',
        'copy': {
            'source':
                'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/',
            'destination': {
                'field': {
                    'name': 'recipe_name',
                    'default': '',
                    'description': 'Name of document to deploy to.',
                    'prefix': 'ITP Audit ',
                    'kind': 'string',
                    'order': 1
                }
            }
        },
        'hour': []
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
                'description': 'BigQuery dataset for store dashboard tables.',
                'name': 'recipe_slug',
                'default': 'ITP_Audit_Dashboard',
                'kind': 'string',
                'order': 1
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
                'order': 1
            }
        },
        'delete': False,
        'report': {
            'filters': {
                'FILTER_PARTNER': {
                    'values': {
                        'field': {
                            'description':
                                'Comma delimited list of DV360 Partner ids.',
                            'name':
                                'dv360_partner_ids',
                            'default':
                                '',
                            'kind':
                                'integer_list',
                            'order':
                                5
                        }
                    }
                },
                'FILTER_ADVERTISER': {
                    'values': {
                        'field': {
                            'description':
                                'Optional: Comma delimited list of DV360 '
                                'Advertiser ids.',
                            'name':
                                'dv360_advertiser_ids',
                            'default':
                                '',
                            'kind':
                                'integer_list',
                            'order':
                                6
                        }
                    }
                }
            },
            'timeout': 90,
            'body': {
                'params': {
                    'type':
                        'TYPE_GENERAL',
                    'metrics': [
                        'METRIC_MEDIA_COST_ADVERTISER', 'METRIC_IMPRESSIONS',
                        'METRIC_CLICKS', 'METRIC_TOTAL_CONVERSIONS',
                        'METRIC_LAST_CLICKS', 'METRIC_LAST_IMPRESSIONS',
                        'METRIC_CM_POST_CLICK_REVENUE',
                        'METRIC_CM_POST_VIEW_REVENUE',
                        'METRIC_REVENUE_ADVERTISER'
                    ],
                    'groupBys': [
                        'FILTER_ADVERTISER', 'FILTER_ADVERTISER_CURRENCY',
                        'FILTER_MEDIA_PLAN', 'FILTER_INSERTION_ORDER',
                        'FILTER_LINE_ITEM', 'FILTER_PAGE_LAYOUT', 'FILTER_WEEK',
                        'FILTER_MONTH', 'FILTER_YEAR', 'FILTER_PARTNER',
                        'FILTER_LINE_ITEM_TYPE', 'FILTER_DEVICE_TYPE',
                        'FILTER_BROWSER'
                    ]
                },
                'metadata': {
                    'dataRange': 'LAST_365_DAYS',
                    'title': {
                        'field': {
                            'description':
                                'Name of report in DV360, should be unique.',
                            'name':
                                'recipe_name',
                            'kind':
                                'string',
                            'order':
                                1,
                            'prefix':
                                'ITP_Audit_Browser_'
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
                }
            }
        }
    }
}, {
    'dcm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'delete': False,
        'out': {
            'bigquery': {
                'is_incremental_load': False,
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_Floodlight_CM_Report'
            }
        },
        'report': {
            'timeout': 90,
            'body': {
                'name': {
                    'field': {
                        'description':
                            'Name of report in DV360, should be unique.',
                        'name':
                            'recipe_name',
                        'kind':
                            'string',
                        'order':
                            1,
                        'prefix':
                            'ITP_Audit_Floodlight_'
                    }
                },
                'floodlightCriteria': {
                    'dateRange': {
                        'kind': 'dfareporting#dateRange',
                        'relativeDateRange': 'LAST_30_DAYS'
                    },
                    'dimensions': [{
                        'name': 'dfa:site',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:floodlightAttributionType',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:interactionType',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:pathType',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:browserPlatform',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:platformType',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:week',
                        'kind': 'dfareporting#sortedDimension'
                    }],
                    'floodlightConfigId': {
                        'matchType': 'EXACT',
                        'value': {
                            'field': {
                                'description':
                                    'Floodlight Configuration Id for the '
                                    'Campaign Manager floodlight report.',
                                'name':
                                    'floodlight_configuration_id',
                                'default':
                                    '',
                                'kind':
                                    'integer',
                                'order':
                                    4
                            }
                        },
                        'kind': 'dfareporting#dimensionValue',
                        'dimensionName': 'dfa:floodlightConfigId'
                    },
                    'reportProperties': {
                        'includeUnattributedIPConversions': False,
                        'includeUnattributedCookieConversions': True
                    },
                    'metricNames': [
                        'dfa:activityClickThroughConversions',
                        'dfa:activityViewThroughConversions',
                        'dfa:totalConversions', 'dfa:totalConversionsRevenue'
                    ]
                },
                'type': 'FLOODLIGHT',
                'schedule': {
                    'active': True,
                    'every': 1,
                    'repeatsOnWeekDays': ['Sunday'],
                    'repeats': 'WEEKLY'
                },
                'format': 'CSV',
                'delivery': {
                    'emailOwner': False
                },
                'kind': 'dfareporting#report'
            },
            'account': {
                'field': {
                    'description': 'Campaign Manager Account Id.',
                    'name': 'cm_account_id',
                    'default': '',
                    'kind': 'string',
                    'order': 2
                }
            }
        }
    }
}, {
    'dcm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'delete': False,
        'out': {
            'bigquery': {
                'is_incremental_load': False,
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_CM_Browser_Report_Dirty'
            }
        },
        'report': {
            'filters': {
                'dfa:advertiser': {
                    'values': {
                        'field': {
                            'description':
                                'Optional: Comma delimited list of CM '
                                'advertiser ids.',
                            'name':
                                'cm_advertiser_ids',
                            'default':
                                '',
                            'kind':
                                'integer_list',
                            'order':
                                3
                        }
                    }
                }
            },
            'timeout': 90,
            'body': {
                'name': {
                    'field': {
                        'name':
                            'recipe_name',
                        'default':
                            'ITP_Audit_Dashboard_Browser',
                        'prefix':
                            'ITP_Audit_Browser_',
                        'description':
                            'Name of the Campaign Manager browser report.',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'schedule': {
                    'active': True,
                    'every': 1,
                    'repeatsOnWeekDays': ['Sunday'],
                    'repeats': 'WEEKLY'
                },
                'type': 'STANDARD',
                'format': 'CSV',
                'delivery': {
                    'emailOwner': False
                },
                'criteria': {
                    'dateRange': {
                        'kind': 'dfareporting#dateRange',
                        'relativeDateRange': 'LAST_365_DAYS'
                    },
                    'dimensionFilters': [],
                    'dimensions': [{
                        'name': 'dfa:campaign',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:campaignId',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:site',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:advertiser',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:advertiserId',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:browserPlatform',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:platformType',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:month',
                        'kind': 'dfareporting#sortedDimension'
                    }, {
                        'name': 'dfa:week',
                        'kind': 'dfareporting#sortedDimension'
                    }],
                    'metricNames': [
                        'dfa:impressions', 'dfa:clicks', 'dfa:totalConversions',
                        'dfa:activityViewThroughConversions',
                        'dfa:activityClickThroughConversions'
                    ]
                },
                'fileName': {
                    'field': {
                        'name':
                            'recipe_name',
                        'default':
                            'ITP_Audit_Dashboard_Browser',
                        'prefix':
                            'ITP_Audit_Browser_',
                        'description':
                            'Name of the Campaign Manager browser report.',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'kind': 'dfareporting#report'
            },
            'account': {
                'field': {
                    'description': 'Campaign Manager Account Id.',
                    'name': 'cm_account_id',
                    'default': '',
                    'kind': 'string',
                    'order': 2
                }
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
                'prefix': 'ITP Audit ',
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
        'tab': 'Enviroment',
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
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_Environment'
            }
        },
        'range': 'A:B'
    }
}, {
    'sheets': {
        'header': True,
        'sheet': {
            'field': {
                'name': 'recipe_name',
                'default': '',
                'description': 'Name of document to deploy to.',
                'prefix': 'ITP Audit ',
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
        'tab': 'Browser',
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
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_Browser'
            }
        },
        'range': 'A:C'
    }
}, {
    'sheets': {
        'header': True,
        'sheet': {
            'field': {
                'name': 'recipe_name',
                'default': '',
                'description': 'Name of document to deploy to.',
                'prefix': 'ITP Audit ',
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
        'tab': 'CM_Browser_lookup',
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
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_CM_Browser_lookup'
            }
        },
        'range': 'A:C'
    }
}, {
    'sheets': {
        'header': True,
        'sheet': {
            'field': {
                'name': 'recipe_name',
                'default': '',
                'description': 'Name of document to deploy to.',
                'prefix': 'ITP Audit ',
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
        'tab': 'Device_Type',
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
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_Device_Type'
            }
        },
        'range': 'A:B'
    }
}, {
    'sheets': {
        'header': True,
        'sheet': {
            'field': {
                'name': 'recipe_name',
                'default': '',
                'description': 'Name of document to deploy to.',
                'prefix': 'ITP Audit ',
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
        'tab': 'Floodlight_Attribution',
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
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_Floodlight_Attribution'
            }
        },
        'range': 'A:B'
    }
}, {
    'dbm': {
        'auth': {
            'field': {
                'description': 'Credentials used for reading data.',
                'name': 'auth_read',
                'default': 'user',
                'kind': 'authentication',
                'order': 1
            }
        },
        'out': {
            'bigquery': {
                'dataset': {
                    'field': {
                        'description':
                            'BigQuery dataset for store dashboard tables.',
                        'name':
                            'recipe_slug',
                        'default':
                            'ITP_Audit_Dashboard',
                        'kind':
                            'string',
                        'order':
                            1
                    }
                },
                'table': 'z_Dv360_Browser_Report_Dirty'
            }
        },
        'report': {
            'name': {
                'field': {
                    'description': 'Name of report in DV360, should be unique.',
                    'name': 'recipe_name',
                    'kind': 'string',
                    'order': 1,
                    'prefix': 'ITP_Audit_Browser_'
                }
            }
        }
    }
}, {
    'itp_audit': {
        'auth': 'service',
        'account': {
            'field': {
                'description': 'Campaign Manager Account Id.',
                'name': 'cm_account_id',
                'default': '',
                'kind': 'string',
                'order': 2
            }
        },
        'timeout': 60,
        'sheet': {
            'field': {
                'name': 'recipe_name',
                'default': '',
                'description': 'Name of document to deploy to.',
                'prefix': 'ITP Audit ',
                'kind': 'string',
                'order': 1
            }
        },
        'dataset': {
            'field': {
                'description': 'BigQuery dataset for store dashboard tables.',
                'name': 'recipe_slug',
                'default': 'ITP_Audit_Dashboard',
                'kind': 'string',
                'order': 1
            }
        }
    }
}]

DAG_FACTORY = DAG_Factory('itp_audit', {'tasks': TASKS}, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
