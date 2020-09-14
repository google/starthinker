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


def Placement(name,
              compatibility,
              size_width,
              size_height,
              paymentSource,
              pricingSchedule_startDate,
              pricingSchedule_endDate,
              campaignId,
              placementStrategyId,
              contentCategoryId,
              siteId=None,
              directorySiteId=None):
  """ Default minial placement definition.

  Args:
    See docs:
      https://developers.google.com/doubleclick-advertisers/v3.2/placements#resource

  Returns:
    Placement JSON.

  """

  body = {
      'kind': 'dfareporting#placement',
      'campaignId': campaignId,
      'name': name,
      'siteId': siteId,
      'directorySiteId': directorySiteId,
      'paymentSource': paymentSource,
      'compatibility': compatibility,
      'size': {
          'width': size_width,
          'height': size_height
      },
      'archived': False,
      'pricingSchedule': {
          'testingStartDate': pricingSchedule_startDate,
          'startDate': pricingSchedule_startDate,
          'endDate': pricingSchedule_endDate,
          'pricingType': 'PRICING_TYPE_CPM',
          'capCostOption': 'CAP_COST_CUMULATIVE',
          'disregardOverdelivery': False,
          'flighted': False,
          'pricingPeriods': [{
              'startDate': pricingSchedule_startDate,
              'endDate': pricingSchedule_endDate,
              'units': 0,
              'rateOrCostNanos': 0,
              'pricingComment': ''
          }],
          'floodlightActivityId': None
      },
      'placementGroupId': None,
      'primary': False,
      'tagSetting': {
          'additionalKeyValues': None,
          'includeClickTracking': True,
          'includeClickThroughUrls': True,
          'keywordOption': 'IGNORE'
      },
      'tagFormats': [
          'PLACEMENT_TAG_STANDARD',
          'PLACEMENT_TAG_IFRAME_JAVASCRIPT',
          'PLACEMENT_TAG_IFRAME_ILAYER',
          'PLACEMENT_TAG_INTERNAL_REDIRECT',
          'PLACEMENT_TAG_JAVASCRIPT',
          'PLACEMENT_TAG_INTERSTITIAL_IFRAME_JAVASCRIPT',
          'PLACEMENT_TAG_INTERSTITIAL_INTERNAL_REDIRECT',
          'PLACEMENT_TAG_INTERSTITIAL_JAVASCRIPT',
          'PLACEMENT_TAG_CLICK_COMMANDS',
          'PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH',
          'PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH_VAST_3',
          'PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH_VAST_4',
          'PLACEMENT_TAG_TRACKING',
          'PLACEMENT_TAG_TRACKING_IFRAME',
          'PLACEMENT_TAG_TRACKING_JAVASCRIPT',
      ],
      'contentCategoryId': contentCategoryId,
      'placementStrategyId': placementStrategyId,
      'lookbackConfiguration': {
          'clickDuration': 14,
          'postImpressionActivitiesDuration': 14
      },
      'comment': '',
      'status': 'DRAFT',
      'sslRequired': False,
      'externalId': '',
      'videoSettings': {
          'kind': 'dfareporting#videoSettings',
          'companionSettings': {
              'kind': 'dfareporting#companionSetting',
              'companionsDisabled': False,
              'enabledSizes': [],
              'imageOnly': False
          },
          'transcodeSettings': {
              'kind': 'dfareporting#transcodeSetting',
              'enabledVideoFormats': []
          },
          'skippableSettings': {
              'kind': 'dfareporting#skippableSetting',
              'skippable': True,
              'skipOffset': {
                  'offsetSeconds': None,
                  'offsetPercentage': 50
              },
              'progressOffset': {
                  'offsetSeconds': None,
                  'offsetPercentage': 50
              }
          },
          'orientation': 'ANY'
      },
      'videoActiveViewOptOut': False,
      'vpaidAdapterChoice': 'BOTH',
      'adBlockingOptOut': False
  }

  # filter out conflicting fields
  if compatibility != 'IN_STREAM_VIDEO':
    del body['videoSettings']

  return body
