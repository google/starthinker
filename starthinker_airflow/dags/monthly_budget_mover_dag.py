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
Monthly Budget Mover

Apply the previous month's budget/spend delta to the current month.  Aggregate up the budget and spend from the previous month of each category declared then apply the delta of the spend and budget equally to each Line Item under that Category.

N
o
 
c
h
a
n
g
e
s
 
m
a
d
e
 
c
a
n
 
b
e
 
m
a
d
e
 
i
n
 
D
V
3
6
0
 
f
r
o
m
 
t
h
e
 
s
t
a
r
t
 
t
o
 
t
h
e
 
e
n
d
 
o
f
 
t
h
i
s
 
p
r
o
c
e
s
s


M
a
k
e
 
s
u
r
e
 
t
h
e
r
e
 
i
s
 
b
u
d
g
e
t
 
i
n
f
o
r
m
a
t
i
o
n
 
f
o
r
 
t
h
e
 
c
u
r
r
e
n
t
 
a
n
d
 
p
r
e
v
i
o
u
s
 
m
o
n
t
h
'
s
 
I
O
s
 
i
n
 
D
V
3
6
0


M
a
k
e
 
s
u
r
e
 
t
h
e
 
p
r
o
v
i
d
e
d
 
s
p
e
n
d
 
r
e
p
o
r
t
 
h
a
s
 
s
p
e
n
d
 
d
a
t
a
 
f
o
r
 
e
v
e
r
y
 
I
O
 
i
n
 
t
h
e
 
p
r
e
v
i
o
u
s
 
m
o
n
t
h


S
p
e
n
d
 
r
e
p
o
r
t
 
m
u
s
t
 
c
o
n
t
a
i
n
 
'
R
e
v
e
n
u
e
 
(
A
d
v
 
C
u
r
r
e
n
c
y
)
'
 
a
n
d
 
'
I
n
s
e
r
t
i
o
n
 
O
r
d
e
r
 
I
D
'


T
h
e
r
e
 
a
r
e
 
n
o
 
d
u
p
l
i
c
a
t
e
 
I
O
 
I
d
s
 
i
n
 
t
h
e
 
c
a
t
e
g
o
r
i
e
s
 
o
u
t
l
i
n
e
d
 
b
e
l
o
w


T
h
i
s
 
p
r
o
c
e
s
s
 
m
u
s
t
 
b
e
 
r
a
n
 
d
u
r
i
n
g
 
t
h
e
 
m
o
n
t
h
 
o
f
 
t
h
e
 
b
u
d
g
e
t
 
i
t
 
i
s
 
u
p
d
a
t
i
n
g


I
f
 
y
o
u
 
r
e
c
e
i
v
e
 
a
 
5
0
2
 
e
r
r
o
r
 
t
h
e
n
 
y
o
u
 
m
u
s
t
 
s
e
p
a
r
a
t
e
 
y
o
u
r
 
j
o
b
s
 
i
n
t
o
 
t
w
o
,
 
b
e
c
a
u
s
e
 
t
h
e
r
e
 
i
s
 
t
o
o
 
m
u
c
h
 
i
n
f
o
r
m
a
t
i
o
n
 
b
e
i
n
g
 
p
u
l
l
e
d
 
i
n
 
t
h
e
 
s
d
f


M
a
n
u
a
l
l
y
 
r
u
n
 
t
h
i
s
 
j
o
b


O
n
c
e
 
t
h
e
 
j
o
b
 
h
a
s
 
c
o
m
p
l
e
t
e
d
 
g
o
 
t
o
 
t
h
e
 
t
a
b
l
e
 
f
o
r
 
t
h
e
 
n
e
w
 
s
d
f
 
a
n
d
 
e
x
p
o
r
t
 
t
o
 
a
 
c
s
v


T
a
k
e
 
t
h
e
 
n
e
w
 
s
d
f
 
a
n
d
 
u
p
l
o
a
d
 
i
t
 
i
n
t
o
 
D
V
3
6
0

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'recipe_name': '',  # 
  'spend_report_id': '',  # The report Id for the DV360 spend report.
  'budget_categories': '{"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',  # A dictionary to show which IO Ids go under which Category. Please view the solutions page for information on format.
  'excluded_ios': '',  # A comma separated list of Inserion Order Ids that should be exluded from the budget calculations
  'filter_type': '',  # The filter type for the filter ids.
  'filter_ids': '',  # The filter ids for the request.
  'dataset': '',  # Dataset that you would like your output tables to be produced in.
}

TASKS = [
  {
    'dataset': {
      'description': 'Create a dataset where data will be combined and transfored for upload.',
      'auth': 'service',
      'dataset': {
        'field': {
          'name': 'dataset',
          'kind': 'string',
          'order': 1,
          'description': 'Place where tables will be created in BigQuery.'
        }
      }
    }
  },
  {
    'monthly_budget_mover': {
      'auth': 'user',
      'spend_report_id': {
        'field': {
          'name': 'spend_report_id',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'The report Id for the DV360 spend report.'
        }
      },
      'budget_categories': {
        'field': {
          'name': 'budget_categories',
          'kind': 'json',
          'order': 3,
          'default': '{"CATEGORY1":[12345,12345,12345], "CATEGORY2":[12345,12345]}',
          'description': 'A dictionary to show which IO Ids go under which Category. Please view the solutions page for information on format.'
        }
      },
      'excluded_ios': {
        'field': {
          'name': 'excluded_ios',
          'kind': 'integer_list',
          'order': 4,
          'description': 'A comma separated list of Inserion Order Ids that should be exluded from the budget calculations'
        }
      },
      'sdf': {
        'auth': 'user',
        'file_types': 'INSERTION_ORDER',
        'filter_type': {
          'field': {
            'name': 'filter_type',
            'kind': 'choice',
            'order': 6,
            'default': '',
            'description': 'The filter type for the filter ids.',
            'choices': [
              'ADVERTISER_ID',
              'CAMPAIGN_ID',
              'INSERTION_ORDER_ID',
              'INVENTORY_SOURCE_ID',
              'LINE_ITEM_ID',
              'PARTNER_ID'
            ]
          }
        },
        'filter_ids': {
          'field': {
            'name': 'filter_ids',
            'kind': 'integer_list',
            'order': 7,
            'default': '',
            'description': 'The filter ids for the request.'
          }
        }
      },
      'out': {
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 8,
            'default': '',
            'description': 'Dataset that you would like your output tables to be produced in.'
          }
        },
        'old_sdf_table_name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'SDF_OLD_',
            'description': ''
          }
        },
        'new_sdf_table_name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'SDF_NEW_',
            'description': ''
          }
        },
        'changes_table_name': {
          'field': {
            'name': 'recipe_name',
            'kind': 'string',
            'prefix': 'SDF_BUDGET_MOVER_LOG_',
            'description': ''
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('monthly_budget_mover', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
