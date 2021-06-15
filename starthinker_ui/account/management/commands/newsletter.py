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
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from starthinker.util.configuration import Configuration
from starthinker.util.email import send_email
from starthinker.util.email.template import EmailTemplate
from starthinker_ui.account.models import Account
"""python starthinker_ui/manage.py newsletter --from kenjora@google.com --template starthinker/task/newsletter/internal/2019_12_03.json --to kenjora@google.com"""


class Command(BaseCommand):
  help = 'Send email status to users'

  def add_arguments(self, parser):
    parser.add_argument(
        '--template',
        action='store',
        dest='template',
        help='Template to use for email construction.',
    )

    parser.add_argument(
        '--from',
        action='store',
        dest='email_from',
        help='Email to send from ( must match an account).',
    )

    parser.add_argument(
        '--to',
        action='store',
        dest='email_to',
        default=None,
        help='Email to send to ( if not givem sends to all ).',
    )

    parser.add_argument(
        '--ignore',
        action='store',
        nargs='+',
        dest='ignore',
        default=[],
        help='Email to send to ( if not givem sends to all ).',
    )

    parser.add_argument(
        '--test',
        action='store_true',
        dest='test',
        default=False,
        help='Test print emails instead of sending them.',
    )

  def handle(self, *args, **kwargs):

    user = None
    accounts = Account.objects.all()

    # find user to send from
    for account in accounts:
      if account.email == kwargs['email_from']:
        user = account.get_credentials_path()

    if user:
      print('SEND USER FOUND')

      # load template
      with open(kwargs['template'], 'r') as json_file:
        email = EmailTemplate(json.load(json_file))

      # loop through accounts
      for account in accounts:
        # if account is given only do that one
        if kwargs['email_to'] is None or account.email == kwargs['email_to']:
          if account.email in kwargs['ignore']:
            print('IGNORING: ', account.email)
          else:
            print('EMAILING: ', account.email)

            if kwargs['test']:
              # write to STDOUT
              print(email.get_html())
            else:
              # send message via email
              send_email(Configuration(user=user), 'user', account.email, kwargs['email_from'], None,
                         email.get_subject(), email.get_text(),
                         email.get_html())
              sleep(1)
