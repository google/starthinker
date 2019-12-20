###########################################################################
# 
#  Copyright 2019 Google Inc.
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
ITP Audit Dashboard

Dashboard that shows performance metrics across browser to see the impact of ITP.

A
 
G
o
o
g
l
e
 
S
h
e
e
t
 
c
a
l
l
e
d
 
<
b
>
I
T
P
 
A
u
d
i
t
 
U
N
D
E
F
I
N
E
D
<
/
b
>
 
w
i
l
l
 
b
e
 
c
r
e
a
t
e
d
 
f
o
r
 
y
o
u
.


A
 
C
M
 
R
e
p
o
r
t
 
c
a
l
l
e
d
 
<
b
>
I
T
P
 
A
u
d
i
t
 
U
N
D
E
F
I
N
E
D
<
/
b
>
 
w
i
l
l
 
b
e
 
c
r
e
a
t
e
d
 
f
o
r
 
y
o
u
.


A
 
D
V
3
6
0
 
R
e
p
o
r
t
 
c
a
l
l
e
d
 
<
b
>
I
T
P
 
A
u
d
i
t
 
U
N
D
E
F
I
N
E
D
<
/
b
>
 
w
i
l
l
 
b
e
 
c
r
e
a
t
e
d
 
f
o
r
 
y
o
u
.


E
d
i
t
 
t
h
e
 
D
V
3
6
0
 
<
b
>
I
T
P
 
A
u
d
i
t
 
U
N
D
E
F
I
N
E
D
<
/
b
>
 
r
e
p
o
r
t
 
a
n
d
 
a
d
d
 
t
h
e
 
f
i
e
l
d
 
<
b
>
M
I
S
S
I
N
G
 
M
E
T
R
I
C
<
/
b
>


R
u
n
 
t
h
i
s
 
r
e
c
i
p
e
.


W
a
i
t
 
f
o
r
 
<
b
>
B
i
g
Q
u
e
r
y
-
>
U
N
D
E
F
I
N
E
D
<
/
b
>
 
t
o
 
b
e
 
c
r
e
a
t
e
d
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'cm_account_id': '',  # Campaign Manager Account Id.
  'advertiser_ids': '',  # Optional, comma separated list of Campaign Manager Advertiser Ids.
  'floodlight_configuration_id': '',  # Floodlight Configuration Id for the Campaign Manager floodlight report.
  'recipe_name': 'ITP_Audit_Dashboard_Browser',  # Name of the Campaign Manager browser report.
}

TASKS = [
  {
    'drive': {
      'auth': 'user',
      'hour': [
      ],
      'copy': {
        'source': 'https://docs.google.com/spreadsheets/d/1rH_PGXOYW2mVdmAYnKbv6kcaB6lQihAyMsGtFfinnqg/',
        'destination': {
          'field': {
            'name': 'recipe_name',
            'prefix': 'ITP Audit',
            'kind': 'string',
            'order': 1,
            'description': 'Name of document to deploy to.',
            'default': ''
          }
        }
      }
    }
  },
  {
    'dataset': {
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'default': 'ITP_Audit_Dashboard',
          'description': 'BigQuery dataset for store dashboard tables.'
        }
      }
    }
  },
  {
    'dcm': {
      'auth': 'user',
      'timeout': 60,
      'report': {
        'account': {
          'field': {
            'name': 'cm_account_id',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Campaign Manager Account Id.'
          }
        },
        'body': {
          'kind': 'dfareporting#report',
          'name': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'prefix': 'ITP_Audit_Floodlight_',
              'description': 'Name of report in DBM, should be unique.'
            }
          },
          'format': 'CSV',
          'type': 'FLOODLIGHT',
          'floodlightCriteria': {
            'dateRange': {
              'kind': 'dfareporting#dateRange',
              'relativeDateRange': 'LAST_30_DAYS'
            },
            'floodlightConfigId': {
              'kind': 'dfareporting#dimensionValue',
              'dimensionName': 'dfa:floodlightConfigId',
              'value': {
                'field': {
                  'name': 'floodlight_configuration_id',
                  'kind': 'integer',
                  'order': 7,
                  'default': '',
                  'description': 'Floodlight Configuration Id for the Campaign Manager floodlight report.'
                }
              },
              'matchType': 'EXACT'
            },
            'reportProperties': {
              'includeUnattributedIPConversions': False,
              'includeUnattributedCookieConversions': True
            },
            'dimensions': [
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:site'
              },
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:floodlightAttributionType'
              },
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:interactionType'
              },
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:pathType'
              },
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:browserPlatform'
              },
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:platformType'
              },
              {
                'kind': 'dfareporting#sortedDimension',
                'name': 'dfa:week'
              }
            ],
            'metricNames': [
              'dfa:activityClickThroughConversions',
              'dfa:activityViewThroughConversions',
              'dfa:totalConversions',
              'dfa:totalConversionsRevenue'
            ]
          },
          'schedule': {
            'active': True,
            'repeats': 'DAILY',
            'every': 1,
            'startDate': '2019-09-11',
            'expirationDate': '2029-12-10'
          },
          'delivery': {
            'emailOwner': False
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'Floodlight_CM_Report',
          'is_incremental_load': False
        }
      },
      'delete': False
    }
  },
  {
    'dbm': {
      'auth': 'user',
      'datastudio': True,
      'report': {
        'name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'ITP_Audit_',
            'description': 'Name of report in DBM, should be unique.'
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'Dv360_Browser_Report_Dirty',
          'autodetect_schema': True,
          'is_incremental_load': False
        }
      }
    }
  },
  {
    'sheets': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit',
          'kind': 'string',
          'order': 1,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Enviroment',
      'range': 'A:B',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'Environment'
        }
      }
    }
  },
  {
    'sheets': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit',
          'kind': 'string',
          'order': 1,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Browser',
      'range': 'A:C',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'Browser'
        }
      }
    }
  },
  {
    'sheets': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit',
          'kind': 'string',
          'order': 1,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'CM_Site_Segments',
      'range': 'A:C',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'CM_Browser_lookup'
        }
      }
    }
  },
  {
    'sheets': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit',
          'kind': 'string',
          'order': 1,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Device_Type',
      'range': 'A:B',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'Device_Type'
        }
      }
    }
  },
  {
    'sheets': {
      'auth': 'user',
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit',
          'kind': 'string',
          'order': 1,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'tab': 'Floodlight_Attribution',
      'range': 'A:B',
      'header': True,
      'out': {
        'auth': 'service',
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'recipe_name',
              'kind': 'string',
              'order': 1,
              'default': 'ITP_Audit_Dashboard',
              'description': 'BigQuery dataset for store dashboard tables.'
            }
          },
          'table': 'Floodlight_Attribution'
        }
      }
    }
  },
  {
    'itp_audit': {
      'auth': 'service',
      'account': {
        'field': {
          'name': 'cm_account_id',
          'kind': 'string',
          'order': 3,
          'default': '',
          'description': 'Campaign Manager Account Id.'
        }
      },
      'dataset': {
        'field': {
          'name': 'recipe_name',
          'kind': 'string',
          'order': 1,
          'default': 'ITP_Audit_Dashboard',
          'description': 'BigQuery dataset for store dashboard tables.'
        }
      },
      'sheet': {
        'field': {
          'name': 'recipe_name',
          'prefix': 'ITP Audit',
          'kind': 'string',
          'order': 1,
          'description': 'Name of document to deploy to.',
          'default': ''
        }
      },
      'cm_browser_report_name': {
        'field': {
          'name': 'recipe_name',
          'kind': 'string',
          'order': 9,
          'prefix': 'ITP_Audit_Browser_',
          'default': 'ITP_Audit_Dashboard_Browser',
          'description': 'Name of the Campaign Manager browser report.'
        }
      },
      'advertiser_ids': {
        'field': {
          'name': 'advertiser_ids',
          'kind': 'string',
          'order': 5,
          'default': '',
          'description': 'Optional, comma separated list of Campaign Manager Advertiser Ids.'
        }
      },
      'timeout': 60
    }
  }
]

DAG_FACTORY = DAG_Factory('itp_audit', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
