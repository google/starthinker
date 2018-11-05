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

This script requires Client Credentials and will fetch and download User Credentials.
To verify that the User Credentials work, it will download and display the user profile.

Google Cloud Projects provide Client Credentials that allow them to act as users.
Using Client Credentials this command line will download user credentials which
can be used with various recipes to act as the user.

### Downloading Client Credentials

Please follow the instructions at the following link.  You will need a Google Cloud Project.
https://cloud.google.com/genomics/docs/how-tos/getting-started#download_credentials_for_api_access

### Scopes Granted To This Application

See SCOPES in util/auth/__init__.py or review util/auth/README.md

### Arguments

- --client / -c - path to client credentials file used to authenticate
- --user / -u - path to user credentials file to be created if it does not exist.

### Example

`python auth/helper.py -u [user credentials path] -c [client credentials path]`

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
