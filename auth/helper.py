###########################################################################
# 
#  Copyright 2018 Google Inc.
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


"""Command line to get user profile, mainly for testing the client auth flow.

Quickly exercise the auth flow for a user and client by fetching the profile.

python auth/helper.py -u [user credentials path] -c [client credentials path]
"""

import json
import argparse

from util.project import project
from util.auth import get_profile


if __name__ == "__main__":

  # all parameters come from project ( forces ignore of json file )
  parser = argparse.ArgumentParser()

  # initialize project
  project.load(parser=parser)

  # get profile
  print 'Profile:', json.dumps(get_profile(), indent=2, sort_keys=True)
