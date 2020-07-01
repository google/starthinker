#!/usr/bin/env python

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

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

REQUIREMENTS = [
  'google-api-python-client',
  'google-auth-oauthlib',
  'jsonpickle',
  'pysftp',
  'pytz',
  'tzlocal',
  'TwitterAPI',
  'python-dateutil',
  'pandas',
  'psutil',
  'moviepy',
  'py-xlsx',
  'simple-salesforce'
]

#TEST_REQUIREMENTS = []

setup(
  name='starthinker',
  version='0.0.9',
  description="StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components.",
  long_description="StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components. To make it easier for partners and clients to work with some of our advertsing solutions, the gTech team has open sourced this framework as a reference implementation.  Our goal is to make managing data workflows using Google Cloud as fast and re-usable as possible, allowing teams to focus on building advertising solutions.",
  author="Paul Kenjora & Mauricio Desidario",
  author_email='kenjora@google.com',
  url='https://github.com/google/starthinker',
  packages=find_packages(),
  package_dir={'starthinker':
               'starthinker'},
  include_package_data=True,
  install_requires=REQUIREMENTS,
  entry_points={
    'console_scripts': [
      'st_auth = starthinker.auth.helper:main',
      'st_cm = starthinker.task.dcm.helper:main'
      'st_dv360 = starthinker.task.dbm.helper:main'
      'st_dv360_beta = starthinker.task.dv360_beta.helper:main'
    ]
  },
  license="Apache License, Version 2.0",
  zip_safe=False,
  keywords='starthinker',
  classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Apache License',
      'Natural Language :: English',
      "Programming Language :: Python :: 3",
  ],
  #test_suite='tests',
  #tests_require=TEST_REQUIREMENTS,
)
