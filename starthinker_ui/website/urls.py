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

from starthinker_ui.website import views

urlpatterns = [
  url(r'^stats/$', views.stats, name='website.stats'),
  url(r'^code/$', views.code, name='website.code'),
  url(r'^solution/$', views.solutions, name='website.solutions'),
  url(r'^solution/(?P<tag>\w+)/$', views.solution, name='website.solution'),
]
