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
import argparse
import textwrap

from starthinker.util.email import send_email
from starthinker.util.email_template import EmailTemplate
from starthinker.util.configuration import commandline_parser, Configuration


def main():

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent("""\
      Command line to send email template via gMail.

      Email templates are JSON that assembles into both HTMl and TXT parts of an email.
      For email sample see: https://github.com/google/starthinker/blob/master/starthinker/task/newsletter/sample.json

      Example:
        - Generate an HTML page from a template, then view via browser.
          python newsletter.py --template scripts/newsletter_sample.json > ~/Downloads/email.html

        - Send an email template via gMail.
          python newsletter.py --template scripts/newsletter_sample.json --email_to kenjora@google.com --email_from kenjora@google.com -u $STARTHINKER_USER
  """))

  # get parameters
  parser.add_argument(
      '--template',
      help='template to use for email',
      default=None,
      required=True)
  parser.add_argument('--email_to', help='email to', default=None)
  parser.add_argument('--email_from', help='email from', default=None)

  # initialize project
  parser = commandline_parser(parser, arguments=('-u', '-c', '-v'))
  args = parser.parse_args()
  config = Configuration(
    user=args.user,
    client=args.client,
    verbose=args.verbose
  )

  # load template
  with open(args.template, 'r') as json_file:
    email = EmailTemplate(json.load(json_file))

  # send or print
  if args.email_to and args.email_from:
    print('EMAILING: ', args.email_to)
    send_email(
      config,
      'user',
      args.email_to,
      args.email_from,
      None,
      email.get_subject(),
      email.get_text(),
      email.get_html()
    )
  else:
    # write to STDOUT
    print(email.get_html())
    print('<pre style="width:600px;margin:0px auto;">%s</pre>' % email.get_text())


if __name__ == '__main__':
  main()
