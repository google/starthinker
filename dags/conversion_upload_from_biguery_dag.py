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

Conversion Upload BigQuery

Move from BigQuery to CM.

Specify a CM Account ID, Floodligh Activity ID and Conversion Type.
Include BigQuery dataset and table.
Columns: Ordinal, timestampMicros, encryptedUserId | encryptedUserIdCandidates | gclid | mobileDeviceId
Include encryption information if using encryptedUserId or encryptedUserIdCandidates.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'account': '',
  'auth_read': 'user',  # Credentials used for reading data.
  'floodlight_activity_id': '',
  'floodlight_conversion_type': 'encryptedUserId',
  'encryption_entity_id': '',
  'encryption_entity_type': 'DCM_ACCOUNT',
  'encryption_entity_source': 'DATA_TRANSFER',
  'bigquery_dataset': '',
  'bigquery_table': '',
  'bigquery_legacy': True,
}

TASKS = [
  {
    'conversion_upload': {
      'activity_id': {
        'field': {
          'order': 1,
          'kind': 'integer',
          'name': 'floodlight_activity_id',
          'default': ''
        }
      },
      'account_id': {
        'field': {
          'order': 0,
          'kind': 'string',
          'name': 'account',
          'default': ''
        }
      },
      'bigquery': {
        'table': {
          'field': {
            'order': 7,
            'kind': 'string',
            'name': 'bigquery_table',
            'default': ''
          }
        },
        'legacy': {
          'field': {
            'order': 8,
            'kind': 'boolean',
            'name': 'bigquery_legacy',
            'default': True
          }
        },
        'dataset': {
          'field': {
            'order': 6,
            'kind': 'string',
            'name': 'bigquery_dataset',
            'default': ''
          }
        }
      },
      'auth': {
        'field': {
          'order': 1,
          'kind': 'authentication',
          'name': 'auth_read',
          'description': 'Credentials used for reading data.',
          'default': 'user'
        }
      },
      'encryptionInfo': {
        'encryptionSource': {
          'field': {
            'order': 5,
            'kind': 'choice',
            'name': 'encryption_entity_source',
            'default': 'DATA_TRANSFER',
            'choices': [
              'AD_SERVING',
              'DATA_TRANSFER',
              'ENCRYPTION_SCOPE_UNKNOWN'
            ]
          }
        },
        'encryptionEntityId': {
          'field': {
            'order': 3,
            'kind': 'integer',
            'name': 'encryption_entity_id',
            'default': ''
          }
        },
        'encryptionEntityType': {
          'field': {
            'order': 4,
            'kind': 'choice',
            'name': 'encryption_entity_type',
            'default': 'DCM_ACCOUNT',
            'choices': [
              'ADWORDS_CUSTOMER',
              'DBM_ADVERTISER',
              'DBM_PARTNER',
              'DCM_ACCOUNT',
              'DCM_ADVERTISER',
              'ENCRYPTION_ENTITY_TYPE_UNKNOWN'
            ]
          }
        }
      },
      'conversion_type': {
        'field': {
          'order': 2,
          'kind': 'choice',
          'name': 'floodlight_conversion_type',
          'default': 'encryptedUserId',
          'choices': [
            'encryptedUserId',
            'encryptedUserIdCandidates',
            'gclid',
            'mobileDeviceId'
          ]
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('conversion_upload_from_biguery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
