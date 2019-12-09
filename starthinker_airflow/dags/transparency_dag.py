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
Transparency Dashboard

Reports the percentage of DCM impressions that can be attributed to a specific domain or application.  Allows diagnostic of which domans and apps are misconfigured by publisher resulting in underreporting.

W
a
i
t
 
f
o
r
 
<
a
 
h
r
e
f
=
'
h
t
t
p
s
:
/
/
c
o
n
s
o
l
e
.
c
l
o
u
d
.
g
o
o
g
l
e
.
c
o
m
/
b
i
g
q
u
e
r
y
?
p
r
o
j
e
c
t
=
U
N
D
E
F
I
N
E
D
&
d
=
U
N
D
E
F
I
N
E
D
'
 
t
a
r
g
e
t
=
'
_
b
l
a
n
k
'
>
B
i
g
Q
u
e
r
y
 
:
 
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
a
>
 
:
 
U
N
D
E
F
I
N
E
D
 
:
 
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
a
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


C
o
p
y
 
D
a
t
a
S
t
u
d
i
o
 
<
a
 
h
r
e
f
=
'
h
t
t
p
s
:
/
/
d
a
t
a
s
t
u
d
i
o
.
g
o
o
g
l
e
.
c
o
m
/
c
/
u
/
0
/
d
a
t
a
s
o
u
r
c
e
s
/
1
A
z
6
d
9
l
o
A
H
o
6
9
G
S
I
y
K
U
f
u
s
r
t
y
f
_
I
D
q
T
V
s
'
 
t
a
r
g
e
t
=
'
_
b
l
a
n
k
'
>
T
r
a
n
s
p
a
r
e
n
c
y
 
C
o
m
b
i
n
e
d
 
K
P
I
<
/
a
>
 
a
n
d
 
c
o
n
n
e
c
t
.


C
o
p
y
 
D
a
t
a
S
t
u
d
i
o
 
<
a
 
h
r
e
f
=
'
h
t
t
p
s
:
/
/
d
a
t
a
s
t
u
d
i
o
.
g
o
o
g
l
e
.
c
o
m
/
c
/
u
/
0
/
r
e
p
o
r
t
i
n
g
/
1
f
o
i
r
c
G
R
x
g
Y
C
L
_
P
R
8
g
f
d
m
Y
O
l
e
B
a
c
n
P
K
w
B
/
p
a
g
e
/
Q
C
X
j
'
 
t
a
r
g
e
t
=
'
_
b
l
a
n
k
'
>
T
r
a
n
s
p
a
r
e
n
c
y
 
B
r
e
a
k
d
o
w
n
<
/
a
>
.


W
h
e
n
 
p
r
o
m
p
t
e
d
 
c
h
o
o
s
e
 
t
h
e
 
n
e
w
 
d
a
t
a
 
s
o
u
r
c
e
 
y
o
u
 
j
u
s
t
 
c
r
e
a
t
e
d
.


O
r
 
g
i
v
e
 
t
h
e
s
e
 
i
n
t
r
u
c
t
i
o
n
s
 
t
o
 
t
h
e
 
c
l
i
e
n
t
,
 
t
h
e
y
 
w
i
l
l
 
h
a
v
e
 
t
o
 
j
o
i
n
 
t
h
e
 
<
a
 
h
r
e
=
'
h
t
t
p
s
:
/
/
g
r
o
u
p
s
.
g
o
o
g
l
e
.
c
o
m
/
d
/
f
o
r
u
m
/
s
t
a
r
t
h
i
n
k
e
r
-
a
s
s
e
t
s
'
 
t
a
r
g
e
t
=
'
_
b
l
a
n
k
'
>
S
t
a
r
T
h
i
n
k
e
r
 
A
s
s
e
t
s
 
G
r
o
u
p
<
/
a
>
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dataset': '',  # Place where tables will be written in BigQuery.
  'recipe_name': '',  # Name of report in CM, should be unique.
  'recipe_project': '',  # Project where BigQuery dataset will be created.
  'dcm_account': '',  # DCM account id of client.
  'dcm_advertisers': '',  # Comma delimited list of DCM advertiser ids.
}

TASKS = [
  {
    'dataset': {
      'hour': [
        1
      ],
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'dataset',
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
            'description': 'DCM account id of client.'
          }
        },
        'filters': {
          'dfa:advertiser': {
            'values': {
              'field': {
                'name': 'dcm_advertisers',
                'kind': 'integer_list',
                'order': 3,
                'default': '',
                'description': 'Comma delimited list of DCM advertiser ids.'
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
              'prefix': 'Transparency_App_',
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
            'description': 'DCM account id of client.'
          }
        },
        'filters': {
          'dfa:advertiser': {
            'values': {
              'field': {
                'name': 'dcm_advertisers',
                'kind': 'integer_list',
                'order': 3,
                'default': '',
                'description': 'Comma delimited list of DCM advertiser ids.'
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
              'prefix': 'Transparency_Domain_',
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
            'description': 'DCM account id of client.'
          }
        },
        'name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'Transparency_Domain_',
            'description': 'Name of report in CM, should be unique.'
          }
        }
      },
      'out': {
        'bigquery': {
          'auth': 'service',
          'dataset': {
            'field': {
              'name': 'dataset',
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
            'description': 'DCM account id of client.'
          }
        },
        'name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'Transparency_App_',
            'description': 'Name of report in CM, should be unique.'
          }
        }
      },
      'out': {
        'bigquery': {
          'auth': 'service',
          'dataset': {
            'field': {
              'name': 'dataset',
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
            'name': 'dataset',
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
              'name': 'dataset',
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
              'name': 'dataset',
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

DAG_FACTORY = DAG_Factory('transparency', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
