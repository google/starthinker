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

GeoLocation_Schema = [
    {
        'name': 'id',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'country_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'region_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'city_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'postal_code',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'dma_code',
        'type': 'INTEGER',
        'mode': 'NULLABLE',
    },
    {
        'name': 'canonical_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
    {
        'name': 'geo_name',
        'type': 'STRING',
        'mode': 'NULLABLE',
    },
]
