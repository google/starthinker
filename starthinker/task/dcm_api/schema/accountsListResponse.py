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

accountsListResponse_Schema = [{
    'name':
        'accounts',
    'type':
        'RECORD',
    'mode':
        'REPEATED',
    'fields': [{
        'name': 'accountPermissionIds',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'description': 'ACCOUNT_PROFILE_BASIC, ACCOUNT_PROFILE_STANDARD',
        'name': 'accountProfile',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'active',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'description':
            'ACTIVE_ADS_TIER_100K, ACTIVE_ADS_TIER_1M, ACTIVE_ADS_TIER_200K, '
            'ACTIVE_ADS_TIER_300K, ACTIVE_ADS_TIER_40K, ACTIVE_ADS_TIER_500K, '
            'ACTIVE_ADS_TIER_750K, ACTIVE_ADS_TIER_75K',
        'name':
            'activeAdsLimitTier',
        'type':
            'STRING',
        'mode':
            'NULLABLE'
    }, {
        'name': 'activeViewOptOut',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    }, {
        'name': 'availablePermissionIds',
        'type': 'INT64',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'countryId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'currencyId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'defaultCreativeSizeId',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'description',
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
        'name': 'locale',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'maximumImageSize',
        'type': 'INT64',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'name': 'nielsenOcrEnabled',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    },
               [{
                   'name': 'exposureToConversionEnabled',
                   'type': 'BOOLEAN',
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
                    'description': '',
                    'name': 'reportGenerationTimeZoneId',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }], {
                    'name': 'shareReportsWithTwitter',
                    'type': 'BOOLEAN',
                    'mode': 'NULLABLE'
                }, {
                    'description': '',
                    'name': 'teaserSizeLimit',
                    'type': 'INT64',
                    'mode': 'NULLABLE'
                }]
}, {
    'description': '',
    'name': 'kind',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'description': '',
    'name': 'nextPageToken',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]
