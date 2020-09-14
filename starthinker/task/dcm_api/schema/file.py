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

file_Schema = [[{
    'description': '',
    'name': 'endDate',
    'type': 'DATE',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description':
        'LAST_14_DAYS, LAST_24_MONTHS, LAST_30_DAYS, LAST_365_DAYS, '
        'LAST_60_DAYS, LAST_7_DAYS, LAST_90_DAYS, MONTH_TO_DATE, '
        'PREVIOUS_MONTH, PREVIOUS_QUARTER, PREVIOUS_WEEK, PREVIOUS_YEAR, '
        'QUARTER_TO_DATE, TODAY, WEEK_TO_DATE, YEAR_TO_DATE, YESTERDAY',
    'name':
        'relativeDateRange',
    'type':
        'STRING',
    'mode':
        'NULLABLE'
}, {
    'description': '',
    'name': 'startDate',
    'type': 'DATE',
    'mode': 'NULLABLE'
}], {
    'description': '',
    'name': 'etag',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'fileName',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': 'CSV, EXCEL',
    'name': 'format',
    'type': 'STRING',
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
}, {
    'description': '',
    'name': 'lastModifiedTime',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'reportId',
    'type': 'INT64',
    'mode': 'NULLABLE'
}, {
    'description': 'CANCELLED, FAILED, PROCESSING, REPORT_AVAILABLE',
    'name': 'status',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'urls',
    'type':
        'RECORD',
    'mode':
        'NULLABLE',
    'fields': [{
        'description': '',
        'name': 'apiUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'browserUrl',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}]
