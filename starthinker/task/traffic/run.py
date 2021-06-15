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
"""Main entry point of Bulkdozer."""

import traceback

from starthinker.util.cm import get_profile_for_api
from starthinker.util.sheets import sheets_get

from starthinker.task.traffic.feed import Feed
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.ad import AdDAO
from starthinker.task.traffic.creative_assets import CreativeAssetDAO
from starthinker.task.traffic.creative_association import CreativeAssociationDAO
from starthinker.task.traffic.creative import CreativeDAO
from starthinker.task.traffic.campaign import CampaignDAO
from starthinker.task.traffic.dynamic_targeting_key import DynamicTargetingKeyDAO
from starthinker.task.traffic.event_tag import EventTagDAO
from starthinker.task.traffic.landing_page import LandingPageDAO
from starthinker.task.traffic.placement import PlacementDAO
from starthinker.task.traffic.placement_group import PlacementGroupDAO
from starthinker.task.traffic.video_format import VideoFormatDAO
from starthinker.task.traffic.store import store
from starthinker.task.traffic.logger import logger

video_format_dao = None
landing_page_dao = None
placement_group_dao = None
campaign_dao = None
creative_association_dao = None
creative_dao = None
placement_dao = None
creative_asset_dao = None
ad_dao = None
event_tag_dao = None
dynamic_targeting_key_dao = None
spreadsheet = None

clean_run = True


def process_feed(config, task, feed_name, dao, print_field, msg='Processing'):
  """Processes a feed that represents a specific entity in the Bulkdozer feed.

  Args:
    feed_name: Name of the feed to process, refer to feed.py for the supported
      feed names.
    dao: The data access object to be used to interact with the CM API and
      update, must match the entity being updated in CM, in the sense that the
      required fields to fetch, create, and update the entity in CM must be
      included in the feed.
    print_field: Field that identifies the item, used to print status messages
      to the Log tab of the Bulkdozer feed.
    msg: Prefix message to use when writing to the Log tab of the Bulkdozer
      feed, for instance we display Processing Campaign for campaign, and
      Uploading Asset for assets.
  """
  feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      feed_name,
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  execute_feed(feed, dao, print_field, msg)


def execute_feed(feed, dao, print_field, msg='Processing'):
  """Executes a specific feed.

  Args:
    feed: Feed object representing the Bulkdozer feed to process.
    dao: The data access object to be used to interact with the CM API and
      update, must match the entity being updated in CM, in the sense that the
      required fields to fetch, create, and update the entity in CM must be
      included in the feed.
    print_field: Field that identifies the item, used to print status messages
      to the Log tab of the Bulkdozer feed.
    msg: Prefix message to use when writing to the Log tab of the Bulkdozer
      feed, for instance we display Processing Campaign for campaign, and
      Uploading Asset for assets.
  """
  global clean_run

  try:
    dao.pre_fetch(feed.feed)

    for feed_item in feed.feed:
      try:
        value = feed_item[print_field]
        print('%s %s' % (msg, value))
        logger.log('%s %s' % (msg, value))
        dao.process(feed_item)
      except Exception as error:
        clean_run = False
        stack = traceback.format_exc()
        print(stack)
        logger.log(str(error))

  finally:
    feed.update()


def setup(config, task):
  """Sets up Bulkdozer configuration and required object to execute the job."""

  if 'dcm_profile_id' not in task and 'account_id' in task:
    task['is_admin'], task[
        'dcm_profile_id'] = get_profile_for_api(config, task['auth'],
                                                task['account_id'])

  if 'is_admin' not in task:
    task['is_admin'] = False

  if 'sheet_url' in task and 'sheet_id' not in task:
    task['sheet_id'] = task['sheet_url']

  # Setting up required objects and parsing parameters
  logger.config = config
  logger.auth = task['auth']
  logger.trix_id = task.get('logger', {}).get('sheet_id',
                                                      task['sheet_id'])
  logger.buffered = True


def init_daos(config, task):
  global video_format_dao
  global landing_page_dao
  global placement_group_dao
  global campaign_dao
  global creative_association_dao
  global creative_dao
  global placement_dao
  global creative_asset_dao
  global ad_dao
  global event_tag_dao
  global dynamic_targeting_key_dao
  global spreadsheet

  spreadsheet = sheets_get(config, task['auth'], task['sheet_id'])

  #store.auth = task['auth']
  #store.trix_id = task.get('store', {}).get('sheet_id', task['sheet_id'])
  #store.load_id_map()

  video_format_dao = VideoFormatDAO(config, task['auth'],
                                    task['dcm_profile_id'],
                                    task['is_admin'])
  landing_page_dao = LandingPageDAO(config, task['auth'],
                                    task['dcm_profile_id'],
                                    task['is_admin'])
  placement_group_dao = PlacementGroupDAO(config, task['auth'],
                                          task['dcm_profile_id'],
                                          task['is_admin'])
  campaign_dao = CampaignDAO(config, task['auth'],
                             task['dcm_profile_id'],
                             task['is_admin'])
  creative_association_dao = CreativeAssociationDAO(
      config, task['auth'], task['dcm_profile_id'],
      task['is_admin'])
  creative_dao = CreativeDAO(config, task['auth'],
                             task['dcm_profile_id'],
                             task['is_admin'])
  placement_dao = PlacementDAO(config, task['auth'],
                               task['dcm_profile_id'],
                               task['is_admin'])
  creative_asset_dao = CreativeAssetDAO(config, task['auth'],
                                        task['dcm_profile_id'],
                                        task['is_admin'], config.project)
  ad_dao = AdDAO(config, task['auth'], task['dcm_profile_id'],
                 task['is_admin'])
  event_tag_dao = EventTagDAO(config, task['auth'],
                              task['dcm_profile_id'],
                              task['is_admin'])
  dynamic_targeting_key_dao = DynamicTargetingKeyDAO(
      config, task['auth'], task['dcm_profile_id'],
      task['is_admin'])


def assets(config, task):
  """Processes assets."""
  process_feed(config, task, 'creative_asset_feed', creative_asset_dao,
               FieldMap.CREATIVE_ASSET_FILE_NAME, 'Uploading creative asset')


def landing_pages(config, task):
  """Processes landing pages."""
  process_feed(config, task, 'landing_page_feed', landing_page_dao,
               FieldMap.CAMPAIGN_LANDING_PAGE_NAME, 'Processing landing page')


def placement_groups(config, task):
  """Processes placement group."""
  process_feed(config, task, 'placement_group_feed', placement_group_dao,
               FieldMap.PLACEMENT_GROUP_NAME, 'Processing placement group')


def campaigns(config, task):
  """Processes campaigns."""
  process_feed(config, task, 'campaign_feed', campaign_dao, FieldMap.CAMPAIGN_NAME,
               'Processing campaign')


def event_tags(config, task):
  """Processes event tags."""
  process_feed(config, task, 'event_tag_feed', event_tag_dao, FieldMap.EVENT_TAG_NAME,
               'Processing event tag')


def placements(config, task):
  """Processes placements."""
  placement_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'placement_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  pricing_schedule_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'placement_pricing_schedule_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  transcode_configs_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'transcode_configs_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  placement_dao.map_placement_transcode_configs(placement_feed.feed,
                                                transcode_configs_feed.feed,
                                                pricing_schedule_feed.feed)

  execute_feed(placement_feed, placement_dao, FieldMap.PLACEMENT_NAME,
               'Processing placement')

  pricing_schedule_feed.update()


def creatives(config, task):
  """Processes creatives."""
  creative_asset_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'creative_asset_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  creative_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'creative_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  third_party_url_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'third_party_url_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  creative_association_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'creative_asset_association_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  click_tag_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'click_tag_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  creative_dao.map_creative_third_party_url_feeds(creative_feed.feed,
                                                  third_party_url_feed.feed)

  creative_dao.map_creative_click_tag_feeds(creative_feed.feed,
                                            click_tag_feed.feed)

  third_party_url_feed.update()

  creative_dao.map_creative_and_association_feeds(
      creative_feed.feed, creative_association_feed.feed)

  creative_dao.map_assets_feed(creative_asset_feed)

  execute_feed(creative_feed, creative_dao, FieldMap.CREATIVE_NAME,
               'Processing creative')

  execute_feed(creative_association_feed, creative_association_dao,
               FieldMap.CREATIVE_ID, 'Associating with campaign, creative id')

  creative_association_feed.update()

  click_tag_feed.update()


def ads(config, task):
  """Processes ads."""
  placement_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'placement_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))
  event_tag_profile_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'event_tag_profile_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))
  ad_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'ad_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))
  ad_creative_assignment_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'ad_creative_assignment_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  ad_placement_assignment_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'ad_placement_assignment_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))
  ad_event_tag_assignment_feed = Feed(
      config, task['auth'],
      task['sheet_id'],
      'event_tag_ad_assignment_feed',
      spreadsheet=spreadsheet,
      timezone=task.get('timezone', None))

  ad_dao.map_feeds(ad_feed.feed, ad_creative_assignment_feed.feed,
                   ad_placement_assignment_feed.feed,
                   ad_event_tag_assignment_feed.feed, placement_feed.feed,
                   event_tag_profile_feed.feed)
  execute_feed(ad_feed, ad_dao, FieldMap.AD_ID, 'Processing Ad')

  ad_creative_assignment_feed.update()
  ad_placement_assignment_feed.update()
  ad_event_tag_assignment_feed.update()
  event_tag_profile_feed.update()


def dynamic_targeting_keys(config, task):
  """Processes dynamic targeting keys."""
  process_feed(config, task, 'dynamic_targeting_key_feed', dynamic_targeting_key_dao,
               FieldMap.DYNAMIC_TARGETING_KEY_NAME,
               'Processing dynamic targeting key')


def traffic(config, task):
  """Main function of Bulkdozer, performs the Bulkdozer job"""
  global clean_run
  if config.verbose:
    print('traffic')

  try:
    setup(config, task)

    logger.clear()
    logger.log('Bulkdozer traffic job starting')
    logger.flush()

    init_daos(config, task)
    assets(config, task)
    landing_pages(config, task)
    campaigns(config, task)
    event_tags(config, task)
    placement_groups(config, task)
    placements(config, task)
    creatives(config, task)
    ads(config, task)
    dynamic_targeting_keys(config, task)

    #if clean_run:
    #  store.clear()

  except Exception as error:
    stack = traceback.format_exc()
    print(stack)

    logger.log(str(error))

  finally:
    logger.log('Bulkdozer traffic job ended')
    logger.flush()
    #store.save_id_map()

  if clean_run:
    print('Done: Clean run.')
  else:
    raise Exception(
        'Done: Errors happened with some of the assets, check your sheet log.')


def _traffic(config, task):
  """For development purposes when debugging a specific entity, this function is handy to run just that entity."""
  setup(config, task)
  init_daos(config, task)
  dynamic_targeting_keys(config, task)
