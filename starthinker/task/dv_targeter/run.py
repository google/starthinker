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
from starthinker.task.dv_editor.line_item import line_item_clear
from starthinker.task.dv_editor.partner import partner_clear
from starthinker.task.dv_editor.partner import partner_load
from starthinker.task.dv_editor.patch import patch_clear

from starthinker.task.dv_targeter.advertiser import advertiser_targeting_load
from starthinker.task.dv_targeter.campaign import campaign_clear
from starthinker.task.dv_targeter.campaign import campaign_load
from starthinker.task.dv_targeter.channel import channel_clear
from starthinker.task.dv_targeter.channel import channel_load
from starthinker.task.dv_targeter.combined_audience import combined_audience_clear
from starthinker.task.dv_targeter.combined_audience import combined_audience_load
from starthinker.task.dv_targeter.custom_list import custom_list_clear
from starthinker.task.dv_targeter.custom_list import custom_list_load
from starthinker.task.dv_targeter.first_and_third_party_audience import first_and_third_party_audience_clear
from starthinker.task.dv_targeter.first_and_third_party_audience import first_and_third_party_audience_load
from starthinker.task.dv_targeter.google_audience import google_audience_clear
from starthinker.task.dv_targeter.google_audience import google_audience_load
from starthinker.task.dv_targeter.insertion_order import insertion_order_clear
from starthinker.task.dv_targeter.insertion_order import insertion_order_load
from starthinker.task.dv_targeter.inventory_group import inventory_group_clear
from starthinker.task.dv_targeter.inventory_group import inventory_group_load
from starthinker.task.dv_targeter.inventory_source import inventory_source_clear
from starthinker.task.dv_targeter.inventory_source import inventory_source_load
from starthinker.task.dv_targeter.line_item import line_item_load
from starthinker.task.dv_targeter.line_item import line_item_targeting_load
from starthinker.task.dv_targeter.location_list import location_list_clear
from starthinker.task.dv_targeter.location_list import location_list_load
from starthinker.task.dv_targeter.negative_keyword_list import negative_keyword_list_clear
from starthinker.task.dv_targeter.negative_keyword_list import negative_keyword_list_load
from starthinker.task.dv_targeter.partner import partner_targeting_load
from starthinker.task.dv_targeter.targeting import targeting_audit
from starthinker.task.dv_targeter.targeting import targeting_assigned_clear
from starthinker.task.dv_targeter.targeting import targeting_audit_clear
from starthinker.task.dv_targeter.targeting import targeting_clear
from starthinker.task.dv_targeter.targeting import targeting_load
from starthinker.task.dv_targeter.targeting import targeting_patch

from starthinker.util.bigquery import query_to_view
from starthinker.util.bigquery import table_create
from starthinker.util.google_api.discovery_to_bigquery import Discovery_To_BigQuery
from starthinker.util.sheets import sheets_clear


@project.from_parameters
def dv_targeter():
  print('COMMAND:', project.task['command'])

  #TODO: Change to load groups ( filters, lookups, etc.. )
  if project.task['command'] == 'Clear':
    targeting_audit_clear()
    targeting_assigned_clear()
    line_item_clear()
    campaign_clear()
    channel_clear()
    custom_list_clear()
    combined_audience_clear()
    google_audience_clear()
    inventory_source_clear()
    inventory_group_clear()
    location_list_clear()
    negative_keyword_list_clear()
    first_and_third_party_audience_clear()
    advertiser_clear()
    partner_clear()

  elif project.task['command'] == 'Load Partners':
    partner_clear()
    partner_load()

  elif project.task['command'] == 'Load Advertisers':
    advertiser_clear()
    advertiser_load()

  elif project.task['command'] == 'Load Inventory':
    inventory_source_clear()
    inventory_group_clear()
    inventory_source_load()
    inventory_group_load()

  elif project.task['command'] == 'Load Locations':
    location_list_clear()
    location_list_load()

  elif project.task['command'] == 'Load Keywords':
    negative_keyword_list_clear()
    negative_keyword_list_load()

  elif project.task['command'] == 'Load Channels':
    channel_clear()
    channel_load()

  elif project.task['command'] == 'Load Audiences':
    google_audience_clear()
    custom_list_clear()
    combined_audience_clear()
    first_and_third_party_audience_clear()
    google_audience_load()
    custom_list_load()
    combined_audience_load()
    first_and_third_party_audience_load()

  elif project.task['command'] == 'Load Line Items':
    campaign_clear()
    campaign_load()
    insertion_order_clear()
    insertion_order_load()
    line_item_clear()
    line_item_load()

  elif project.task['command'] == 'Load Targeting':
    targeting_clear()
    targeting_assigned_clear()

    targeting_load()
    partner_targeting_load()
    advertiser_targeting_load()
    line_item_targeting_load()

  elif project.task['command'] in ('Preview', 'Patch'):
    #targeting_audit_clear()
    #patch_clear()

    #targeting_audit()
    targeting_patch(commit=project.task['command'] == 'Patch')

if __name__ == '__main__':
  dv_targeter()
