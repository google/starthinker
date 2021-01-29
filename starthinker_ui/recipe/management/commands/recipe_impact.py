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

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker.util.project import project
from starthinker.util.dbm import report_get as dbm_report_get
from starthinker.util.bigquery import rows_to_table, query_to_table, query_to_rows, table_exists

from starthinker_ui.account.models import Account
from starthinker_ui.recipe.models import Recipe


def account_from_dt(values):
  print('account_from_dt', values)
  return int(values['bucket'].replace('dcdt_-dcm_account', '').split('_', 1)[0])


def account_from_dbm_report(report_id, report_name):
  print('account_from_dbm_report', report_id, report_name)

  partners = []

  if report_id or report_name:
    try:
      report = dbm_report_get('user', report_id, report_name)
    except Exception as e:
      print(e, report_id, report_name)
      report = None

    if report:
      for filter in report['params']['filters']:
        if filter['type'] == 'FILTER_PARTNER':
          partners.append(filter['value'])

  return partners


class Command(BaseCommand):
  help = 'Prints recipe acounts.'

  def add_arguments(self, parser):
    parser.add_argument(
        '--recipes',
        action='store',
        dest='recipes',
        type=int,
        default=3,
        help='Number of recipes to pull at one time.',
    )

    parser.add_argument(
        '--test',
        action='store_true',
        dest='test',
        default=False,
        help='Test print rows instead of writing them.',
    )

  def handle(self, *args, **kwargs):

    impact = [
    ]  #{ 'day': DATE, 'deployment':INT, 'account': INT, 'product': STRING, 'recipe': STRING, 'user': STRING }
    missing = {}
    id_max = 0

    project.initialize(_service=settings.UI_SERVICE, _verbose=True)

    if table_exists('service', 'google.com:starthinker', 'dashboard',
                    'ST_Scripts'):
      id_max = next(
          query_to_rows(
              'service',
              'google.com:starthinker',
              'dashboard',
              'SELECT MAX(Deployment) FROM ST_Scripts',
              legacy=False))[0]

    for recipe in Recipe.objects.filter(
        id__gt=id_max).order_by('id')[:kwargs['recipes']]:

      project.initialize(
          _user=recipe.account.get_credentials_path(),
          _service=settings.UI_SERVICE,
          _verbose=True)

      values = recipe.get_values()
      for v in values:
        if v['tag'] in ('dcm_to_bigquery', 'dcm_to_sheets', 'dcm_to_storage',
                        'dcm_run', 'conversion_upload_from_bigquery',
                        'conversion_upload_from_sheets'):
          impact.append({
              'day': recipe.birthday,
              'deployment': recipe.id,
              'account': v['values'].get('account'),
              'script': v['tag'],
              'product': 'dcm',
              'user': recipe.account.email.replace('@google.com', '')
          })
        elif v['tag'] in ('dbm_to_bigquery', 'dbm_to_sheets', 'dbm_to_storage'):
          for partner in account_from_dbm_report(
              v['values'].get('dbm_report_id'),
              v['values'].get('dbm_report_name')):
            impact.append({
                'day': recipe.birthday,
                'deployment': recipe.id,
                'account': partner,
                'script': v['tag'],
                'product': 'dbm',
                'user': recipe.account.email.replace('@google.com', '')
            })
        elif v['tag'] in ('dt',):
          impact.append({
              'day': recipe.birthday,
              'deployment': recipe.id,
              'account': account_from_dt(v['values']),
              'script': v['tag'],
              'product': 'dcm',
              'user': recipe.account.email.replace('@google.com', '')
          })
        elif v['tag'] == 'barnacle':
          for account in v['values']['accounts']:
            impact.append({
                'day': recipe.birthday,
                'deployment': recipe.id,
                'account': account,
                'script': v['tag'],
                'product': 'dcm',
                'user': recipe.account.email.replace('@google.com', '')
            })
        elif v['tag'] in ('entity',):
          for partner in v['values']['partners']:
            impact.append({
                'day': recipe.birthday,
                'deployment': recipe.id,
                'account': partner,
                'script': v['tag'],
                'product': 'dbm',
                'user': recipe.account.email.replace('@google.com', '')
            })
        elif v['tag'] == 'itp':
          impact.append({
              'day': recipe.birthday,
              'deployment': recipe.id,
              'account': v['values']['dcm_account'],
              'script': v['tag'],
              'product': 'dcm',
              'user': recipe.account.email.replace('@google.com', '')
          })
          impact.append({
              'day': recipe.birthday,
              'deployment': recipe.id,
              'account': v['values']['dbm_partner'],
              'script': v['tag'],
              'product': 'dbm',
              'user': recipe.account.email.replace('@google.com', '')
          })
        elif v['tag'] == 'itp_audit':
          impact.append({
              'day': recipe.birthday,
              'deployment': recipe.id,
              'account': v['values']['cm_account_id'],
              'script': v['tag'],
              'product': 'dcm',
              'user': recipe.account.email.replace('@google.com', '')
          })
          for partner in account_from_dbm_report(
              None, v['values'].get('dv360_report_name')):
            impact.append({
                'day': recipe.birthday,
                'deployment': recipe.id,
                'account': partner,
                'script': v['tag'],
                'product': 'dbm',
                'user': recipe.account.email.replace('@google.com', '')
            })
        else:
          impact.append({
              'day': recipe.birthday,
              'deployment': recipe.id,
              'account': None,
              'script': v['tag'],
              'product': None,
              'user': recipe.account.email.replace('@google.com', '')
          })
          missing.setdefault(v['tag'], 0)
          missing[v['tag']] += 1

    if impact:
      if kwargs['test']:
        print(impact)
      else:

        print('WRITING TO ST_Scripts')
        rows_to_table(
            'service',
            'google.com:starthinker',
            'dashboard',
            'ST_Scripts', [(i['day'], i['deployment'], i['user'], i['product'],
                            i['script'], i['account']) for i in impact],
            schema=[
                {
                    'mode': 'REQUIRED',
                    'name': 'Day',
                    'type': 'Date'
                },
                {
                    'mode': 'REQUIRED',
                    'name': 'Deployment',
                    'type': 'INTEGER'
                },
                {
                    'mode': 'REQUIRED',
                    'name': 'User',
                    'type': 'STRING'
                },
                {
                    'mode': 'NULLABLE',
                    'name': 'Product',
                    'type': 'STRING'
                },
                {
                    'mode': 'NULLABLE',
                    'name': 'Recipe',
                    'type': 'STRING'
                },
                {
                    'mode': 'NULLABLE',
                    'name': 'Account',
                    'type': 'INTEGER'
                },
            ],
            skip_rows=0,
            disposition='WRITE_TRUNCATE' if id_max == 0 else 'WRITE_APPEND',
            wait=True)

      print('MISSING', missing)
      print('Coverage:', (len(impact) * 100) / (len(missing) + len(impact)))
    else:
      print('No recipes newer than:', id_max)
