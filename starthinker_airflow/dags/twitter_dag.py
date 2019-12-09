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
Twitter Targeting

Adjusts line item settings based on Twitter hashtags and locations specified in a sheet.

P
r
o
v
i
d
e
 
a
 
s
h
e
e
t
s
 
U
R
L
.
 
N
o
 
a
c
c
o
u
n
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
 
r
e
q
u
i
r
e
d
.


C
l
i
c
k
 
<
b
>
R
u
n
 
N
o
w
<
/
b
>
 
o
n
c
e
 
a
n
d
 
a
 
n
e
w
 
t
a
b
 
c
a
l
l
e
d
 
<
b
>
T
w
i
t
t
e
r
 
T
r
i
g
g
e
r
s
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
 
a
d
d
e
d
 
t
o
 
t
h
e
 
s
h
e
e
t
.


F
o
l
l
o
w
 
i
n
s
t
r
u
c
t
i
o
n
s
 
o
n
 
t
h
e
 
s
h
e
e
t
s
 
t
a
b
.


C
l
i
c
k
 
<
b
>
R
u
n
 
N
o
w
<
/
b
>
 
a
g
a
i
n
,
 
t
r
e
n
d
s
 
a
r
e
 
d
o
w
n
l
o
a
d
e
d
 
a
n
d
 
t
r
i
g
g
e
r
e
d


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
  'dataset': '',  # Place where tables will be created in BigQuery.
  'sheet_url': '',  # URL to sheet where Line Item settings will be read from.
  'twitter_secret': '',  # Twitter API secret token.
  'twitter_key': '',  # Twitter API key token.
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
    'sheets': {
      'description': 'Read mapping of hash tags to line item toggles from sheets.',
      'auth': 'user',
      'template': {
        'url': 'https://docs.google.com/spreadsheets/d/1iYCGa2NKOZiL2mdT4yiDfV_SWV9C7SUosXdIr4NAEXE/edit?usp=sharing',
        'tab': 'Twitter Triggers'
      },
      'sheet': {
        'field': {
          'name': 'sheet_url',
          'kind': 'string',
          'order': 2,
          'description': 'URL to sheet where Line Item settings will be read from.',
          'default': ''
        }
      },
      'tab': 'Twitter Triggers',
      'range': 'A8:T',
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          'table': 'Twitter_Triggers',
          'schema': [
            {
              'name': 'Location',
              'type': 'STRING',
              'mode': 'REQUIRED'
            },
            {
              'name': 'WOEID',
              'type': 'INTEGER',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Hashtag',
              'type': 'STRING',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Line_Item_Id',
              'type': 'INTEGER',
              'mode': 'REQUIRED'
            },
            {
              'name': 'Line_Item_Name',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Status',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Start_Date',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_End_Date',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Budget_Type',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Budget_Amount',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Pacing',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Pacing_Rate',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Pacing_Amount',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Frequency_Enabled',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Frequency_Exposures',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Frequency_Period',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Line_Item_Frequency_Amount',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Bid_Price',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Partner_Revenue_Model',
              'type': 'STRING',
              'mode': 'NULLABLE'
            },
            {
              'name': 'Partner_Revenue_Amount',
              'type': 'STRING',
              'mode': 'NULLABLE'
            }
          ]
        }
      }
    }
  },
  {
    'twitter': {
      'description': 'Read trends from Twitter and place into BigQuery.',
      'auth': 'service',
      'secret': {
        'field': {
          'name': 'twitter_secret',
          'kind': 'string',
          'order': 3,
          'default': '',
          'description': 'Twitter API secret token.'
        }
      },
      'key': {
        'field': {
          'name': 'twitter_key',
          'kind': 'string',
          'order': 4,
          'default': '',
          'description': 'Twitter API key token.'
        }
      },
      'trends': {
        'places': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'dataset',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            },
            'table': 'Twitter_Triggers',
            'columns': [
              'WOEID'
            ]
          }
        }
      },
      'out': {
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          'table': 'Twitter_Trends_Place'
        }
      }
    }
  },
  {
    'lineitem': {
      'description': 'Read current lineitem settings from DBM into BigQuery, so it can be joined with Twitter analysis.',
      'auth': 'user',
      'read': {
        'advertisers': [
        ],
        'insertionorders': [
        ],
        'lineitems': [
          9915840
        ],
        'out': {
          'bigquery': {
            'dataset': {
              'field': {
                'name': 'dataset',
                'kind': 'string',
                'description': 'Place where tables will be created in BigQuery.'
              }
            },
            'table': 'LineItem_Reads'
          }
        }
      }
    }
  },
  {
    'bigquery': {
      'description': 'Get all triggered lineitmes from sheet, if they have a keyword match in twitter, take the triger values, else take the default values (default>trigger).  Take all non-null values from trigger and overlay over current DBM values. Will be used to upload to DBM.',
      'auth': 'service',
      'from': {
        'query': "SELECT o.Line_Item_Id AS Line_Item_Id, o.Partner_Name AS Partner_Name, o.Partner_Id AS Partner_Id, o.Advertiser_Name AS Advertiser_Name, o.IO_Name AS IO_Name, IFNULL(t.Line_Item_Name, o.Line_Item_Name) AS Line_Item_Name, o.Line_Item_Timestamp AS Line_Item_Timestamp , IFNULL(t.Line_Item_Status, o.Line_Item_Status) AS Line_Item_Status, o.IO_Start_Date AS IO_Start_Date, o.IO_End_Date AS IO_End_Date, o.IO_Budget_Type AS IO_Budget_Type, o.IO_Budget_Amount AS IO_Budget_Amount, o.IO_Pacing AS IO_Pacing, o.IO_Pacing_Rate AS IO_Pacing_Rate, o.IO_Pacing_Amount AS IO_Pacing_Amount, IFNULL(t.Line_Item_Start_Date, o.Line_Item_Start_Date) AS Line_Item_Start_Date, IFNULL(t.Line_Item_End_Date, o.Line_Item_End_Date) AS Line_Item_End_Date, IFNULL(t.Line_Item_Budget_Type, o.Line_Item_Budget_Type) AS Line_Item_Budget_Type, IFNULL(t.Line_Item_Budget_Amount, o.Line_Item_Budget_Amount) AS Line_Item_Budget_Amount, IFNULL(t.Line_Item_Pacing, o.Line_Item_Pacing) AS Line_Item_Pacing, IFNULL(t.Line_Item_Pacing_Rate, o.Line_Item_Pacing_Rate) AS Line_Item_Pacing_Rate, IFNULL(t.Line_Item_Pacing_Amount, o.Line_Item_Pacing_Amount) AS Line_Item_Pacing_Amount, IFNULL(t.Line_Item_Frequency_Enabled, o.Line_Item_Frequency_Enabled) AS Line_Item_Frequency_Enabled, IFNULL(t.Line_Item_Frequency_Exposures, o.Line_Item_Frequency_Exposures) AS Line_Item_Frequency_Exposures, IFNULL(t.Line_Item_Frequency_Period, o.Line_Item_Frequency_Period) AS Line_Item_Frequency_Period, IFNULL(t.Line_Item_Frequency_Amount, o.Line_Item_Frequency_Amount) AS Line_Item_Frequency_Amount, IFNULL(t.Bid_Price, o.Bid_Price) AS Bid_Price, IFNULL(t.Partner_Revenue_Model, o.Partner_Revenue_Model) AS Partner_Revenue_Model, IFNULL(t.Partner_Revenue_Amount, o.Partner_Revenue_Amount) AS Partner_Revenue_Amount, o.Current_Audience_Targeting_Ids AS Current_Audience_Targeting_Ids , o.Current_Audience_Targeting_Names AS Current_Audience_Targeting_Names FROM `[PARAMETER].LineItem_Reads` AS o LEFT JOIN ( SELECT Line_Item_Id, ANY_VALUE(SPLIT(Line_Item_Name, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Name, ANY_VALUE(SPLIT(Line_Item_Status, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Status, ANY_VALUE(SPLIT(Line_Item_Start_Date, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Start_Date, ANY_VALUE(SPLIT(Line_Item_End_Date, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_End_Date, ANY_VALUE(SPLIT(Line_Item_Budget_Type, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Budget_Type, ANY_VALUE(CAST(SPLIT(Line_Item_Budget_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Line_Item_Budget_Amount, ANY_VALUE(SPLIT(Line_Item_Pacing, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Pacing, ANY_VALUE(SPLIT(Line_Item_Pacing_Rate, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Pacing_Rate, ANY_VALUE(CAST(SPLIT(Line_Item_Pacing_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Line_Item_Pacing_Amount, ANY_VALUE(CAST(SPLIT(Line_Item_Frequency_Enabled, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS BOOL)) AS Line_Item_Frequency_Enabled, ANY_VALUE(SPLIT(Line_Item_Frequency_Exposures, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Frequency_Exposures, ANY_VALUE(SPLIT(Line_Item_Frequency_Period, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Line_Item_Frequency_Period, ANY_VALUE(CAST(SPLIT(Line_Item_Frequency_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS INT64)) AS Line_Item_Frequency_Amount, ANY_VALUE(CAST(SPLIT(Bid_Price, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Bid_Price, ANY_VALUE(SPLIT(Partner_Revenue_Model, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))]) AS Partner_Revenue_Model, ANY_VALUE(CAST(SPLIT(Partner_Revenue_Amount, '>')[SAFE_OFFSET(IF(Triggered, 1, 0))] AS FLOAT64)) AS Partner_Revenue_Amount FROM ( SELECT WOEID, Hashtag, Line_Item_Id, Line_Item_Name, Line_Item_Status, Line_Item_Start_Date, Line_Item_End_Date, Line_Item_Budget_Type, Line_Item_Budget_Amount, Line_Item_Pacing, Line_Item_Pacing_Rate, Line_Item_Pacing_Amount, Line_Item_Frequency_Enabled, Line_Item_Frequency_Exposures, Line_Item_Frequency_Period, Line_Item_Frequency_Amount, Bid_Price, Partner_Revenue_Model, Partner_Revenue_Amount, CONCAT(CAST(WOEID AS STRING), LOWER(Hashtag)) IN (SELECT CONCAT(CAST(WOEID AS STRING), LOWER(REPLACE(name, '#', ''))) FROM `[PARAMETER].Twitter_Trends_Place` GROUP BY 1) AS Triggered FROM `[PARAMETER].Twitter_Triggers`) GROUP BY 1) AS t ON o.Line_Item_Id=t.Line_Item_Id;",
        'parameters': [
          {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          {
            'field': {
              'name': 'dataset',
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
            'name': 'dataset',
            'kind': 'string',
            'description': 'Place where tables will be created in BigQuery.'
          }
        },
        'view': 'LineItem_Writes'
      }
    }
  },
  {
    'lineitem': {
      'description': 'Write lineitem settings to DBM after transformation.',
      'auth': 'user',
      'write': {
        'dry_run': False,
        'bigquery': {
          'dataset': {
            'field': {
              'name': 'dataset',
              'kind': 'string',
              'description': 'Place where tables will be created in BigQuery.'
            }
          },
          'table': 'LineItem_Writes'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('twitter', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
