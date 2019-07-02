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

compatibleFields_Schema = [
  {
    "mode": "NULLABLE", 
    "type": "STRING", 
    "description": "", 
    "name": "kind"
  }, 
  [
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensions", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "reachByFrequencyMetrics", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "pivotedActivityMetrics", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensionFilters", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "metrics", 
      "mode": "REPEATED"
    }
  ], 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "metrics", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "perInteractionDimensions", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "conversionDimensions", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "customFloodlightVariables", 
      "mode": "REPEATED"
    }
  ], 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "breakdown", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "metrics", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "overlapMetrics", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensionFilters", 
      "mode": "REPEATED"
    }
  ], 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "metrics", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensionFilters", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensions", 
      "mode": "REPEATED"
    }
  ], 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "metrics", 
      "mode": "REPEATED"
    }, 
    {
      "mode": "NULLABLE", 
      "type": "STRING", 
      "description": "", 
      "name": "kind"
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "pivotedActivityMetrics", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensionFilters", 
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
          "type": "STRING", 
          "description": "", 
          "name": "name"
        }
      ], 
      "type": "RECORD", 
      "name": "dimensions", 
      "mode": "REPEATED"
    }
  ]
]
