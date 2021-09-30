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
import math

from django.shortcuts import render
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings

from starthinker.tool.colab import recipe_to_colab
from starthinker.tool.example import recipe_to_python
from starthinker_ui.account.decorators import permission_admin
from starthinker_ui.recipe.forms_script import ScriptForm
from starthinker_ui.recipe.models import Recipe, utc_milliseconds
from starthinker_ui.recipe.dag import script_to_dag
from starthinker_ui.recipe.log import log_manager_scale
from starthinker_ui.recipe.compute import group_instances_list, group_instances_resize


def recipe_list(request):
  recipes = {
    'running': [],
    'paused': [],
    'finished': [],
    'errors': [],
    'manual': []
  }

  if request.user.is_authenticated:
    for recipe in request.user.recipe_set.all():
      if recipe.manual:
        recipes['manual'].append(recipe)
      elif not recipe.active or recipe.get_log()['status'] == 'NEW':
        recipes['paused'].append(recipe)
      elif recipe.get_log()['status'] == 'FINISHED':
        recipes['finished'].append(recipe)
      elif recipe.get_log()['status'] == 'ERROR':
        recipes['errors'].append(recipe)
      else:
        recipes['running'].append(recipe)

  return render(request, 'recipe/recipe_list.html', {'recipes': recipes})


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
      if request.POST.get('save_and_run') == '1':
        return recipe_run(request, form_script.instance.pk)
      else:
        return HttpResponseRedirect(form_script.instance.link_edit())
    else:
      messages.error(
        request,
        'Recipe Script Errors: %s' % ' '.join(form_script.get_errors())
      )
  else:
    form_script = ScriptForm(
      manual,
      recipe,
      request.user,
      scripts=request.GET.get('scripts', '')
    )

  return render(request, 'recipe/recipe_edit.html', {
    'form_script': form_script,
    'manual': manual
  })


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
      recipe.force()
      messages.success(request, 'Recipe dispatched, will run once in progress task completes.')
    else:
      recipe.force()
      autoscale(request)
      messages.success(request, 'Recipe dispatched, give it a few minutes to start.')
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


@permission_admin()
def recipe_status(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    log = recipe.get_log()
    log['report'] = render_to_string('recipe/log.html', {'log': log})
  except Recipe.DoesNotExist:
    log = {}
  return JsonResponse(log)


@csrf_exempt
def recipe_start(request):
  try:
    recipe = Recipe.objects.get(reference=request.POST.get('reference', 'invalid'))
    if recipe.is_running():
      response = HttpResponse('RECIPE INTERRUPTED', content_type='text/plain')
    else:
      response = HttpResponse('RECIPE STARTED', content_type='text/plain')
    recipe.force()
  except Recipe.DoesNotExist as e:
    response = HttpResponseNotFound('RECIPE NOT FOUND', content_type='text/plain')
  return response


@csrf_exempt
def recipe_stop(request):
  try:
    recipe = Recipe.objects.get(reference=request.POST.get('reference', 'invalid'))
    if recipe.is_running():
      response = HttpResponse('RECIPE INTERRUPTED', content_type='text/plain')
    else:
      response = HttpResponse('RECIPE STOPPED', content_type='text/plain')
    recipe.cancel()
  except Recipe.DoesNotExist as e:
    response = HttpResponseNotFound('RECIPE NOT FOUND', content_type='text/plain')
  return response


@permission_admin()
def recipe_download(request, pk):
  return render(request, 'recipe/download.html', {'recipe': pk})


@permission_admin()
def recipe_json(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    data = recipe.get_json(credentials=False)
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=recipe_%s.json' % recipe.slug()
    return response
  except Exception as e:
    recipe = None
    messages.error(request, str(e))

  return HttpResponseRedirect('/recipe/download/%s/' % pk)


@permission_admin()
def recipe_colab(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    data = recipe_to_colab(recipe.slug(), '', [], recipe.get_json(credentials=False)['tasks'])
    response = HttpResponse(data, content_type='application/vnd.jupyter')
    response['Content-Disposition'] = 'attachment; filename=colab_%s.ipynb' % recipe.slug()
    return response
  except Exception as e:
    messages.error(request, str(e))
    raise (e)
  return HttpResponseRedirect('/recipe/download/%s/' % pk)


@permission_admin()
def recipe_airflow(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    data = script_to_dag(recipe.slug(), recipe.name, '', [], recipe.get_json(credentials=False)['tasks'])
    response = HttpResponse(data, content_type='text/x-python')
    response['Content-Disposition'] = 'attachment; filename=airflow_%s.py' % recipe.slug()
    return response
  except Exception as e:
    messages.error(request, str(e))
    raise (e)
  return HttpResponseRedirect('/recipe/download/%s/' % pk)


@permission_admin()
def recipe_python(request, pk):
  try:
    recipe = request.user.recipe_set.get(pk=pk)
    data = recipe_to_python(recipe.slug(), '', [], recipe.get_json(credentials=False)['tasks'])
    response = HttpResponse(data, content_type='text/x-python')
    response['Content-Disposition'] = 'attachment; filename=python_%s.py' % recipe.slug()
    return response
  except Exception as e:
    messages.error(request, str(e))
    raise (e)
  return HttpResponseRedirect('/recipe/download/%s/' % pk)


def autoscale(request):

  scale = {
    'jobs': 0,
    'workers': {
      'jobs': settings.WORKER_JOBS,
      'max': settings.WORKER_MAX,
      'existing': 0,
      'required': 0
    }
  }

  # get task and worker list
  scale['jobs'] = Recipe.objects.filter(
    active=True,
    job_utm__lt=utc_milliseconds()
  ).exclude(job_utm=0).count()

  scale['workers']['existing'] = 3 if request == 'TEST' else sum(
    1 for instance in group_instances_list(('PROVISIONING', 'STAGING', 'RUNNING'))
  )

  scale['workers']['required'] = min(
    settings.WORKER_MAX, math.ceil(scale['jobs'] / scale['workers']['jobs'])
  )

  if request != 'TEST' and scale['workers']['required'] > scale['workers']['existing']:
    group_instances_resize(scale['workers']['required'])

  # log the scaling operation
  log_manager_scale(scale)

  return JsonResponse(scale)
