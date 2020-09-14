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

conversionsBatchInsertResponse_Schema = [{
    'name': 'hasFailures',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name':
        'status',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [[{
        'name': 'childDirectedTreatment',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name':
            'customVariables',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description':
                'U1, U10, U100, U11, U12, U13, U14, U15, U16, U17, U18, U19, '
                'U2, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U3, '
                'U30, U31, U32, U33, U34, U35, U36, U37, U38, U39, U4, U40, '
                'U41, U42, U43, U44, U45, U46, U47, U48, U49, U5, U50, U51, '
                'U52, U53, U54, U55, U56, U57, U58, U59, U6, U60, U61, U62, '
                'U63, U64, U65, U66, U67, U68, U69, U7, U70, U71, U72, U73, '
                'U74, U75, U76, U77, U78, U79, U8, U80, U81, U82, U83, U84, '
                'U85, U86, U87, U88, U89, U9, U90, U91, U92, U93, U94, U95, '
                'U96, U97, U98, U99',
            'name':
                'type',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description': '',
            'name': 'value',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'description': '',
        'name': 'encryptedUserId',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'encryptedUserIdCandidates',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'floodlightActivityId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'floodlightConfigurationId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'gclid',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'limitAdTracking',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'mobileDeviceId',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'nonPersonalizedAd',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'ordinal',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'quantity',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'timestampMicros',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'name': 'treatmentForUnderage',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'value',
        'type': 'FLOAT64',
        'mode': 'NULLABLE'
    }], {
        'name':
            'errors',
        'type':
            'RECORD',
        'mode':
            'REPEATED',
        'fields': [{
            'description':
                'INTERNAL, INVALID_ARGUMENT, NOT_FOUND, PERMISSION_DENIED',
            'name':
                'code',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'message',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }]
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }]
}]
