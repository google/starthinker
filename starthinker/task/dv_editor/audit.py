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

from starthinker.util.data import get_rows
from starthinker.util.data import put_rows
from starthinker.util.sheets import sheets_clear

from starthinker.task.dv_editor.bid_strategy import bid_strategy_audit
from starthinker.task.dv_editor.frequency_cap import frequency_cap_audit
from starthinker.task.dv_editor.integration_detail import integration_detail_audit
from starthinker.task.dv_editor.insertion_order import insertion_order_audit
from starthinker.task.dv_editor.line_item import line_item_audit
from starthinker.task.dv_editor.line_item_map import line_item_map_audit
from starthinker.task.dv_editor.pacing import pacing_audit
from starthinker.task.dv_editor.partner_cost import partner_cost_audit
from starthinker.task.dv_editor.segment import segment_audit


def audit_clear(config, task):
  sheets_clear(
    config,
    task['auth_sheets'],
    task['sheet'],
    'Audit',
    'A2:Z'
  )


def audit_load(config, task):
  bid_strategy_audit(config, task)
  integration_detail_audit(config, task)
  frequency_cap_audit(config, task)
  line_item_map_audit(config, task)
  pacing_audit(config, task)
  partner_cost_audit(config, task)
  segment_audit(config, task)
  insertion_order_audit(config, task)
  line_item_audit(config, task)

  # write audits to sheet
  put_rows(
    config,
    task['auth_sheets'],
    { 'sheets': {
      'sheet': task['sheet'],
      'tab': 'Audit',
      'header':False,
      'range': 'A2'
    }},
    get_rows(
      config,
      task['auth_bigquery'],
      { 'bigquery': {
        'dataset': task['dataset'],
        'query': """SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_InsertionOrders`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_Segments`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_LineItems`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_LineItemMaps`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_Pacing`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_BidStrategy`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_FrequencyCaps`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_PartnerCosts`
          UNION ALL
            SELECT Operation, Severity, Id, Error
            FROM `{dataset}.AUDIT_IntegrationDetails`
        """.format(**task),
        "legacy": False
      }}
    )
  )
