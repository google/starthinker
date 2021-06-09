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

from starthinker.util.project import from_parameters

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


@from_parameters
def dv_editor(project, task):
  print('COMMAND:', task['command'])

  if task['command'] == 'Load Partners':
    partner_clear(project, task)
    partner_load(project, task)
    pass

  elif task['command'] == 'Load Advertisers':
    advertiser_clear(project, task)
    advertiser_load(project, task)

  elif task['command'] == 'Load Campaigns':
    campaign_clear(project, task)
    campaign_load(project, task)

  elif task['command'] == 'Load Insertion Orders and Line Items':
    creative_clear(project, task)
    creative_load(project, task)
    insertion_order_clear(project, task)
    insertion_order_load(project, task)
    line_item_clear(project, task)
    line_item_load(project, task)
    segment_clear(project, task)
    segment_load(project, task)
    pacing_clear(project, task)
    pacing_load(project, task)
    bid_strategy_clear(project, task)
    bid_strategy_load(project, task)
    frequency_cap_clear(project, task)
    frequency_cap_load(project, task)
    partner_cost_clear(project, task)
    partner_cost_load(project, task)
    integration_detail_clear(project, task)
    integration_detail_load(project, task)

  elif task['command'] in ('Preview', 'Update'):
    audit_clear(project, task)
    patch_clear(project, task)
    audit_load(project, task)

    line_item_insert(project, task, commit=task['command'] == 'Update')
    insertion_order_insert(project, task, commit=task['command'] == 'Update')

    insertion_order_patch(project, task, commit=task['command'] == 'Update')
    line_item_patch(project, task, commit=task['command'] == 'Update')
    line_item_map_patch(project, task, commit=task['command'] == 'Update')

    segment_patch(project, task, commit=task['command'] == 'Update')
    pacing_patch(project, task, commit=task['command'] == 'Update')
    bid_strategy_patch(project, task, commit=task['command'] == 'Update')
    frequency_cap_patch(project, task, commit=task['command'] == 'Update')
    partner_cost_patch(project, task, commit=task['command'] == 'Update')
    integration_detail_patch(project, task, commit=task['command'] == 'Update')

  elif task['command'] == 'Clear Partners':
    partner_clear(project, task)

  elif task['command'] == 'Clear Advertisers':
    advertiser_clear(project, task)

  elif task['command'] == 'Clear Campaigns':
    campaign_clear(project, task)

  elif task['command'] == 'Clear Insertion Orders and Line Items':
    creative_clear(project, task)

    segment_clear(project, task)
    pacing_clear(project, task)
    bid_strategy_clear(project, task)
    frequency_cap_clear(project, task)
    partner_cost_clear(project, task)
    integration_detail_clear(project, task)

    insertion_order_clear(project, task)
    line_item_map_clear(project, task)
    line_item_clear(project, task)

  elif task['command'] == 'Clear Preview':
    audit_clear(project, task)

  elif task['command'] == 'Clear Update':
    patch_clear(project, task)

  elif task['command'] == 'Clear All':
    partner_clear(project, task)
    advertiser_clear(project, task)
    campaign_clear(project, task)
    creative_clear(project, task)

    segment_clear(project, task)
    pacing_clear(project, task)
    bid_strategy_clear(project, task)
    frequency_cap_clear(project, task)
    partner_cost_clear(project, task)
    integration_detail_clear(project, task)

    insertion_order_clear(project, task)
    line_item_map_clear(project, task)
    line_item_clear(project, task)

    audit_clear(project, task)
    patch_clear(project, task)

if __name__ == '__main__':
  dv_editor()
