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

'''
ITP Audit Dashboard

Dashboard that shows performance metrics across browser to see the impact of ITP.

Follow the steps in the below document
https://docs.google.com/document/d/1HaRCMaBBEo0tSKwnofWNtaPjlW0ORcVHVwIRabct4fY/edit?usp=sharing

'''

from starthinker_airflow.factory import DAG_Factory
 
USER_CONN_ID = "google_cloud_default" # The connection to use for user authentication.
GCP_CONN_ID = "" # The connection to use for service authentication.

INPUTS = {
  "dataset":"ITP_Audit_Dashboard", # BigQuery dataset for store dashboard tables.
  "sheet_url":"", # Sheet URL for the Segments sheet.
  "cm_account_id":"", # Campaign Manager Account Id.
  "advertiser_ids":"", # Comma separated list of Campaign Manager Advertiser Ids.  Leave blank for no advertiser filtering.
  "floodlight_configuration_id":, # Floodlight Configuration Id for the Campaign Manager floodlight report.
  "floodlight_report_name":"ITP_Audit_Dashboard_Floodlight", # Campaign Manager Floodlight report name.
  "dv360_report_name":"ITP_Audit_Browser_Report", # DV360 Browser report name.
  "cm_browser_report_name":"ITP_Audit_Dashboard_Browser", # Name of the Campaign Manager browser report.
}

TASKS = [
  {
    "dataset": {
      "auth": "service",
      "dataset": {
        "field": {
          "name": "dataset",
          "kind": "string",
          "order": 1,
          "default": "ITP_Audit_Dashboard",
          "description": "BigQuery dataset for store dashboard tables."
        }
      }
    }
  },
  {
    "dcm": {
      "auth": "user",
      "timeout": 60,
      "report": {
        "account": {
          "field": {
            "name": "cm_account_id",
            "kind": "string",
            "order": 3,
            "default": "",
            "description": "Campaign Manager Account Id."
          }
        },
        "body": {
          "kind": "dfareporting#report",
          "name": {
            "field": {
              "name": "floodlight_report_name",
              "kind": "string",
              "order": 8,
              "default": "ITP_Audit_Dashboard_Floodlight",
              "description": "Campaign Manager Floodlight report name."
            }
          },
          "fileName": {
            "field": {
              "name": "floodlight_report_name",
              "kind": "string",
              "order": 8,
              "default": "ITP_Audit_Dashboard_Floodlight",
              "description": "Campaign Manager Floodlight report name."
            }
          },
          "format": "CSV",
          "type": "FLOODLIGHT",
          "floodlightCriteria": {
            "dateRange": {
              "kind": "dfareporting#dateRange",
              "relativeDateRange": "LAST_30_DAYS"
            },
            "floodlightConfigId": {
              "kind": "dfareporting#dimensionValue",
              "dimensionName": "dfa:floodlightConfigId",
              "value": {
                "field": {
                  "name": "floodlight_configuration_id",
                  "kind": "integer",
                  "order": 7,
                  "default": "",
                  "description": "Floodlight Configuration Id for the Campaign Manager floodlight report."
                }
              },
              "matchType": "EXACT"
            },
            "reportProperties": {
              "includeUnattributedIPConversions": false,
              "includeUnattributedCookieConversions": true
            },
            "dimensions": [
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:site"
              },
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:floodlightAttributionType"
              },
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:interactionType"
              },
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:pathType"
              },
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:browserPlatform"
              },
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:platformType"
              },
              {
                "kind": "dfareporting#sortedDimension",
                "name": "dfa:week"
              }
            ],
            "metricNames": [
              "dfa:activityClickThroughConversions",
              "dfa:activityViewThroughConversions",
              "dfa:totalConversions",
              "dfa:totalConversionsRevenue"
            ]
          },
          "schedule": {
            "active": true,
            "repeats": "DAILY",
            "every": 1,
            "startDate": "2019-09-11",
            "expirationDate": "2029-12-10"
          },
          "delivery": {
            "emailOwner": false
          }
        }
      },
      "out": {
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "Floodlight_CM_Report",
          "is_incremental_load": false
        }
      },
      "delete": false
    }
  },
  {
    "dbm": {
      "auth": "user",
      "datastudio": true,
      "report": {
        "name": {
          "field": {
            "name": "dv360_report_name",
            "kind": "string",
            "order": 8,
            "default": "ITP_Audit_Browser_Report",
            "description": "DV360 Browser report name."
          }
        }
      },
      "out": {
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "Dv360_Browser_Report_Dirty",
          "autodetect_schema": true,
          "is_incremental_load": false
        }
      }
    }
  },
  {
    "sheets": {
      "auth": "user",
      "sheet": {
        "field": {
          "name": "sheet_url",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Sheet URL for the Segments sheet."
        }
      },
      "tab": "Enviroment",
      "range": "A:B",
      "header": true,
      "out": {
        "auth": "service",
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "Environment"
        }
      }
    }
  },
  {
    "sheets": {
      "auth": "user",
      "sheet": {
        "field": {
          "name": "sheet_url",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Sheet URL for the Segments sheet."
        }
      },
      "tab": "Browser",
      "range": "A:C",
      "header": true,
      "out": {
        "auth": "service",
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "Browser"
        }
      }
    }
  },
  {
    "sheets": {
      "auth": "user",
      "sheet": {
        "field": {
          "name": "sheet_url",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Sheet URL for the Segments sheet."
        }
      },
      "tab": "CM_Site_Segments",
      "range": "A:C",
      "header": true,
      "out": {
        "auth": "service",
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "CM_Browser_lookup"
        }
      }
    }
  },
  {
    "sheets": {
      "auth": "user",
      "sheet": {
        "field": {
          "name": "sheet_url",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Sheet URL for the Segments sheet."
        }
      },
      "tab": "Device_Type",
      "range": "A:B",
      "header": true,
      "out": {
        "auth": "service",
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "Device_Type"
        }
      }
    }
  },
  {
    "sheets": {
      "auth": "user",
      "sheet": {
        "field": {
          "name": "sheet_url",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Sheet URL for the Segments sheet."
        }
      },
      "tab": "Floodlight_Attribution",
      "range": "A:B",
      "header": true,
      "out": {
        "auth": "service",
        "bigquery": {
          "dataset": {
            "field": {
              "name": "dataset",
              "kind": "string",
              "order": 1,
              "default": "ITP_Audit_Dashboard",
              "description": "BigQuery dataset for store dashboard tables."
            }
          },
          "table": "Floodlight_Attribution"
        }
      }
    }
  },
  {
    "itp_audit": {
      "auth": "service",
      "account": {
        "field": {
          "name": "cm_account_id",
          "kind": "string",
          "order": 3,
          "default": "",
          "description": "Campaign Manager Account Id."
        }
      },
      "dataset": {
        "field": {
          "name": "dataset",
          "kind": "string",
          "order": 1,
          "default": "ITP_Audit_Dashboard",
          "description": "BigQuery dataset for store dashboard tables."
        }
      },
      "sheet": {
        "field": {
          "name": "sheet_url",
          "kind": "string",
          "order": 2,
          "default": "",
          "description": "Sheet URL for the Segments sheet."
        }
      },
      "cm_browser_report_name": {
        "field": {
          "name": "cm_browser_report_name",
          "kind": "string",
          "order": 9,
          "default": "ITP_Audit_Dashboard_Browser",
          "description": "Name of the Campaign Manager browser report."
        }
      },
      "advertiser_ids": {
        "field": {
          "name": "advertiser_ids",
          "kind": "string",
          "order": 5,
          "default": "",
          "description": "Comma separated list of Campaign Manager Advertiser Ids.  Leave blank for no advertiser filtering."
        }
      },
      "timeout": 60
    }
  }
]

DAG_FACTORY = DAG_Factory('itp_audit', { 'tasks':TASKS }, INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == "__main__":
  DAG_FACTORY.print_commandline()
