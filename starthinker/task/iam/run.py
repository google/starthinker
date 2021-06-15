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
""" Handler that executes { "iam":{...}} task in recipe JSON.

Grants roles to users in Google Cloud Projects.  Typically you define a role
in the cloud project that grants a collection of permissions for assets in
that project.  Use this call to quickly grant a user a role.

Users who authenticate against your client credentials DO NOT automatically get
access permission.  That still needs to be granted on a case by case basis.
Placing a call to this handler early in a recipe JSON ensures the user executing
the recipe has the right privileges.

This handler should be called with "service" auth in the the JSON.  The service
should
be able to assign roles.

### Command Line COnvenience

Mostly a helper function, your service credential will already have a higher
level
of role granting and you need it to grant the role to your user.  So there is
NO SECURITY benefit, just a conveniece.

### UI Security

In a UI environment such as a web application, where users DO NOT have access to
the service credentials, but the server does have access to user credentials,
this
handler allows the service to securely grant additional roles to users.

### Good Practice

Using roles is a better practice than assigning permissions to user accounts
individually because it allows for better tracking and quicker revocation.
Changing a role permission changes all user at once without having to track
down individuals.  We highly recommend using roles.

"""

from starthinker.util.auth import set_iam


def iam(config, task):
  set_iam(
    config,
    task['auth'],
    config.project,
    task['role'],
    task['email']
  )
