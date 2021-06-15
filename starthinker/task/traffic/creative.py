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
"""Handles creation and updates of Creatives."""

import json

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.creative_assets import CreativeAssetDAO
from starthinker.task.traffic.landing_page import LandingPageDAO


class CreativeDAO(BaseDAO):
  """Creative data access object.

  Inherits from BaseDAO and implements creative specific logic for creating and
  updating creatives.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes CreativeDAO with profile id and authentication scheme."""
    super(CreativeDAO, self).__init__(config, auth, profile_id, is_admin)

    self._entity = 'CREATIVE'

    self._parent_filter_name = 'advertiserId'
    self._parent_filter_field_name = FieldMap.ADVERTISER_ID

    self._id_field = FieldMap.CREATIVE_ID
    self._search_field = FieldMap.CREATIVE_NAME
    self._list_name = 'creatives'
    self._parent_dao = None

    self.creative_asset_dao = CreativeAssetDAO(config, auth, profile_id, is_admin, None)
    self.landing_page_dao = LandingPageDAO(config, auth, profile_id, is_admin)

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(CreativeDAO, self)._api(iterate).creatives()

  def _assignment_matches(self, item, assignment):
    if item.get(FieldMap.CREATIVE_ID, None) and assignment.get(
        FieldMap.CREATIVE_ID, None):
      return item.get(FieldMap.CREATIVE_ID,
                      None) == assignment.get(FieldMap.CREATIVE_ID, None)
    else:
      return item.get(FieldMap.CREATIVE_NAME,
                      '1') == assignment.get(FieldMap.CREATIVE_NAME, '2')

  def map_creative_third_party_url_feeds(self, creative_feed,
                                         third_party_url_feed):
    """Maps third party url feed to the corresponding creative.

    Third party URL is a child object to the creative, and there is a 1 creative
    to many third party urls relationship. In Bulkdozer they are represented by
    two separate tab in the feed, and this method maps the creatives to their
    respective third party URLs based on the creative ID.

    Args:
      creative_feed: Creative feed.
      third_party_url_feed: Third party url feed.
    """
    for creative in creative_feed:
      creative['third_party_urls'] = [
          third_party_url for third_party_url in third_party_url_feed
          if self._assignment_matches(creative, third_party_url)
      ]

  def map_creative_click_tag_feeds(self, creative_feed, click_tag_feed):
    """Maps click tag feed to the corresponding creative.

    Click Tag is a child object to the creative, and there is a 1 creative
    to many click tags relationship. In Bulkdozer they are represented by
    two separate tab in the feed, and this method maps the creatives to their
    respective click tags based on the creative ID.

    Args:
      creative_feed: Creative feed.
      click_tag_feed: Click tag feed.
    """
    for creative in creative_feed:
      creative['click_tags'] = [
          click_tag for click_tag in click_tag_feed
          if self._assignment_matches(creative, click_tag)
      ]

  def map_creative_and_association_feeds(self, creative_feed,
                                         creative_association_feed):
    """Maps creative association feed to the corresponding creative.

    Creative association is a child object to the creative, and there is a 1
    creative to many creative association relationship. In Bulkdozer they are
    represented by two separate tab in the feed, and this method maps the
    creatives to their respective creative association based on the creative ID.

    Args:
      creative_feed: Creative feed.
      creative_association_feed: Creative association feed.
    """
    for creative in creative_feed:
      creative['associations'] = [
          association for association in creative_association_feed
          if self._assignment_matches(creative, association)
      ]

  def _associate_third_party_urls(self, feed_item, creative):
    """Associate third party urls with the respective creative DCM object.

    This method transforms all child feed mapped earlier into DCM formatted
    associations within the creative object so it can be pushed to the API.

    Args:
      feed_item: Feed item representing the creative.
      creative: DCM creative object being created or updated.
    """
    third_party_urls = []
    for third_party_url in feed_item.get('third_party_urls', []):
      third_party_url_type = FieldMap.THIRD_PARTY_URL_TYPE_MAP.get(
          third_party_url.get(FieldMap.THIRD_PARTY_URL_TYPE, None))
      if third_party_url_type:
        third_party_urls.append({
            'thirdPartyUrlType': third_party_url_type,
            'url': third_party_url.get(FieldMap.THIRD_PARTY_URL, None)
        })

    if third_party_urls:
      creative['thirdPartyUrls'] = third_party_urls

  def _associate_click_tags(self, feed_item, creative):
    """Associate click tags with the respective creative DCM object.

    This method transforms all child feed mapped earlier into DCM formatted
    associations within the creative object so it can be pushed to the API.

    Args:
      feed_item: Feed item representing the creative.
      creative: DCM creative object being created or updated.
    """
    click_tags = []
    for click_tag in feed_item.get('click_tags', []):
      lp = self.landing_page_dao.get(
          click_tag, column_name=FieldMap.CLICK_TAG_LANDING_PAGE_ID)

      ct = {
          'eventName': click_tag.get(FieldMap.CLICK_TAG_EVENT, None),
          'name': click_tag.get(FieldMap.CLICK_TAG_NAME, None),
          'clickThroughUrl': {}
      }

      if (click_tag.get(FieldMap.CLICK_TAG_LANDING_PAGE_ID)):
        ct['clickThroughUrl']['landingPageId'] = click_tag.get(
            FieldMap.CLICK_TAG_LANDING_PAGE_ID) if not lp else lp['id']
      elif (click_tag.get(FieldMap.CLICK_TAG_CUSTOM_CLICK_THROUGH_URL)):
        ct['clickThroughUrl']['customClickThroughUrl'] = click_tag.get(
            FieldMap.CLICK_TAG_CUSTOM_CLICK_THROUGH_URL)

      click_tags.append(ct)

    if click_tags:
      creative['clickTags'] = click_tags

  def _process_update(self, item, feed_item):
    """Updates a creative based on the values from the feed.

    Args:
      item: Object representing the creative to be updated, this object is
        updated directly.
      feed_item: Feed item representing creative values from the Bulkdozer feed.
    """
    item['name'] = feed_item.get(FieldMap.CREATIVE_NAME, None)

    self._associate_third_party_urls(feed_item, item)

    self._associate_click_tags(feed_item, item)

  def _process_new(self, feed_item):
    """Creates a new creative DCM object from a feed item representing an creative from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the creative from the Bulkdozer feed.

    Returns:
      A creative object ready to be inserted in DCM through the API.

    """
    creative = {
        'advertiserId': feed_item.get(FieldMap.ADVERTISER_ID, None),
        'name': feed_item.get(FieldMap.CREATIVE_NAME, None),
        'active': True
    }

    self._associate_third_party_urls(feed_item, creative)
    self._associate_click_tags(feed_item, creative)

    # Video Creatives
    if feed_item.get(FieldMap.CREATIVE_TYPE, None) == 'VIDEO':
      creative['type'] = 'INSTREAM_VIDEO'

      for association in feed_item.get('associations', []):
        identifier = self.creative_asset_dao.get_identifier(
            association, self._creative_asset_feed)
        creative['creativeAssets'] = [{
            'assetIdentifier': identifier,
            'role': 'PARENT_VIDEO'
        }]

      del creative['active']

    #Display Creatives
    elif feed_item.get(FieldMap.CREATIVE_TYPE, None) == 'DISPLAY':
      creative['type'] = 'DISPLAY'

      # Creative Size
      if feed_item.get(FieldMap.CREATIVE_WIDTH, None) and feed_item.get(
          FieldMap.CREATIVE_HEIGHT, None):
        creative['size'] = {
            'kind': 'dfareporting#size',
            'width': feed_item.get(FieldMap.CREATIVE_WIDTH, None),
            'height': feed_item.get(FieldMap.CREATIVE_HEIGHT, None)
        }

      # Add Creative Assets
      for association in feed_item.get('associations', []):
        identifier = self.creative_asset_dao.get_identifier(
            association, self._creative_asset_feed)
        creative['creativeAssets'] = [{
            'assetIdentifier': identifier,
            'role': 'PRIMARY'
        }]

        # Backup Asset
        if feed_item.get(FieldMap.CREATIVE_BACKUP_ASSET_ID,
                         None) and feed_item.get(
                             FieldMap.CREATIVE_BACKUP_ASSET_ID, None) != '':
          backup_identifier = self.creative_asset_dao.get_backup_identifier(
              association, self._creative_asset_feed)

          creative['backupImageReportingLabel'] = feed_item.get(
              FieldMap.CREATIVE_BACKUP_NAME, None)

          # Parse Features
          backup_features = feed_item.get(FieldMap.BACKUP_IMAGE_FEATURES, None)
          if backup_features != None or backup_features != '':
            features = backup_features.split(',')
            creative['backupImageFeatures'] = features

          creative['backupImageTargetWindow'] = {
              'targetWindowOption':
                  feed_item.get(FieldMap.BACKUP_IMAGE_TARGET_WINDOW_OPTION,
                                None),
              'customHtml':
                  feed_item.get(FieldMap.BACKUP_IMAGE_CUSTOM_HTML, None)
          }

          lp = self.landing_page_dao.get(
              feed_item,
              column_name=FieldMap.BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID)
          creative['backupImageClickThroughUrl'] = {
              'landingPageId':
                  feed_item.get(
                      FieldMap.BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID)
                  if not lp else lp['id']
          }

          # Backup Image
          creative['creativeAssets'].append({
              'assetIdentifier': backup_identifier,
              'role': 'BACKUP_IMAGE'
          })

      del creative['active']

    else:
      raise Exception('Only video and display are supported at the moment!')
    # (mauriciod@): I didn't pull the display creative stuff from jeltz in here,
    # because I am splitting things up differently, and the backup image will
    # have to be uploaded in the creative_assets dao

    return creative

  def map_assets_feed(self, creative_asset_feed):
    self._creative_asset_feed = creative_asset_feed

  def _post_process(self, feed_item, new_item):
    """Maps ids and names of related entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    creative feed.

    Args:
      feed_item: Feed item representing the creative from the Bulkdozer feed.
      item: The DCM creative being updated or created.
    """
    # TODO loop through 3p urls and update the feed
    for third_party_url in feed_item.get('third_party_urls', []):
      third_party_url[FieldMap.CREATIVE_ID] = new_item['id']
      third_party_url[FieldMap.CREATIVE_NAME] = new_item['name']

    for association in feed_item.get('associations', []):
      association[FieldMap.CREATIVE_ID] = self.get(association)['id']
      association[FieldMap.CREATIVE_NAME] = self.get(association)['name']

      dcm_association = self.creative_asset_dao.get(association, required=True)
      if dcm_association:
        association[FieldMap.CREATIVE_ASSET_ID] = dcm_association.get(
            'id', None)
        association[FieldMap.CREATIVE_ASSET_NAME] = dcm_association.get(
            'name', None)
        backup_lp = self.landing_page_dao.get(
            feed_item,
            column_name=FieldMap.BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID)
        if backup_lp:
          association[
              FieldMap
              .BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID] = backup_lp['id']
          association[
              FieldMap
              .BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_NAME] = backup_lp['name']
        # Backup Asset Id
        backup_asset = self.creative_asset_dao.get(
            association, column_name=FieldMap.CREATIVE_BACKUP_ASSET_ID)

        if backup_asset:
          association[FieldMap.CREATIVE_BACKUP_ASSET_ID] = backup_asset['id']

        # association[FieldMap.BACKUP_ASSET_ID] = dcm_association.get(
        #     'id', None)

    # Update Click Tags
    for click_tag in feed_item.get('click_tags', []):
      #Update Creative info
      click_tag[FieldMap.CREATIVE_ID] = new_item['id']
      click_tag[FieldMap.CREATIVE_NAME] = new_item['name']

      # Update Landing Page
      click_tag_lp = self.landing_page_dao.get(
          click_tag, column_name=FieldMap.CLICK_TAG_LANDING_PAGE_ID)
      if click_tag_lp:
        click_tag[FieldMap.CLICK_TAG_LANDING_PAGE_ID] = click_tag_lp['id']
        click_tag[FieldMap.CLICK_TAG_LANDING_PAGE_NAME] = click_tag_lp['name']

    # Backup Asset Id
    backup_asset = self.creative_asset_dao.get(
        feed_item, column_name=FieldMap.CREATIVE_BACKUP_ASSET_ID)

    if backup_asset:
      feed_item[FieldMap.CREATIVE_BACKUP_ASSET_ID] = backup_asset['id']

    # Backup Landing Page Id
    backup_lp = self.landing_page_dao.get(
        feed_item,
        column_name=FieldMap.BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID)
    if backup_lp:
      feed_item[
          FieldMap.BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID] = backup_lp['id']
      feed_item[
          FieldMap
          .BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_NAME] = backup_lp['name']
