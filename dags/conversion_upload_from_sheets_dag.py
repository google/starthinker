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

Conversion Upload Sheets

Move form Sheets to CM.

Specify a CM Account ID, Floodligh Activity ID and Conversion Type.
Include Sheets url, tab, and range, omit headers in range.
Columns: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId
Include encryption information if using encryptedUserId or encryptedUserIdCandidates.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'dcm_account': '',
  'auth_read': 'user',  # Credentials used for reading data.
  'floodlight_activity_id': '',
  'floodlight_conversion_type': 'encryptedUserId',
  'encryption_entity_id': '',
  'encryption_entity_type': 'DCM_ACCOUNT',
  'encryption_entity_source': 'DATA_TRANSFER',
  'sheet_url': '',
  'sheet_tab': '',
  'sheet_range': '',
}

TASKS = [
  {
    'conversion_upload': {
      'encryptionInfo': {
        'encryptionEntityType': {
          'field': {
            'choices': [
              'ADWORDS_CUSTOMER',
              'DBM_ADVERTISER',
              'DBM_PARTNER',
              'DCM_ACCOUNT',
              'DCM_ADVERTISER',
              'ENCRYPTION_ENTITY_TYPE_UNKNOWN'
            ],
            'order': 4,
            'name': 'encryption_entity_type',
            'default': 'DCM_ACCOUNT',
            'kind': 'choice'
          }
        },
        'encryptionEntityId': {
          'field': {
            'order': 3,
            'name': 'encryption_entity_id',
            'default': '',
            'kind': 'integer'
          }
        },
        'encryptionSource': {
          'field': {
            'choices': [
              'AD_SERVING',
              'DATA_TRANSFER',
              'ENCRYPTION_SCOPE_UNKNOWN'
            ],
            'order': 5,
            'name': 'encryption_entity_source',
            'default': 'DATA_TRANSFER',
            'kind': 'choice'
          }
        }
      },
      'sheets': {
        'url': {
          'field': {
            'order': 9,
            'name': 'sheet_url',
            'default': '',
            'kind': 'string'
          }
        },
        'tab': {
          'field': {
            'order': 10,
            'name': 'sheet_tab',
            'default': '',
            'kind': 'string'
          }
        },
        'range': {
          'field': {
            'order': 11,
            'name': 'sheet_range',
            'default': '',
            'kind': 'string'
          }
        }
      },
      'auth': {
        'field': {
          'description': 'Credentials used for reading data.',
          'kind': 'authentication',
          'name': 'auth_read',
          'order': 1,
          'default': 'user'
        }
      },
      'activity_id': {
        'field': {
          'order': 1,
          'name': 'floodlight_activity_id',
          'default': '',
          'kind': 'integer'
        }
      },
      'account_id': {
        'field': {
          'order': 0,
          'name': 'dcm_account',
          'default': '',
          'kind': 'string'
        }
      },
      'conversion_type': {
        'field': {
          'choices': [
            'encryptedUserId',
            'encryptedUserIdCandidates',
            'gclid',
            'mobileDeviceId'
          ],
          'order': 2,
          'name': 'floodlight_conversion_type',
          'default': 'encryptedUserId',
          'kind': 'choice'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('conversion_upload_from_sheets', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
