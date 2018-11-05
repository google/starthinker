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
"""Handles creation and updates of video formats.

"""

import traceback
import sys
import time
import json

from traffic.dao import BaseDAO
from traffic.feed import FieldMap


class VideoFormatDAO(BaseDAO):
  """Video format data access object.

  Inherits from BaseDAO and implements video format specific logic for creating
  and
  updating video format.
  """

  def __init__(self, auth, profile_id):
    """Initializes VideoFormatDAO with profile id and authentication scheme."""
    super(VideoFormatDAO, self).__init__(auth, profile_id)

    self.profile_id = profile_id
    self._service = self.service.videoFormats()

    self._video_formats = None

  def get_video_formats(self):
    """Fetches video formats from CM.

    Returns:
      The lists of video formats from CM.
    """

    if not self._video_formats:
      self._video_formats = self._retry(self._service.list(
          profileId=self.profile_id))['videoFormats']

    return self._video_formats

  def translate_transcode_config(self, transcode_config):
    """Given a transcode config, returns the CM transcodes that match the config.

    Args:
      transcode_config: The transcode configuration feed item.

    Returns:
      All trancode objects from Campaign Manager that match the transcode configuration specified.
    """
    result = []

    try:
      min_width = int(transcode_config.get(FieldMap.TRANSCODE_MIN_WIDTH, 0))
      min_height = int(transcode_config.get(FieldMap.TRANSCODE_MIN_HEIGHT, 0))
      min_bitrate = int(transcode_config.get(FieldMap.TRANSCODE_MIN_BITRATE, 0))

      max_width = int(transcode_config.get(FieldMap.TRANSCODE_MAX_WIDTH, sys.maxint))
      max_height = int(transcode_config.get(FieldMap.TRANSCODE_MAX_HEIGHT, sys.maxint))
      max_bitrate = int(transcode_config.get(FieldMap.TRANSCODE_MAX_BITRATE, sys.maxint))
    except:
      return result

    file_types = [
        file_type for file_type in FieldMap.TRANSCODE_FILE_TYPES
        if transcode_config.get(file_type, False)
    ]

    for video_format in self.get_video_formats():
      if min_width <= video_format['resolution']['width'] and \
          video_format['resolution']['width'] <= max_width \
          and min_height <= video_format['resolution']['height'] \
          and video_format['resolution']['height'] <= max_height \
          and min_bitrate <= video_format['targetBitRate'] \
          and video_format['targetBitRate'] <= max_bitrate \
          and video_format['fileType'] in file_types:
        result.append(video_format['id'])

    return result
