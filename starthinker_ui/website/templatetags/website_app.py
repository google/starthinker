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

import re
import json
import hashlib

from urllib import quote_plus
from django import template
from django.utils.html import mark_safe
from django.forms.widgets import CheckboxInput
from django.utils.encoding import force_unicode

from starthinker_ui.recipe.forms_json import json_get_fields as json_get_fields_imported

register = template.Library()


@register.filter
def sort(value):
  return sorted(value)


@register.filter
def icon(value):
  return ''


@register.simple_tag
def request_solution(script):
  subject = "Request For A %s StarThinker Solution" % script.get_name()
  body = "Hi,\n\nI'd like to learn more about the %s solution.\n\nStarThinker Link: %s\n\nCan we set up some time to over it?\n\nThanks" % (
    script.get_name(),
    script.get_link()
  )
  return mark_safe('mailto:%s?subject=%s&body=%s' % (
    ','.join(script.get_authors()).replace(' ', ''), 
    quote_plus(subject),
    quote_plus(body)
  ))

@register.simple_tag
def mailto(emails, subject='', body=''):
  return mark_safe('mailto:%s?subject=%s&body=%s' % (
    ','.join(emails).replace(' ', ''), 
    quote_plus(subject),
    quote_plus(body)
  ))


@register.filter
def json_pretty(data):
  return json.dumps(data, indent=4)


@register.filter
def is_checkbox(field):
  return isinstance(field.field.widget, CheckboxInput)


@register.filter
def multiply(value, arg):
  return value*arg


@register.filter
def json_get_fields(value):
  return json_get_fields_imported(value)


@register.filter
def task_status_icon(event):

  if event == 'JOB_TIMEOUT': icon = 'alarm_off'
  elif event == 'JOB_ERROR': icon = 'error'
  elif event == 'JOB_END': icon = 'done_outline'
  elif event == 'JOB_START': icon = 'directions_walk'
  elif event == 'JOB_PENDING': icon = 'hourglass_empty'
  else: icon = 'hourglass_empty'

  return mark_safe('<i class="small material-icons-outlined" style="vertical-align: middle;">%s</i>&nbsp;&nbsp;' % icon)


@register.filter
def calvin_id(name):
  return (5*10**10) + int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16) % 10**9 # 5 + 9 digits


@register.filter
def email_to_ldap(email):
  try: return email.split('@')[0].lower()
  except: return ''


class GaplessNode(template.Node):

  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    return re.sub(r'\n\s*\n+', '\n', force_unicode(self.nodelist.render(context).strip()))


@register.tag
def gapless(parser, token):
  nodelist = parser.parse(('endgapless',))
  parser.delete_first_token()
  return GaplessNode(nodelist)
