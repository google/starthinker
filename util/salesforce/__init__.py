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

import os
import pprint
import urlparse
import urllib
import json
from third_party.simple_salesforce import Salesforce

from util.project import project

CONSUMER_SECRET = 2713950824552591511
CONSUMER_KEY = '3MVG9CEn_O3jvv0w5B5mOO0WKtxbhWg1NHgdYYRZ6P0HW5YL2QnoK4Nx0J.EpI5_DJjL6g8PEfYKJJFKuftIx'
CALLBACK = 'https://login.salesforce.com/services/oauth2/success'
LOGIN_URL = 'https://login.salesforce.com/services/oauth2/authorize?response_type=token&client_id=%s&redirect_uri=%s' % (CONSUMER_KEY, CALLBACK)


def authenticate():
  print "Visit: ", LOGIN_URL

  browser = raw_input('Open it in a browser for you (y/n)?')
  if browser == 'y': os.system("open '%s'" % LOGIN_URL)

  url_result = raw_input('If the page says "Remote Access Application Authorization", copy and paste the URL:')
  result = dict(urlparse.parse_qsl(url_result.split("success#")[1]));
  token = urllib.unquote(result["access_token"])
  instance_url = urllib.unquote(result["instance_url"])

  return token, instance_url


def get_service():
  try:
    with open(project.configuration['setup']['auth']['salesforce'], 'r') as data_file:
      data_auth = json.load(data_file)
  except:
    token, instance_url = authenticate()
    with open(project.configuration['setup']['auth']['salesforce'], 'w') as data_file:
      data_auth = { 'instance_url':instance_url, 'token':token }
      data_file.write(json.dumps(data_auth))
  return Salesforce(instance_url=data_auth['instance_url'], session_id=data_auth['token'])


def get_contact():
  sf = get_service()
  records = sf.query("SELECT Id, Name, Email FROM Contact")
  pprint.PrettyPrinter().pprint(records['records'])


def get_objects():
  sf = get_service()
  for obj in sf.describe()['sobjects']:
    yield obj

#  [obj['name'] for obj in description['sobjects'] if obj['queryable']]

def get_object_fields(name):
  sf = get_service()
  salesforceObject = sf.__getattr__(name)
  fieldNames = [field['name'] for field in salesforceObject.describe()['fields']]

  print fieldNames

  # then build a SOQL query against that object and do a query_all
#  try:
#    results = sf.query_all( "SELECT " + ", ".join(fieldNames) + " FROM " + name  )['records']
#    for row in results:
#    row.pop('attributes',None)
#  except SalesforceMalformedRequest as e:


def get_case():
  sf = get_service()
  
  pprint.PrettyPrinter().pprint(sf.describe())

  records = sf.query("SELECT CaseComment FROM Case")
  pprint.PrettyPrinter().pprint(records['records'])


def set_account(data):
  sf = get_service()
  sf.Account.create({'Name':'Testing'})
  
def set_attachemtn(data):
  sf = get_service()
  sf.Account.create({'Name':'Testing'})


if __name__ == "__main__":
  #authenticate()
  #get_case()

  #for obj in get_objects(): print obj['name']

  get_object_fields('Account')

  #set_account()



