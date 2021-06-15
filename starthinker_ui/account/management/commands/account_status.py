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

import json
import pprint
from time import sleep
from datetime import datetime
from random import sample

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from starthinker.util.configuration import Configuration
from starthinker.util.email import send_email
from starthinker.util.email.template import EmailTemplate
from starthinker_ui.account.models import Account
from starthinker_ui.recipe.scripts import Script
#from starthinker_ui.storage.models import storage_list
from starthinker_ui.website.templatetags.website_app import mailto

EMAIL_FROM = 'starthinker@google.com'
EMAIL_CC = ''
EMAIL_SUBJECT = 'StarThinker Status Update'
EMAIL_PARAGRAPH = ('Here is your weekly job status summary.  StarThinker is '
                   'sending you this report because you have jobs running in '
                   'the system.')

HELP_LINKS = [
    {
        'name':
            'Solution Gallery',
        'description':
            'A list of available solutions you can deploy for clients, their '
            'impact, and deployment instructions.',
        'button': {
            'text': 'go/starthinker-solutions',
            'link': 'go/starthinker-solutions',
        }
    },
    {
        'name':
            'How To Tutorial',
        'description':
            'Slides that show how to use StarThinker to creat recipes and run '
            'solutions.  Includes both technical and point and click examples '
            'for CSE / TS / PAS / Sales.',
        'button': {
            'text': 'go/starthinker-howto',
            'link': 'go/starthinker-howto',
        }
    },
    {
        'name':
            'Feature Requests And Bugs',
        'description':
            'Submit feature requests and help us track down bugs and improve '
            'the tool for the whole team.',
        'button': {
            'text': 'go/starthinker-bugs',
            'link': 'go/starthinker-bugs',
        }
    },
    {
        'name':
            'Technical Documentation',
        'description':
            'The Product Requirements Document has everything you need to '
            'leverage the StarThinker library for the next solution sprint.',
        'button': {
            'text': 'go/starthinker-prd',
            'link': 'go/starthinker-prd',
        }
    },
]

RECIPE_SCHEMA = [
    {
        'name': 'Recipe',
        'type': 'STRING'
    },
    {
        'name': 'Status',
        'type': 'STRING'
    },
    {
        'name': 'Last Run',
        'type': 'STRING'
    },
    {
        'name': 'Link',
        'type': 'STRING'
    },
]

IMPACT_SCHEMA = [
    {
        'name': 'Impact',
        'type': 'STRING'
    },
    {
        'name': 'Level',
        'type': 'INTEGER'
    },
]

DETAILS_SCHEMA = [
    {
        'name': 'Detail',
        'type': 'STRING'
    },
    {
        'name': 'Information',
        'type': 'INTEGER'
    },
]


class Command(BaseCommand):
  help = 'Send email status to users'

  def add_arguments(self, parser):
    parser.add_argument(
        '--email',
        action='store',
        dest='email',
        default=None,
        help='Run a specific email.',
    )

    parser.add_argument(
        '--test',
        action='store_true',
        dest='test',
        default=False,
        help='Test print emails.',
    )

  def handle(self, *args, **kwargs):

    # loop through accounts
    for account in Account.objects.all():
      # if account is given only do that one
      if kwargs['email'] is None or account.email == kwargs['email']:
        print('CHECKING: ', account.email)

        status = False

        # start an email template
        email = EmailTemplate()
        email.segment_next()
        email.greeting(account.name)
        email.paragraph(EMAIL_PARAGRAPH)

        # loop through recipes
        rows = []
        for recipe in account.recipe_set.all():
          log = recipe.get_log()
          rows.append([
              recipe.name,
              log.get('status'),
              log.get('ago'),
              'http://starthinker.corp.google.com/recipe/edit/%d/' % recipe.pk
          ])

        if rows:
          email.segment_next()
          email.header('Recipe Status')
          email.table(RECIPE_SCHEMA, rows)
          status = True

        # loop through storage
        #rows = []
        #for recipe in storage_list(account):
        #  recipe.log = logs.get(recipe.uid(), {})
        #  rows.append([recipe.name, recipe.log.get('status'), recipe.log.get('time_ago'), recipe.link_storage])

        if rows:
          email.segment_next()
          email.header('Storage Status')
          email.table(RECIPE_SCHEMA, rows)
          status = True

          #        # if at least one solution or recipe is running....
          #        if status:
          #
          #          # show one random recipe
          #          email.segment_next()
          #          email.header('Featured Recipes')
          #          email.paragraph('Each week we feature three recipes that could help your client or agency project.  This weeks featured recipe is...')
          #
          #          # script: card ( fetch random )
          #          for s in sample(list(Script.get_scripts()), 3):
          #            email.header(s.get_name())
          #            email.paragraph(s.get_description())
          #
          #            # solution pitch
          #            email.paragraph('Benefits', bold=True)
          #            email.list(s.get_pitches())
          #
          #            # solution impact
          #            email.table(IMPACT_SCHEMA, [(i[0], '%d%%' % i[1]) for i in s.get_impacts().items()])
          #
          #            email.table(DETAILS_SCHEMA, [
          #              ('Requires', ', '.join([r[0] for r in s.get_requirements().items() if r[1]])),
          #              ('Categories', ', '.join(s.get_categories())),
          #              ('Authors', mailto(s.get_authors()))
          #            ])
          #
          #            email.button('Launch %s' % s.get_name(), '%s/client/edit/' % settings.CONST_URL, big=True)
          #
          #            if s.get_open_source():
          #              email.button('Avaliable As Open Source', s.get_open_source(), big=True)
          #
          #          # loop through links
          #          email.segment_next()
          #          email.header('Helpful Links')
          #          email.paragraph('Reduce solution delivery to minutes and create custom solutions that exceed clients expectations with these helpful guides and tips.')
          for h in HELP_LINKS:
            email.section(h['name'], h['description'], None,
                          h['button']['link'], h['button']['text'])

          if kwargs['test']:
            # write to STDOUT
            print(email.get_html())
          else:
            print('EMAILING: ', account.email)
            # send message via email
            send_email(Configuration(user=account.get_credentials_path()), 'user', account.email, EMAIL_FROM, EMAIL_CC,
                       EMAIL_SUBJECT, email.get_text(), email.get_html())
            sleep(3)
