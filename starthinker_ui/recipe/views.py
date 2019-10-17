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
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from starthinker_ui.account.decorators import permission_admin
from starthinker_ui.recipe.forms_script import ScriptForm
from starthinker_ui.recipe.models import Recipe


def recipe_list(request):
  if request.user.is_authenticated:
    recipes = request.user.recipe_set.all()
  else:
    recipes = []
  return render(request, "recipe/recipe_list.html", { 'recipes':recipes })


@permission_admin()
def recipe_edit(request, pk=None, manual=False):
  if pk:
    recipe = request.user.recipe_set.get(pk=pk)
    manual = recipe.manual
  else:
    recipe = None

  if request.method == 'POST':
    form_script = ScriptForm(manual, recipe, request.user, request.POST)
    if form_script.is_valid():
      form_script.save()
      messages.success(request, 'Recipe updated.')
      return HttpResponseRedirect(form_script.instance.link_edit())
    else:
      print('ERRORS', form_script.get_errors())
      messages.error(request, 'Recipe Script Errors: %s' % form_script.get_errors())
  else:
    form_script = ScriptForm(manual, recipe, request.user, scripts=request.GET.get('scripts', ''))

  return render(request, "recipe/recipe_edit.html", { 'form_script':form_script, 'manual':manual })


@permission_admin()
def recipe_manual(request, pk=None):
  return recipe_edit(request, pk=None, manual=True)


@permission_admin()
def recipe_delete(request, pk=None):
  request.user.recipe_set.filter(pk=pk).delete() 
  messages.success(request, 'Recipe deleted.')
  return HttpResponseRedirect('/')


@permission_admin()
def recipe_run(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    if recipe.is_running():
      messages.success(request, 'Recipe dispatched, will run once in progress task completes.')
    else:
      messages.success(request, 'Recipe dispatched, give it a few minutes to start.')
    recipe.force()
  except Recipe.DoesNotExist as e:
    messages.error(request, str(e))
  return HttpResponseRedirect('/recipe/edit/%s/' % pk)


@permission_admin()
def recipe_cancel(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    if recipe.is_running():
      messages.success(request, 'Recipe cancelled, active task will stop shortly.')
    else:
      messages.success(request, 'Recipe cancelled, no tasks are running.')
    recipe.cancel()
  except Recipe.DoesNotExist as e:
    messages.error(request, str(e))
  return HttpResponseRedirect('/recipe/edit/%s/' % pk)


@csrf_exempt
def recipe_start(request):
  try:
    recipe = Recipe.objects.get(reference=request.POST.get('reference', 'invalid'))
    if recipe.is_running():
      response = HttpResponse('RECIPE INTERRUPTED', content_type="text/plain")
    else:
      response = HttpResponse('RECIPE STARTED', content_type="text/plain")
    recipe.force()
  except Recipe.DoesNotExist as e:
    response = HttpResponseNotFound('RECIPE NOT FOUND', content_type="text/plain")
  return response


@csrf_exempt
def recipe_stop(request):
  try:
    recipe = Recipe.objects.get(reference=request.POST.get('reference', 'invalid'))
    if recipe.is_running():
      response = HttpResponse('RECIPE INTERRUPTED', content_type="text/plain")
    else:
      response = HttpResponse('RECIPE STOPPED', content_type="text/plain")
    recipe.cancel()
  except Recipe.DoesNotExist as e:
    response = HttpResponseNotFound('RECIPE NOT FOUND', content_type="text/plain")
  return response


@permission_admin()
def recipe_download(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    data = recipe.get_json(credentials=False)
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=recipe_%s.json' % recipe.uid()
    return response
  except Exception as e:
    messages.error(request, str(e))
  return HttpResponseRedirect('/recipe/edit/%s/' % pk)
