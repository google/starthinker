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

from itertools import chain

from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.management import call_command
from django.http import HttpResponse

from starthinker_ui.account.decorators import permission_admin
from starthinker_ui.account.models import Account
from starthinker_ui.recipe.scripts import Script
from starthinker_ui.recipe.models import Recipe


def solutions(request):
  scripts = [s for s in Script.get_scripts() if s.is_solution()]

  # if open source then request will be null
  if not request: 
    scripts = [s for s in scripts if s.get_open_source()]
  
  context = {
    'scripts':scripts,
    'categories':sorted(set(chain.from_iterable([s.get_categories() for s in scripts]))),
    'catalysts':sorted(set(chain.from_iterable([s.get_catalysts() for s in scripts]))),
    'requirements':sorted(set(chain.from_iterable([s.get_requirements() for s in scripts]))),
    'external':(request is None)
  }

  # if open source then request will be null
  if not request: 
    return render_to_string("website/solutions.html", context)
  else:
    return render(request, "website/solutions.html", context)


def solution(request, tag):
  script = Script(tag)
  if request: 
    return render(request, "website/solution.html", { 'script':script })
  else: 
    return render_to_string('website/solution.html', { 'script':script, "external":True })


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
    return render_to_string('website/code.html', { 'products':products, "external":True })


def get_metrics():

  metrics = {
    'account':{} , #'account':{ 'recipe':'', 'script':'', 'author':'' }
    'script':{}, # 'script':{ 'account':'', 'recipe':'' }
    'author':{}, # 'author':{ 'account':'', 'recipe':'', 'script' }
  }

  totals = {
    'account':set(),
    'author':set(),
    'script':set(),
    'recipe':set(),
  }

  for account in Account.objects.all():
    totals['account'].add(account.name)

    for recipe in account.recipe_set.all():
      totals['recipe'].add(recipe.pk)

      for s in recipe.get_values():
        script = Script(s['tag'])
        authors = script.get_authors()

        metrics['account'].setdefault(account.name, {'recipe':set(), 'script':set(), 'author':set()})
        metrics['account'][account.name]['recipe'].add(recipe.pk)
        metrics['account'][account.name]['script'].add(s['tag'])
        metrics['account'][account.name]['author'].update(authors)

        totals['script'].add(s['tag'])
        metrics['script'].setdefault(s['tag'], {'account':set(), 'recipe':set()})
        metrics['script'][s['tag']]['recipe'].add(recipe.pk)
        metrics['script'][s['tag']]['account'].add(account.name)

        for author in authors:
          totals['author'].add(author)
          metrics['author'].setdefault(author, {'account':set(), 'recipe':set(), 'script':set()})
          metrics['author'][author]['account'].add(account.name)
          metrics['author'][author]['recipe'].add(recipe.pk)
          metrics['author'][author]['script'].add(s['tag'])

  # compute totals
  for dimension in totals.keys():
    totals[dimension] = len(totals[dimension])
     
  for metric_key, metric in metrics.items():
    for row_key, row in metric.items():
      for dimension in row.keys():
        row[dimension] = len(row[dimension])
        row['%s_percent' % dimension] = (row[dimension] * 100) / (totals[dimension] or 1)
        row[metric_key] = row_key
    metrics[metric_key] = metrics[metric_key].values()

  return metrics
       
@permission_admin()
def stats(request):
  return render(request, "website/stats.html", { 'metrics':get_metrics() })
