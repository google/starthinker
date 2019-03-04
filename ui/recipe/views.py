# -*- coding: utf-8 -*-

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

from __future__ import unicode_literals
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from starthinker.ui.account.decorators import permission_admin
from starthinker.ui.recipe.forms_script import ScriptForm
from starthinker.manager.log import log_get, JOB_STARTED

def recipe_list(request):
  logs = log_get()
  recipes = request.user.recipe_set.all() if request.user.is_authenticated() else []
  for recipe in recipes:
    recipe.log = logs.get(recipe.uid(), {})
  return render(request, "recipe/recipe_list.html", { 'recipes':recipes })


@permission_admin()
def recipe_edit(request, pk=None):
  recipe = request.user.recipe_set.get(pk=pk) if pk else None

  if request.method == 'POST':
    form_script = ScriptForm(recipe, request.user, request.POST)
    if form_script.is_valid():
      form_script.save()
      messages.success(request, 'Recipe updated.')
      return HttpResponseRedirect(form_script.instance.link_edit())
    else:
      print 'ERRORS', form_script.get_errors()
      messages.error(request, 'Recipe Script Errors: %s' % form_script.get_errors())
  else:
    form_script = ScriptForm(recipe, request.user, scripts=request.GET.get('scripts', ''))

  return render(request, "recipe/recipe_edit.html", { 'form_script':form_script })

@permission_admin()
def recipe_delete(request, pk=None):
  request.user.recipe_set.filter(pk=pk).delete() 
  messages.success(request, 'Recipe deleted.')
  return HttpResponseRedirect('/')


@permission_admin()
def recipe_run(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    if recipe.log.get('status') == JOB_STARTED:
      messages.error(request, 'Wait for current job to finish.')
    else:
      recipe.run()
      messages.success(request, 'Recipe deployed.')
  except Exception, e:
    messages.error(request, str(e))
  return HttpResponseRedirect('/recipe/edit/%s/' % pk)


@permission_admin()
def recipe_download(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    filename, data = recipe.get_json(credentials=False)
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
  except Exception, e:
    messages.error(request, str(e))
  return HttpResponseRedirect('/recipe/edit/%s/' % pk)
