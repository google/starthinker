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


class StringExtensions:

  @staticmethod
  def convertDateStrToDateTimeStr(date, time='00:00:00'):
    """Convert Date string (YYYY-MM-DD) to a datetime string by adding the desired time (YYYY-MM-DDTHH:mm:SSZ)

                Args:
                        date: the date as a string to be converted
                        time: the time as a string to be added to the date

                Returns:
                        A string representation of a datetime in the following
                        format YYYY-MM-DDTHH:mm:SSZ
                """
    if not date == None:
      date = '%sT%sZ' % (date, time)

    return date

  @staticmethod
  def convertDateTimeStrToDateStr(datetime):
    """  Convert a DateTime string (YYYY-MM-DDTHH:mm:SSZ) to just a Date string by removing the time (YYYY-MM-DD)

                Args:
                        datetime: the datetime as a string

                Returns:
                        A string representation of the date in the following
                        format YYYY-MM-DD
                """
    if not datetime == None and 'T' in datetime:
      datetime = datetime.split('T')[0]

    return datetime
