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

from django.shortcuts import render
from django.template.loader import render_to_string

from starthinker_ui.recipe.scripts import Script


def help(request):
  # if open source then request will be null
  if request:
    return render(request, 'website/help.html', {})
  else:
    return render_to_string('website/help.html', {'external': True})


def solutions(request):
  # if open source then request will be null
  if request:
    return render(request, 'website/solutions.html', {})
  else:
    return render_to_string('website/solutions.html', {'external': True})


def solution(request, tag):
  script = Script(tag)
  # if open source then request will be null
  if request:
    return render(request, 'website/solution.html', {'script': script})
  else:
    return render_to_string('website/solution.html', {
        'script': script,
        'external': True
    })
