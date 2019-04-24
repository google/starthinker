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


from django.conf.urls import url

import views

urlpatterns = [
  url(r'^storage/$', views.view_storage_list, name='storage.list'),
  url(r'^storage/link/$', views.view_storage_link, name='storage.link'),
  url(r'^storage/run/(?P<recipe>[\w\.]+)?/?$', views.view_storage_run, name='storage.run'),
]
