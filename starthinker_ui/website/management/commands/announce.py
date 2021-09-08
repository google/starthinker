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

from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from starthinker.util.email import send_email
from starthinker.util.email.template import EmailTemplate
from starthinker_ui.recipe.scripts import Script


class Command(BaseCommand):
  help = 'Generate Newsletter Of New Solutions'

  def add_arguments(self, parser):
    parser.add_argument(
        '--days',
        action='store',
        dest='days',
        default=90,
        type=int,
        help='Number of days to go back for recipes.',
    )

  def handle(self, *args, **kwargs):
    day = date.today() - timedelta(days=kwargs['days'])

    email = {
        'subject':
            'Announcing Six New Open Source Modules For Ecosystems',
        'style': {
            'background': '#f2f2f2',
            'foreground': '#ffffff',
            'text': '#414347',
            'link': '#4285f4',
            'font': 'Roboto, Helvetica, Arial sans-serif;',
            'align': 'left'
        },
        'logo':
            'https://storage.googleapis.com/starthinker-ui/gTech_StarThinker.png',
        'body': {
            'sections': [{
                'header':
                    'Six New Solutions For Partners To Build New Services',
                'paragraph':
                    'In Q1, StarThinker released 6 new building blocks '
                    'available as Python, Airflow, Colab, and no-coding UI.  '
                    'These building blocks are now open sourve and availbale '
                    'for deployment by Partners.  Below is a description of '
                    'each solution and possible service or efficiency gain by '
                    'partners.',
                'grid': []
            }]
        },
        'footer': [{
            'text': 'Internal UI',
            'link': 'http://go/starthinker'
        }, {
            'text': 'GitHub Solution Gallery',
            'link': 'https://google.github.io/starthinker/'
        }, {
            'text': 'Google3 Repository',
            'link': 'http://go/starthinker-google3'
        }, {
            'text': 'GOB Repository ( Official )',
            'link': 'http://go/starthinker-code'
        }, {
            'text': 'GitHub Repository',
            'link': 'https://github.com/google/starthinker'
        }],
        'copyright':
            'Copyright 2020 Google LLC'
    }

    odd = True
    for s in Script.get_scripts():
      if s.get_released() < day:
        continue
      print('SCRIPT: ', s.get_tag())

      if not s.get_image():
        continue

      row = [{
          'image': {
              'src': s.get_image(),
              'link': s.get_link_client()
          }
      }, {
          'header': '[%s](%s)' % (s.get_name(), s.get_link_client()),
          'paragraph': s.get_description()
      }]
      email['body']['sections'][0]['grid'].append(row)

      if odd:
        row.reverse()
      odd = not odd

    email = EmailTemplate(email)

    # send or print
    #if project.args.email_to and project.args.email_from:
    #  print('EMAILING: ', project.args.email_to)
    #  send_email('user', project.args.email_to, project.args.email_from, None, email.get_subject(), email.get_text(), email.get_html())
    #else:
    if 1:
      # write to STDOUT
      print(email.get_html())
      print('<pre style="width:600px;margin:0px auto;">%s</pre>' %
            email.get_text())
