# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/auth/web.py](/auth/web.py)

Sample code for Google OAuth designed for a web application and pub/sub.

### Problem

User credentials typically need to be downoaded from a web application, and
then refreshed periodically.  When jobs are run in a distributed pub/sub,
multiple processes may need a refreshed user token at once.  Refreshing the
token for one job but not others will invalidate the token for the other jobs.

### Solution

Store the downloaded user credentials in a Google Cloud Bucket and let multiple 
jobs fetch and update the token in a central location.  This sample shows how to
get, store, and retrieve the user credentials in a token refresh safe way. The key 
is using BucketCredentials, it does all the token management under the hood.

### Sample Google Auth Used As Login

User hits a web flow that requires authentication, instead of calling app login logic
call toauth_star to begin the Google Web Login Process. For safety, only trivial values
should be added as parameters to the auth URL, DO NOT USE THIS TO PASSACCOUNT KEYS.

`oauth_start()`

User will be presented with a Google Login Flow, which will request all scopes defined 
in SCOPES.  Future plan is to leverage incremental scoping. 

Once user completes the Google Login flow, by either cancelling or authenticating, 
the redirect comes back.  Now the application needs to verify the auth, and request
the actual credentials. Somwhere in the app the redirect_uri passed above needs to
point to:

`oauth_callback(request):`

Thats it, user is now created or logged in, the BucketCredentials will load, update, 
and store the token as necessary under the hood. In your application and pub/sub
always use BucketCredentials, for example see get_profile(...) for a typical API
call using distributed bucket credentials:

```
credentials = get_credentials(user_id)
service = discovery.build('oauth2', 'v2', credentials.authorize(httplib2.Http()))
profile = service.userinfo().get().execute()
```



## [/auth/helper.py](/auth/helper.py)

Command line to get user profile, mainly for testing the client auth flow.

This script requires Client Credentials and will fetch and download User Credentials.
To verify that the User Credentials work, it will download and display the user profile.

Google Cloud Projects provide Client Credentials that allow them to act as users.
Using Client Credentials this command line will download user credentials which
can be used with various recipes to act as the user.

Downloading Client Credentials

https://cloud.google.com/genomics/docs/how-tos/getting-started#download_credentials_for_api_access

Scopes Granted To This Application

See SCOPES in util/auth/__init__.py or review util/auth/README.md

Arguments

  --client / -c - path to client credentials file used to authenticate
  --user / -u - path to user credentials file to be created if it does not exist.

Example

  python auth/helper.py -u [user credentials path] -c [client credentials path]


