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

import json
from urllib.request import Request, urlopen


def dynamite_write(room, key, token, text):
  url = 'https://chat.googleapis.com/v1/spaces/%s/messages?key=%s&token=%s' % (
      room, key, token)
  data = json.dumps({
      'sender': {
          'displayName':
              'StarThinker',
          'avatarUrl':
              'https://www.gstatic.com/images/icons/material/system/2x/chat_googblue_48dp.png'
      },
      'text': text
  })
  f = urlopen(
      urllib.request.Request(url, data, {
          'Content-Type': 'application/json',
          'Content-Length': len(data)
      }))
  response = f.read()
  f.close()
  return response
