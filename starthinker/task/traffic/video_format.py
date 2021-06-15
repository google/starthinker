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
"""Handles creation and updates of video formats."""

import sys

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap


class VideoFormatDAO(BaseDAO):
  """Video format data access object.

  Inherits from BaseDAO and implements video format specific logic for creating
  and
  updating video format.
  """

  def __init__(self, config, auth, profile_id, is_admin):
    """Initializes VideoFormatDAO with profile id and authentication scheme."""
    super(VideoFormatDAO, self).__init__(config, auth, profile_id)

    self.profile_id = profile_id

    self._video_formats = None

  def _api(self, iterate=False):
    """Returns an DCM API instance for this DAO."""
    return super(VideoFormatDAO, self)._api(iterate).videoFormats()

  def get_video_formats(self):
    """Fetches video formats from CM.

    Returns:
      The lists of video formats from CM.
    """

    if not self._video_formats:
      self._video_formats = list(
          self._api(iterate=True).list(profileId=self.profile_id).execute())

    return self._video_formats

  def translate_transcode_config(self, transcode_configs):
    """Given a transcode config, returns the CM transcodes that match the config.

    Args:
      transcode_config: The transcode configuration feed item.

    Returns:
      All trancode objects from Campaign Manager that match the transcode
      configuration specified.
    """
    result = []
    REALLY_BIG_INT = 9223372036854775807

    try:
      for video_format in self.get_video_formats():
        for transcode_config in transcode_configs:
          min_width = int(transcode_config.get(FieldMap.TRANSCODE_MIN_WIDTH, 0))
          min_height = int(
              transcode_config.get(FieldMap.TRANSCODE_MIN_HEIGHT, 0))
          min_bitrate = int(
              transcode_config.get(FieldMap.TRANSCODE_MIN_BITRATE, 0))

          max_width = int(
              transcode_config.get(FieldMap.TRANSCODE_MAX_WIDTH,
                                   REALLY_BIG_INT))
          max_height = int(
              transcode_config.get(FieldMap.TRANSCODE_MAX_HEIGHT,
                                   REALLY_BIG_INT))
          max_bitrate = int(
              transcode_config.get(FieldMap.TRANSCODE_MAX_BITRATE,
                                   REALLY_BIG_INT))

          file_format = transcode_config.get(FieldMap.TRANSCODE_FORMAT, '')

          # There is one video format entry of id 15 in CM that represents the
          # Source File setting, it has no file type and no resolution, we are
          # using SOURCE_FILE as an artificial handle to allow this transcode
          # configuration to be selected from the sheet
          if file_format == 'SOURCE_FILE':
            if 15 not in result:
              result.append(15)
          elif min_width <= video_format['resolution']['width'] \
              and video_format['resolution']['width'] <= max_width \
              and min_height <= video_format['resolution']['height'] \
              and video_format['resolution']['height'] <= max_height \
              and min_bitrate <= video_format['targetBitRate'] \
              and video_format['targetBitRate'] <= max_bitrate \
              and video_format.get('fileType', '') == file_format:
            if video_format['id'] not in result:
              result.append(video_format['id'])
    except:
      raise Exception('Error determining file formats for transcode')

    return result
