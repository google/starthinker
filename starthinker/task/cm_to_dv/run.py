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

from starthinker.util import has_values
from starthinker.util.data import get_rows

from starthinker.task.cm_to_dv.cm_account import cm_account_clear
from starthinker.task.cm_to_dv.cm_account import cm_account_load

from starthinker.task.cm_to_dv.cm_advertiser import cm_advertiser_clear
from starthinker.task.cm_to_dv.cm_advertiser import cm_advertiser_load

from starthinker.task.cm_to_dv.cm_campaign import cm_campaign_clear
from starthinker.task.cm_to_dv.cm_campaign import cm_campaign_load

from starthinker.task.cm_to_dv.cm_placement import cm_placement_clear
from starthinker.task.cm_to_dv.cm_placement import cm_placement_load

from starthinker.task.cm_to_dv.cm_placement_group import cm_placement_group_clear
from starthinker.task.cm_to_dv.cm_placement_group import cm_placement_group_load

from starthinker.task.cm_to_dv.cm_profile import cm_profile_clear
from starthinker.task.cm_to_dv.cm_profile import cm_profile_load

from starthinker.task.cm_to_dv.cm_site import cm_site_clear
from starthinker.task.cm_to_dv.cm_site import cm_site_load

from starthinker.task.cm_to_dv.dv_advertiser import dv_advertiser_clear
from starthinker.task.cm_to_dv.dv_advertiser import dv_advertiser_load

from starthinker.task.cm_to_dv.dv_algorithm import dv_algorithm_clear
from starthinker.task.cm_to_dv.dv_algorithm import dv_algorithm_load

from starthinker.task.cm_to_dv.dv_campaign import dv_campaign_clear
from starthinker.task.cm_to_dv.dv_campaign import dv_campaign_load

from starthinker.task.cm_to_dv.dv_insertion_order import dv_insertion_order_clear
from starthinker.task.cm_to_dv.dv_insertion_order import dv_insertion_order_load

from starthinker.task.cm_to_dv.dv_line_item import dv_line_item_clear
from starthinker.task.cm_to_dv.dv_line_item import dv_line_item_load

from starthinker.task.cm_to_dv.dv_partner import dv_partner_clear
from starthinker.task.cm_to_dv.dv_partner import dv_partner_load

from starthinker.task.cm_to_dv.preview_io import preview_io_clear
from starthinker.task.cm_to_dv.preview_io import preview_io_load
from starthinker.task.cm_to_dv.preview_io import preview_io_insert

from starthinker.task.cm_to_dv.preview_li import preview_li_clear
from starthinker.task.cm_to_dv.preview_li import preview_li_load
from starthinker.task.cm_to_dv.preview_li import preview_li_insert

from starthinker.task.cm_to_dv.log import log_clear
from starthinker.task.cm_to_dv.log import log_clear

def cm_to_dv(config, task):
  print('COMMAND:', task['command'])

  if task['command'] == 'Clear':

    dv_line_item_clear(config, task)
    dv_insertion_order_clear(config, task)
    dv_campaign_clear(config, task)
    dv_advertiser_clear(config, task)
    dv_algorithm_clear(config, task)
    dv_partner_clear(config, task)

    cm_profile_clear(config, task)
    cm_account_clear(config, task)
    cm_advertiser_clear(config, task)
    cm_campaign_clear(config, task)
    cm_placement_clear(config, task)
    cm_placement_group_clear(config, task)
    cm_site_clear(config, task)

    preview_io_clear(config, task)
    preview_li_clear(config, task)
    log_clear(config, task)

  elif task['command'] == 'Load':

    # load if profile filters are missing
    if not has_values(get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'CM Profiles',
        'header':False,
        'range': 'A2:A'
      }}
    )):
      print('CM Profile Load')
      cm_profile_load(config, task)

    # load if account filters are missing
    elif not has_values(get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'CM Accounts',
        'header':False,
        'range': 'A2:A'
      }}
    )):
      cm_account_load(config, task)

    # load if advertiser filters are missing
    elif not has_values(get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'CM Advertisers',
        'header':False,
        'range': 'A2:A'
      }}
    )):
      print('CM Advertiser Load')
      cm_advertiser_load(config, task)

    # load if advertiser filters are missing
    elif not has_values(get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'CM Campaigns',
        'header':False,
        'range': 'A2:A'
      }}
    )):
      print('CM Campaigns Load')
      cm_campaign_load(config, task)

    else:
      print('CM Placement Load')
      cm_placement_load(config, task)
      cm_placement_group_load(config, task)
      cm_site_load(config, task)


    # load if partner filters are missing
    if not has_values(get_rows(
      config,
      task['auth_sheets'],
      { 'sheets': {
        'sheet': task['sheet'],
        'tab': 'DV Partners',
        'header':False,
        'range': 'A2:A'
      }}
    )):
      print('DV Partner Load')
      dv_partner_load(config, task)

    # load if advertiser filters are missing
    elif not has_values(get_rows(
        config,
        task['auth_sheets'],
        { 'sheets': {
          'sheet': task['sheet'],
          'tab': 'DV Advertisers',
          'header':False,
          'range': 'A2:A'
        }}
      )):
        print('DV Advertiser Load')
        dv_advertiser_load(config, task)

    # load if advertiser filters are present
    else:
      print('DV Campaign / IO / LI Load')
      dv_algorithm_load(config, task)
      dv_campaign_load(config, task)
      dv_insertion_order_load(config, task)
      dv_line_item_load(config, task)

  elif task['command'] == 'Preview':
    log_clear(config, task)
    preview_io_load(config, task)
    preview_li_load(config, task)

  elif task['command'] == 'Insert':
    log_clear(config, task)
    preview_io_insert(config, task)
    preview_li_insert(config, task)
