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

#import pandas
from itertools import chain

from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.management import call_command
from django.http import HttpResponse

from starthinker_ui.account.decorators import permission_admin
from starthinker_ui.account.models import Account
from starthinker_ui.recipe.scripts import Script
from starthinker_ui.recipe.models import Recipe
from starthinker_ui.storage.models import storage_list


def solutions(request):
  scripts = [s for s in Script.get_scripts() if s.is_solution()]
  categories = sorted(set(chain.from_iterable([s.get_categories() for s in scripts])))
  return render(request, "website/solutions.html", { 'scripts':scripts, 'categories':categories })


def solution(request, tag):
  script = Script(tag)
  return render(request, "website/solution.html", { 'script':script })


# also called by website/management/commands/code.py without request to render open source doc
def code(request):
  scripts = sorted(Script.get_scripts(), key=lambda s: s.get_name()) 
  products = {}

  for s in scripts: 
    if s.get_open_source(): 
      products.setdefault(s.get_product(), [])
      products[s.get_product()].append(s)
    
  products = sorted([{ 'name':k, 'scripts':v } for k,v in products.items()], key=lambda p: p['name'])

  if request:
    return render(request, "website/code.html", { 'products':products })
  else:
    return render_to_string('website/code.html', { 'products':products })


#@permission_admin()
#def stats(request):
#
#  data = []
#
#  # flatten all data into one table
#  def data_row(account_id, account_name, recipe_id, recipe_name, script, script_author):
#    data.append([account_id, account_name, recipe_id, recipe_name, script, script_author])
#
#  for account in Account.objects.all():
#    for recipe in account.recipe_set.all():
#      for s in recipe.get_values():
#        script = Script(s['tag'])
#        data_row(account.pk, account.name, recipe.pk, recipe.name,  s['tag'], None)
#        for author in script.get_authors():
#          data_row(account.pk, account.name, recipe.pk, recipe.name, s['tag'], author)
#
#    #for recipe in storage_recipes(account):
#
#  # create a database for anlaysis
#  db = pandas.DataFrame.from_records(
#    data, 
#    columns=['account_id', 'account_name', 'recipe_id', 'recipe_name', 'script', 'script_author']
#  )
#
#  uniques = {
#    'accounts':db['account_id'].nunique(),
#    'recipes':db['recipe_id'].nunique(),
#    'scripts':db['script'].nunique(),
#    'script_authors':db['script_author'].nunique(),
#  }
#
#  # compute account values
#  def db_compute(key, aggregate):
#    data = db.groupby([key]).agg(aggregate).to_dict('records')
#    return db_unique([dict([(k[1], v) for k,v in d.items()]) for d in data])
#
#  def db_unique(data):
#    for row in data:
#      for key in uniques.keys():
#        if key in row: row['%s_percent' % key] = (((row[key] * 100) / uniques[key]) if uniques[key] else 0)
#    return data
#       
#  metrics = {
#    'accounts':db_compute('account_id', {
#      'account_name':{ 'account':'first' },
#      'recipe_id':{ 'recipes':'nunique' },
#      'script':{ 'scripts':'nunique' },
#      'script_author':{ 'script_authors':'nunique' },
#    }),
#    
#    'scripts':db_compute('script', {
#      'script':{ 'script':'first' },
#      'account_id':{ 'accounts':'nunique' },
#      'recipe_id':{ 'recipes':'nunique' },
#    }),
#
#    'script_authors':db_compute('script_author', {
#      'script_author':{ 'author':'first' },
#      'account_id':{ 'accounts':'nunique' },
#      'recipe_id':{ 'recipes':'nunique' },
#      'script':{ 'scripts':'nunique' },
#    }),
#  }
#
#  return render(request, "website/stats.html", { 'metrics':metrics })


def cron(request):
  if request.META.get('HTTP_X_APPENGINE_CRON') == 'true' and request.META.get('REMOTE_ADDR') == '0.1.0.1':
    call_command('recipe_to_json', '--remote')
    call_command('storage_to_json', '--remote')
  return HttpResponse(status=204)

