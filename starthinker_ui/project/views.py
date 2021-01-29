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

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from starthinker_ui.account.decorators import permission_admin
from starthinker_ui.project.models import Project
from starthinker_ui.project.forms import ProjectForm


def project_list(request):
  projects = request.user.project_set.all(
  ) if request.user.is_authenticated else None
  return render(request, 'project/project_list.html', {'projects': projects})


@permission_admin()
def project_edit(request, pk=None):
  project = request.user.project_set.get(pk=pk) if pk else None

  if request.method == 'POST':
    form_project = ProjectForm(request.user, request.POST, instance=project)
    if form_project.is_valid():
      form_project.save()
      messages.success(request, 'Project updated.')
      return HttpResponseRedirect(form_project.instance.link_edit())
    else:
      print('ERRORS', form_project.get_errors())
      messages.error(request, 'Project Errors: %s' % form_project.get_errors())
  else:
    form_project = ProjectForm(request.user, instance=project)

  return render(request, 'project/project_edit.html',
                {'form_project': form_project})


@permission_admin()
def project_delete(request, pk=None):
  request.user.project_set.filter(pk=pk).delete()
  messages.success(request, 'Project deleted.')
  return HttpResponseRedirect('/project/')
