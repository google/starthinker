###########################################################################
#
#  Copyright 2019 Google Inc.
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

encryptionInfo_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "encryptionEntityId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "AD_SERVING, DATA_TRANSFER, ENCRYPTION_SCOPE_UNKNOWN", 
    "name": "encryptionSource"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ADWORDS_CUSTOMER, DBM_ADVERTISER, DBM_PARTNER, DCM_ACCOUNT, DCM_ADVERTISER, DFP_NETWORK_CODE, ENCRYPTION_ENTITY_TYPE_UNKNOWN", 
    "name": "encryptionEntityType"
  }
]
