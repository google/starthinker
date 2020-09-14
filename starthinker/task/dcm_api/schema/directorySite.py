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

directorySite_Schema = [
    {
        'name': 'active',
        'type': 'BOOLEAN',
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
        'name': 'inpageTagFormats',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'name': 'interstitialTagFormats',
        'type': 'STRING',
        'mode': 'REPEATED'
    }, {
        'description': '',
        'name': 'kind',
        'type': 'STRING',
        'mode': 'NULLABLE'
    }, {
        'description': '',
        'name': 'name',
        'type': 'STRING',
        'mode': 'NULLABLE'
    },
    [{
        'name': 'activeViewOptOut',
        'type': 'BOOLEAN',
        'mode': 'NULLABLE'
    },
     [{
         'description': '',
         'name': 'dfpNetworkCode',
         'type': 'STRING',
         'mode': 'NULLABLE'
     }, {
         'description': '',
         'name': 'dfpNetworkName',
         'type': 'STRING',
         'mode': 'NULLABLE'
     }, {
         'name': 'programmaticPlacementAccepted',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'pubPaidPlacementAccepted',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'publisherPortalOnly',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }], {
         'name': 'instreamVideoPlacementAccepted',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }, {
         'name': 'interstitialPlacementAccepted',
         'type': 'BOOLEAN',
         'mode': 'NULLABLE'
     }], {
         'description': '',
         'name': 'url',
         'type': 'STRING',
         'mode': 'NULLABLE'
     }
]
