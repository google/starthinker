# -*- coding: utf-8 -*-

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

from django.db import models


class JsonField(models.TextField):

  # python to SQL
  def get_prep_value(self, value):
    if value is None:
      return None
    elif isinstance(value, str):
      return value
    else:
      try:
        return json.dumps(value)
      except:        raise ValidationError(_('Bad JSON string.'))

  # SQL to python
  def from_db_value(self, value, expression, connection, context):
    return json.loads(value)

  # any source to python
  def to_python(self, value):
    if value is None:
      return None
    if isinstance(value, str):
      try:
        return json.loads(value)
      except:        raise ValidationError(_('Bad JSON string.'))
    else:
      return value
