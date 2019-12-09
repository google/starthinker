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
Barnacle

Gives DCM clients ability to see which profiles have access to which parts of an account. Loads DCM user profile mappings using the API into BigQuery and connects to a DataStudio dashboard.

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
-
>
C
M
_
*
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
-
>
B
a
r
n
a
c
l
e
_
*
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
,
 
t
h
e
n
 
c
o
p
y
 
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
 
t
h
e
 
f
o
l
l
o
w
i
n
g
 
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
.


J
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
 
t
o
 
a
c
c
e
s
s
 
t
h
e
 
f
o
l
l
o
w
i
n
g
 
a
s
s
e
t
s


C
o
p
y
 
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
o
p
e
n
/
1
a
6
K
-
X
d
P
U
z
C
Y
R
X
Z
p
1
Z
c
m
e
O
U
O
U
R
c
9
w
n
2
J
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
B
a
r
n
a
c
l
e
 
P
r
o
f
i
l
e
 
A
d
v
e
r
t
i
s
e
r
 
M
a
p
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
o
p
e
n
/
1
N
E
z
r
Q
W
W
n
P
j
k
D
9
0
i
U
w
N
-
A
S
K
b
V
B
z
o
e
B
d
o
T
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
a
r
n
a
c
l
e
 
P
r
o
f
i
l
e
 
C
a
m
p
a
i
g
n
 
M
a
p
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
o
p
e
n
/
1
-
Y
G
D
i
Q
P
D
n
k
0
g
D
7
8
_
Q
O
Y
5
X
d
T
X
R
l
T
r
L
e
E
q
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
a
r
n
a
c
l
e
 
P
r
o
f
i
l
e
 
R
e
p
o
r
t
 
M
a
p
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
o
p
e
n
/
1
v
_
G
R
a
i
t
w
P
a
H
H
K
U
z
f
J
Z
Y
N
B
h
z
o
t
v
Z
-
b
R
7
Y
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
a
r
n
a
c
l
e
 
P
r
o
f
i
l
e
 
S
i
t
e
 
M
a
p
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
o
p
e
n
/
1
4
t
W
l
h
7
y
i
q
z
x
K
J
I
p
p
M
F
V
O
w
2
M
o
M
t
Q
V
_
u
c
E
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
a
r
n
a
c
l
e
 
P
r
o
f
i
l
e
s
 
C
o
n
n
e
c
t
i
o
n
s
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
o
p
e
n
/
1
m
a
v
j
x
v
H
S
E
P
f
J
q
5
a
W
4
F
Y
g
C
X
s
B
C
E
5
r
t
h
Z
G
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
a
r
n
a
c
l
e
 
R
e
p
o
r
t
 
D
e
l
i
v
e
r
y
 
P
r
o
f
i
l
e
s
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
o
p
e
n
/
1
A
z
k
_
N
u
l
-
a
u
i
n
f
4
N
n
D
q
8
T
9
f
D
y
i
K
k
U
W
D
7
A
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
a
r
n
a
c
l
e
 
R
o
l
e
s
 
D
u
p
l
i
c
a
t
e
s
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
o
p
e
n
/
1
o
g
o
o
f
p
K
t
q
k
L
w
c
W
9
q
C
_
J
u
_
J
v
J
d
I
a
j
s
j
N
I
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
a
r
n
a
c
l
e
 
R
o
l
e
s
 
N
o
t
 
U
s
e
d
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
o
p
e
n
/
1
x
L
g
Z
P
j
O
P
D
t
m
P
y
E
q
Y
M
i
M
b
W
w
M
I
8
-
W
T
s
l
f
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
B
a
r
n
a
c
l
e
 
S
i
t
e
 
C
o
n
t
a
c
t
s
 
P
r
o
f
i
l
e
s
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
o
p
e
n
/
1
g
j
x
H
m
0
j
U
l
Q
U
d
0
j
M
u
x
a
O
l
m
r
l
8
g
O
X
1
k
y
K
T
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
a
r
n
a
c
l
e
 
R
e
p
o
r
t
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
s
 
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
.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'dataset': '',  # Place where tables will be written in BigQuery.
  'project': '',  # Project where BigQuery dataset will be created.
  'accounts': [],  # Comma separated DCM account ids.
}

TASKS = [
  {
    'dataset': {
      'description': 'The dataset will hold multiple tables, amke sure it exists.',
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
    'barnacle': {
      'description': 'Will create tables with format CM_* to hold each endpoint via a call to the API list function. Exclude reports for its own task.',
      'hour': [
        1
      ],
      'auth': 'user',
      'endpoints': [
        'accounts',
        'subaccounts',
        'profiles',
        'advertisers',
        'campaigns',
        'sites',
        'roles'
      ],
      'accounts': {
        'single_cell': True,
        'values': {
          'field': {
            'name': 'accounts',
            'kind': 'integer_list',
            'order': 2,
            'default': [
            ],
            'description': 'Comma separated DCM account ids.'
          }
        }
      },
      'out': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Google BigQuery dataset to create tables in.'
          }
        }
      }
    }
  },
  {
    'barnacle': {
      'description': 'Will create tables with format CM_* to hold each endpoint via a call to the API list function. Reports run long so seperate task.',
      'hour': [
        3
      ],
      'auth': 'user',
      'endpoints': [
        'reports'
      ],
      'accounts': {
        'single_cell': True,
        'values': {
          'field': {
            'name': 'accounts',
            'kind': 'integer_list',
            'order': 2,
            'default': [
            ],
            'description': 'Comma separated DCM account ids.'
          }
        }
      },
      'out': {
        'auth': 'service',
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Google BigQuery dataset to create tables in.'
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'hour': [
        8
      ],
      'description': 'Combine profile, account, subaccount, and roles into one view, used by other views in this workflow.',
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': " SELECT   P.profileId AS profileId,   P.accountId AS accountId,   P.subaccountId AS subaccountId,   P.name AS Profile_Name,    P.email AS Profile_Email,    REGEXP_EXTRACT(P.email, r'@(.+)') AS Profile_Domain,   P.userAccessType AS Profile_userAccessType,    P.active AS Profie_active,    P.traffickerType AS Profile_traffickerType,    P.comments AS Profile_comments,   P.userRoleId AS Profile_userRoleId,    R.role_name AS Role_role_name,    R.role_defaultUserRole AS Role_role_defaultUserRole,    R.permission_name AS Role_permission_name,        R.permission_availability AS Role_permission_availability,   A.name AS Account_name,   A.active AS Account_active,   A.description AS Account_description,   A.locale AS Account_locale,   S.name AS SubAccount_name FROM `[PARAMETER].[PARAMETER].CM_Profiles` AS P  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Roles` AS R    ON P.userRoleId=R.roleId LEFT JOIN `[PARAMETER].[PARAMETER].CM_Accounts` AS A    ON P.accountId=A.accountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_SubAccounts` AS S    ON P.accountId=S.accountId   AND P.subaccountId=S.subaccountId ; ",
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Profile_Role_Account_SubAccount_Map'
      }
    }
  },
  {
    'bigquery': {
      'description': 'Combine profiles and advertisers.',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT   APRASM.*,   A.advertiserId AS advertiserId,   A.name AS Advertiser_name,    A.status AS Advertiser_status,    A.defaultEmail AS Advertiser_defaultEmail,    A.suspended AS Advertiser_suspended FROM `[PARAMETER].[PARAMETER].CM_Profile_Advertisers` As PA LEFT JOIN `[PARAMETER].[PARAMETER].Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM    ON PA.profileID=APRASM.profileID LEFT JOIN `[PARAMETER].[PARAMETER].CM_Advertisers` AS A    ON PA.advertiserId=A.advertiserId ; ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Profile_Advertiser_Map'
      }
    }
  },
  {
    'bigquery': {
      'description': 'Profile to campaign mapping.',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT   APRASM.*,   C.campaignId AS campaignId,   C.name AS Campaign_name,    C.archived AS Campaign_archived,   IF(C.startDate <= CURRENT_DATE() AND C.endDate >= CURRENT_DATE(), True, False) AS Campaign_running,   ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), C.lastModifiedInfo_time, DAY) / 7) AS Campaign_Modified_Weeks_Ago FROM `[PARAMETER].[PARAMETER].CM_Profile_Campaigns` As PC LEFT JOIN `[PARAMETER].[PARAMETER].Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM    ON PC.profileID=APRASM.profileID  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Campaigns` AS C    ON PC.campaignId=C.campaignId ; ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Profile_Campaign_Map'
      }
    }
  },
  {
    'bigquery': {
      'description': 'The logic query for Deal Finder, transforms report into view used by datastudio.',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT   APRASM.*,   R.reportId AS reportId,   R.name AS Report_name,    R.type AS Report_type,   R.format AS Report_format,   R.schedule_active AS Report_schedule_active,   R.schedule_repeats AS Report_schedule_repeats,   ROUND(TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), R.lastModifiedTime, DAY) / 7) AS Report_Modified_Weeks_Ago,   DATE_DIFF(R.schedule_expirationDate, CURRENT_DATE(), MONTH) AS Report_Schedule_Weeks_To_Go FROM `[PARAMETER].[PARAMETER].CM_Reports` As R LEFT JOIN `[PARAMETER].[PARAMETER].Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM    ON R.profileID=APRASM.profileID ; ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Profile_Report_Map'
      }
    }
  },
  {
    'bigquery': {
      'description': 'The logic query for Deal Finder, transforms report into view used by datastudio.',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT   APRASM.*,   S.siteId AS siteId,   S.name AS Site_Name,    S.keyName AS Site_keyName,    S.approved AS Site_approved FROM `[PARAMETER].[PARAMETER].CM_Profile_Sites` As PS LEFT JOIN `[PARAMETER].[PARAMETER].Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM    ON PS.profileID=APRASM.profileID  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Sites` AS S    ON PS.siteId=S.siteId ; ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Profile_Site_Map'
      }
    }
  },
  {
    'bigquery': {
      'description': 'The logic query for Deal Finder, transforms report into view used by datastudio.',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT    APRASM.* FROM `[PARAMETER].[PARAMETER].Barnacle_Profile_Role_Account_SubAccount_Map` AS APRASM LEFT JOIN `[PARAMETER].[PARAMETER].CM_Profile_Advertisers` AS PA    ON APRASM.profileId=PA.profileId  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Profile_Campaigns` AS PC    ON APRASM.profileId=PC.profileId  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Profile_Sites` AS PS   ON APRASM.profileId=PS.profileId  WHERE   PA.advertiserId IS NULL   AND PC.campaignId IS NULL   AND PS.siteId IS NULL  ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Profiles_Connections'
      }
    }
  },
  {
    'bigquery': {
      'description': '',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT   RD.accountId AS accountId,   RD.subaccountId AS subaccountId,   RD.reportId AS reportId,   A.name AS Account_name,   A.active AS Account_active,   SA.name as SubAccount_name,   R.name as Report_name,   R.schedule_active AS Report_schedule_active,   RD.emailOwnerDeliveryType AS Delivery_emailOwnerDeliveryType,   RD.deliveryType AS Delivery_deliveryType,   RD.email AS Delivery_email,   RD.message AS Delivery_message,   IF(RD.email in (SELECT email from `[PARAMETER].[PARAMETER].CM_Profiles`), True, False) AS Profile_Match_Exists FROM `[PARAMETER].[PARAMETER].CM_Report_Deliveries` AS RD  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Accounts` AS A    ON RD.accountId=A.accountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_SubAccounts` AS SA    ON RD.subaccountId=SA.subaccountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_Reports` AS R    ON RD.reportId=R.reportId ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Report_Delivery_Profiles'
      }
    }
  },
  {
    'bigquery': {
      'description': '',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': ' SELECT   R.accountId AS accountId,   R.subaccountId AS subaccountId,   R.roleId AS roleId,   A.name AS Account_name,   A.active AS Account_active,   SA.name AS SubAccount_name,   R.role_name as Role_role_name,   R.role_defaultUserRole AS Role_role_defaultUserRole,   R.permission_name AS Role_permission_name,   R.permission_availability AS Role_permission_availability   FROM `[PARAMETER].[PARAMETER].CM_Roles` AS R LEFT JOIN `[PARAMETER].[PARAMETER].CM_Accounts` AS A on R.accountId=A.accountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_SubAccounts` AS SA on R.subaccountId=SA.subaccountId WHERE roleId NOT IN (   SELECT roleId FROM `[PARAMETER].[PARAMETER].CM_Profile_Roles`  ) ',
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Roles_Not_Used'
      }
    }
  },
  {
    'bigquery': {
      'description': '',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': " SELECT   SC.accountId AS accountId,   SC.subaccountId AS subaccountId,   SC.siteId AS siteId,   SC.contactId AS contactId,   A.name AS Account_name,   A.active AS Account_active,   SA.name as SubAccount_name,   S.name as Site_name,   S.approved AS Site_approved,   SC.email AS Site_Contact_email,   CONCAT(SC.firstName, ' ', sc.lastname) AS Site_Contact_Name,   SC.phone AS Site_Contact_phone,   SC.contactType AS Site_Contact_contactType,   IF(sc.email in (SELECT email from `[PARAMETER].[PARAMETER].CM_Profiles`), True, False) AS Profile_Match_Exists FROM `[PARAMETER].[PARAMETER].CM_Site_Contacts` AS SC  LEFT JOIN `[PARAMETER].[PARAMETER].CM_Accounts` AS A    ON SC.accountId=A.accountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_SubAccounts` AS SA    ON SC.accountId=SA.accountId    AND SC.subaccountId=SA.subaccountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_Sites` AS S    ON SC.siteId=S.siteId ; ",
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Site_Contacts_Profiles'
      }
    }
  },
  {
    'bigquery': {
      'description': '',
      'hour': [
        8
      ],
      'auth': 'service',
      'from': {
        'legacy': False,
        'query': " WITH   profile_counts AS (   SELECT userRoleId, COUNT(profileId) as profile_count   FROM `[PARAMETER].[PARAMETER].CM_Profiles`   GROUP BY 1  ),  permission_fingerprints AS (   SELECT     accountId,     subaccountId,     roleId,     role_name,     role_defaultUserRole,     SUM(profile_count) AS profile_count,     FARM_FINGERPRINT(       ARRAY_TO_STRING(       ARRAY_AGG(         DISTINCT permission_name ORDER BY permission_name ASC       ), ',', '-'     )   ) AS permissions_fingerprint   FROM     `[PARAMETER].[PARAMETER].CM_Roles` AS R   LEFT JOIN profile_counts AS P   ON R.roleId = P.userRoleId   GROUP BY     accountId,     subaccountId,     roleId,     role_name,     role_defaultUserRole )  SELECT    PFL.accountId AS accountId,   A.name AS Account_name,   A.active AS Account_active,   PFL.subaccountId AS subaccountId,    SA.name AS SubAccount_name,   PFL.roleId AS roleId,   PFL.role_name AS role_name,   PFL.role_defaultUserRole AS role_defaultUserRole,   COALESCE(PFL.profile_count, 0) AS profile_count,   PFR.roleId AS duplicate_roleId,   PFR.role_name AS duplicate_role_name,   PFR.role_defaultUserRole AS duplicate_role_defaultUserRole,   COALESCE(PFR.profile_count, 0) AS duplicate_profile_count FROM permission_fingerprints AS PFL LEFT JOIN `[PARAMETER].[PARAMETER].CM_Accounts` AS A on PFL.accountId=A.accountId LEFT JOIN `[PARAMETER].[PARAMETER].CM_SubAccounts` AS SA on PFL.subaccountId=SA.subaccountId LEFT JOIN permission_fingerprints AS PFR    ON PFL.permissions_fingerprint=PFR.permissions_fingerprint   AND PFL.accountId=PFR.accountId   AND COALESCE(PFL.subaccountId, 0)=COALESCE(PFR.subaccountId, 0) WHERE PFL.roleId != PFR.roleId ; ",
        'parameters': [
          {
            'field': {
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
              'name': 'project',
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
        ]
      },
      'to': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be written in BigQuery.'
          }
        },
        'view': 'Barnacle_Roles_Duplicates'
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('barnacle', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
