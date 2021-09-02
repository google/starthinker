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
"""Handles creation and updates of Ads."""

import time, json

from starthinker.task.traffic.campaign import CampaignDAO
from starthinker.task.traffic.class_extensions import StringExtensions
from starthinker.task.traffic.creative import CreativeDAO
from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.event_tag import EventTagDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.landing_page import LandingPageDAO
from starthinker.task.traffic.placement import PlacementDAO
from starthinker.task.traffic.store import store


class AdDAO(BaseDAO):
  """Ad data access object.

  Inherits from BaseDAO and implements ad specific logic for creating and
  updating ads.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes AdDAO with profile id and authentication scheme."""
    super(AdDAO, self).__init__(config, auth, profile_id, is_admin)

    self._id_field = FieldMap.AD_ID
    self._search_field = FieldMap.AD_NAME
    self._list_name = 'ads'

    self._creative_dao = CreativeDAO(config, auth, profile_id, is_admin)
    self._placement_dao = PlacementDAO(config, auth, profile_id, is_admin)
    self._campaign_dao = CampaignDAO(config, auth, profile_id, is_admin)
    self._event_tag_dao = EventTagDAO(config, auth, profile_id, is_admin)
    self._landing_page_dao = LandingPageDAO(config, auth, profile_id, is_admin)

    self._parent_filter_name = 'campaignIds'
    self._parent_dao = self._campaign_dao
    self._parent_filter_field_name = FieldMap.CAMPAIGN_ID

    self._entity = 'AD'

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(AdDAO, self)._api(iterate).ads()

  def _api_creatives(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(AdDAO, self)._api(iterate).creatives()

  def _wait_creative_activation(self, creative_id, timeout=128):
    """Waits for a creative to become active.

    This function checks the if the creative is active in intervals that
    increase exponentially (exponential backoff).

    Args:
      creative_id: Creative identifier.
      timeout: Optional parameter, determines how many seconds to wait for the
        activation.

    Raises:
      Exception: In case the creative doesn't activate within the specified
      timeout

    """
    # Only wait for creative activation if it is a new creative trafficked by
    # this Bulkdozer session
    if store.get('CREATIVE', creative_id):
      creative = self._api_creatives().get(
          profileId=self.profile_id, id=creative_id).execute()
      wait = 2

      while not creative['active'] and timeout > 0:
        print('Waiting %s seconds for creative %s activation...' %
              (wait, creative_id))
        time.sleep(wait)
        timeout -= wait
        wait *= 2
        creative = self._api_creatives().get(
            profileId=self.profile_id, id=creative_id).execute()

      if not creative['active']:
        raise Exception(
            'Creative %s failed to activate within defined timeout' %
            creative['id'])

  def _wait_all_creative_activation(self, feed_item, timeout=128):
    """Waits for activation of all creatives that should be associated to the feed item that represents an ad.

    Args:
      feed_item: Feed item representing an Ad from the Bulkdozer feed.
      timeout: Optional parameter identifying how long to wait for all creatives
        to be activated in seconds.

    Raises:
      Exception: In case one or more creatives do not get activated within the
      specified timeout.

    """
    for association in feed_item['creative_assignment']:
      creative = self._creative_dao.get(association, required=True)
      self._wait_creative_activation(creative['id'], timeout)

  def _assignment_matches(self, item, assignment):
    if item.get(FieldMap.AD_ID, None) and assignment.get(FieldMap.AD_ID, None):
      return item.get(FieldMap.AD_ID,
                      None) == assignment.get(FieldMap.AD_ID, None)
    else:
      return item.get(FieldMap.AD_NAME,
                      '1') == assignment.get(FieldMap.AD_NAME, '2')

  def map_feeds(self, ad_feed, ad_creative_assignment, ad_placement_assignment,
                ad_event_tag_assignment, placement_feed,
                event_tag_profile_feed):
    """Maps subfeeds to the corresponding ad.

    The Ad is an object that has several other dependent entities, they could be
    other entities like creative assignment, or complex sub objects in the ad
    entity like the placement assignment. This function maps those feeds by ID
    and injects the child feeds into the feed item representing the ad.

    Also, the ad level is where placement event tag profiles are assigned, and
    therefore this function is also responsible to determining if the placement
    event tag profile should be used, or if the direct event tag assignment in
    the ad should be used.

    Args:
      ad_feed: Ad feed.
      ad_creative_assignment: Ad creative assignment feed.
      ad_placement_assignment: Ad placement assignment feed.
      placement_feed: Placement feed.
      event_tag_profile_feed: Event tag profile feed.
    """
    for ad in ad_feed:
      ad['creative_assignment'] = [
          association for association in ad_creative_assignment
          if self._assignment_matches(ad, association)
      ]

      ad['placement_assignment'] = [
          association for association in ad_placement_assignment
          if self._assignment_matches(ad, association)
      ]

      if ad.get(FieldMap.PLACEMENT_ID, None) or ad.get(FieldMap.PLACEMENT_NAME,
                                                       None):
        ad['placement_assignment'].append(ad)

      ad['event_tag_assignment'] = [
          association for association in ad_event_tag_assignment
          if self._assignment_matches(ad, association)
      ]

      if ad.get(FieldMap.EVENT_TAG_ID, None) or ad.get(FieldMap.EVENT_TAG_NAME,
                                                       None):
        ad['event_tag_assignment'].append(ad)

      # Identify all event tag profiles associated with the placements
      ad['placement_event_tag_profile'] = []
      for placement_assignment in ad['placement_assignment']:
        placement = self._placement_dao.get(placement_assignment, required=True)

        if placement:
          ad_placement = None
          for item in placement_feed:
            if int(placement['id']) == item.get(FieldMap.PLACEMENT_ID, None):
              ad_placement = item

          if ad_placement:
            event_tag_profile_name = ad_placement.get(
                FieldMap.EVENT_TAG_PROFILE_NAME, '')

            if event_tag_profile_name:
              ad['placement_event_tag_profile'] += [
                  event_tag_profile
                  for event_tag_profile in event_tag_profile_feed
                  if event_tag_profile.get(FieldMap.EVENT_TAG_PROFILE_NAME,
                                           None) == event_tag_profile_name
              ]

  def _setup_rotation_strategy(self, creative_rotation, feed_item):
    """Analyzes the feed and sets up rotation strategy for the ad.

    For better user experience, the creative rotaion values that come from the
    feed map directly to values in the UI, this function is responsible for
    translating that to API specific values for the creative rotation objects
    under the ad.

    Args:
      creative_rotation: Feed item representing the creative rotation setup from
        the feed.
      feed_item: Feed item representing the ad.
    """
    option = feed_item.get(FieldMap.CREATIVE_ROTATION, 'Even').upper()

    if option == 'EVEN':
      creative_rotation['type'] = 'CREATIVE_ROTATION_TYPE_RANDOM'
      creative_rotation['weightCalculationStrategy'] = 'WEIGHT_STRATEGY_EQUAL'
    elif option == 'SEQUENTIAL':
      creative_rotation['type'] = 'CREATIVE_ROTATION_TYPE_SEQUENTIAL'
      creative_rotation['weightCalculationStrategy'] = None
    elif option == 'CUSTOM':
      creative_rotation['type'] = 'CREATIVE_ROTATION_TYPE_RANDOM'
      creative_rotation['weightCalculationStrategy'] = 'WEIGHT_STRATEGY_CUSTOM'
    elif option == 'CLICK-THROUGH RATE':
      creative_rotation['type'] = 'CREATIVE_ROTATION_TYPE_RANDOM'
      creative_rotation[
          'weightCalculationStrategy'] = 'WEIGHT_STRATEGY_HIGHEST_CTR'
    elif option == 'OPTIMIZED':
      creative_rotation['type'] = 'CREATIVE_ROTATION_TYPE_RANDOM'
      creative_rotation[
          'weightCalculationStrategy'] = 'WEIGHT_STRATEGY_OPTIMIZED'

  def _process_update(self, item, feed_item):
    """Updates an ad based on the values from the feed.

    Args:
      item: Object representing the ad to be updated, this object is updated
        directly.
      feed_item: Feed item representing ad values from the Bulkdozer feed.
    """
    campaign = self._campaign_dao.get(feed_item, required=True)

    item['active'] = feed_item.get(FieldMap.AD_ACTIVE, True)

    if item['active']:
      self._wait_all_creative_activation(feed_item)

    self._setup_rotation_strategy(item['creativeRotation'], feed_item)

    if feed_item['creative_assignment']:
      item['creativeRotation']['creativeAssignments'] = []

    item['placementAssignments'] = []
    item['eventTagOverrides'] = []

    self._process_assignments(
        feed_item, item['creativeRotation'].get('creativeAssignments', []),
        item['placementAssignments'], item['eventTagOverrides'], campaign)

    if 'deliverySchedule' in item:
      item['deliverySchedule']['priority'] = feed_item.get(
          FieldMap.AD_PRIORITY, None)

    if feed_item.get(FieldMap.AD_HARDCUTOFF, "") != "":
      if not 'deliverySchedule' in item:
        item['deliverySchedule'] = {}

      item['deliverySchedule']['hardCutoff'] = feed_item.get(
          FieldMap.AD_HARDCUTOFF)

    item['archived'] = feed_item.get(FieldMap.AD_ARCHIVED, False)

    if 'T' in feed_item.get(FieldMap.AD_END_DATE, None):
      item['endTime'] = feed_item.get(FieldMap.AD_END_DATE, None)
    else:
      item['endTime'] = StringExtensions.convertDateStrToDateTimeStr(
          feed_item.get(FieldMap.AD_END_DATE, None), '23:59:59')

    if 'T' in feed_item.get(FieldMap.AD_START_DATE, None):
      item['startTime'] = feed_item.get(FieldMap.AD_START_DATE, None)
    else:
      item['startTime'] = StringExtensions.convertDateStrToDateTimeStr(
          feed_item.get(FieldMap.AD_START_DATE, None))

    item['name'] = feed_item.get(FieldMap.AD_NAME, None)

    self._process_landing_page(item, feed_item)

  def _process_assignments(self, feed_item, creative_assignments,
                           placement_assignments, event_tag_assignments,
                           campaign):
    """Updates the ad by setting the values of child objects based on secondary feeds.

    Args:
      feed_item: Feed item representing the ad from the Bulkdozer feed.
      creative_assignments: Feed items representing creative assignments related
        with the current ad.
      placement_assignments: Feed items representing placement assignments
        related with the current ad.
      event_tag_assignments: Feed items representing event tag assignments
        related with the current ad.
    """
    assigned_creatives = []
    assigned_placements = []
    assigned_event_tags = []

    for assignment in feed_item['creative_assignment']:
      creative = self._creative_dao.get(assignment, required=True)
      assignment[FieldMap.CREATIVE_ID] = creative['id']

      if not creative['id'] in assigned_creatives:
        assigned_creatives.append(creative['id'])

        sequence = assignment.get(FieldMap.CREATIVE_ROTATION_SEQUENCE, None)
        weight = assignment.get(FieldMap.CREATIVE_ROTATION_WEIGHT, None)

        sequence = sequence if type(sequence) is int else None
        weight = weight if type(weight) is int else None

        if assignment.get(FieldMap.AD_CREATIVE_ROTATION_START_TIME, ''):
          startTime = (
              assignment.get(FieldMap.AD_CREATIVE_ROTATION_START_TIME,
                             '') if 'T' in assignment.get(
                                 FieldMap.AD_CREATIVE_ROTATION_START_TIME, '')
              else StringExtensions.convertDateStrToDateTimeStr(
                  feed_item.get(FieldMap.AD_CREATIVE_ROTATION_START_TIME,
                                None)))
          assignment[FieldMap.AD_CREATIVE_ROTATION_START_TIME] = startTime
        else:
          startTime = None

        if assignment.get(FieldMap.AD_CREATIVE_ROTATION_END_TIME, ''):
          endTime = (
              assignment.get(FieldMap.AD_CREATIVE_ROTATION_END_TIME, '') if
              'T' in assignment.get(FieldMap.AD_CREATIVE_ROTATION_END_TIME, '')
              else StringExtensions.convertDateStrToDateTimeStr(
                  feed_item.get(FieldMap.AD_CREATIVE_ROTATION_END_TIME, None),
                  '23:59:59'))
          assignment[FieldMap.AD_CREATIVE_ROTATION_END_TIME] = endTime
        else:
          endTime = None

        lp = None
        if assignment.get(FieldMap.AD_LANDING_PAGE_ID,
                          '') != 'CAMPAIGN_DEFAULT':
          lp = self._landing_page_dao.get(assignment, required=True)
        else:
          lp = self._landing_page_dao.get(
              {FieldMap.AD_LANDING_PAGE_ID: campaign['defaultLandingPageId']},
              required=True)

        creative_assignment = {
            'active': True,
            'sequence': sequence,
            'weight': weight,
            'creativeId': assignment.get(FieldMap.CREATIVE_ID, None),
            'startTime': startTime,
            'endTime': endTime,
            'clickThroughUrl': {
                'defaultLandingPage':
                    False if
                    (assignment.get(FieldMap.AD_LANDING_PAGE_ID, '') or
                     assignment.get(FieldMap.CUSTOM_CLICK_THROUGH_URL, '')) and
                    assignment.get(FieldMap.AD_LANDING_PAGE_ID,
                                   '') != 'CAMPAIGN_DEFAULT' else True,
                'landingPageId':
                    lp.get('id', None) if lp else None,
                'customClickThroughUrl':
                    assignment.get(FieldMap.CUSTOM_CLICK_THROUGH_URL, '')
            }
        }

        if creative.get('exitCustomEvents'):
          creative_assignment['richMediaExitOverrides'] = []

          if assignment.get(FieldMap.AD_LANDING_PAGE_ID, '') or assignment.get(
              FieldMap.CUSTOM_CLICK_THROUGH_URL, ''):
            for exit_custom_event in creative.get('exitCustomEvents', []):
              creative_assignment['richMediaExitOverrides'].append({
                  'exitId': exit_custom_event['id'],
                  'enabled': True,
                  'clickThroughUrl': {
                      'defaultLandingPage':
                          False if
                          (assignment.get(FieldMap.AD_LANDING_PAGE_ID, '') or
                           assignment.get(FieldMap.CUSTOM_CLICK_THROUGH_URL, '')
                          ) and assignment.get(FieldMap.AD_LANDING_PAGE_ID, '')
                          != 'CAMPAIGN_DEFAULT' else True,
                      'landingPageId':
                          lp.get('id', None) if lp else None,
                      'customClickThroughUrl':
                          assignment.get(FieldMap.CUSTOM_CLICK_THROUGH_URL, '')
                  }
              })

        creative_assignments.append(creative_assignment)

    for assignment in feed_item['placement_assignment']:
      placement = self._placement_dao.get(assignment, required=True)
      if placement:
        assignment[FieldMap.PLACEMENT_ID] = placement['id']

        if not placement['id'] in assigned_placements:
          assigned_placements.append(placement['id'])

          placement_assignments.append({
              'active': True,
              'placementId': assignment.get(FieldMap.PLACEMENT_ID, None),
          })

    event_tags = [{
        'assignment': item,
        'event_tag': self._event_tag_dao.get(item, required=True)
    } for item in feed_item['event_tag_assignment']]

    event_tags += [{
        'assignment': item,
        'event_tag': self._event_tag_dao.get(item, required=True)
    } for item in feed_item['placement_event_tag_profile']]

    for item in event_tags:
      assignment = item['assignment']
      event_tag = item['event_tag']

      if event_tag:
        assignment[FieldMap.EVENT_TAG_ID] = event_tag['id']

        if not event_tag['id'] in assigned_event_tags:
          assigned_event_tags.append(event_tag['id'])

          event_tag_assignments.append({
              'id': event_tag['id'],
              'enabled': assignment.get(FieldMap.EVENT_TAG_ENABLED, True)
          })

  def _process_new(self, feed_item):
    """Creates a new ad DCM object from a feed item representing an ad from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the ad from the Bulkdozer feed.

    Returns:
      An ad object ready to be inserted in DCM through the API.

    """
    if feed_item.get(FieldMap.AD_ACTIVE, None):
      self._wait_all_creative_activation(feed_item)

    campaign = self._campaign_dao.get(feed_item, required=True)

    creative_assignments = []
    placement_assignments = []
    event_tag_assignments = []
    self._process_assignments(feed_item, creative_assignments,
                              placement_assignments, event_tag_assignments,
                              campaign)

    creative_rotation = {'creativeAssignments': creative_assignments}

    self._setup_rotation_strategy(creative_rotation, feed_item)

    delivery_schedule = {
        'impressionRatio': '1',
        'priority': feed_item.get(FieldMap.AD_PRIORITY, None),
        'hardCutoff': feed_item.get(FieldMap.AD_HARDCUTOFF, None)
    }

    ad = {
        'active':
            feed_item.get(FieldMap.AD_ACTIVE, None),
        'archived':
            feed_item.get(FieldMap.AD_ARCHIVED, None),
        'campaignId':
            campaign['id'],
        'creativeRotation':
            creative_rotation,
        'deliverySchedule':
            delivery_schedule,
        'endTime':
            feed_item.get(FieldMap.AD_END_DATE, None) if 'T' in feed_item.get(
                FieldMap.AD_END_DATE, None) else
            StringExtensions.convertDateStrToDateTimeStr(
                feed_item.get(FieldMap.AD_END_DATE, None), '23:59:59'),
        'name':
            feed_item.get(FieldMap.AD_NAME, None),
        'placementAssignments':
            placement_assignments,
        'startTime':
            feed_item.get(FieldMap.AD_START_DATE, None) if 'T' in feed_item.get(
                FieldMap.AD_START_DATE, None) else
            StringExtensions.convertDateStrToDateTimeStr(
                feed_item.get(FieldMap.AD_START_DATE, None)),
        'type':
            feed_item.get(FieldMap.AD_TYPE, 'AD_SERVING_STANDARD_AD'),
        'eventTagOverrides':
            event_tag_assignments
    }

    self._process_landing_page(ad, feed_item)

    return ad

  def _process_landing_page(self, item, feed_item):
    """Configures ad landing page.

    Args:
      item: DCM ad object to update.
      feed_item: Feed item representing the ad from the Bulkdozer feed
    """
    if feed_item.get(FieldMap.AD_LANDING_PAGE_ID, ''):

      landing_page = self._landing_page_dao.get(feed_item, required=True)
      item['clickThroughUrl'] = {'landingPageId': landing_page['id']}

    if feed_item.get(FieldMap.AD_URL_SUFFIX, ''):
      item['clickThroughUrlSuffixProperties'] = {
          'overrideInheritedSuffix': True,
          'clickThroughUrlSuffix': feed_item.get(FieldMap.AD_URL_SUFFIX, '')
      }
    else:
      item['clickThroughUrlSuffixProperties'] = {
          'overrideInheritedSuffix': False
      }

  def _sub_entity_map(self, assignments, item, campaign):
    """Maps ids and names of sub entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    ad feed.

    Args:
      assignments: List of child feeds to map.
      item: The DCM ad object that was updated or created.
      campaign: The campaign object associated with the ad.
    """
    for assignment in assignments:
      placement = self._placement_dao.get(assignment, required=True)
      event_tag = self._event_tag_dao.get(assignment, required=True)
      creative = self._creative_dao.get(assignment, required=True)

      landing_page = None
      if assignment.get(FieldMap.AD_LANDING_PAGE_ID, '') != 'CAMPAIGN_DEFAULT':
        landing_page = self._landing_page_dao.get(assignment, required=True)

      if landing_page:
        assignment[FieldMap.AD_LANDING_PAGE_ID] = landing_page['id']

      if item:
        assignment[FieldMap.AD_ID] = item['id']
        assignment[FieldMap.AD_NAME] = item['name']

      if campaign:
        assignment[FieldMap.CAMPAIGN_ID] = campaign['id']
        assignment[FieldMap.CAMPAIGN_NAME] = campaign['name']

      if placement:
        assignment[FieldMap.PLACEMENT_ID] = placement['id']
        assignment[FieldMap.PLACEMENT_NAME] = placement['name']

      if creative:
        assignment[FieldMap.CREATIVE_ID] = creative['id']
        assignment[FieldMap.CREATIVE_NAME] = creative['name']

      if event_tag:
        assignment[FieldMap.EVENT_TAG_ID] = event_tag['id']
        assignment[FieldMap.EVENT_TAG_NAME] = event_tag['name']

  def _post_process(self, feed_item, item):
    """Maps ids and names of related entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    ad feed.

    Args:
      feed_item: Feed item representing the ad from the Bulkdozer feed.
      item: The DCM ad being updated or created.
    """
    campaign = self._campaign_dao.get(feed_item, required=True)
    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    landing_page = self._landing_page_dao.get(feed_item, required=True)

    if landing_page:
      feed_item[FieldMap.AD_LANDING_PAGE_ID] = landing_page['id']

    self._sub_entity_map(feed_item['creative_assignment'], item, campaign)
    self._sub_entity_map(feed_item['placement_assignment'], item, campaign)
    self._sub_entity_map(feed_item['event_tag_assignment'], item, campaign)
