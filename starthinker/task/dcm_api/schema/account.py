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

account_Schema = [
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
    "name": "countryId"
  }, 
  {
    "type": "INT64", 
    "name": "availablePermissionIds", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "description"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "maximumImageSize"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "currencyId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "defaultCreativeSizeId"
  }, 
  {
    "type": "INT64", 
    "name": "accountPermissionIds", 
    "mode": "REPEATED"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "nielsenOcrEnabled", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ACCOUNT_PROFILE_BASIC, ACCOUNT_PROFILE_STANDARD", 
    "name": "accountProfile"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "name"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "locale"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "teaserSizeLimit"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "reportGenerationTimeZoneId"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "exposureToConversionEnabled", 
      "mode": "NULLABLE"
    }, 
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "clickDuration"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "postImpressionActivitiesDuration"
      }
    ]
  ], 
  {
    "type": "BOOLEAN", 
    "name": "active", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "activeViewOptOut", 
    "mode": "NULLABLE"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "shareReportsWithTwitter", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "ACTIVE_ADS_TIER_100K, ACTIVE_ADS_TIER_1M, ACTIVE_ADS_TIER_200K, ACTIVE_ADS_TIER_300K, ACTIVE_ADS_TIER_40K, ACTIVE_ADS_TIER_500K, ACTIVE_ADS_TIER_750K, ACTIVE_ADS_TIER_75K", 
    "name": "activeAdsLimitTier"
  }
]
