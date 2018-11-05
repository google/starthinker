# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/auth/helper.py](/auth/helper.py)

Command line to get user profile, mainly for testing the client auth flow.

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


