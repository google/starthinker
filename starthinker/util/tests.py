###########################################################################
#
#  Copyright 2021 Google LLC
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

import unittest
import io

from starthinker.util.csv import find_utf8_split, response_utf8_stream


class TestCSV(unittest.TestCase):
  """Test the CSV module.  Currently only testing utf-8 function but WIP.
  """

  def test_find_utf8_split(self):
    """  Tests: find_utf8_split, response_utf8_stream

    Verify that encoding is an issue when not boundry aligned.
    Run boundary detection against 3 different UTF-8 encodings of different byte lengths.
    Pick 17 (prime) as a chunk size to ensure utf-8 byte boundary is hit.
    Run against multiple chunks to ensure test goes in and out of utf-8 alignement.

    """

    string_ascii = bytes('"#$%&()*+,-./0123456789:;<=>?@ABCDEF', 'utf-8')
    string_arabic = bytes('،؛؟ءآأؤإئابةتثجحخدذرزسشصضطظعغـفقكلم', 'utf-8')
    string_misc = bytes('⌀⌂⌃⌄⌅⌆⌇⌈⌉⌊⌋⌌⌍⌎⌏⌐⌑⌒⌓⌔⌕⌖⌗⌘⌙⌚⌛⌜⌝⌞⌟⌠⌡⌢⌣', 'utf-8')
    string_cjk = bytes('豈更車勞擄櫓爐盧老蘆虜路露魯鷺碌祿綠菉錄縷陋勒諒量', 'utf-8')

    # verify raw split causes error
    try:
      string_ascii[:17].decode("utf-8")
    except UnicodeDecodeError:
      self.fail("ASCII bytes should fit within utf-8.")

    with self.assertRaises(UnicodeDecodeError):
      string_arabic[:17].decode("utf-8")

    with self.assertRaises(UnicodeDecodeError):
      string_misc[:17].decode("utf-8")

    with self.assertRaises(UnicodeDecodeError):
      string_cjk[:17].decode("utf-8")

    # verify various utf-8 lengths work
    self.assertEqual(next(response_utf8_stream(io.BytesIO(string_ascii), 17)), '"#$%&()*+,-./0123')
    self.assertEqual(next(response_utf8_stream(io.BytesIO(string_arabic), 17)), '،؛؟ءآأؤإ')
    self.assertEqual(next(response_utf8_stream(io.BytesIO(string_misc), 17)), '⌀⌂⌃⌄⌅')

    # verify middle and last parts of splits work
    chunks = response_utf8_stream(io.BytesIO(string_cjk), 17)
    self.assertEqual(next(chunks), '豈更車勞擄')
    self.assertEqual(next(chunks), '櫓爐盧老蘆虜')
    self.assertEqual(next(chunks), '路露魯鷺碌祿')
    self.assertEqual(next(chunks), '綠菉錄縷陋')
    self.assertEqual(next(chunks), '勒諒量')

if __name__ == '__main__':
  unittest.main()
