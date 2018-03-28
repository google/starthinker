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

import time
import json

from traffic.dao import BaseDAO
from traffic.creative import CreativeDAO
from traffic.placement import PlacementDAO
from traffic.campaign import CampaignDAO
from traffic.feed import FieldMap
from traffic.event_tag import EventTagDAO


class AdDAO(BaseDAO):

  def __init__(self, auth, profile_id):
    super(AdDAO, self).__init__(auth, profile_id)

    self._service = self.service.ads()
    self._id_field = FieldMap.AD_ID
    self._search_field = FieldMap.AD_NAME
    self._list_name = 'ads'

    self._creative_dao = CreativeDAO(auth, profile_id)
    self._placement_dao = PlacementDAO(auth, profile_id)
    self._campaign_dao = CampaignDAO(auth, profile_id)
    self._event_tag_dao = EventTagDAO(auth, profile_id)

    self._entity = 'AD'

  def _wait_creative_activation(self, creative_id, timeout=1800):
    creative = self._retry(self.service.creatives().get(
        profileId=self.profile_id, id=creative_id))
    wait = 30

    while not creative['active'] and timeout > 0:
      time.sleep(wait)
      timeout -= wait
      wait *= 2
      creative = self._retry(self.service.creatives().get(
          profileId=self.profile_id, id=creative_id))

    if not creative['active']:
      raise Exception('Creative %s failed to activate within defined timeout' %
                      creative['id'])

  def _wait_all_creative_activation(self, feed_item, timeout=1800):
    for association in feed_item['creative_assignment']:
      creative = self._creative_dao.get(association)
      self._wait_creative_activation(creative['id'], timeout)

  def map_feeds(self, ad_feed, ad_creative_assignment, ad_placement_assignment, ad_event_tag_assignment):
    for ad in ad_feed:
      ad['creative_assignment'] = [
          association for association in ad_creative_assignment
          if association[FieldMap.AD_ID] == ad[FieldMap.AD_ID]
      ]

      ad['placement_assignment'] = [
          association for association in ad_placement_assignment
          if association[FieldMap.AD_ID] == ad[FieldMap.AD_ID]
      ]

      ad['event_tag_assignment'] = [
          association for association in ad_event_tag_assignment
          if association[FieldMap.AD_ID] == ad[FieldMap.AD_ID]
      ]

  def _process_update(self, item, feed_item):
    self._wait_all_creative_activation(feed_item)

    item['creativeRotation']['type'] = feed_item[FieldMap.CREATIVE_ROTATION_TYPE]
    item['creativeRotation']['weightCalculationStrategy'] = feed_item[FieldMap.CREATIVE_ROTATION_WEIGHT_CALCULATION_STRATEGY]
    item['creativeRotation']['creativeAssignments'] = []

    item['placementAssignments'] = []
    item['eventTagOverrides'] = []

    self._process_assignments(feed_item, item['creativeRotation']['creativeAssignments'], item['placementAssignments'], item['eventTagOverrides'])

    if 'deliverySchedule' in item:
      item['deliverySchedule']['priority'] = feed_item[FieldMap.AD_PRIORITY]

    item['active'] = feed_item[FieldMap.AD_ACTIVE]
    item['archived'] = feed_item[FieldMap.AD_ARCHIVED]

    if 'T' in feed_item[FieldMap.AD_END_DATE]:
      item['endTime'] = feed_item[FieldMap.AD_END_DATE]
    else:
      item['endTime'] = '%sT23:59:59Z' % feed_item[FieldMap.AD_END_DATE]

    if 'T' in feed_item[FieldMap.AD_START_DATE]:
      item['startTime'] = feed_item[FieldMap.AD_START_DATE]
    else:
      item['startTime'] = '%sT00:00:00Z' % feed_item[FieldMap.AD_START_DATE]

    item['name'] = feed_item[FieldMap.AD_NAME]

  def _process_assignments(self, feed_item, creative_assignments, placement_assignments, event_tag_assignments):
    assigned_creatives = []
    assigned_placements = []
    assigned_event_tags = []

    for assignment in feed_item['creative_assignment']:
      creative = self._creative_dao.get(assignment)
      assignment[FieldMap.CREATIVE_ID] = creative['id']

      if not creative['id'] in assigned_creatives:
        assigned_creatives.append(creative['id'])

        creative_assignments.append({
            'active': True,
            'sequence': assignment[FieldMap.CREATIVE_ROTATION_SEQUENCE],
            'weight': assignment[FieldMap.CREATIVE_ROTATION_WEIGHT],
            'creativeId': assignment[FieldMap.CREATIVE_ID],
            'clickThroughUrl': {
                'defaultLandingPage': True
            }
        })

    for assignment in feed_item['placement_assignment']:
      placement = self._placement_dao.get(assignment)
      assignment[FieldMap.PLACEMENT_ID] = placement['id']

      if not placement['id'] in assigned_placements:
        assigned_placements.append(placement['id'])

        placement_assignments.append({
            'active': True,
            'placementId': assignment[FieldMap.PLACEMENT_ID],
        })

    for assignment in feed_item['event_tag_assignment']:
      event_tag = self._event_tag_dao.get(assignment)
      if event_tag:
        assignment[FieldMap.EVENT_TAG_ID] = event_tag['id']

        if not event_tag['id'] in assigned_event_tags:
          assigned_event_tags.append(event_tag['id'])

          event_tag_assignments.append({
              'id': event_tag['id'],
              'enabled': True
          })

  def _process_new(self, feed_item):

    self._wait_all_creative_activation(feed_item)
    campaign = self._campaign_dao.get(feed_item)

    creative_assignments = []
    placement_assignments = []
    event_tag_assignments = []
    self._process_assignments(feed_item, creative_assignments, placement_assignments, event_tag_assignments)

    # Construct creative rotation.
    creative_rotation = {
        'creativeAssignments': creative_assignments,
        'type': feed_item[FieldMap.CREATIVE_ROTATION_TYPE],
        'weightCalculationStrategy': feed_item[FieldMap.CREATIVE_ROTATION_WEIGHT_CALCULATION_STRATEGY]
    }

    # Construct delivery schedule.
    delivery_schedule = {
        'impressionRatio': '1',
        'priority': feed_item[FieldMap.AD_PRIORITY]
    }

    # Ad
    ad = {
        'active': feed_item[FieldMap.AD_ACTIVE],
        'archived': feed_item[FieldMap.AD_ARCHIVED],
        'campaignId': campaign['id'],
        'creativeRotation': creative_rotation,
        'deliverySchedule': delivery_schedule,
        'endTime': '%sT23:59:59Z' % feed_item[FieldMap.AD_END_DATE],
        'name': feed_item[FieldMap.AD_NAME],
        'placementAssignments': placement_assignments,
        'startTime': feed_item[FieldMap.AD_START_DATE] if 'T' in feed_item[FieldMap.AD_START_DATE] else '%sT00:00:00Z' % feed_item[FieldMap.AD_START_DATE],
        'type': 'AD_SERVING_STANDARD_AD',
        'eventTagOverrides': event_tag_assignments
    }

    return ad

  def _sub_entity_map(self, assignments, item, campaign):
    for assignment in assignments:
      placement = self._placement_dao.get(assignment)
      event_tag = self._event_tag_dao.get(assignment)
      creative = self._creative_dao.get(assignment)

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

    campaign = self._campaign_dao.get(feed_item)
    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    self._sub_entity_map(feed_item['creative_assignment'], item, campaign)
    self._sub_entity_map(feed_item['placement_assignment'], item, campaign)
    self._sub_entity_map(feed_item['event_tag_assignment'], item, campaign) 
