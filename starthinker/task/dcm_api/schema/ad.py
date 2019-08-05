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

ad_Schema = [
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "clickThroughUrlSuffix"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "overrideInheritedSuffix", 
      "mode": "NULLABLE"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "campaignId"
  }, 
  [
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "languageCode"
        }, 
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
          "name": "id"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "languages", 
      "mode": "REPEATED"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "advertiserId"
  }, 
  [
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dartId"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "sslEnabled", 
          "mode": "NULLABLE"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "countryCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "countries", 
      "mode": "REPEATED"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "excludeCountries", 
      "mode": "NULLABLE"
    }, 
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "countryDartId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "code"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "countryCode"
        }
      ], 
      "type": "RECORD", 
      "name": "postalCodes", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
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
          "name": "countryDartId"
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
          "name": "countryCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "regionCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dartId"
        }
      ], 
      "type": "RECORD", 
      "name": "regions", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
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
          "name": "countryDartId"
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
          "name": "countryCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metroCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "regionCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "metroDmaId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dartId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "regionDartId"
        }
      ], 
      "type": "RECORD", 
      "name": "cities", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
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
          "name": "countryDartId"
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
          "name": "countryCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "metroCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dmaId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dartId"
        }
      ], 
      "type": "RECORD", 
      "name": "metros", 
      "mode": "REPEATED"
    }
  ], 
  {
    "fields": [
      {
        "mode": "NULLABLE", 
        "type": "STRING", 
        "description": "CREATIVE_GROUP_ONE, CREATIVE_GROUP_TWO", 
        "name": "creativeGroupNumber"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "creativeGroupId"
      }
    ], 
    "type": "RECORD", 
    "name": "creativeGroupAssignments", 
    "mode": "REPEATED"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "AD_PRIORITY_01, AD_PRIORITY_02, AD_PRIORITY_03, AD_PRIORITY_04, AD_PRIORITY_05, AD_PRIORITY_06, AD_PRIORITY_07, AD_PRIORITY_08, AD_PRIORITY_09, AD_PRIORITY_10, AD_PRIORITY_11, AD_PRIORITY_12, AD_PRIORITY_13, AD_PRIORITY_14, AD_PRIORITY_15, AD_PRIORITY_16", 
      "name": "priority"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "hardCutoff", 
      "mode": "NULLABLE"
    }, 
    [
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "duration"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "impressions"
      }
    ], 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "impressionRatio"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "value"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "dimensionName"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "etag"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
      "name": "matchType"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "id"
    }
  ], 
  {
    "fields": [
      {
        "type": "BOOLEAN", 
        "name": "enabled", 
        "mode": "NULLABLE"
      }, 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "id"
      }
    ], 
    "type": "RECORD", 
    "name": "eventTagOverrides", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "id"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "accountId"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "archived", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "targetingTemplateId"
  }, 
  [
    {
      "fields": [
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
          "name": "id"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "platformTypes", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "majorVersion"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "id"
        }, 
        [
          {
            "type": "BOOLEAN", 
            "name": "mobile", 
            "mode": "NULLABLE"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "dartId"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "kind"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "name"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "desktop", 
            "mode": "NULLABLE"
          }
        ], 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "minorVersion"
        }
      ], 
      "type": "RECORD", 
      "name": "operatingSystemVersions", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "majorVersion"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "browserVersionId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dartId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "minorVersion"
        }
      ], 
      "type": "RECORD", 
      "name": "browsers", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
        {
          "type": "BOOLEAN", 
          "name": "mobile", 
          "mode": "NULLABLE"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "dartId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "desktop", 
          "mode": "NULLABLE"
        }
      ], 
      "type": "RECORD", 
      "name": "operatingSystems", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
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
          "name": "countryDartId"
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
          "description": "", 
          "name": "countryCode"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "mobileCarriers", 
      "mode": "REPEATED"
    }, 
    {
      "fields": [
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
          "name": "id"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "connectionTypes", 
      "mode": "REPEATED"
    }
  ], 
  [
    {
      "fields": [
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "weight"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "sequence"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "applyEventTags", 
          "mode": "NULLABLE"
        }, 
        {
          "fields": [
            [
              {
                "mode": "NULLABLE", 
                "type": "STRING", 
                "description": "", 
                "name": "computedClickThroughUrl"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "STRING", 
                "description": "", 
                "name": "customClickThroughUrl"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "INT64", 
                "description": "", 
                "name": "landingPageId"
              }, 
              {
                "type": "BOOLEAN", 
                "name": "defaultLandingPage", 
                "mode": "NULLABLE"
              }
            ], 
            {
              "type": "BOOLEAN", 
              "name": "enabled", 
              "mode": "NULLABLE"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "exitId"
            }
          ], 
          "type": "RECORD", 
          "name": "richMediaExitOverrides", 
          "mode": "REPEATED"
        }, 
        {
          "type": "BOOLEAN", 
          "name": "sslCompliant", 
          "mode": "NULLABLE"
        }, 
        {
          "fields": [
            {
              "mode": "NULLABLE", 
              "type": "STRING", 
              "description": "CREATIVE_GROUP_ONE, CREATIVE_GROUP_TWO", 
              "name": "creativeGroupNumber"
            }, 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "creativeGroupId"
            }
          ], 
          "type": "RECORD", 
          "name": "creativeGroupAssignments", 
          "mode": "REPEATED"
        }, 
        {
          "fields": [
            [
              {
                "mode": "NULLABLE", 
                "type": "STRING", 
                "description": "", 
                "name": "computedClickThroughUrl"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "STRING", 
                "description": "", 
                "name": "customClickThroughUrl"
              }, 
              {
                "mode": "NULLABLE", 
                "type": "INT64", 
                "description": "", 
                "name": "landingPageId"
              }, 
              {
                "type": "BOOLEAN", 
                "name": "defaultLandingPage", 
                "mode": "NULLABLE"
              }
            ], 
            {
              "mode": "NULLABLE", 
              "type": "INT64", 
              "description": "", 
              "name": "creativeId"
            }
          ], 
          "type": "RECORD", 
          "name": "companionCreativeOverrides", 
          "mode": "REPEATED"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "DATETIME", 
          "description": "", 
          "name": "startTime"
        }, 
        [
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "computedClickThroughUrl"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "customClickThroughUrl"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "INT64", 
            "description": "", 
            "name": "landingPageId"
          }, 
          {
            "type": "BOOLEAN", 
            "name": "defaultLandingPage", 
            "mode": "NULLABLE"
          }
        ], 
        {
          "type": "BOOLEAN", 
          "name": "active", 
          "mode": "NULLABLE"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "INT64", 
          "description": "", 
          "name": "creativeId"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "DATETIME", 
          "description": "", 
          "name": "endTime"
        }, 
        [
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "kind"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "value"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "dimensionName"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "etag"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
            "name": "matchType"
          }, 
          {
            "mode": "NULLABLE", 
            "type": "STRING", 
            "description": "", 
            "name": "id"
          }
        ]
      ], 
      "type": "RECORD", 
      "name": "creativeAssignments", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "WEIGHT_STRATEGY_CUSTOM, WEIGHT_STRATEGY_EQUAL, WEIGHT_STRATEGY_HIGHEST_CTR, WEIGHT_STRATEGY_OPTIMIZED", 
      "name": "weightCalculationStrategy"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "creativeOptimizationConfigurationId"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "CREATIVE_ROTATION_TYPE_RANDOM, CREATIVE_ROTATION_TYPE_SEQUENTIAL", 
      "name": "type"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "computedClickThroughUrl"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "customClickThroughUrl"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "landingPageId"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "defaultLandingPage", 
      "mode": "NULLABLE"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "comments"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "expression"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "value"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "dimensionName"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "etag"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
      "name": "matchType"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "id"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "width"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "type": "BOOLEAN", 
      "name": "iab", 
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
      "type": "INT64", 
      "description": "", 
      "name": "height"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "AD_SERVING_CLICK_TRACKER, AD_SERVING_DEFAULT_AD, AD_SERVING_STANDARD_AD, AD_SERVING_TRACKING", 
    "name": "type"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "sslRequired", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "INT64", 
    "description": "", 
    "name": "audienceSegmentId"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "expression"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "value"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "dimensionName"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "etag"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
      "name": "matchType"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "id"
    }
  ], 
  [
    {
      "type": "BOOLEAN", 
      "name": "overrideInheritedEventTag", 
      "mode": "NULLABLE"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "defaultClickThroughEventTagId"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "time"
    }
  ], 
  {
    "mode": "NULLABLE", 
    "type": "DATETIME", 
    "description": "", 
    "name": "startTime"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "active", 
    "mode": "NULLABLE"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "APP, APP_INTERSTITIAL, DISPLAY, DISPLAY_INTERSTITIAL, IN_STREAM_AUDIO, IN_STREAM_VIDEO", 
    "name": "compatibility"
  }, 
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
    "name": "subaccountId"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "name"
  }, 
  [
    {
      "type": "BOOLEAN", 
      "name": "userLocalTime", 
      "mode": "NULLABLE"
    }, 
    {
      "type": "INT64", 
      "name": "hoursOfDay", 
      "mode": "REPEATED"
    }, 
    {
      "type": "STRING", 
      "name": "daysOfWeek", 
      "mode": "REPEATED"
    }
  ], 
  [
    {
      "mode": "NULLABLE", 
      "type": "INT64", 
      "description": "", 
      "name": "time"
    }
  ], 
  {
    "type": "BOOLEAN", 
    "name": "sslCompliant", 
    "mode": "NULLABLE"
  }, 
  {
    "fields": [
      {
        "type": "BOOLEAN", 
        "name": "active", 
        "mode": "NULLABLE"
      }, 
      [
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "kind"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "value"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "dimensionName"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "etag"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "BEGINS_WITH, CONTAINS, EXACT, WILDCARD_EXPRESSION", 
          "name": "matchType"
        }, 
        {
          "mode": "NULLABLE", 
          "type": "STRING", 
          "description": "", 
          "name": "id"
        }
      ], 
      {
        "mode": "NULLABLE", 
        "type": "INT64", 
        "description": "", 
        "name": "placementId"
      }, 
      {
        "type": "BOOLEAN", 
        "name": "sslRequired", 
        "mode": "NULLABLE"
      }
    ], 
    "type": "RECORD", 
    "name": "placementAssignments", 
    "mode": "REPEATED"
  }, 
  {
    "mode": "NULLABLE", 
    "type": "DATETIME", 
    "description": "", 
    "name": "endTime"
  }, 
  {
    "type": "BOOLEAN", 
    "name": "dynamicClickTracker", 
    "mode": "NULLABLE"
  }
]
