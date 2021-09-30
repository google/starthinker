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

from django.conf.urls import url

from starthinker_ui.recipe import views

urlpatterns = [
    url(r'^recipe/edit/(?P<pk>\d+)?/?$', views.recipe_edit, name='recipe.edit'),
    url(r'^recipe/manual/(?P<pk>\d+)?/?$', views.recipe_manual, name='recipe.manual'),
    url(r'^recipe/delete/(?P<pk>\d+)/$', views.recipe_delete, name='recipe.delete'),
    url(r'^recipe/run/(?P<pk>\d+)/$', views.recipe_run, name='recipe.run'),
    url(r'^recipe/cancel/(?P<pk>\d+)/$', views.recipe_cancel, name='recipe.cancel'),
    url(r'^recipe/status/(?P<pk>\d+)/$', views.recipe_status, name='recipe.status'),
    url(r'^recipe/download/(?P<pk>\d+)?/?$', views.recipe_download, name='recipe.download'),
    url(r'^recipe/download/json/(?P<pk>\d+)/$', views.recipe_json, name='recipe.json'),
    url(r'^recipe/download/colab/(?P<pk>\d+)/$', views.recipe_colab, name='recipe.colab'),
    url(r'^recipe/download/python/(?P<pk>\d+)/$', views.recipe_python, name='recipe.python'),
    url(r'^recipe/download/airflow/(?P<pk>\d+)/$', views.recipe_airflow, name='recipe.airflow'),
    url(r'^recipe/start/$', views.recipe_start, name='recipe.start'),
    url(r'^recipe/stop/$', views.recipe_stop, name='recipe.stop'),
    url(r'^$', views.recipe_list, name='recipe.list'),
    url(r'^recipe/autoscale/$', views.autoscale, name='recipe.autoscale'),
]
