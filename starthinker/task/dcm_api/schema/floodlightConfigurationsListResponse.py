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

floodlightConfigurationsListResponse_Schema = [{
    'name':
        'floodlightConfigurations',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [
        {
            'description': '',
            'name': 'accountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'advertiserId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'dimensionName',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'etag',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'id',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
            'name': 'matchType',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'value',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'name': 'analyticsDataSharingEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        },
        [[{
            'name': 'audible',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'timeMillis',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'timePercent',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'viewabilityPercent',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'id',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'name',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'name': 'exposureToConversionEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': 'MONDAY, SUNDAY',
            'name': 'firstDayOfWeek',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'id',
            'type': 'INT64',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'dimensionName',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'etag',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'id',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': 'BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION',
            'name': 'matchType',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'value',
            'type': 'STRING',
            'mode': 'NULLABLE'
        }], {
            'name': 'inAppAttributionTrackingEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'kind',
            'type': 'STRING',
            'mode': 'NULLABLE'
        },
        [{
            'description': '',
            'name': 'clickDuration',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }, {
            'description': '',
            'name': 'postImpressionActivitiesDuration',
            'type': 'INT64',
            'mode': 'NULLABLE'
        }], {
            'description':
                'EXCLUDE_NATURAL_SEARCH_CONVERSION_ATTRIBUTION, '
                'INCLUDE_NATURAL_SEARCH_CONVERSION_ATTRIBUTION, '
                'INCLUDE_NATURAL_SEARCH_TIERED_CONVERSION_ATTRIBUTION',
            'name':
                'naturalSearchConversionAttributionOption',
            'type':
                'STRING',
            'mode':
                'NULLABLE'
        },
        [{
            'name': 'omnitureCostDataEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name': 'omnitureIntegrationEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }], {
            'description': '',
            'name': 'subaccountId',
            'type': 'INT64',
            'mode': 'NULLABLE'
        },
        [{
            'name': 'dynamicTagEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }, {
            'name': 'imageTagEnabled',
            'type': 'BOOLEAN',
            'mode': 'NULLABLE'
        }], {
            'name':
                'thirdPartyAuthenticationTokens',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
                'description': '',
                'name': 'name',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'value',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }]
        }, {
            'name':
                'userDefinedVariableConfigurations',
            'type':
                'RECORD',
            'mode':
                'REPEATED',
            'fields': [{
                'description': 'NUMBER, STRING',
                'name': 'dataType',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description': '',
                'name': 'reportName',
                'type': 'STRING',
                'mode': 'NULLABLE'
            }, {
                'description':
                    'U1, U10, U100, U11, U12, U13, U14, U15, U16, U17, U18, '
                    'U19, U2, U20, U21, U22, U23, U24, U25, U26, U27, U28, '
                    'U29, U3, U30, U31, U32, U33, U34, U35, U36, U37, U38, '
                    'U39, U4, U40, U41, U42, U43, U44, U45, U46, U47, U48, '
                    'U49, U5, U50, U51, U52, U53, U54, U55, U56, U57, U58, '
                    'U59, U6, U60, U61, U62, U63, U64, U65, U66, U67, U68, '
                    'U69, U7, U70, U71, U72, U73, U74, U75, U76, U77, U78, '
                    'U79, U8, U80, U81, U82, U83, U84, U85, U86, U87, U88, '
                    'U89, U9, U90, U91, U92, U93, U94, U95, U96, U97, U98, U99',
                'name':
                    'variableType',
                'type':
                    'STRING',
                'mode':
                    'NULLABLE'
            }]
        }
    ]
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
