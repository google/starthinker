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

Federal Reserve Series Data

Download federal reserve series.

Specify the values for a <a href='https://fred.stlouisfed.org/docs/api/fred/series_observations.html' target='_blank'>Fred observations API call</a>.
A table will appear in the dataset.

'''

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = "starthinker_user" # The connection to use for user authentication.
GCP_CONN_ID = "starthinker_service" # The connection to use for service authentication.

INPUTS = {
  'auth': 'service',  # Credentials used for writing data.
  'fred_api_key': '',  # 32 character alpha-numeric lowercase string.
  'fred_series_id': '',  # Series ID to pull data from.
  'fred_units': 'lin',  # A key that indicates a data value transformation.
  'fred_frequency': '',  # An optional parameter that indicates a lower frequency to aggregate values to.
  'fred_aggregation_method': 'avg',  # A key that indicates the aggregation method used for frequency aggregation.
  'project': '',  # Existing BigQuery project.
  'dataset': '',  # Existing BigQuery dataset.
}

TASKS = [
  {
    'fred': {
      'out': {
        'bigquery': {
          'project': {
            'field': {
              'order': 10,
              'kind': 'string',
              'name': 'project',
              'description': 'Existing BigQuery project.',
              'default': ''
            }
          },
          'dataset': {
            'field': {
              'order': 11,
              'kind': 'string',
              'name': 'dataset',
              'description': 'Existing BigQuery dataset.',
              'default': ''
            }
          }
        }
      },
      'series': [
        {
          'series_id': {
            'field': {
              'order': 2,
              'kind': 'string',
              'name': 'fred_series_id',
              'description': 'Series ID to pull data from.',
              'default': ''
            }
          },
          'units': {
            'field': {
              'description': 'A key that indicates a data value transformation.',
              'choices': [
                'lin',
                'chg',
                'ch1',
                'pch',
                'pc1',
                'pca',
                'cch',
                'cca',
                'log'
              ],
              'order': 3,
              'kind': 'choice',
              'name': 'fred_units',
              'default': 'lin'
            }
          },
          'aggregation_method': {
            'field': {
              'description': 'A key that indicates the aggregation method used for frequency aggregation.',
              'choices': [
                'avg',
                'sum',
                'eop'
              ],
              'order': 5,
              'kind': 'choice',
              'name': 'fred_aggregation_method',
              'default': 'avg'
            }
          }
        }
      ],
      'frequency': {
        'field': {
          'description': 'An optional parameter that indicates a lower frequency to aggregate values to.',
          'choices': [
            '',
            'd',
            'w',
            'bw',
            'm',
            'q',
            'sa',
            'a',
            'wef',
            'weth',
            'wew',
            'wetu',
            'wem',
            'wesu',
            'wesa',
            'bwew',
            'bwem'
          ],
          'order': 4,
          'kind': 'choice',
          'name': 'fred_frequency',
          'default': ''
        }
      },
      'api_key': {
        'field': {
          'order': 1,
          'kind': 'string',
          'name': 'fred_api_key',
          'description': '32 character alpha-numeric lowercase string.',
          'default': ''
        }
      },
      'auth': {
        'field': {
          'order': 0,
          'kind': 'authentication',
          'name': 'auth',
          'description': 'Credentials used for writing data.',
          'default': 'service'
        }
      }
    }
  }
]

DAG_FACTORY = DAG_Factory('fred_series_to_bigquery', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
