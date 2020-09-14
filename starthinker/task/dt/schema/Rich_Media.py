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

Rich_Media_Schema = [{
    'name': 'Partitiontime',
    'type': 'TIMESTAMP',
    'mode': 'NULLABLE'
}, {
    'name': 'Event_Time',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'User_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Advertiser_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Campaign_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Ad_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Rendering_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Creative_Version',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Site_Id_Dcm',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Country_Code',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'State_Region',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Browser_Platform_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Browser_Platform_Version',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Placement_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Operating_System_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner_1_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner_2_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner_3_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner_4_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Partner_5_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Null_User_Id_Reason_Groups',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Rich_Media_Event_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Rich_Media_Event_Type_Id',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Impression_Id',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Creative_Pixel_Size',
    'type': 'STRING',
    'mode': 'NULLABLE'
}, {
    'name': 'Custom_Event_Counters',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Custom_Event_Timers',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Event_Counters',
    'type': 'INTEGER',
    'mode': 'NULLABLE'
}, {
    'name': 'Event_Timers',
    'type': 'FLOAT',
    'mode': 'NULLABLE'
}]
