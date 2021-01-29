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

LineItem_Write_Schema = [{
    'name': 'Line Item Id',
    'type': 'INTEGER',
    'mode': 'REQUIRED'
}, {
    'name': 'Partner Name',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Advertiser Name',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Name',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Name',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Timestamp',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Status',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Start Date',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO End Date',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Budget Type',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Budget Amount',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Pacing',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Pacing Rate',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'IO Pacing Amount',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Start Date',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item End Date',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Budget Type',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Budget Amount',
    'type': 'FLOAT',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Pacing',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Pacing Rate',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Pacing Amount',
    'type': 'FLOAT',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Frequency Enabled',
    'type': 'BOOLEAN',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Frequency Exposures',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Frequency Period',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Line Item Frequency Amount',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Bid Price',
    'type': 'FLOAT',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner Revenue Model',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner Revenue Amount',
    'type': 'FLOAT',
    'mode': 'NULLABLE'
}, {
    'name': 'Current Audience Targeting Ids',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Current Audience Targeting Names',
    'type': 'STRING',
    'mode': 'NULLABLE'
}]

LineItem_Read_Schema = [{
    'name': s['name'].replace(' ', '_'),
    'type': s['type'],
    'mode': s['mode'],
} for s in LineItem_Write_Schema]
