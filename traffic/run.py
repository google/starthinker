###########################################################################
#
#  Copyright 2017 Google Inc.
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
"""Main entry point of Bulkdozer.

"""

from util.project import project
from traffic.feed import Feed
from traffic.feed import FieldMap
from traffic.ad import AdDAO
from traffic.creative_assets import CreativeAssetDAO
from traffic.video_format import VideoFormatDAO
from traffic.creative_association import CreativeAssociationDAO
from traffic.creative import CreativeDAO
from traffic.campaign import CampaignDAO
from traffic.landing_page import LandingPageDAO
from traffic.placement import PlacementDAO
from traffic.event_tag import EventTagDAO
from traffic.store import store
from traffic.config import config
from traffic.logger import logger
import json
import sys
import traceback
from util.auth import get_service

video_format_dao = None
landing_page_dao = None
campaign_dao = None
creative_association_dao = None
creative_dao = None
placement_dao = None
creative_asset_dao = None
ad_dao = None
event_tag_dao = None


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
  feed = Feed(project.task['auth'], project.task['sheet_id'], feed_name)

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
  for feed_item in feed.feed:
    value = str(feed_item[print_field])
    print '%s %s' % (msg, value.encode('utf-8'))
    logger.log('%s %s' % (msg, value.encode('utf-8')))
    dao.process(feed_item)
    feed.update()


def setup():
  """Sets up Bulkdozer configuration and required object to execute the job.

  """
  global video_format_dao
  global landing_page_dao
  global campaign_dao
  global creative_association_dao
  global creative_dao
  global placement_dao
  global creative_asset_dao
  global ad_dao
  global event_tag_dao

  # Setting up required objects and parsing parameters
  store.auth = project.task['auth']
  store.trix_id = project.task.get('store', {}).get('sheet_id',
                                                    project.task['sheet_id'])
  store.load_id_map()

  config.auth = project.task['auth']
  config.trix_id = project.task.get('store', {}).get('sheet_id',
                                                     project.task['sheet_id'])
  config.load()

  logger.auth = project.task['auth']
  logger.trix_id = project.task.get('logger', {}).get('sheet_id',
                                                      project.task['sheet_id'])
  video_format_dao = VideoFormatDAO(project.task['auth'],
                                    project.task['dcm_profile_id'])
  landing_page_dao = LandingPageDAO(project.task['auth'],
                                    project.task['dcm_profile_id'])
  campaign_dao = CampaignDAO(project.task['auth'],
                             project.task['dcm_profile_id'])
  creative_association_dao = CreativeAssociationDAO(
      project.task['auth'], project.task['dcm_profile_id'])
  creative_dao = CreativeDAO(project.task['auth'],
                             project.task['dcm_profile_id'])
  placement_dao = PlacementDAO(project.task['auth'],
                               project.task['dcm_profile_id'])
  creative_asset_dao = CreativeAssetDAO(
      project.task['auth'], project.task['dcm_profile_id'], project.id)
  ad_dao = AdDAO(project.task['auth'], project.task['dcm_profile_id'])
  event_tag_dao = EventTagDAO(project.task['auth'],
                              project.task['dcm_profile_id'])


def assets():
  """Processes assets.

  """
  process_feed('creative_asset_feed', creative_asset_dao,
               FieldMap.CREATIVE_ASSET_FILE_NAME, 'Uploading creative asset')


def landing_pages():
  """Processes landing pages.

  """
  process_feed('landing_page_feed', landing_page_dao,
               FieldMap.CAMPAIGN_LANDING_PAGE_NAME, 'Processing landing page')


def campaigns():
  """Processes campaigns.

  """
  process_feed('campaign_feed', campaign_dao, FieldMap.CAMPAIGN_NAME,
               'Processing campaign')


def event_tags():
  """Processes event tags.

  """
  process_feed('event_tag_feed', event_tag_dao, FieldMap.EVENT_TAG_NAME,
               'Processing event tag')


def placements():
  """Processes placements.

  """
  placement_feed = Feed(project.task['auth'], project.task['sheet_id'],
                        'placement_feed')

  pricing_schedule_feed = Feed(project.task['auth'], project.task['sheet_id'],
                               'placement_pricing_schedule_feed')

  transcode_configs_feed = Feed(project.task['auth'], project.task['sheet_id'],
                                'transcode_configs_feed')

  placement_dao.map_placement_transcode_configs(placement_feed.feed,
                                                transcode_configs_feed.feed,
                                                pricing_schedule_feed.feed)

  execute_feed(placement_feed, placement_dao, FieldMap.PLACEMENT_NAME,
               'Processing placement')


def creatives():
  """Processes creatives.

  """
  creative_feed = Feed(project.task['auth'], project.task['sheet_id'],
                       'creative_feed')

  third_party_url_feed = Feed(project.task['auth'], project.task['sheet_id'],
                              'third_party_url_feed')

  creative_association_feed = Feed(project.task['auth'],
                                   project.task['sheet_id'],
                                   'creative_asset_association_feed')

  creative_dao.map_creative_third_party_url_feeds(creative_feed.feed,
                                                  third_party_url_feed.feed)
  creative_dao.map_creative_and_association_feeds(
      creative_feed.feed, creative_association_feed.feed)

  execute_feed(creative_feed, creative_dao, FieldMap.CREATIVE_NAME,
               'Processing creative')

  creative_association_feed.update()
  third_party_url_feed.update()

  process_feed('creative_campaign_association_feed', creative_association_dao,
               FieldMap.CREATIVE_ID, 'Associating with campaign, creative id')


def ads():
  """Processes ads.

  """
  placement_feed = Feed(project.task['auth'], project.task['sheet_id'],
                        'placement_feed')
  event_tag_profile_feed = Feed(project.task['auth'], project.task['sheet_id'],
                                'event_tag_profile_feed')
  ad_feed = Feed(project.task['auth'], project.task['sheet_id'], 'ad_feed')
  ad_creative_assignment_feed = Feed(project.task['auth'],
                                     project.task['sheet_id'],
                                     'ad_creative_assignment_feed')

  ad_placement_assignment_feed = Feed(project.task['auth'],
                                      project.task['sheet_id'],
                                      'ad_placement_assignment_feed')
  ad_event_tag_assignment_feed = Feed(project.task['auth'],
                                      project.task['sheet_id'],
                                      'event_tag_ad_assignment_feed')

  ad_dao.map_feeds(ad_feed.feed, ad_creative_assignment_feed.feed,
                   ad_placement_assignment_feed.feed,
                   ad_event_tag_assignment_feed.feed, placement_feed.feed,
                   event_tag_profile_feed.feed)
  execute_feed(ad_feed, ad_dao, FieldMap.AD_ID, 'Processing Ad')

  ad_creative_assignment_feed.update()
  ad_placement_assignment_feed.update()
  ad_event_tag_assignment_feed.update()
  event_tag_profile_feed.update()


def traffic():
  """Main function of Bulkdozer, performs the Bulkdozer job

  """
  if project.verbose:
    print 'traffic'

  try:
    setup()

    if config.mode in ['ALWAYS', 'ONCE']:
      logger.clear()
      logger.log('Bulkdozer traffic job starting')
      logger.log('Execution config is %s' % config.mode)

      if config.mode == 'ONCE':
        config.mode = 'OFF'
        config.update()

      assets()
      landing_pages()
      campaigns()
      event_tags()
      placements()
      creatives()
      ads()

      store.clear()
  except Exception as error:
    stack = traceback.format_exc()
    print stack

    logger.log(str(error))
  finally:
    logger.log('Bulkdozer traffic job ended')


def test():
  """For development purposes when debugging a specific entity, this function is handy to run just that entity.

  """
  setup()
  ads()


if __name__ == '__main__':
  """Main entry point of Bulkdozer.

  """
  project.load('traffic')
  traffic()
  #test()
