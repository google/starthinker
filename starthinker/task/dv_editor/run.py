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

from starthinker.util.project import project

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
from starthinker.task.dv_editor.insertion_order import insertion_order_audit
from starthinker.task.dv_editor.insertion_order import insertion_order_clear
from starthinker.task.dv_editor.insertion_order import insertion_order_insert
from starthinker.task.dv_editor.insertion_order import insertion_order_load
from starthinker.task.dv_editor.insertion_order import insertion_order_patch
from starthinker.task.dv_editor.integration_detail import integration_detail_clear
from starthinker.task.dv_editor.integration_detail import integration_detail_load
from starthinker.task.dv_editor.integration_detail import integration_detail_patch
from starthinker.task.dv_editor.line_item import line_item_audit
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


@project.from_parameters
def dv_editor():
  print('COMMAND:', project.task['command'])

  if project.task['command'] == 'Load Partners':
    partner_clear()
    partner_load()

  elif project.task['command'] == 'Load Advertisers':
    advertiser_clear()
    advertiser_load()

  elif project.task['command'] == 'Load Campaigns':
    campaign_clear()
    campaign_load()

  elif project.task['command'] == 'Load Insertion Orders and Line Items':
    creative_clear()
    creative_load()
    insertion_order_clear()
    insertion_order_load()
    line_item_clear()
    line_item_load()
    segment_clear()
    segment_load()
    pacing_clear()
    pacing_load()
    bid_strategy_clear()
    bid_strategy_load()
    frequency_cap_clear()
    frequency_cap_load()
    partner_cost_clear()
    partner_cost_load()
    integration_detail_clear()
    integration_detail_load()

  elif project.task['command'] in ('Preview', 'Patch'):
    audit_clear()
    patch_clear()
    audit_load()

    line_item_insert(commit=project.task['command'] == 'Patch')
    insertion_order_insert(commit=project.task['command'] == 'Patch')

    insertion_order_patch(commit=project.task['command'] == 'Patch')
    line_item_patch(commit=project.task['command'] == 'Patch')
    line_item_map_patch(commit=project.task['command'] == 'Patch')

    segment_patch(commit=project.task['command'] == 'Patch')
    pacing_patch(commit=project.task['command'] == 'Patch')
    bid_strategy_patch(commit=project.task['command'] == 'Patch')
    frequency_cap_patch(commit=project.task['command'] == 'Patch')
    partner_cost_patch(commit=project.task['command'] == 'Patch')
    integration_detail_patch(commit=project.task['command'] == 'Patch')

  elif project.task['command'] == 'Clear Partners':
    partner_clear()

  elif project.task['command'] == 'Clear Advertisers':
    advertiser_clear()

  elif project.task['command'] == 'Clear Campaigns':
    campaign_clear()

  elif project.task['command'] == 'Clear Insertion Orders and Line Items':
    creative_clear()

    segment_clear()
    pacing_clear()
    bid_strategy_clear()
    frequency_cap_clear()
    partner_cost_clear()
    integration_detail_clear()

    insertion_order_clear()
    line_item_map_clear()
    line_item_clear()

  elif project.task['command'] == 'Clear Preview':
    audit_clear()

  elif project.task['command'] == 'Clear Patch':
    patch_clear()

  elif project.task['command'] == 'Clear All':
    partner_clear()
    advertiser_clear()
    campaign_clear()
    creative_clear()

    segment_clear()
    pacing_clear()
    bid_strategy_clear()
    frequency_cap_clear()
    partner_cost_clear()
    integration_detail_clear()

    insertion_order_clear()
    line_item_map_clear()
    line_item_clear()

    audit_clear()
    patch_clear()

if __name__ == '__main__':
  dv_editor()
