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

import json
from copy import deepcopy

from setup import EXECUTE_PATH, UI_BUCKET_AUTH
from util.project import project
from util.auth import get_profile, BucketCredentials


if __name__ == "__main__":

  project.load()

  # make sure project has a unique universal ID ( used for logs )
  project.get_uuid()

  # move local credentials to bucket
  cloud_path = '%s:remote/%s.json' % (UI_BUCKET_AUTH, get_profile()['id'])
  BucketCredentials.from_local(cloud_path, project.configuration['setup']['auth']['user']).to_bucket() # BROKEN: cannot write to credentails bucket as that is inscure! 
  
  # So how do we make the local token refreshable?
    # do we store it on th enative project and manipulate it there? ( complex )
    # do we pass it in the json and create a copy ( deauth local version )
    # do we scrap this altogether and run all remote jobs via the UI?

  # create a copy of the configuration and swap for bucket credentials
  remote_config = deepcopy(project.configuration)
  remote_config['setup']['auth']['source'] = 'remote'
  remote_config['setup']['auth']['user'] = cloud_path
  
  # push to pub sub
  print json.dumps(remote_config)
  # MAURICIO: remote_pub(json.dumps(remote_config))

  print "Remote Execution Log: https://storage.cloud.google.com/starthinker-log/%s/" % project.get_uuid()
