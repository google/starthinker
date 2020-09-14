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

from starthinker.util.dcm import get_profile_for_api
from starthinker.util.project import project
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


def process_feed(feed_name, dao, print_field, msg='Processing'):
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
      project.task['auth'],
      project.task['sheet_id'],
      feed_name,
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

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


def setup():
  """Sets up Bulkdozer configuration and required object to execute the job."""

  if not 'dcm_profile_id' in project.task and 'account_id' in project.task:
    project.task['is_admin'], project.task[
        'dcm_profile_id'] = get_profile_for_api(project.task['auth'],
                                                project.task['account_id'])

  if not 'is_admin' in project.task:
    project.task['is_admin'] = False

  if 'sheet_url' in project.task and not 'sheet_id' in project.task:
    project.task['sheet_id'] = project.task['sheet_url']

  # Setting up required objects and parsing parameters
  logger.auth = project.task['auth']
  logger.trix_id = project.task.get('logger', {}).get('sheet_id',
                                                      project.task['sheet_id'])
  logger.buffered = True


def init_daos():
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

  spreadsheet = sheets_get(project.task['auth'], project.task['sheet_id'])

  #store.auth = project.task['auth']
  #store.trix_id = project.task.get('store', {}).get('sheet_id', project.task['sheet_id'])
  #store.load_id_map()

  video_format_dao = VideoFormatDAO(project.task['auth'],
                                    project.task['dcm_profile_id'],
                                    project.task['is_admin'])
  landing_page_dao = LandingPageDAO(project.task['auth'],
                                    project.task['dcm_profile_id'],
                                    project.task['is_admin'])
  placement_group_dao = PlacementGroupDAO(project.task['auth'],
                                          project.task['dcm_profile_id'],
                                          project.task['is_admin'])
  campaign_dao = CampaignDAO(project.task['auth'],
                             project.task['dcm_profile_id'],
                             project.task['is_admin'])
  creative_association_dao = CreativeAssociationDAO(
      project.task['auth'], project.task['dcm_profile_id'],
      project.task['is_admin'])
  creative_dao = CreativeDAO(project.task['auth'],
                             project.task['dcm_profile_id'],
                             project.task['is_admin'])
  placement_dao = PlacementDAO(project.task['auth'],
                               project.task['dcm_profile_id'],
                               project.task['is_admin'])
  creative_asset_dao = CreativeAssetDAO(project.task['auth'],
                                        project.task['dcm_profile_id'],
                                        project.task['is_admin'], project.id)
  ad_dao = AdDAO(project.task['auth'], project.task['dcm_profile_id'],
                 project.task['is_admin'])
  event_tag_dao = EventTagDAO(project.task['auth'],
                              project.task['dcm_profile_id'],
                              project.task['is_admin'])
  dynamic_targeting_key_dao = DynamicTargetingKeyDAO(
      project.task['auth'], project.task['dcm_profile_id'],
      project.task['is_admin'])


def assets():
  """Processes assets."""
  process_feed('creative_asset_feed', creative_asset_dao,
               FieldMap.CREATIVE_ASSET_FILE_NAME, 'Uploading creative asset')


def landing_pages():
  """Processes landing pages."""
  process_feed('landing_page_feed', landing_page_dao,
               FieldMap.CAMPAIGN_LANDING_PAGE_NAME, 'Processing landing page')


def placement_groups():
  """Processes placement group."""
  process_feed('placement_group_feed', placement_group_dao,
               FieldMap.PLACEMENT_GROUP_NAME, 'Processing placement group')


def campaigns():
  """Processes campaigns."""
  process_feed('campaign_feed', campaign_dao, FieldMap.CAMPAIGN_NAME,
               'Processing campaign')


def event_tags():
  """Processes event tags."""
  process_feed('event_tag_feed', event_tag_dao, FieldMap.EVENT_TAG_NAME,
               'Processing event tag')


def placements():
  """Processes placements."""
  placement_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'placement_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  pricing_schedule_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'placement_pricing_schedule_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  transcode_configs_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'transcode_configs_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  placement_dao.map_placement_transcode_configs(placement_feed.feed,
                                                transcode_configs_feed.feed,
                                                pricing_schedule_feed.feed)

  execute_feed(placement_feed, placement_dao, FieldMap.PLACEMENT_NAME,
               'Processing placement')

  pricing_schedule_feed.update()


def creatives():
  """Processes creatives."""
  creative_asset_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'creative_asset_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  creative_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'creative_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  third_party_url_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'third_party_url_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  creative_association_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'creative_asset_association_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  click_tag_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'click_tag_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

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


def ads():
  """Processes ads."""
  placement_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'placement_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))
  event_tag_profile_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'event_tag_profile_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))
  ad_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'ad_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))
  ad_creative_assignment_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'ad_creative_assignment_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  ad_placement_assignment_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'ad_placement_assignment_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))
  ad_event_tag_assignment_feed = Feed(
      project.task['auth'],
      project.task['sheet_id'],
      'event_tag_ad_assignment_feed',
      spreadsheet=spreadsheet,
      timezone=project.task.get('timezone', None))

  ad_dao.map_feeds(ad_feed.feed, ad_creative_assignment_feed.feed,
                   ad_placement_assignment_feed.feed,
                   ad_event_tag_assignment_feed.feed, placement_feed.feed,
                   event_tag_profile_feed.feed)
  execute_feed(ad_feed, ad_dao, FieldMap.AD_ID, 'Processing Ad')

  ad_creative_assignment_feed.update()
  ad_placement_assignment_feed.update()
  ad_event_tag_assignment_feed.update()
  event_tag_profile_feed.update()


def dynamic_targeting_keys():
  """Processes dynamic targeting keys."""
  process_feed('dynamic_targeting_key_feed', dynamic_targeting_key_dao,
               FieldMap.DYNAMIC_TARGETING_KEY_NAME,
               'Processing dynamic targeting key')


@project.from_parameters
def traffic():
  """Main function of Bulkdozer, performs the Bulkdozer job"""
  global clean_run
  if project.verbose:
    print('traffic')

  try:
    setup()

    logger.clear()
    logger.log('Bulkdozer traffic job starting')
    logger.flush()

    init_daos()
    assets()
    landing_pages()
    campaigns()
    event_tags()
    placement_groups()
    placements()
    creatives()
    ads()
    dynamic_targeting_keys()

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


@project.from_parameters
def _traffic():
  """For development purposes when debugging a specific entity, this function is handy to run just that entity."""
  setup()
  init_daos()
  dynamic_targeting_keys()


if __name__ == '__main__':
  """Main entry point of Bulkdozer."""
  traffic()
