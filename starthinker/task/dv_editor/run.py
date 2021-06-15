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

from starthinker.task.dv_editor.advertiser import advertiser_clear
from starthinker.task.dv_editor.advertiser import advertiser_load
from starthinker.task.dv_editor.audit import audit_clear
from starthinker.task.dv_editor.audit import audit_load
from starthinker.task.dv_editor.bid_strategy import bid_strategy_clear
from starthinker.task.dv_editor.bid_strategy import bid_strategy_load
from starthinker.task.dv_editor.bid_strategy import bid_strategy_patch
from starthinker.task.dv_editor.campaign import campaign_clear
from starthinker.task.dv_editor.campaign import campaign_load
from starthinker.task.dv_editor.creative import creative_clear
from starthinker.task.dv_editor.creative import creative_load
from starthinker.task.dv_editor.frequency_cap import frequency_cap_clear
from starthinker.task.dv_editor.frequency_cap import frequency_cap_load
from starthinker.task.dv_editor.frequency_cap import frequency_cap_patch
from starthinker.task.dv_editor.insertion_order import insertion_order_clear
from starthinker.task.dv_editor.insertion_order import insertion_order_insert
from starthinker.task.dv_editor.insertion_order import insertion_order_load
from starthinker.task.dv_editor.insertion_order import insertion_order_patch
from starthinker.task.dv_editor.integration_detail import integration_detail_clear
from starthinker.task.dv_editor.integration_detail import integration_detail_load
from starthinker.task.dv_editor.integration_detail import integration_detail_patch
from starthinker.task.dv_editor.line_item import line_item_clear
from starthinker.task.dv_editor.line_item import line_item_insert
from starthinker.task.dv_editor.line_item import line_item_load
from starthinker.task.dv_editor.line_item import line_item_patch
from starthinker.task.dv_editor.line_item_map import line_item_map_clear
from starthinker.task.dv_editor.line_item_map import line_item_map_patch
from starthinker.task.dv_editor.pacing import pacing_clear
from starthinker.task.dv_editor.pacing import pacing_load
from starthinker.task.dv_editor.pacing import pacing_patch
from starthinker.task.dv_editor.patch import patch_clear
from starthinker.task.dv_editor.partner import partner_clear
from starthinker.task.dv_editor.partner import partner_load
from starthinker.task.dv_editor.partner_cost import partner_cost_clear
from starthinker.task.dv_editor.partner_cost import partner_cost_load
from starthinker.task.dv_editor.partner_cost import partner_cost_patch
from starthinker.task.dv_editor.segment import segment_clear
from starthinker.task.dv_editor.segment import segment_load
from starthinker.task.dv_editor.segment import segment_patch


def dv_editor(config, task):
  print('COMMAND:', task['command'])

  if task['command'] == 'Load Partners':
    partner_clear(config, task)
    partner_load(config, task)
    pass

  elif task['command'] == 'Load Advertisers':
    advertiser_clear(config, task)
    advertiser_load(config, task)

  elif task['command'] == 'Load Campaigns':
    campaign_clear(config, task)
    campaign_load(config, task)

  elif task['command'] == 'Load Insertion Orders and Line Items':
    creative_clear(config, task)
    creative_load(config, task)
    insertion_order_clear(config, task)
    insertion_order_load(config, task)
    line_item_clear(config, task)
    line_item_load(config, task)
    segment_clear(config, task)
    segment_load(config, task)
    pacing_clear(config, task)
    pacing_load(config, task)
    bid_strategy_clear(config, task)
    bid_strategy_load(config, task)
    frequency_cap_clear(config, task)
    frequency_cap_load(config, task)
    partner_cost_clear(config, task)
    partner_cost_load(config, task)
    integration_detail_clear(config, task)
    integration_detail_load(config, task)

  elif task['command'] in ('Preview', 'Update'):
    audit_clear(config, task)
    patch_clear(config, task)
    audit_load(config, task)

    line_item_insert(config, task, commit=task['command'] == 'Update')
    insertion_order_insert(config, task, commit=task['command'] == 'Update')

    insertion_order_patch(config, task, commit=task['command'] == 'Update')
    line_item_patch(config, task, commit=task['command'] == 'Update')
    line_item_map_patch(config, task, commit=task['command'] == 'Update')

    segment_patch(config, task, commit=task['command'] == 'Update')
    pacing_patch(config, task, commit=task['command'] == 'Update')
    bid_strategy_patch(config, task, commit=task['command'] == 'Update')
    frequency_cap_patch(config, task, commit=task['command'] == 'Update')
    partner_cost_patch(config, task, commit=task['command'] == 'Update')
    integration_detail_patch(config, task, commit=task['command'] == 'Update')

  elif task['command'] == 'Clear Partners':
    partner_clear(config, task)

  elif task['command'] == 'Clear Advertisers':
    advertiser_clear(config, task)

  elif task['command'] == 'Clear Campaigns':
    campaign_clear(config, task)

  elif task['command'] == 'Clear Insertion Orders and Line Items':
    creative_clear(config, task)

    segment_clear(config, task)
    pacing_clear(config, task)
    bid_strategy_clear(config, task)
    frequency_cap_clear(config, task)
    partner_cost_clear(config, task)
    integration_detail_clear(config, task)

    insertion_order_clear(config, task)
    line_item_map_clear(config, task)
    line_item_clear(config, task)

  elif task['command'] == 'Clear Preview':
    audit_clear(config, task)

  elif task['command'] == 'Clear Update':
    patch_clear(config, task)

  elif task['command'] == 'Clear All':
    partner_clear(config, task)
    advertiser_clear(config, task)
    campaign_clear(config, task)
    creative_clear(config, task)

    segment_clear(config, task)
    pacing_clear(config, task)
    bid_strategy_clear(config, task)
    frequency_cap_clear(config, task)
    partner_cost_clear(config, task)
    integration_detail_clear(config, task)

    insertion_order_clear(config, task)
    line_item_map_clear(config, task)
    line_item_clear(config, task)

    audit_clear(config, task)
    patch_clear(config, task)
