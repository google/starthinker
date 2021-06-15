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

import re
import json

from googleapiclient.errors import HttpError
from starthinker.util.google_api import API_DV360

RE_URL = re.compile(r'^.*://')

class Assigned_Targeting:


  def _check_settable(func):
    def wrapper(self, *args, **kwargs):
      operation = func.__name__.replace('add_', '').replace('delete_', '')
      if self.lineitem:
        return func(self, *args, **kwargs)
      elif self.partner:
        if operation == 'channel':
          return func(self, *args, **kwargs)
      elif self.advertiser:
        if operation in ('channel', 'content_label', 'sensitive_category'):
          return func(self, *args, **kwargs)
    return wrapper


  def __init__(self, config, auth, partnerId=None, advertiserId=None, lineItemId=None):
    self.config = config
    self.auth = auth
    self.partner = partnerId
    self.advertiser = advertiserId
    self.lineitem = lineItemId

    self.channels = { 'delete':[], 'add':[] }
    self.options_cache = {}
    self.assigneds_cache = {}
    self.add_cache = set()
    self.delete_cache = set()
    self.exists_cache = {}
    self.audience_cache = None

    self.delete_requests = {}
    self.create_requests = {}

    self.warnings = []


  def _url_domain(self, url):
    return '.'.join(RE_URL.sub('', url).split('.')[-2:])


  def _delete(self, targeting_type, *args):
    try:
      if not self.already_deleted(targeting_type, *args):
        targeting_id = self._already_exists(targeting_type, *args)
        if targeting_id:
          self.delete_requests.setdefault(targeting_type, []).append(targeting_id)
        else:
          self.warnings.append('Already deleted at this layer %s.' % targeting_type)
    except HttpError as e:
      self.warnings.append('Targeting Error: %s' % str(e))


  def _get_id(self, options, key, *args):
    for option in options:
      if option.get('inheritance', 'NOT_INHERITED') != 'NOT_INHERITED': continue

      if option['targetingType'] == 'TARGETING_TYPE_CHANNEL':
        if option['channelDetails']['channelId'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_APP_CATEGORY':
        if option['appCategoryDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_APP':
        if option['appDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_URL':
        if option['urlDetails']['url'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_DAY_AND_TIME':
        if (option['dayAndTimeDetails']['dayOfWeek'] == args[0]
        and option['dayAndTimeDetails']['startHour'] == args[1]
        and option['dayAndTimeDetails']['endHour'] == args[2]
        and option['dayAndTimeDetails']['timeZoneResolution'] == args[3]):
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_AGE_RANGE':
        if option['ageRangeDetails']['ageRange'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_REGIONAL_LOCATION_LIST':
        if option['regionalLocationListDetails']['regionalLocationListId'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_PROXIMITY_LOCATION_LIST':
        if option['proximityLocationListDetails']['proximityLocationListId'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_GENDER':
        if option['genderDetails']['gender'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_VIDEO_PLAYER_SIZE':
        if option['videoPlayerSizeDetails']['videoPlayerSize'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_USER_REWARDED_CONTENT':
        if option['userRewardedContentDetails']['userRewardedContent'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_PARENTAL_STATUS':
        if option['parentalStatusDetails']['parentalStatus'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_CONTENT_INSTREAM_POSITION':
        if not args: # single value on lookup
          return option[key]
        elif option['contentInstreamPositionDetails']['contentInstreamPosition'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION':
        if not args: # single value on lookup
          return option[key]
        elif option['contentOutstreamPositionDetails']['contentOutstreamPosition'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_DEVICE_TYPE':
        if option['deviceTypeDetails']['deviceType'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_BROWSER':
        if option['browserDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_HOUSEHOLD_INCOME':
        if option['householdIncomeDetails']['householdIncome'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_ON_SCREEN_POSITION':
        if option['onScreenPositionDetails']['onScreenPosition'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_CARRIER_AND_ISP':
        if option['carrierAndIspDetails']['displayName'] == args[0] and option['carrierAndIspDetails']['type'] == args[1]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_KEYWORD':
        if option['keywordDetails']['keyword'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_NEGATIVE_KEYWORD_LIST':
        if option['negativeKeywordListDetails']['negativeKeywordListId'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_OPERATING_SYSTEM':
        if option['operatingSystemDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_DEVICE_MAKE_MODEL':
        if option['deviceMakeModelDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_ENVIRONMENT':
        if option['environmentDetails']['environment'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_INVENTORY_SOURCE':
        if option['inventorySourceDetails']['inventorySourceId'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_CATEGORY': # fix add check for negative flag
        if option['categoryDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_VIEWABILITY':
        if not args: # single value on lookup
          return option[key]
        elif option['viewabilityDetails']['viewability'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_AUTHORIZED_SELLER_STATUS':
        if not args: # single value on lookup
          return option[key]
        elif option['authorizedSellerStatusDetails']['authorizedSellerStatus'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_LANGUAGE':
        if option['languageDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_GEO_REGION':
        if (option['geoRegionDetails']['displayName'] == args[0]
        and option['geoRegionDetails']['geoRegionType'] == args[1]):
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_INVENTORY_SOURCE':
        if option['inventorySourceGroupDetails']['inventorySourceGroupId'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION':
        if 'digitalContentLabelExclusionDetails' in option:
          if option['digitalContentLabelExclusionDetails']['contentRatingTier'] == args[0]:
            return option[key]
        else:
          if option['digitalContentLabelDetails']['contentRatingTier'] == args[0]:
            return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION':
        if 'sensitiveCategoryExclusionDetails' in option and option['sensitiveCategoryExclusionDetails']['sensitiveCategory'] == args[0]:
          return option[key]
        elif 'sensitiveCategoryDetails' in option and option['sensitiveCategoryDetails']['sensitiveCategory'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_EXCHANGE':
        if option['exchangeDetails'].get('exchange') == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_SUB_EXCHANGE':
        if option['subExchangeDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_AUDIENCE_GROUP':
        return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_THIRD_PARTY_VERIFIER':
        raise NotImplementedError
    return None


  def already_added(self, targeting_type, *args):
    token = '%s%s' % (targeting_type, json.dumps(args))
    if token in self.add_cache:
      return True
    else:
      self.add_cache.add(token)
      return False


  def already_deleted(self, targeting_type, *args):
    token = '%s%s' % (targeting_type, json.dumps(args))
    if token in self.delete_cache:
      return True
    else:
      self.delete_cache.add(token)
      return False


  def _already_exists(self, targeting_type, *args):
    token = '%s%s' % (targeting_type, json.dumps(args))
    if token not in self.exists_cache:
      self.exists_cache[token] = self.get_assigned_id(targeting_type, *args)
    return self.exists_cache[token]


  def already_exists(self, targeting_type, *args):
    token = '%s%s' % (targeting_type, json.dumps(args))
    if token not in self.exists_cache:
      self.exists_cache[token] = self.get_assigned_id(targeting_type, *args)
      if self.exists_cache[token]:
        self.warnings.append('Already set %s.' % targeting_type)
    return self.exists_cache[token]


  def get_option_list(self, targeting_type):
    if targeting_type not in self.options_cache:
      self.options_cache[targeting_type] = list(API_DV360(
        self.config, self.auth,
        iterate=True
      ).targetingTypes().targetingOptions().list(
        advertiserId=str(self.advertiser),
        targetingType=targeting_type
      ).execute())
    return self.options_cache[targeting_type]


  def get_option_id(self, targeting_type, *args):
    return self._get_id(
      self.get_option_list(targeting_type),
      'targetingOptionId',
      *args
    )


  def get_assigned_list(self, targeting_type):
    if targeting_type not in self.assigneds_cache:
      if self.lineitem:
        self.assigneds_cache[targeting_type] = list(API_DV360(
          self.config, self.auth,
          iterate=True
        ).advertisers().lineItems().targetingTypes().assignedTargetingOptions().list(
          lineItemId=str(self.lineitem),
          advertiserId=str(self.advertiser),
          targetingType=targeting_type
        ).execute())
      elif self.partner:
        self.assigneds_cache[targeting_type] = list(API_DV360(
          self.config, self.auth,
          iterate=True
        ).partners().targetingTypes().assignedTargetingOptions().list(
          partnerId=str(self.partner),
          targetingType=targeting_type
        ).execute())
      elif self.advertiser:
        self.assigneds_cache[targeting_type] = list(API_DV360(
          self.config, self.auth,
          iterate=True
        ).advertisers().targetingTypes().assignedTargetingOptions().list(
          advertiserId=str(self.advertiser),
          targetingType=targeting_type
        ).execute())
    return self.assigneds_cache[targeting_type]


  def get_assigned_id(self, targeting_type, *args):
    if targeting_type == 'TARGETING_TYPE_AUDIENCE_GROUP': return 'audienceGroup'
    else:
      return self._get_id(
        self.get_assigned_list(targeting_type),
        'assignedTargetingOptionId',
        *args
      )


  def get_assigned_audience(self, audience_type):
    if self.audience_cache is None:
      self.audience_cache = (self.get_assigned_list('TARGETING_TYPE_AUDIENCE_GROUP') or [{}])[0]
    return self.audience_cache.get(audience_type, {})


  @_check_settable
  def add_authorized_seller(self, authorizedSellerStatus):
    if not self.already_added('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS'):
      self.delete_authorized_seller()
      self.create_requests.setdefault('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', [])
      self.create_requests['TARGETING_TYPE_AUTHORIZED_SELLER_STATUS'].append({ 'authorizedSellerStatusDetails':{
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', authorizedSellerStatus)
      }})


  @_check_settable
  def delete_authorized_seller(self, authorizedSellerStatus):
    self._delete('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', authorizedSellerStatus)


  @_check_settable
  def add_user_rewarded_content(self, userRewardedContent):
    if not self.already_added('TARGETING_TYPE_USER_REWARDED_CONTENT'):
      self.delete_user_rewarded_content()
      self.create_requests.setdefault('TARGETING_TYPE_USER_REWARDED_CONTENT', [])
      self.create_requests['TARGETING_TYPE_USER_REWARDED_CONTENT'].append({ 'userRewardedContentDetails':{
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_USER_REWARDED_CONTENT', userRewardedContent)
      }})


  @_check_settable
  def delete_user_rewarded_content(self, userRewardedContent):
    self._delete('TARGETING_TYPE_USER_REWARDED_CONTENT', userRewardedContent)


  @_check_settable
  def add_exchange(self, exchange):
    if not self.already_added('TARGETING_TYPE_EXCHANGE', exchange):
      self.delete_exchange(exchange)
      self.create_requests.setdefault('TARGETING_TYPE_EXCHANGE', [])
      self.create_requests['TARGETING_TYPE_EXCHANGE'].append({ 'exchangeDetails':{
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_EXCHANGE', exchange)
      }})


  @_check_settable
  def delete_exchange(self, exchange):
    self._delete('TARGETING_TYPE_EXCHANGE', exchange)


  @_check_settable
  def add_sub_exchange(self, subExchange):
    if not self.already_added('TARGETING_TYPE_SUB_EXCHANGE', subExchange):
      if not self.already_exists('TARGETING_TYPE_SUB_EXCHANGE', subExchange):
        self.delete_sub_exchange(subExchange)
        self.create_requests.setdefault('TARGETING_TYPE_SUB_EXCHANGE', [])
        self.create_requests['TARGETING_TYPE_SUB_EXCHANGE'].append({ 'subExchangeDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_SUB_EXCHANGE', subExchange)
        }})


  @_check_settable
  def delete_sub_exchange(self, subExchange):
    self._delete('TARGETING_TYPE_SUB_EXCHANGE', subExchange)


  @_check_settable
  def add_channel(self, channelId, negative):
    if not self.already_added('TARGETING_TYPE_CHANNEL', channelId):
      if not self.already_exists('TARGETING_TYPE_CHANNEL', channelId, negative):
        self.delete_channel(channelId)
        self.create_requests.setdefault('TARGETING_TYPE_CHANNEL', [])
        self.create_requests['TARGETING_TYPE_CHANNEL'].append({ 'channelDetails':{
          'channelId': channelId,
          'negative':negative
        }})


  @_check_settable
  def delete_channel(self, channelId):
    self._delete('TARGETING_TYPE_CHANNEL', channelId)


  @_check_settable
  def add_inventory_source(self, inventorySourceId):
    if not self.already_added('TARGETING_TYPE_INVENTORY_SOURCE', inventorySourceId):
      if not self.already_exists('TARGETING_TYPE_INVENTORY_SOURCE', inventorySourceId):
        self.delete_inventory_source(inventorySourceId)
        self.create_requests.setdefault('TARGETING_TYPE_INVENTORY_SOURCE', [])
        self.create_requests['TARGETING_TYPE_INVENTORY_SOURCE'].append({ 'inventorySourceDetails':{
          'inventorySourceId': inventorySourceId,
        }})


  @_check_settable
  def delete_inventory_source(self, inventorySourceId):
    self._delete('TARGETING_TYPE_INVENTORY_SOURCE', inventorySourceId)


  @_check_settable
  def add_inventory_group(self, inventorySourceGroupId):
    if not self.already_added('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', inventorySourceGroupId):
      if not self.already_exists('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', inventorySourceGroupId):
        self.delete_inventory_source_group(inventorySourceGroupId)
        self.create_requests.setdefault('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', [])
        self.create_requests['TARGETING_TYPE_INVENTORY_SOURCE_GROUP'].append({ 'inventorySourceGroupDetails':{
          'inventorySourceGroupId': inventorySourceGroupId
      }})


  @_check_settable
  def delete_inventory_group(self, inventorySourceGroupId):
    self._delete('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', inventorySourceGroupId)


  @_check_settable
  def add_url(self, url, negative):
    url = self._url_domain(url)
    if not self.already_added('TARGETING_TYPE_URL', url):
      if not self.already_exists('TARGETING_TYPE_URL', url, negative):
        self.delete_url(url)
        self.create_requests.setdefault('TARGETING_TYPE_URL', [])
        self.create_requests['TARGETING_TYPE_URL'].append({ 'urlDetails':{
          'url': url,
          'negative':negative
        }})


  @_check_settable
  def delete_url(self, url):
    url = self._url_domain(url)
    self._delete('TARGETING_TYPE_URL', url)


  @_check_settable
  def add_app(self, app, negative):
    if not self.already_added('TARGETING_TYPE_APP', app):
      if not self.already_exists('TARGETING_TYPE_APP', app):
        self.delete_app(app)
        self.create_requests.setdefault('TARGETING_TYPE_APP', [])
        self.create_requests['TARGETING_TYPE_APP'].append({ 'appDetails':{
          'appId': app,
          'negative':negative
        }})


  @_check_settable
  def delete_app(self, app):
    self._delete('TARGETING_TYPE_APP', app)


  @_check_settable
  def add_app_category(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_APP_CATEGORY', displayName):
      if not self.already_exists('TARGETING_TYPE_APP_CATEGORY', displayName, negative):
        self.delete_app_category(displayName)
        self.create_requests.setdefault('TARGETING_TYPE_APP_CATEGORY', [])
        self.create_requests['TARGETING_TYPE_APP_CATEGORY'].append({ 'appCategoryDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_APP_CATEGORY', displayName),
          'negative':negative
        }})


  @_check_settable
  def delete_app_category(self, displayName):
    self._delete('TARGETING_TYPE_APP_CATEGORY', displayName)


  @_check_settable
  def add_content_label(self, contentRatingTier):
    if not self.already_added('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', contentRatingTier):
      if not self.already_exists('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', contentRatingTier):
        self.create_requests.setdefault('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', [])
        self.create_requests['TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION'].append({ 'digitalContentLabelExclusionDetails':{
          'excludedTargetingOptionId': self.get_option_id('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', contentRatingTier)
        }})


  @_check_settable
  def delete_content_label(self, contentRatingTier):
    self._delete('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', contentRatingTier)


  @_check_settable
  def add_sensitive_category(self, sensitiveCategory):
    if not self.already_added('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', sensitiveCategory):
      if not self.already_exists('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', sensitiveCategory):
        self.create_requests.setdefault('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', [])
        self.create_requests['TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION'].append({ 'sensitiveCategoryExclusionDetails':{
          'excludedTargetingOptionId': self.get_option_id('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', sensitiveCategory)
        }})


  @_check_settable
  def delete_sensitive_category(self, sensitiveCategory):
    self._delete('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', sensitiveCategory)


  @_check_settable
  def add_negative_keyword_list(self, negativeKeywordListId):
    if not self.already_added('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', negativeKeywordListId):
      if not self.already_exists('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', negativeKeywordListId):
        self.create_requests.setdefault('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', [])
        self.create_requests['TARGETING_TYPE_NEGATIVE_KEYWORD_LIST'].append({ 'negativeKeywordListDetails':{
          'negativeKeywordListId': negativeKeywordListId
        }})


  @_check_settable
  def delete_negative_keyword_list(self, negativeKeywordListId):
    self._delete('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', negativeKeywordListId)


  @_check_settable
  def add_category(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_CATEGORY', displayName):
      if not self.already_exists('TARGETING_TYPE_CATEGORY', displayName, negative):
        self.create_requests.setdefault('TARGETING_TYPE_CATEGORY', [])
        self.create_requests['TARGETING_TYPE_CATEGORY'].append({ 'categoryDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_CATEGORY', displayName),
          'negative': negative
        }})


  @_check_settable
  def delete_category(self, displayName):
    self._delete('TARGETING_TYPE_CATEGORY', displayName)


  @_check_settable
  def add_keyword(self, keyword, negative):
    if not self.already_added('TARGETING_TYPE_KEYWORD', keyword):
      if not self.already_exists('TARGETING_TYPE_KEYWORD', keyword, negative):
        self.create_requests.setdefault('TARGETING_TYPE_KEYWORD', [])
        self.create_requests['TARGETING_TYPE_KEYWORD'].append({ 'keywordDetails':{
          'keyword': keyword,
          'negative': negative
        }})


  @_check_settable
  def delete_keyword(self, keyword):
    self._delete('TARGETING_TYPE_KEYWORD', keyword)


  @_check_settable
  def add_age_range(self, ageRange):
    if not self.already_added('TARGETING_TYPE_AGE_RANGE', ageRange):
      if not self.already_exists('TARGETING_TYPE_AGE_RANGE', ageRange):
        self.create_requests.setdefault('TARGETING_TYPE_AGE_RANGE', [])
        self.create_requests['TARGETING_TYPE_AGE_RANGE'].append({ 'ageRangeDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_AGE_RANGE', ageRange)
        }})


  @_check_settable
  def delete_age_range(self, ageRange):
    self._delete('TARGETING_TYPE_AGE_RANGE', ageRange)


  @_check_settable
  def add_gender(self, gender):
    if not self.already_added('TARGETING_TYPE_GENDER', gender):
      if not self.already_exists('TARGETING_TYPE_GENDER', gender):
        self.create_requests.setdefault('TARGETING_TYPE_GENDER', [])
        self.create_requests['TARGETING_TYPE_GENDER'].append({ 'genderDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_GENDER', gender)
        }})


  @_check_settable
  def delete_gender(self, gender):
    self._delete('TARGETING_TYPE_GENDER', gender)


  @_check_settable
  def add_parental_status(self, parentalStatus):
    if not self.already_added('TARGETING_TYPE_PARENTAL_STATUS', parentalStatus):
      if not self.already_exists('TARGETING_TYPE_PARENTAL_STATUS', parentalStatus):
        self.create_requests.setdefault('TARGETING_TYPE_PARENTAL_STATUS', [])
        self.create_requests['TARGETING_TYPE_PARENTAL_STATUS'].append({ 'parentalStatusDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_PARENTAL_STATUS', parentalStatus)
        }})


  @_check_settable
  def delete_parental_status(self, parentalStatus):
    self._delete('TARGETING_TYPE_PARENTAL_STATUS', parentalStatus)


  @_check_settable
  def add_household_income(self, householdIncome):
    if not self.already_added('TARGETING_TYPE_HOUSEHOLD_INCOME', householdIncome):
      if not self.already_exists('TARGETING_TYPE_HOUSEHOLD_INCOME', householdIncome):
        self.create_requests.setdefault('TARGETING_TYPE_HOUSEHOLD_INCOME', [])
        self.create_requests['TARGETING_TYPE_HOUSEHOLD_INCOME'].append({ 'householdIncomeDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_HOUSEHOLD_INCOME', householdIncome)
        }})


  @_check_settable
  def delete_household_income(self, householdIncome):
    self._delete('TARGETING_TYPE_HOUSEHOLD_INCOME', householdIncome)


  @_check_settable
  def add_language(self, displayName, negative):
    displayName = displayName.title()
    if not self.already_added('TARGETING_TYPE_LANGUAGE', displayName):
      if not self.already_exists('TARGETING_TYPE_LANGUAGE', displayName):
        self.create_requests.setdefault('TARGETING_TYPE_LANGUAGE', [])
        self.create_requests['TARGETING_TYPE_LANGUAGE'].append({ 'languageDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_LANGUAGE', displayName),
          'negative':negative
        }})


  @_check_settable
  def delete_language(self, displayName):
    displayName = displayName.title()
    self._delete('TARGETING_TYPE_LANGUAGE', displayName)


  @_check_settable
  def add_included_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency, group):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedFirstAndThirdPartyAudienceGroups', [])

    audience = { "firstAndThirdPartyAudienceId": firstAndThirdPartyAudienceId, "recency": recency }
    group = min(max(group, 1), 10)

    while len(audiences['includedFirstAndThirdPartyAudienceGroups']) < group:
      audiences['includedFirstAndThirdPartyAudienceGroups'].append({'settings':[]})

    if audience not in audiences['includedFirstAndThirdPartyAudienceGroups'][group - 1]['settings']:
      audiences['includedFirstAndThirdPartyAudienceGroups'][group - 1]['settings'].append(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }


  @_check_settable
  def delete_included_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency, group):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedFirstAndThirdPartyAudienceGroups', [])

    audience = { "firstAndThirdPartyAudienceId": firstAndThirdPartyAudienceId, "recency": recency }
    group = min(max(group, 1), 10)

    while len(audiences['includedFirstAndThirdPartyAudienceGroups']) < group:
      audiences['includedFirstAndThirdPartyAudienceGroups'].append({'settings':[]})

    if audience in audiences['includedFirstAndThirdPartyAudienceGroups'][group - 1]['settings']:
      audiences['includedFirstAndThirdPartyAudienceGroups'][group - 1]['settings'].remove(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }



  @_check_settable
  def add_excluded_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('excludedFirstAndThirdPartyAudienceGroup', { 'settings':[] })

    audience = { "firstAndThirdPartyAudienceId": firstAndThirdPartyAudienceId, "recency": recency }
    if audience not in audiences['excludedFirstAndThirdPartyAudienceGroup']['settings']:
      audiences['excludedFirstAndThirdPartyAudienceGroup']['settings'].append(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def delete_excluded_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('excludedFirstAndThirdPartyAudienceGroup', { 'settings':[] })

    audience = { "firstAndThirdPartyAudienceId": firstAndThirdPartyAudienceId, "recency": recency }
    if audience in audiences['excludedFirstAndThirdPartyAudienceGroup']['settings']:
      audiences['excludedFirstAndThirdPartyAudienceGroup']['settings'].remove(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def add_included_google_audience(self, googleAudienceId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedGoogleAudienceGroup', { 'settings':[] })

    audience = { 'googleAudienceId':googleAudienceId }
    if audience not in audiences['includedGoogleAudienceGroup']['settings']:
      audiences['includedGoogleAudienceGroup']['settings'].append(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def delete_included_google_audience(self, googleAudienceId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedGoogleAudienceGroup', { 'settings':[] })

    audience = { 'googleAudienceId':googleAudienceId }
    if audience in audiences['includedGoogleAudienceGroup']['settings']:
      audiences['includedGoogleAudienceGroup']['settings'].remove(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def add_excluded_google_audience(self, googleAudienceId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('excludedGoogleAudienceGroup', { 'settings':[] })

    audience = { 'googleAudienceId':googleAudienceId }
    if audience not in audiences['excludedGoogleAudienceGroup']['settings']:
      audiences['excludedGoogleAudienceGroup']['settings'].append(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def delete_excluded_google_audience(self, googleAudienceId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('excludedGoogleAudienceGroup', { 'settings':[] })

    audience = { 'googleAudienceId':googleAudienceId }
    if audience in audiences['excludedGoogleAudienceGroup']['settings']:
      audiences['excludedGoogleAudienceGroup']['settings'].remove(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def add_included_custom_list(self, customListId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedCustomListGroup', { 'settings':[] })

    audience = { 'customListId':customListId }
    if audience not in audiences['includedCustomListGroup']['settings']:
      audiences['includedCustomListGroup']['settings'].append(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def delete_included_custom_list(self, customListId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedCustomListGroup', { 'settings':[] })

    audience = { 'customListId':customListId }
    if audience in audiences['includedCustomListGroup']['settings']:
      audiences['includedCustomListGroup']['settings'].remove(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def add_included_combined_audience(self, combinedAudienceId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedCombinedAudienceGroup', { 'settings':[] })

    audience = { 'combinedAudienceId':combinedAudienceId }
    if audience not in audiences['includedCombinedAudienceGroup']['settings']:
      audiences['includedCombinedAudienceGroup']['settings'].append(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def delete_included_combined_audience(self, combinedAudienceId):
    audiences = self.get_assigned_audience('audienceGroupDetails')
    audiences.setdefault('includedCombinedAudienceGroup', { 'settings':[] })

    audience = { 'combinedAudienceId':combinedAudienceId }
    if audience in audiences['includedCombinedAudienceGroup']['settings']:
      audiences['includedCombinedAudienceGroup']['settings'].remove(audience)
      self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP'] = { 'audienceGroupDetails':audiences }
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  @_check_settable
  def add_device_type(self, deviceType):
    if not self.already_added('TARGETING_TYPE_DEVICE_TYPE', deviceType):
      if not self.already_exists('TARGETING_TYPE_DEVICE_TYPE', deviceType):
        self.create_requests.setdefault('TARGETING_TYPE_DEVICE_TYPE', [])
        self.create_requests['TARGETING_TYPE_DEVICE_TYPE'].append({ 'deviceTypeDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_DEVICE_TYPE', deviceType)
        }})


  @_check_settable
  def delete_device_type(self, deviceType):
    self._delete('TARGETING_TYPE_DEVICE_TYPE', deviceType)


  @_check_settable
  def add_make_model(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_DEVICE_MAKE_MODEL', displayName):
      if not self.already_exists('TARGETING_TYPE_DEVICE_MAKE_MODEL', displayName, negative): # fix delete of negative
        self.create_requests.setdefault('TARGETING_TYPE_DEVICE_MAKE_MODEL', [])
        self.create_requests['TARGETING_TYPE_DEVICE_MAKE_MODEL'].append({ 'deviceMakeModelDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_DEVICE_MAKE_MODEL', displayName),
          'negative':negative
        }})


  @_check_settable
  def delete_make_model(self, displayName):
    self._delete('TARGETING_TYPE_DEVICE_MAKE_MODEL', displayName)


  @_check_settable
  def add_operating_system(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_OPERATING_SYSTEM', displayName):
      if not self.already_added('TARGETING_TYPE_OPERATING_SYSTEM', displayName, negative): # fix delete of negative
        self.create_requests.setdefault('TARGETING_TYPE_OPERATING_SYSTEM', [])
        self.create_requests['TARGETING_TYPE_OPERATING_SYSTEM'].append({ 'operatingSystemDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_OPERATING_SYSTEM', displayName),
          'negative':negative
        }})


  @_check_settable
  def delete_operating_system(self, displayName):
    self._delete('TARGETING_TYPE_OPERATING_SYSTEM', displayName)


  @_check_settable
  def add_browser(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_BROWSER', displayName):
      if not self.already_exists('TARGETING_TYPE_BROWSER', displayName, negative): # fix delete of negative
        self.create_requests.setdefault('TARGETING_TYPE_BROWSER', [])
        self.create_requests['TARGETING_TYPE_BROWSER'].append({ 'browserDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_BROWSER', displayName),
          'negative':negative
        }})


  @_check_settable
  def delete_browser(self, displayName):
    self._delete('TARGETING_TYPE_BROWSER', displayName)


  @_check_settable
  def add_environment(self, environment):
    if not self.already_added('TARGETING_TYPE_ENVIRONMENT', environment):
      if not self.already_exists('TARGETING_TYPE_ENVIRONMENT', environment):
        self.create_requests.setdefault('TARGETING_TYPE_ENVIRONMENT', [])
        self.create_requests['TARGETING_TYPE_ENVIRONMENT'].append({ 'environmentDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_ENVIRONMENT', environment),
        }})


  @_check_settable
  def delete_environment(self, environment):
    self._delete('TARGETING_TYPE_ENVIRONMENT', environment)


  @_check_settable
  def add_carrier_and_isp(self, displayName, negative):
    lookupName, lookupType = displayName.rsplit(' - ',1)
    lookupType = 'CARRIER_AND_ISP_TYPE_%s' % lookupType

    if not self.already_added('TARGETING_TYPE_CARRIER_AND_ISP', displayName):
      if not self.already_exists('TARGETING_TYPE_CARRIER_AND_ISP', displayName, negative):  # fix delete of negative
        self.create_requests.setdefault('TARGETING_TYPE_CARRIER_AND_ISP', [])
        self.create_requests['TARGETING_TYPE_CARRIER_AND_ISP'].append({ 'carrierAndIspDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_CARRIER_AND_ISP', lookupName, lookupType),
          'negative':negative
        }})


  @_check_settable
  def delete_carrier_and_isp(self, displayName):
    lookupName, lookupType = displayName.rsplit(' - ',1)
    lookupType = 'CARRIER_AND_ISP_TYPE_%s' % lookupType

    self._delete('TARGETING_TYPE_CARRIER_AND_ISP', lookupName, lookupType)


  @_check_settable
  def add_day_and_time(self, dayOfWeek, startHour, endHour, timeZoneResolution):
    if not self.already_added('TARGETING_TYPE_DAY_AND_TIME', dayOfWeek, startHour, endHour, timeZoneResolution):
      if not self.already_exists('TARGETING_TYPE_DAY_AND_TIME', dayOfWeek, startHour, endHour, timeZoneResolution):
        self.create_requests.setdefault('TARGETING_TYPE_DAY_AND_TIME', [])
        self.create_requests['TARGETING_TYPE_DAY_AND_TIME'].append({ 'dayAndTimeDetails':{
          'dayOfWeek': dayOfWeek,
          'startHour': startHour,
          'endHour': endHour,
          'timeZoneResolution': timeZoneResolution
        }})


  @_check_settable
  def delete_day_and_time(self, dayOfWeek, startHour, endHour, timeZoneResolution):
    self._delete('TARGETING_TYPE_DAY_AND_TIME', dayOfWeek, startHour, endHour, timeZoneResolution)


  @_check_settable
  def add_geo_region(self, displayName, geoRegionType, negative):
    if not self.already_added('TARGETING_TYPE_GEO_REGION', displayName):
      if not self.already_exists('TARGETING_TYPE_GEO_REGION', displayName, negative): # fix delete of negative
        self.create_requests.setdefault('TARGETING_TYPE_GEO_REGION', [])
        self.create_requests['TARGETING_TYPE_GEO_REGION'].append({ 'geoRegionDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_GEO_REGION', displayName, geoRegionType),
          'negative':negative
        }})


  @_check_settable
  def delete_geo_region(self, displayName):
    self._delete('TARGETING_TYPE_GEO_REGION', displayName)


  @_check_settable
  def add_proximity_location_list(self, proximityLocationListId, proximityRadiusRange):
    if not self.already_added('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', proximityLocationListId):
      if not self.already_exists('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', proximityLocationListId, proximityRadiusRange): # fix delete of range
        self.create_requests.setdefault('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', [])
        self.create_requests['TARGETING_TYPE_PROXIMITY_LOCATION_LIST'].append({ 'proximityLocationListDetails':{
          'proximityLocationListId':proximityLocationListId,
          'proximityRadiusRange':proximityRadiusRange
        }})


  @_check_settable
  def delete_proximity_location_list(self, proximityLocationListId):
    self._delete('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', proximityLocationListId)


  @_check_settable
  def add_regional_location_list(self, regionalLocationListId, negative):
    if not self.already_added('TARGETING_TYPE_REGIONAL_LOCATION_LIST', regionalLocationListId):
      if not self.already_exists('TARGETING_TYPE_REGIONAL_LOCATION_LIST', regionalLocationListId):
        self.create_requests.setdefault('TARGETING_TYPE_REGIONAL_LOCATION_LIST', [])
        self.create_requests['TARGETING_TYPE_REGIONAL_LOCATION_LIST'].append({ 'regionalLocationListDetails':{
          'regionalLocationListId': regionalLocationListId,
          'negative':negative
        }})


  @_check_settable
  def delete_regional_location_list(self, regionalLocationListId):
    self._delete('TARGETING_TYPE_REGIONAL_LOCATION_LIST', regionalLocationListId)


  @_check_settable
  def add_video_player_size(self, videoPlayerSize):
    if not self.already_added('TARGETING_TYPE_VIDEO_PLAYER_SIZE', videoPlayerSize):
      if not self.already_exists('TARGETING_TYPE_VIDEO_PLAYER_SIZE', videoPlayerSize):
        self.create_requests.setdefault('TARGETING_TYPE_VIDEO_PLAYER_SIZE', [])
        self.create_requests['TARGETING_TYPE_VIDEO_PLAYER_SIZE'].append({ 'videoPlayerSizeDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_VIDEO_PLAYER_SIZE', videoPlayerSize)
        }})


  @_check_settable
  def delete_video_player_size(self, videoPlayerSize):
    self._delete('TARGETING_TYPE_VIDEO_PLAYER_SIZE', videoPlayerSize)


  @_check_settable
  def add_in_stream_position(self, contentInstreamPosition):
    if not self.already_added('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', contentInstreamPosition):
      if not self.already_exists('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', contentInstreamPosition):
        self.create_requests.setdefault('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', [])
        self.create_requests['TARGETING_TYPE_CONTENT_INSTREAM_POSITION'].append({ 'contentInstreamPositionDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', contentInstreamPosition)
        }})


  @_check_settable
  def delete_in_stream_position(self, contentInstreamPosition):
    self._delete('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', contentInstreamPosition)


  @_check_settable
  def add_out_stream_position(self, contentOutstreamPosition):
    if not self.already_added('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION', contentOutstreamPosition):
      if not self.already_exists('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION', contentOutstreamPosition):
        self.create_requests.setdefault('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION', [])
        self.create_requests['TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION'].append({ 'contentOutstreamPositionDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION', contentOutstreamPosition)
        }})


  @_check_settable
  def delete_out_stream_position(self, contentOutstreamPosition):
    self._delete('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION', contentOutstreamPosition)


  @_check_settable
  def add_on_screen_position(self, onScreenPosition):
    if not self.already_added('TARGETING_TYPE_ON_SCREEN_POSITION'):
      if not self.already_exists('TARGETING_TYPE_ON_SCREEN_POSITION', onScreenPosition):
       self.create_requests.setdefault('TARGETING_TYPE_ON_SCREEN_POSITION', [])
       self.create_requests['TARGETING_TYPE_ON_SCREEN_POSITION'].append({ 'onScreenPositionDetails':{
         'targetingOptionId': self.get_option_id('TARGETING_TYPE_ON_SCREEN_POSITION', onScreenPosition)
       }})


  @_check_settable
  def delete_on_screen_position(self, onScreenPosition):
    self._delete('TARGETING_TYPE_ON_SCREEN_POSITION', onScreenPosition)


  @_check_settable
  def add_viewability(self, viewability):
    if not self.already_added('TARGETING_TYPE_VIEWABILITY'):
      if not self.already_exists('TARGETING_TYPE_VIEWABILITY', viewability):
        self._delete('TARGETING_TYPE_VIEWABILITY')
        self.create_requests.setdefault('TARGETING_TYPE_VIEWABILITY', [])
        self.create_requests['TARGETING_TYPE_VIEWABILITY'].append({ 'viewabilityDetails':{
          'targetingOptionId': self.get_option_id('TARGETING_TYPE_VIEWABILITY', viewability)
        }})


  @_check_settable
  def delete_viewability(self, viewability):
    self._delete('TARGETING_TYPE_VIEWABILITY', viewability)


  def get_warnings(self):
    return self.warnings


  def get_body(self):
    if self.delete_requests or self.create_requests:
      return {
        'deleteRequests': [{
          'targetingType': k,
          'assignedTargetingOptionIds': v
        } for k, v in self.delete_requests.items()],
        'createRequests': [{
          'targetingType': k,
          'assignedTargetingOptions': v
        } for k, v in self.create_requests.items()]
      }
    else:
      return {}


  def execute(self):
    body = self.get_body()
    if body:
      if self.lineitem:
        return API_DV360(
          self.config, self.auth,
        ).advertisers().lineItems().bulkEditLineItemAssignedTargetingOptions(
          lineItemId=str(self.lineitem),
          advertiserId=str(self.advertiser),
        ).execute()
      elif self.partner:
        return API_DV360(
          self.config, self.auth
        ).partners().bulkEditPartnerAssignedTargetingOptions(
          partnerId=str(self.partner),
        ).execute()
      elif self.advertiser:
        return API_DV360(
          self.config, self.auth,
        ).advertisers().bulkEditAdvertiserAssignedTargetingOptions(
          advertiserId=str(self.advertiser),
        ).execute()
