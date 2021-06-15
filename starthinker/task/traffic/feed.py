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
"""Handles interactions with the Buldozer feed.

This module has all the column name mappings, reads and writes data to the
Google Sheet that represents the Bulkdozer feed, and
"""

import json
import pytz

from starthinker.util.sheets import sheets_get, sheets_read, sheets_write
from dateutil import parser


class FieldMap:
  """Contains static maps of column names and enumerations.

  This class maps user friendly field names with API enumeration values, it also
  maps Bulkdozer feed column names to constants so those can be referenced
  indirectly.
  """
  THIRD_PARTY_URL_TYPE_MAP = {
      'Start': 'VIDEO_START',
      'First quartile': 'VIDEO_FIRST_QUARTILE',
      'Midpoint': 'VIDEO_MIDPOINT',
      'Third quartile': 'VIDEO_THIRD_QUARTILE',
      'Complete': 'VIDEO_COMPLETE',
      'Mute': 'VIDEO_MUTE',
      'Pause': 'VIDEO_PAUSE',
      'Rewind': 'VIDEO_REWIND',
      'Full screen': 'VIDEO_FULLSCREEN',
      'Stop': 'VIDEO_STOP',
      'Custom click': 'CLICK_TRACKING',
      'Skip': 'VIDEO_SKIP',
      'Progress': 'VIDEO_PROGRESS'
  }

  AD_ID = 'Ad ID'
  AD_NAME = 'Ad Name'
  AD_START_DATE = 'Ad Start Date'
  AD_END_DATE = 'Ad End Date'
  AD_ACTIVE = 'Ad Active'
  AD_ARCHIVED = 'Ad Archived'
  AD_PRIORITY = 'Ad Priority'
  AD_LANDING_PAGE_ID = 'Landing Page ID'
  AD_CREATIVE_ROTATION_START_TIME = 'Start Date'
  AD_CREATIVE_ROTATION_END_TIME = 'End Date'
  AD_HARDCUTOFF = 'Hard Cutoff'
  AD_TYPE = 'Ad Type'
  AD_URL_SUFFIX = 'URL Suffix'
  CUSTOM_CLICK_THROUGH_URL = 'Custom URL'

  ADVERTISER_ID = 'Advertiser ID'

  ASSET_SIZE = 'Asset Size'

  CAMPAIGN_ID = 'Campaign ID'
  CAMPAIGN_NAME = 'Campaign Name'
  CAMPAIGN_START_DATE = 'Campaign Start Date'
  CAMPAIGN_END_DATE = 'Campaign End Date'
  CAMPAIGN_LANDING_PAGE_NAME = 'Landing Page Name'
  CAMPAIGN_LANDING_PAGE_URL = 'Landing Page URL'
  CAMPAIGN_LANDING_PAGE_ID = 'Landing Page ID'

  CAMPAIGN_CREATIVE_ASSOCIATION_ID = 'Campaign Creative Association ID'
  CREATIVE_ASSET_BUCKET_NAME = 'Creative Asset Bucket Name'
  CREATIVE_ASSET_ID = 'Creative Asset ID'
  CREATIVE_ASSET_NAME = 'Creative Asset Name'
  CREATIVE_ASSET_FILE_NAME = 'Creative Asset File Name'

  CREATIVE_NAME = 'Creative Name'
  CREATIVE_TYPE = 'Creative Type'
  CREATIVE_ID = 'Creative ID'
  CREATIVE_ROTATION = 'Creative Rotation'
  CREATIVE_ROTATION_SEQUENCE = 'Creative Rotation Sequence'
  CREATIVE_ROTATION_WEIGHT = 'Creative Rotation Weight'
  CREATIVE_WIDTH = 'Width (Display Only)'
  CREATIVE_HEIGHT = 'Height (Display Only)'

  CREATIVE_BACKUP_ASSET_ID = 'Backup Asset ID'
  CREATIVE_BACKUP_NAME = 'Creative Backup Name'
  BACKUP_IMAGE_FEATURES = 'Backup Image Features'
  BACKUP_IMAGE_TARGET_WINDOW_OPTION = 'Backup Image Target Window Option'
  BACKUP_IMAGE_CUSTOM_HTML = 'Backup Image Custom HTML'
  BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_ID = ('Backup Image Click Through '
                                                'Landing Page ID')
  BACKUP_IMAGE_CLICK_THROUGH_LANDING_PAGE_NAME = ('Backup Image Click Through '
                                                  'Landing Page Name')
  CLICK_TAGS = 'clickTags'
  CLICK_TAG_NAME = 'Click Tag Name'
  CLICK_TAG_EVENT = 'Click Tag Event'
  CLICK_TAG_LANDING_PAGE_ID = 'Click Tag Landing Page ID'
  CLICK_TAG_LANDING_PAGE_NAME = 'Click Tag Landing Page Name'
  CLICK_TAG_CUSTOM_CLICK_THROUGH_URL = 'Custom Click Through URL'

  PLACEMENT_GROUP_ID = 'Placement Group ID'
  PLACEMENT_GROUP_NAME = 'Placement Group Name'
  PLACEMENT_GROUP_TYPE = 'Placement Group Type'
  PLACEMENT_GROUP_START_DATE = 'Placement Group Start Date'
  PLACEMENT_GROUP_END_DATE = 'Placement Group End Date'
  PLACEMENT_GROUP_PRICING_TYPE = 'Pricing Type'

  PLACEMENT_ID = 'Placement ID'
  PLACEMENT_NAME = 'Placement Name'
  PLACEMENT_START_DATE = 'Placement Start Date'
  PLACEMENT_END_DATE = 'Placement End Date'
  PLACEMENT_TYPE = 'Type'
  PLACEMENT_ARCHIVED = 'Archived'
  PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION = 'Active View and Verification'
  PLACEMENT_AD_BLOCKING = 'Ad Blocking'
  PLACEMENT_PRICING_TESTING_START = 'Pricing Schedule Testing Starts'
  PLACEMENT_PRICING_COST_STRUCTURE = 'Pricing Schedule Cost Structure'
  PLACEMENT_PRICING_SCHEDULE_COST_STRUCTURE = 'Pricing Schedule Cost Structure'
  PLACEMENT_PRICING_SCHEDULE_RATE = 'Pricing Period Rate'
  PLACEMENT_PERIOD_START = 'Pricing Period Start Date'
  PLACEMENT_PERIOD_END = 'Pricing Period End Date'
  PLACEMENT_PERIOD_UNITS = 'Pricing Period Units'
  PLACEMENT_PERIOD_RATE = 'Pricing Period Rate'
  PLACEMENT_SKIPPABLE = 'Skippable'
  PLACEMENT_SKIP_OFFSET_SECONDS = 'Skip Offset Seconds'
  PLACEMENT_SKIP_OFFSET_PERCENTAGE = 'Skip Offset Percentage'
  PLACEMENT_PROGRESS_OFFSET_SECONDS = 'Progress Offset Seconds'
  PLACEMENT_ADDITIONAL_KEY_VALUES = 'Additional Key Values'
  PLACEMENT_PROGRESS_OFFSET_PERCENTAGE = 'Progress Offset Percentage'

  EVENT_TAG_NAME = 'Event Tag Name'
  EVENT_TAG_STATUS = 'Event Tag Status'
  EVENT_TAG_TYPE = 'Event Tag Type'
  EVENT_TAG_URL = 'Event Tag URL'
  EVENT_TAG_ID = 'Event Tag ID'
  EVENT_TAG_ENABLED_BY_DEFAULT = 'Enable By Default'
  EVENT_TAG_PROFILE_NAME = 'Event Tag Profile'
  EVENT_TAG_ENABLED = 'Enabled'

  SITE_ID = 'Site ID'

  TRANSCODE_ID = 'Transcode ID'
  TRANSCODE_MIN_WIDTH = 'Min Width'
  TRANSCODE_MAX_WIDTH = 'Max Width'
  TRANSCODE_MIN_HEIGHT = 'Min Height'
  TRANSCODE_MAX_HEIGHT = 'Max Height'
  TRANSCODE_MIN_BITRATE = 'Min Bitrate (kbps)'
  TRANSCODE_MAX_BITRATE = 'Max Bitrate (kbps)'
  TRANSCODE_FORMAT = 'Format'

  THIRD_PARTY_URL_TYPE = '3P URL Type'
  THIRD_PARTY_URL = '3P URL'

  LP_DAWN_CAMPAIGN_ID = 'CM Campaign ID'
  LP_DAWN_EMAIL = 'Email Address'
  LP_DAWN_LP_ID = 'CM Landing Page ID'
  LP_DAWN_URL = 'Desired Landing Page URL'
  LP_DAWN_DATE_FOR_UPDATE = 'Date for Update (Central Time)'
  LP_DAWN_TIME_FOR_UPDATE = 'Time for Update (Central Time)'
  LP_DAWN_STATUS = 'Status'
  LP_DAWN_UPDATE_TIME = 'Update Time'
  LP_DAWN_MESSAGE = 'Message'

  DYNAMIC_TARGETING_KEY_NAME = 'Key Name'
  DYNAMIC_TARGETING_KEY_OBJECT_TYPE = 'Object Type'
  DYNAMIC_TARGETING_KEY_OBJECT_ID = 'Object ID'


class Feed:
  """Maps Bulkdozer feed items to and from dictionaries."""
  """Maps of internal feed names and Bulkdozer feed tabs.

  Each value is a list because if the first options is not found, it falls back
  to the subsequent one. E.g. lading_page_feed will first try to find a tab
  called "Landing Page", if that isn't found it will use the "Campaign" feed
  isntead, this allows end users to customize the tool behavior by adding or
  removing certain tabs.
  """
  _feed_name_tab_map = {
      'ad_feed': ['Ad'],
      'campaign_feed': ['Campaign'],
      'creative_asset_feed': ['Creative Asset'],
      'creative_feed': ['Creative'],
      'event_tag_feed': ['Event Tag'],
      'landing_page_feed': ['Landing Page', 'Campaign'],
      'placement_group_feed': ['Placement Group'],
      'placement_feed': ['Placement'],
      'third_party_url_feed': ['3P URLs'],
      'ad_creative_assignment_feed': ['Ad Creative Assignment', 'Ad'],
      'ad_placement_assignment_feed': ['Ad Placement Assignment', 'Ad'],
      'event_tag_ad_assignment_feed': ['Event Tag Ad Assignment', 'Ad'],
      'placement_pricing_schedule_feed': ['Placement Pricing Schedule'],
      'creative_asset_association_feed': [
          'Asset Creative Assignment', 'Creative'
      ],
      'creative_campaign_association_feed': [
          'Campaign Creative Assignment', 'Creative'
      ],
      'click_tag_feed': ['Click Tag'],
      'transcode_configs_feed': ['Transcode Configuration'],
      'event_tag_profile_feed': ['Event Tag Profile'],
      'lp_dawn': ['Form Responses 1'],
      'lp_dawn_status': ['Status'],
      'dynamic_targeting_key_feed': ['Dynamic Targeting Keys']
  }

  def __init__(self,
               config,
               auth,
               trix_id,
               feed_name,
               parse=True,
               spreadsheet=None,
               timezone=None):
    """Initializes the feed with parameters.

    Args:
      auth: The authentication scheme to use based on the json configuration
        file.
      trix_id: Unique identifier of the Google Sheet that represents the
        Bulkdozer feed.
      feed_name: The name of the feed to initialize.
      spreadsheet: Optional, the spreadsheet object representing the Bulkdozer
        feed spreadsheet, useful to limit calls to the sheets API and allow
        multiple Feed objects to use the same spreadsheet instance. This is used
        to determine which tabs exist in the feed so the correct one can be
        selected for the entity this Feed object represents.
    """
    self.config = config
    self.auth = auth
    self.trix_id = trix_id
    self.trix_range = 'A1:AZ'
    self.feed_name = feed_name
    self._parse = parse
    self._timezone = timezone or 'America/New_York'

    # TODO: Make sure we only read the spreadsheet object or the list of tabs
    # once
    if spreadsheet:
      self.spreadsheet = spreadsheet
    else:
      self.spreadsheet = sheets_get(self.config, self.auth, self.trix_id)

    self.raw_feed = self._get_feed()
    self.feed = self._feed_to_dict(parse=self._parse)

  def update(self):
    """Updates the related Bulkdozer feed item with the values in this object."""
    new_feed = self._dict_to_feed(parse=self._parse)

    if len(new_feed) > 1:
      sheets_write(self.config, self.auth, self.trix_id, self.tab_name, self.trix_range,
                   new_feed)

  def _get_feed(self):
    """Fetches the feed based on initialization parameters.

    Returns:
      List of lists that represents the rows and columns of the feed. If the
      feed isn't found returns a list with an empty list.
    """

    if self.feed_name in self._feed_name_tab_map:
      for tab_name in self._feed_name_tab_map[self.feed_name]:
        for sheet in self.spreadsheet['sheets']:
          if sheet['properties']['title'] == tab_name:
            self.tab_name = tab_name
            return sheets_read(self.config, self.auth, self.trix_id, tab_name,
                               self.trix_range)

    return [[]]

  def _convert_date(self, value):
    """Converts dates into a Bulkdozer specific format to be written back to the Feed.

    Args:
      value: String representation of the date.

    Returns:
      Bulkdozer string representation of a date. Returns null if the value
      cannot be parsed into a date.
    """
    try:
      result = parser.parse(value)

      if not result.tzinfo:
        result = pytz.timezone(self._timezone).localize(result)

      if ':' in value:
        return result.strftime('%Y-%m-%dT%H:%M:%S.000%z')
      else:
        return result.strftime('%Y-%m-%d')
    except:
      return None

  def _convert_int(self, value):
    """Converts a value into a integer.

    Args:
      value: String representation of a field from the Bulkdozer feed.

    Returns:
      If possible to convert value into an integer, returns the integer
      representation, otherwise None.
    """
    try:
      return int(value)
    except:
      return None

  def _convert_float(self, value):
    """Conversta a value into a float."""
    try:
      return float(value)
    except:
      return None

  def _parse_value(self, value):
    """Parses a string value into a type specific value infering the correct type based on the data.

    Args:
      value: The value to parse.

    Returns:
      The representation of the value in the correct data type.
    """
    if isinstance(value, str):
      if value.upper() == 'TRUE':
        return True
      elif value.upper() == 'FALSE':
        return False
      else:
        int_value = self._convert_int(value)

        if int_value:
          return int_value
        else:
          float_value = self._convert_float(value)

          if float_value:
            return float_value
          else:
            date_value = self._convert_date(value)

            if date_value:
              return date_value
            else:
              return value
    else:
      return value

  def _dict_to_feed(self, parse=True):
    """Turns a feed into a list of strings to be written back to the feed.

    Args:
      feed: Dictionary list to convert into a list of lists of strings.

    Returns:
     List of list of strings representing the values of the feed.

    """
    if not self.raw_feed:
      return []

    headers = self.raw_feed[0]

    row = 1

    for item in self.feed:
      for key in iter(item.keys()):
        if key in headers:
          column = headers.index(key)
          value = self._parse_value(item[key]) if parse else item[key]
          while column >= len(self.raw_feed[row]):
            self.raw_feed[row].append('')

          self.raw_feed[row][column] = value

      row += 1

    return self.raw_feed

  def _feed_to_dict(self, parse=True):
    """Turns a raw feed from Google Sheets into a list of dictionaries.

    Args:
      raw_feed: List of list of strings representing the feed from Google
        Sheets.

    Returns:
      List of dictionaries with the data from the feed
    """
    if not self.raw_feed:
      return None

    result = []

    header = self.raw_feed[0]

    for line in self.raw_feed[1:]:
      if line and ''.join(line):
        i = 0
        item = {}
        for index, column_header in enumerate(header):
          if index < len(line):
            item[column_header] = self._parse_value(
                line[index].strip()) if parse else line[index].strip()
          else:
            item[column_header] = ''

        result.append(item)
      else:
        break

    return result
