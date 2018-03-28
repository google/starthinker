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
from traffic.logger import logger
import json
import sys


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
  feed = Feed(project.task['auth'], project.task[feed_name].get('sheet_id', project.task['sheet_id']), project.task[feed_name]['range'])

  execute_feed(feed, dao, print_field, msg)

def execute_feed(feed, dao, print_field, msg='Processing'):
  for feed_item in feed.feed:
    print '%s %s' % (msg, feed_item[print_field])
    logger.log('%s %s' % (msg, feed_item[print_field]))
    dao.process(feed_item)
    feed.update()

def setup():
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
  store.trix_id = project.task.get('store', {}).get('sheet_id', project.task['sheet_id'])
  store.load_id_map()

  logger.auth = project.task['auth']
  logger.trix_id = project.task.get('logger', {}).get('sheet_id', project.task['sheet_id'])
  logger.clear()

  video_format_dao = VideoFormatDAO(project.task['auth'], project.task['dcm_profile_id'])
  landing_page_dao = LandingPageDAO(project.task['auth'], project.task['dcm_profile_id'])
  campaign_dao = CampaignDAO(project.task['auth'], project.task['dcm_profile_id'])
  creative_association_dao = CreativeAssociationDAO(project.task['auth'], project.task['dcm_profile_id'])
  creative_dao = CreativeDAO(project.task['auth'], project.task['dcm_profile_id'])
  placement_dao = PlacementDAO(project.task['auth'], project.task['dcm_profile_id'])
  creative_asset_dao = CreativeAssetDAO(project.task['auth'], project.task['dcm_profile_id'], project.id)
  ad_dao = AdDAO(project.task['auth'], project.task['dcm_profile_id'])
  event_tag_dao = EventTagDAO(project.task['auth'], project.task['dcm_profile_id'])

def assets():
  process_feed('creative_asset_feed', creative_asset_dao, FieldMap.CREATIVE_ASSET_FILE_NAME, 'Uploading creative asset')

def landing_pages():
  process_feed('landing_page_feed', landing_page_dao, FieldMap.CAMPAIGN_LANDING_PAGE_NAME, 'Processing landing page')

def campaigns():
  process_feed('campaign_feed', campaign_dao, FieldMap.CAMPAIGN_NAME, 'Processing campaign')

def event_tags():
  process_feed('event_tag_feed', event_tag_dao, FieldMap.EVENT_TAG_NAME, 'Processing event tag')

def placements():
  placement_feed = Feed(project.task['auth'], project.task['placement_feed'].get('sheet_id', project.task['sheet_id']), project.task['placement_feed']['range'])
  transcode_configs_feed = Feed(project.task['auth'], project.task['transcode_configs_feed'].get('sheet_id', project.task['sheet_id']), project.task['transcode_configs_feed']['range'])
  placement_dao.map_placement_transcode_configs(placement_feed.feed, transcode_configs_feed.feed)
  execute_feed(placement_feed, placement_dao, FieldMap.PLACEMENT_NAME, 'Processing placement')

def creatives():
  creative_feed = Feed(project.task['auth'], project.task['creative_feed'].get('sheet_id', project.task['sheet_id']), project.task['creative_feed']['range'])
  creative_association_feed = Feed(project.task['auth'], project.task['creative_asset_association_feed'].get('sheet_id', project.task['sheet_id']), project.task['creative_asset_association_feed']['range'])
  creative_dao.map_creative_and_association_feeds(creative_feed.feed, creative_association_feed.feed)
  execute_feed(creative_feed, creative_dao, FieldMap.CREATIVE_NAME, 'Processing creative')
  creative_association_feed.update()
  process_feed('creative_campaign_association_feed', creative_association_dao, FieldMap.CREATIVE_ID, 'Associating with campaign, creative id')

def ads():
  ad_feed = Feed(project.task['auth'], project.task['ad_feed'].get('sheet_id', project.task['sheet_id']), project.task['ad_feed']['range'])
  ad_creative_assignment_feed = Feed(project.task['auth'], project.task['ad_creative_assignment_feed'].get('sheet_id', project.task['sheet_id']), project.task['ad_creative_assignment_feed']['range'])
  ad_placement_assignment_feed = Feed(project.task['auth'], project.task['ad_placement_assignment_feed'].get('sheet_id', project.task['sheet_id']), project.task['ad_placement_assignment_feed']['range'])
  ad_event_tag_assignment_feed = Feed(project.task['auth'], project.task['event_tag_ad_assignment_feed'].get('sheet_id', project.task['sheet_id']), project.task['event_tag_ad_assignment_feed']['range'])
  ad_dao.map_feeds(ad_feed.feed, ad_creative_assignment_feed.feed, ad_placement_assignment_feed.feed, ad_event_tag_assignment_feed.feed)
  execute_feed(ad_feed, ad_dao, FieldMap.AD_ID, 'Processing Ad')

  ad_creative_assignment_feed.update()
  ad_placement_assignment_feed.update()
  ad_event_tag_assignment_feed.update()

def traffic():
  if project.verbose: print 'traffic'

  try:
    setup()

    logger.log('Bulkdozer traffic job starting')
    assets()
    landing_pages()
    campaigns()
    event_tags()
    placements()
    creatives()
    ads()
  except:
    logger.log(sys.exc_info()[0])
  finally:
    logger.log('Bulkdozer traffic job ended')

def test():
  setup()
  ads()

if __name__ == "__main__":
  project.load('traffic')
  traffic()
  #test()
