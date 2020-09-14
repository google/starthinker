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

projectsListResponse_Schema = [{
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'nextPageToken',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'projects',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'description': '',
        'name': 'accountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'advertiserId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description':
            'PLANNING_AUDIENCE_AGE_18_24, PLANNING_AUDIENCE_AGE_25_34, '
            'PLANNING_AUDIENCE_AGE_35_44, PLANNING_AUDIENCE_AGE_45_54, '
            'PLANNING_AUDIENCE_AGE_55_64, PLANNING_AUDIENCE_AGE_65_OR_MORE, '
            'PLANNING_AUDIENCE_AGE_UNKNOWN',
        'name':
            'audienceAgeGroup',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description':
            'PLANNING_AUDIENCE_GENDER_FEMALE, PLANNING_AUDIENCE_GENDER_MALE',
        'name':
            'audienceGender',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'description': '',
        'name': 'budget',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'clientBillingCode',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'clientName',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'endDate',
        'type': 'DATE',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'id',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, [{
        'description': '',
        'name': 'time',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }], {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'overview',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'startDate',
        'type': 'DATE',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'subaccountId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetClicks',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetConversions',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetCpaNanos',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetCpcNanos',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetCpmActiveViewNanos',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetCpmNanos',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'targetImpressions',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }]
}]
