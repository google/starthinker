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
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source: 

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu	   
    l) Install All

--------------------------------------------------------------

Video Overlay

Add images, text, and audio to videos.

Provide either a sheet or a BigQuery table.
Each video edit will be read from the sheet or table.

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  'sheet': '',  # Name or URL of sheet.
  'tab': '',  # Name of sheet tab.
  'project': '',  # Google Cloud Project Identifier.
  'dataset': '',  # Name of dataset.
  'table': '',  # Name of table.
}

TASKS = [
  {
    'sheets': {
      '__comment__': 'Copy the tamplate sheet to the users sheet.  If it already exists, nothing happens.',
      'auth': 'user',
      'template': {
        'sheet': 'https://docs.google.com/spreadsheets/d/1BXRHWz-1P3gNS92WZy-3sPZslU8aalXa8heOgygWEFs/edit#gid=0',
        'tab': 'Video'
      },
      'sheet': {
        'field': {
          'name': 'sheet',
          'kind': 'string',
          'order': 1,
          'default': '',
          'description': 'Name or URL of sheet.'
        }
      },
      'tab': {
        'field': {
          'name': 'tab',
          'kind': 'string',
          'order': 2,
          'default': '',
          'description': 'Name of sheet tab.'
        }
      }
    }
  },
  {
    'video': {
      '__comment__': 'Read video effects and values from sheet and/or bigquery.',
      'auth': 'user',
      'sheets': {
        'sheet': {
          'field': {
            'name': 'sheet',
            'kind': 'string',
            'order': 1,
            'default': '',
            'description': 'Name or URL of sheet.'
          }
        },
        'tab': {
          'field': {
            'name': 'tab',
            'kind': 'string',
            'order': 2,
            'default': '',
            'description': 'Name of sheet tab.'
          }
        }
      },
      'bigquery': {
        'project': {
          'field': {
            'name': 'project',
            'kind': 'string',
            'order': 3,
            'default': '',
            'description': 'Google Cloud Project Identifier.'
          }
        },
        'dataset': {
          'field': {
            'name': 'dataset',
            'kind': 'string',
            'order': 4,
            'default': '',
            'description': 'Name of dataset.'
          }
        },
        'table': {
          'field': {
            'name': 'table',
            'kind': 'string',
            'order': 5,
            'default': '',
            'description': 'Name of table.'
          }
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('video', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
