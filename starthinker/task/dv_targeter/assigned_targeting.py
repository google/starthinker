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

from googleapiclient.errors import HttpError
from starthinker.util.google_api import API_DV360


class Assigned_Targeting:

  def __init__(self, auth, partnerId=None, advertiserId=None, lineItemId=None):
    self.auth = auth
    self.partner = partnerId
    self.advertiser = advertiserId
    self.lineitem = lineItemId

    self.channels = { 'delete':[], 'add':[] }
    self.options_cache = {}
    self.assigneds_cache = {}
    self.add_cache = set()
    self.delete_cache = set()
    self.audience_cache = None

    self.delete_requests = {}
    self.create_requests = {}


  def _delete(self, targeting_type, value=''):
    try:
      if not self.already_deleted(targeting_type, value):
        targeting_id = self.get_assigned_id(targeting_type, value)
        if targeting_id is not None:
          self.delete_requests.setdefault(targeting_type, []).append(targeting_id)
    except HttpError:
      pass


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
        if option['contentInstreamPositionDetails']['contentInstreamPosition'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION':
        if option['contentOutstreamPositionDetails']['contentOutstreamPosition'] == args[0]:
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
        if option['carrierAndIspDetails']['displayName'] == args[0]:
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
      elif option['targetingType'] == 'TARGETING_TYPE_CATEGORY':
        if option['categoryDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_VIEWABILITY':
        return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_AUTHORIZED_SELLER_STATUS':
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
        if option['digitalContentLabelExclusionDetails']['contentRatingTier'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION':
        if option['sensitiveCategoryExclusionDetails']['sensitiveCategory'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_EXCHANGE':
        if option['exchangeDetails']['exchange'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_SUB_EXCHANGE':
        if option['subExchangeDetails']['displayName'] == args[0]:
          return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_AUDIENCE_GROUP':
        return option[key]
      elif option['targetingType'] == 'TARGETING_TYPE_THIRD_PARTY_VERIFIER':
        raise NotImplementedError
    return None


  def already_added(self, targeting_type, value=''):
    token = '%s%s' % (targeting_type, value)
    if token in self.add_cache:
      return True
    else:
      self.add_cache.add(token)
      return False


  def already_deleted(self, targeting_type, value=''):
    token = '%s%s' % (targeting_type, value)
    if token in self.delete_cache:
      return True
    else:
      self.delete_cache.add(token)
      return False


  def get_option_list(self, targeting_type):
    if targeting_type not in self.options_cache:
      self.options_cache[targeting_type] = list(API_DV360(
        self.auth,
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
          self.auth,
          iterate=True
        ).advertisers().lineItems().targetingTypes().assignedTargetingOptions().list(
          lineItemId=str(self.lineitem),
          advertiserId=str(self.advertiser),
          targetingType=targeting_type
        ).execute())
      elif self.advertiser:
        self.assigneds_cache[targeting_type] = list(API_DV360(
          self.auth,
          iterate=True
        ).advertisers().targetingTypes().assignedTargetingOptions().list(
          advertiserId=str(self.advertiser),
          targetingType=targeting_type
        ).execute())
      elif self.partner:
        self.assigneds_cache[targeting_type] = list(API_DV360(
          self.auth,
          iterate=True
        ).partners().targetingTypes().assignedTargetingOptions().list(
          partnerId=str(self.partner),
          targetingType=targeting_type
        ).execute())
    return self.assigneds_cache[targeting_type]


  def get_assigned_id(self, targeting_type, *args):
    return self._get_id(
      self.get_assigned_list(targeting_type),
      'assignedTargetingOptionId',
      *args
    )


  def get_assigned_audience(self):
    if self.audience_cache is None:
      self.audience_cache = self.get_assigned_list('TARGETING_TYPE_AUDIENCE_GROUP')[0]
    return self.audience_cache


  def add_authorized_seller(self, authorizedSellerStatus):
    if not self.already_added('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS'):
      self.delete_authorized_seller()
      self.create_requests.setdefault('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', [])
      self.create_requests['TARGETING_TYPE_AUTHORIZED_SELLER_STATUS'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', authorizedSellerStatus)
      })


  def delete_authorized_seller(self):
    self._delete('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS')


  def add_user_rewarded_content(self, userRewardedContent):
    if not self.already_added('TARGETING_TYPE_USER_REWARDED_CONTENT'):
      self.delete_user_rewarded_content()
      self.create_requests.setdefault('TARGETING_TYPE_USER_REWARDED_CONTENT', [])
      self.create_requests['TARGETING_TYPE_USER_REWARDED_CONTENT'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', userRewardedContent)
      })


  def delete_user_rewarded_content(self):
    self._delete('TARGETING_TYPE_USER_REWARDED_CONTENT')


  def add_exchange(self, exchange):
    if not self.already_added('TARGETING_TYPE_EXCHANGE', exchange):
      self.delete_exchange(exchange)
      self.create_requests.setdefault('TARGETING_TYPE_EXCHANGE', [])
      self.create_requests['TARGETING_TYPE_EXCHANGE'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', exchange)
      })


  def delete_exchange(self, exchange):
    self._delete('TARGETING_TYPE_EXCHANGE', exchange)


  def add_sub_exchange(self, subExchange):
    if not self.already_added('TARGETING_TYPE_SUB_EXCHANGE', subExchange):
      self.delete_sub_exchange(subExchange)
      self.create_requests.setdefault('TARGETING_TYPE_SUB_EXCHANGE', [])
      self.create_requests['TARGETING_TYPE_SUB_EXCHANGE'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_AUTHORIZED_SELLER_STATUS', subExchange)
      })


  def delete_sub_exchange(self, subExchange):
    self._delete('TARGETING_TYPE_SUB_EXCHANGE', subExchange)


  def add_channel(self, channelId, negative):
    if not self.already_added('TARGETING_TYPE_CHANNEL', channelId):
      self.delete_channel(channelId)
      self.create_requests.setdefault('TARGETING_TYPE_CHANNEL', [])
      self.create_requests['TARGETING_TYPE_CHANNEL'].append({
        'channelId': channelId,
        'negative':negative
      })


  def delete_channel(self, channelId):
    self._delete('TARGETING_TYPE_CHANNEL', channelId)


  def add_inventory_source(self, inventorySourceId):
    if not self.already_added('TARGETING_TYPE_INVENTORY_SOURCE', inventorySourceId):
      self.delete_inventory_source(inventorySourceId)
      self.create_requests.setdefault('TARGETING_TYPE_INVENTORY_SOURCE', [])
      self.create_requests['TARGETING_TYPE_INVENTORY_SOURCE'].append({
        'inventorySourceId': inventorySourceId,
      })


  def delete_inventory_source(self, inventorySourceId):
    self._delete('TARGETING_TYPE_INVENTORY_SOURCE', inventorySourceId)


  def add_inventory_group(self, inventorySourceGroupId):
    if not self.already_added('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', inventorySourceGroupId):
      self.delete_inventory_source_group(inventorySourceGroupId)
      self.create_requests.setdefault('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', [])
      self.create_requests['TARGETING_TYPE_INVENTORY_SOURCE_GROUP'].append({
        'inventorySourceGroupId': inventorySourceGroupId
      })


  def delete_inventory_group(self, inventorySourceGroupId):
    self._delete('TARGETING_TYPE_INVENTORY_SOURCE_GROUP', inventorySourceGroupId)


  def add_url(self, url, negative):
    if not self.already_added('TARGETING_TYPE_URL', url):
      self.delete_url(url)
      self.create_requests.setdefault('TARGETING_TYPE_URL', [])
      self.create_requests['TARGETING_TYPE_URL'].append({
        'url': url,
        'negative':negative
      })


  def delete_url(self, url):
    self._delete('TARGETING_TYPE_URL', url)


  def add_app(self, app, negative):
    if not self.already_added('TARGETING_TYPE_APP', app):
      self.delete_app(app)
      self.create_requests.setdefault('TARGETING_TYPE_APP', [])
      self.create_requests['TARGETING_TYPE_APP'].append({
        'appId': app,
        'negative':negative
      })


  def delete_app(self, app):
    self._delete('TARGETING_TYPE_APP', app)


  def add_app_category(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_APP_CATEGORY'):
      self.delete_app_category(displayName)
      self.create_requests.setdefault('TARGETING_TYPE_APP_CATEGORY', [])
      self.create_requests['TARGETING_TYPE_APP_CATEGORY'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_APP_CATEGORY', displayName),
        'negative':negative
      })


  def delete_app_category(self):
    self._delete('TARGETING_TYPE_APP_CATEGORY')


  def add_content_label(self, contentRatingTier):
    if not self.already_added('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION'):
      self.delete_content_label(contentRatingTier)
      self.create_requests.setdefault('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', [])
      self.create_requests['TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION'].append({
        'excludedTargetingOptionId': self.get_option_id('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION', contentRatingTier)
      })


  def delete_content_label(self):
    self._delete('TARGETING_TYPE_DIGITAL_CONTENT_LABEL_EXCLUSION')


  def add_sensitive_category(self, sensitiveCategory):
    if not self.already_added('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION'):
      self.delete_sensitive_category()
      self.create_requests.setdefault('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', [])
      self.create_requests['TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION'].append({
        'excludedTargetingOptionId': self.get_option_id('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION', sensitiveCategory)
      })


  def delete_sensitive_category(self):
    self._delete('TARGETING_TYPE_SENSITIVE_CATEGORY_EXCLUSION')


  def add_negative_keyword_list(self, negativeKeywordListId):
    if not self.already_added('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', negativeKeywordListId):
      self.delete_negative_keyword_list(negativeKeywordListId)
      self.create_requests.setdefault('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', [])
      self.create_requests['TARGETING_TYPE_NEGATIVE_KEYWORD_LIST'].append({
        'negativeKeywordListId': negativeKeywordListId
      })


  def delete_negative_keyword_list(self, negativeKeywordListId):
    self._delete('TARGETING_TYPE_NEGATIVE_KEYWORD_LIST', negativeKeywordListId)


  def add_category(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_APP_CATEGORY'):
      self.delete_category(displayName)
      self.create_requests.setdefault('TARGETING_TYPE_APP_CATEGORY', [])
      self.create_requests['TARGETING_TYPE_APP_CATEGORY'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_APP_CATEGORY', displayName),
        'negative': negative
      })


  def delete_category(self, displayName):
    self._delete('TARGETING_TYPE_APP_CATEGORY', displayName)


  def add_keyword(self, keyword, negative):
    if not self.already_added('TARGETING_TYPE_KEYWORD'):
      self.delete_keyword(keyword)
      self.create_requests.setdefault('TARGETING_TYPE_KEYWORD', [])
      self.create_requests['TARGETING_TYPE_KEYWORD'].append({
        'keyword': keyword,
        'negative': negative
      })


  def delete_keyword(self, keyword):
    self._delete('TARGETING_TYPE_KEYWORD', keyword)


  def add_age_range(self, ageRange):
    if not self.already_added('TARGETING_TYPE_AGE_RANGE', ageRange):
      self.delete_age_range(ageRange)
      self.create_requests.setdefault('TARGETING_TYPE_AGE_RANGE', [])
      self.create_requests['TARGETING_TYPE_AGE_RANGE'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_AGE_RANGE', ageRange)
      })


  def delete_age_range(self, ageRange):
    self._delete('TARGETING_TYPE_AGE_RANGE', ageRange)


  def add_gender(self, gender):
    if not self.already_added('TARGETING_TYPE_GENDER'):
      self.delete_gender(gender)
      self.create_requests.setdefault('TARGETING_TYPE_GENDER', [])
      self.create_requests['TARGETING_TYPE_GENDER'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_GENDER', gender)
      })


  def delete_gender(self, gender):
    self._delete('TARGETING_TYPE_GENDER', gender)


  def add_parental_status(self, parentalStatus):
    if not self.already_added('TARGETING_TYPE_PARENTAL_STATUS'):
      self.delete_parental_status(parentalStatus)
      self.create_requests.setdefault('TARGETING_TYPE_PARENTAL_STATUS', [])
      self.create_requests['TARGETING_TYPE_PARENTAL_STATUS'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_PARENTAL_STATUS', parentalStatus)
      })


  def delete_parental_status(self, parentalStatus):
    self._delete('TARGETING_TYPE_PARENTAL_STATUS', parentalStatus)


  def add_household_income(self, householdIncome):
    if not self.already_added('TARGETING_TYPE_HOUSEHOLD_INCOME'):
      self.delete_household_income(householdIncome)
      self.create_requests.setdefault('TARGETING_TYPE_HOUSEHOLD_INCOME', [])
      self.create_requests['TARGETING_TYPE_HOUSEHOLD_INCOME'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_HOUSEHOLD_INCOME', householdIncome)
      })


  def delete_household_income(self, householdIncome):
    self._delete('TARGETING_TYPE_HOUSEHOLD_INCOME', householdIncome)


  def add_language(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_LANGUAGE'):
      self.delete_language()
      self.create_requests.setdefault('TARGETING_TYPE_LANGUAGE', [])
      self.create_requests['TARGETING_TYPE_LANGUAGE'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_LANGUAGE', displayName),
        'negative':negative
      })


  def delete_language(self, displayName):
    self._delete('TARGETING_TYPE_LANGUAGE', displayName)


  def add_included_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency):
    print('Sorry not built yet.')
    #if not self.already_added('TARGETING_TYPE_AUDIENCE_GROUP+1P_AND_3P', firstAndThirdPartyAudienceId):


  def delete_included_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency):
    print('Sorry not built yet.')
    #self._delete('TARGETING_TYPE_AUDIENCE_GROUP')


  def add_excluded_1p_and_3p_audience(self, firstAndThirdPartyAudienceId, recency):
    if not self.already_added('TARGETING_TYPE_AUDIENCE_GROUP+1P_AND_3P', firstAndThirdPartyAudienceId):
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      exists = False
      for audience in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedFirstAndThirdPartyAudienceGroup']['settings']:
        if firstAndThirdPartyAudienceId == audience['firstAndThirdPartyAudienceId']:
          audience['recency'] = recency
          exists = True
          break

      if not exists:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedFirstAndThirdPartyAudienceGroup']['settings'].append({
          "firstAndThirdPartyAudienceId": firstAndThirdPartyAudienceId,
          "recency": recency
        })


  def delete_excluded_1p_and_3p_audience(self, firstAndThirdPartyAudienceId):
    if not self.already_deleted('TARGETING_TYPE_AUDIENCE_GROUP+1P_AND_3P', firstAndThirdPartyAudienceId):
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      try:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedFirstAndThirdPartyAudienceGroup']['settings'].remove({
          "firstAndThirdPartyAudienceId": firstAndThirdPartyAudienceId,
          "recency": recency
        })
      except ValueError:
        pass


  def add_included_google_audience(self, googleAudienceId):
    if not self.already_added('TARGETING_TYPE_AUDIENCE_GROUP+GOOGLE', googleAudienceId):
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'googleAudienceId':googleAudienceId }
      if audience not in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedGoogleAudienceGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedGoogleAudienceGroup']['settings'].append(audience)


  def delete_included_google_audience(self, googleAudienceId):
    if not self.already_deleted('TARGETING_TYPE_AUDIENCE_GROUP+GOOGLE', googleAudience):
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'googleAudienceId':googleAudienceId }
      if audience in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedGoogleAudienceGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedGoogleAudienceGroup']['settings'].remove(audience)


  def add_excluded_google_audience(self, googleAudienceId):
    if not self.already_added('TARGETING_TYPE_AUDIENCE_GROUP+GOOGLE', googleAudienceId):
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'googleAudienceId':googleAudienceId }
      if audience not in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedGoogleAudienceGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedGoogleAudienceGroup']['settings'].append(audience)


  def delete_excluded_google_audience(self, googleAudienceId):
    if not self.already_deleted('TARGETING_TYPE_AUDIENCE_GROUP+GOOGLE', googleAudience):
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'googleAudienceId':googleAudienceId }
      if audience in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedGoogleAudienceGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['excludedGoogleAudienceGroup']['settings'].remove(audience)


  def add_included_custom_list(self, customListId):
    if not self.already_added('TARGETING_TYPE_AUDIENCE_GROUP+CUSTOM', customListId):
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'customListId':customListId }
      if audience not in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCustomListGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCustomListGroup']['settings'].append(audience)


  def delete_included_custom_audience(self, customListId):
    if not self.already_deleted('TARGETING_TYPE_AUDIENCE_GROUP+CUSTOM', customListId):
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'customListId':customListId }
      if audience in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCustomListGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCustomListGroup']['settings'].remove(audience)


  def add_included_combined_audience(self, combinedAudienceId):
    if not self.already_added('TARGETING_TYPE_AUDIENCE_GROUP+CUSTOM', combinedAudienceId):
      self._delete('TARGETING_TYPE_AUDIENCE_GROUP')
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'combinedAudienceId':combinedAudienceId }
      if audience not in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCombinedAudienceGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCombinedAudienceGroup']['settings'].append(audience)


  def delete_included_combined_audience(self, combinedAudienceId):
    if not self.already_deleted('TARGETING_TYPE_AUDIENCE_GROUP+CUSTOM', combinedAudienceId):
      self.create_requests.setdefault('TARGETING_TYPE_AUDIENCE_GROUP', self.get_assigned_audience())

      audience = { 'combinedAudienceId':combinedAudienceId }
      if audience in self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCombinedAudienceGroup']['settings']:
        self.create_requests['TARGETING_TYPE_AUDIENCE_GROUP']['includedCombinedAudienceGroup']['settings'].remove(audience)


  def add_device_type(self, deviceType, negative):
    if not self.already_added('TARGETING_TYPE_DEVICE_TYPE'):
      self.delete_device_type()
      self.create_requests.setdefault('TARGETING_TYPE_DEVICE_TYPE', [])
      self.create_requests['TARGETING_TYPE_DEVICE_TYPE'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_DEVICE_TYPE', deviceType),
        'negative':negative
      })


  def delete_device_type(self):
    self._delete('TARGETING_TYPE_DEVICE_TYPE')


  def add_operating_system(self, displayName):
    if not self.already_added('TARGETING_TYPE_OPERATING_SYSTEM'):
      self.delete_operating_system()
      self.create_requests.setdefault('TARGETING_TYPE_OPERATING_SYSTEM', [])
      self.create_requests['TARGETING_TYPE_OPERATING_SYSTEM'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_OPERATING_SYSTEM', displayName),
        'negative':negative
      })


  def delete_operating_system(self):
    self._delete('TARGETING_TYPE_OPERATING_SYSTEM')


  def add_browser(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_BROWSER'):
      self.delete_browser()
      self.create_requests.setdefault('TARGETING_TYPE_BROWSER', [])
      self.create_requests['TARGETING_TYPE_BROWSER'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_BROWSER', displayName),
        'negative':negative
      })


  def delete_browser(self):
    self._delete('TARGETING_TYPE_BROWSER')


  def add_environment(self, environment):
    if not self.already_added('TARGETING_TYPE_ENVIRONMENT'):
      self.delete_environment()
      self.create_requests.setdefault('TARGETING_TYPE_ENVIRONMENT', [])
      self.create_requests['TARGETING_TYPE_ENVIRONMENT'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_ENVIRONMENT', environment),
      })


  def delete_environment(self):
    self._delete('TARGETING_TYPE_ENVIRONMENT')


  def add_carrier_and_isp(self, displayName, negative):
    if not self.already_added('TARGETING_TYPE_CARRIER_AND_ISP'):
      self.delete_carrier_and_isp()
      self.create_requests.setdefault('TARGETING_TYPE_CARRIER_AND_ISP', [])
      self.create_requests['TARGETING_TYPE_CARRIER_AND_ISP'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_CARRIER_AND_ISP', displayName),
        'negative':negative
      })


  def delete_carrier_and_isp(self):
    self._delete('TARGETING_TYPE_CARRIER_AND_ISP')


  def add_day_and_time(self, dayOfWeek, startHour, endHour, timeZoneResolution):
    if not self.already_added('TARGETING_TYPE_DAY_AND_TIME', dayOfWeek):
      self.delete_day_of_week(dayOfWeek)
      self.create_requests.setdefault('TARGETING_TYPE_DAY_AND_TIME', [])
      self.create_requests['TARGETING_TYPE_DAY_AND_TIME'].append({
        'dayOfWeek': dayOfWeek,
        'startHour': startHour,
        'endHour': endHour,
        'timeZoneResolution': timeZoneResolution
      })


  def delete_and_time(self, dayOfWeek):
    self._delete('TARGETING_TYPE_DAY_AND_TIME', dayOfWeek)


  def add_geo_region(self, displayName, geoRegionType, negative):
    if not self.already_added('TARGETING_TYPE_GEO_REGION', displayName):
      self.delete_geo_region(displayName)
      self.create_requests.setdefault('TARGETING_TYPE_GEO_REGION', [])
      self.create_requests['TARGETING_TYPE_GEO_REGION'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_GEO_REGION', displayName, geoRegionType),
        'negative':negative
      })


  def delete_geo_region(self, displayName):
    self._delete('TARGETING_TYPE_GEO_REGION', displayName)


  def add_proximity_location_list(self, proximityLocationListId, proximityRadiusRange):
    if not self.already_added('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', proximityLocationListId):
      self.delete_proximity_location_list(proximityLocationListId)
      self.create_requests.setdefault('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', [])
      self.create_requests['TARGETING_TYPE_PROXIMITY_LOCATION_LIST'].append({
        'proximityLocationListId':proximityLocationListId,
        'proximityRadiusRange':proximityRadiusRange
      })


  def delete_proximity_location_list(self, proximityLocationListId):
    self._delete('TARGETING_TYPE_PROXIMITY_LOCATION_LIST', proximityLocationListId)


  def add_regional_location_list(self, regionalLocationListId, negative):
    if not self.already_added('TARGETING_TYPE_REGIONAL_LOCATION_LIST', regionalLocationListId):
      self.delete_regional_location_list(regionalLocationListId)
      self.create_requests.setdefault('TARGETING_TYPE_REGIONAL_LOCATION_LIST', [])
      self.create_requests['TARGETING_TYPE_REGIONAL_LOCATION_LIST'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_REGIONAL_LOCATION_LIST', regionalLocationListId),
        'negative':negative
      })


  def delete_regional_location_list(self, regionalLocationListId):
    self._delete('TARGETING_TYPE_REGIONAL_LOCATION_LIST', regionalLocationListId)


  def add_video_player_size(self, videoPlayerSize):
    if not self.already_added('TARGETING_TYPE_VIDEO_PLAYER_SIZE'):
      self.delete_video_player_size()
      self.create_requests.setdefault('TARGETING_TYPE_VIDEO_PLAYER_SIZE', [])
      self.create_requests['TARGETING_TYPE_VIDEO_PLAYER_SIZE'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_VIDEO_PLAYER_SIZE', videoPlayerSize)
      })


  def delete_video_player_size(self):
    self._delete('TARGETING_TYPE_VIDEO_PLAYER_SIZE')


  def add_in_stream_position(self, contentInstreamPosition):
    if not self.already_added('TARGETING_TYPE_CONTENT_INSTREAM_POSITION'):
      self.delete_in_stream_position()
      self.create_requests.setdefault('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', [])
      self.create_requests['TARGETING_TYPE_CONTENT_INSTREAM_POSITION'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', contentInstreamPosition)
      })


  def delete_in_stream_position(self):
    self._delete('TARGETING_TYPE_CONTENT_INSTREAM_POSITION')


  def add_out_stream_position(self, contentOutstreamPosition):
    if not self.already_added('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION'):
      self.delete_out_stream_position()
      self.create_requests.setdefault('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION', [])
      self.create_requests['TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_CONTENT_INSTREAM_POSITION', contentOutstreamPosition)
      })


  def delete_out_stream_position(self):
    self._delete('TARGETING_TYPE_CONTENT_OUTSTREAM_POSITION')


  def add_on_screen_position(self, onScreenPosition):
    if not self.already_added('TARGETING_TYPE_ON_SCREEN_POSITION'):
      self.delete_on_screen_position()
      self.create_requests.setdefault('TARGETING_TYPE_ON_SCREEN_POSITION', [])
      self.create_requests['TARGETING_TYPE_ON_SCREEN_POSITION'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_ON_SCREEN_POSITION', onScreenPosition)
      })


  def delete_on_screen_position(self):
    self._delete('TARGETING_TYPE_ON_SCREEN_POSITION')


  def add_viewability(self, viewability):
    if not self.already_added('TARGETING_TYPE_VIEWABILITY'):
      self.delete_viewability()
      self.create_requests.setdefault('TARGETING_TYPE_VIEWABILITY', [])
      self.create_requests['TARGETING_TYPE_VIEWABILITY'].append({
        'targetingOptionId': self.get_option_id('TARGETING_TYPE_VIEWABILITY', viewability)
      })


  def delete_viewability(self):
    self._delete('TARGETING_TYPE_VIEWABILITY')


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
          self.auth,
        ).advertisers().lineItems().bulkEditLineItemAssignedTargetingOptions(
          lineItemId=str(self.lineitem),
          advertiserId=str(self.advertiser),
        ).execute()
      elif self.advertiser:
        return API_DV360(
          self.auth,
        ).advertisers().bulkEditAdvertiserAssignedTargetingOptions(
          advertiserId=str(self.advertiser),
        ).execute()
      elif self.partner:
        return API_DV360(
          self.auth
        ).partners().bulkEditPartnerAssignedTargetingOptions(
          partnerId=str(self.partner),
        ).execute()
