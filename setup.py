#!/usr/bin/env python

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

# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

REQUIREMENTS = [
    'google-api-python-client',
    'google-auth',
    'google-auth-oauthlib',
    'google-auth-httplib2',
    'google-cloud-bigquery==2.13',
    'pysftp',
    'pytz',
    'tzlocal',
    'TwitterAPI',
    'python-dateutil',
    'psutil',
    'moviepy==1.0.0',
    'py-xlsx',
    'simple-salesforce',
    'smartsheet-python-sdk'
]

setup(
    name='starthinker',
    version='2.1.4',
    description='StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components.',
    long_description='StarThinker is a Google gTech built python framework for creating and sharing re-usable workflow components. To make it easier for partners and clients to work with some of our advertsing solutions, the gTech team has open sourced this framework as a reference implementation.  Our goal is to make managing data workflows using Google Cloud as fast and re-usable as possible, allowing teams to focus on building advertising solutions.',
    author='Paul Kenjora',
    author_email='kenjora@google.com',
    url='https://github.com/google/starthinker',
    packages=find_packages(),
    package_dir={'starthinker': 'starthinker'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'st_auth = starthinker.tool.auth:main',
            'st_validate = starthinker.tool.validate:main',
            'st_recipe = starthinker.tool.recipe:main',
            'st_colab = starthinker.tool.colab:main',
            'st_cm = starthinker.tool.cm:main',
            'st_dv = starthinker.tool.dv:main',
            'st_bigquery = starthinker.tool.bigquery:main',
            'st_google_api = starthinker.tool.google_api:main',
            'st_newsletter = starthinker.tool.newsletter:main'
            'st_test = starthinker.tool.test:main'
        ]
    },
    license='Apache License, Version 2.0',
    zip_safe=False,
    keywords='starthinker',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ]
)
