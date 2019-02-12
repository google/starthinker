# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/task/traffic/store.py](/task/traffic/store.py)

Manages id maps and caching.

  Id mapping is important because if an execution fails, the context of maps of
  ext ids and concrete CM ids is lost, the Store maintains a persistent map that
  can be referenced througout an execution allowing for successful retries.

  Caching is important for performance reasons, and to reduce the number of
  calls to the CM API.



## class Store

  Class that handles interaction with the Store.

  


###   __init__(self):


    Initializes the store.

    Since this is a sigleton, before the fist usage the trix id and auth scheme
    must be set.
    


###   clear(self):


    Clears the store in the Bulkdozer feed.

    


###   translate(self, entity, identifier):


    Given an id, returns its counterpart.

    ext id to cm id and vice versa.

    Args:
      entity: The name of the entity for which the ID relates.
      identifier: Ext id or actual CM id to map.
    


###   save_id_map(self):


    Saves the ID map into the Bulkdozer feed.

    


###   set(self, entity, keys, item):


    Sets an item in the cache.

    Args:
      entity: The name of the entity cache to use.
      keys: The keys to set this item to. Typically this will contain the ext id
        and the actual CM id.
      item: The item to cache.
    


###   get(self, entity, key):


    Gets and item from the cache.

    Args:
      entity: The entity cache to use.
      key: The key to use to lookup the cached item.
    


###   map(self, entity, ext_id, dcm_id):


    Maps a CM id and an ext id for an entity.

    Args:
      entity: The name of the entity for which the ID relates.
      ext_id: Placeholder ext id.
      dcm_id: Real CM id of the object.
    


###   load_id_map(self):


    Loads the ID map from the Bulkdozer feed into the object.

    

## [/task/traffic/run.py](/task/traffic/run.py)

Main entry point of Bulkdozer.




### landing_pages():


  Processes landing pages.

  


### event_tags():


  Processes event tags.

  


### ads():


  Processes ads.

  


### campaigns():


  Processes campaigns.

  


### assets():


  Processes assets.

  


### execute_feed(feed, dao, print_field, msg='Processing'):


  Executes a specific feed.

  Args:
    feed: Feed object representing the Bulkdozer feed to process.
    dao: The data access object to be used to interact with the CM API and
      update, must match the entity being updated in CM, in the sense that the
      required fields to fetch, create, and update the entity in CM must be
      included in the feed.
    print_field: Field that identifies the item, used to print status messages
      to the Log tab of the Bulkdozer feed.
    msg: Prefix message to use when writing to the Log tab of the Bulkdozer
      feed, for instance we display Processing Campaign for campaign, and
      Uploading Asset for assets.
  


### traffic():


  For development purposes when debugging a specific entity, this function is handy to run just that entity.

  
  Main entry point of Bulkdozer.

  


### setup():


  Sets up Bulkdozer configuration and required object to execute the job.

  


### placement_groups():


  Processes placement group.

  


### test():


  Main function of Bulkdozer, performs the Bulkdozer job

  


### placements():


  Processes placements.

  


### process_feed(feed_name, dao, print_field, msg='Processing'):


  Processes a feed that represents a specific entity in the Bulkdozer feed.

  Args:
    feed_name: Name of the feed to process, refer to feed.py for the supported
      feed names.
    dao: The data access object to be used to interact with the CM API and
      update, must match the entity being updated in CM, in the sense that the
      required fields to fetch, create, and update the entity in CM must be
      included in the feed.
    print_field: Field that identifies the item, used to print status messages
      to the Log tab of the Bulkdozer feed.
    msg: Prefix message to use when writing to the Log tab of the Bulkdozer
      feed, for instance we display Processing Campaign for campaign, and
      Uploading Asset for assets.
  


### dynamic_targeting_keys():


  Processes dynamic targeting keys.

  


### creatives():


  Processes creatives.

  

## [/task/traffic/landing_page.py](/task/traffic/landing_page.py)

Handles creation and updates of landing pages.




## class LandingPageDAO

  Landing page data access object.

  Inherits from BaseDAO and implements landing page specific logic for creating
  and
  updating landing pages.
  


###   __init__(self, auth, profile_id):


    Initializes LandingPageDAO with profile id and authentication scheme.

    super(LandingPageDAO, self).__init__(auth, profile_id)

    self._service = self.service.advertiserLandingPages()
    self._id_field = FieldMap.CAMPAIGN_LANDING_PAGE_ID
    self._search_field = FieldMap.CAMPAIGN_LANDING_PAGE_NAME
    self._list_name = 'landingPages'
    self._entity = 'LANDING_PAGE'
    self._parent_filter_name = 'advertiserIds'
    self._parent_filter_field_name = FieldMap.ADVERTISER_ID
    self._parent_dao = None

  def _process_update(self, item, feed_item):
    Updates an landing page based on the values from the feed.
    

    item['name'] = feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_NAME, None)
    item['url'] = feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_URL, None)

  def _process_new(self, feed_item):
    Creates a new landing page DCM object from a feed item representing a landing page from the Bulkdozer feed.
    
    return {
        'name': feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_NAME, None),
        'url': feed_item.get(FieldMap.CAMPAIGN_LANDING_PAGE_URL, None),
        'advertiserId': feed_item.get(FieldMap.ADVERTISER_ID, None)
    }

## [/task/traffic/config.py](/task/traffic/config.py)

Utility to read and write configuration data to the Bulkdozer feed.




## class Config

  Class that handles reading and writing of configuration to the Bulkdozer feed.

  


###   __init__(self):


    Initializes Config with default mode to ALWAYS.

    


###   load(self):


    Loads configs from Bulkdozer feed and applies values to object properties.

    


###   update(self):


    Writes configurations back to the Bulkdozer feed.

    

## [/task/traffic/placement_group.py](/task/traffic/placement_group.py)

Handles creation and updates of placement groups.




## class PlacementGroupDAO

  Placement group data access object.

  Inherits from BaseDAO and implements placement group specific logic for creating
  and
  updating placement group.
  


###   __init__(self, auth, profile_id):


    Initializes PlacementGroupDAO with profile id and authentication scheme.

    super(PlacementGroupDAO, self).__init__(auth, profile_id)

    self.campaign_dao = CampaignDAO(auth, profile_id)
    self._service = self.service.placementGroups()
    self._id_field = FieldMap.PLACEMENT_GROUP_ID
    self._search_field = FieldMap.PLACEMENT_GROUP_NAME
    self._list_name = 'placementGroups'
    self._entity = 'PLACEMENT_GROUP'

    self._parent_filter_name = 'campaignIds'
    self._parent_filter_field_name = FieldMap.CAMPAIGN_ID
    self._parent_dao = self.campaign_dao

  def _process_update(self, item, feed_item):
    Updates a placement group based on the values from the feed.
    
    campaign = self.campaign_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    item['name'] = feed_item.get(FieldMap.PLACEMENT_GROUP_NAME, None)
    item['placementGroupType'] = feed_item.get(FieldMap.PLACEMENT_GROUP_TYPE, None)
    item['pricingSchedule']['startDate'] = feed_item.get(FieldMap.PLACEMENT_GROUP_START_DATE, None)
    item['pricingSchedule']['endDate'] = feed_item.get(FieldMap.PLACEMENT_GROUP_END_DATE, None)
    item['pricingSchedule']['pricingType'] = feed_item.get(FieldMap.PLACEMENT_GROUP_PRICING_TYPE, None)

  def _process_new(self, feed_item):
    Creates a new placement group DCM object from a feed item representing a placement group from the Bulkdozer feed.
    
    campaign = self.campaign_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    return {
        'advertiserId': feed_item.get(FieldMap.ADVERTISER_ID, None),
        'campaignId': campaign['id'] if campaign else None,
        'siteId': feed_item.get(FieldMap.SITE_ID, None),
        'name': feed_item.get(FieldMap.PLACEMENT_GROUP_NAME, None),
        'placementGroupType': feed_item.get(FieldMap.PLACEMENT_GROUP_TYPE, None),
        'pricingSchedule': {
          'startDate': feed_item.get(FieldMap.PLACEMENT_GROUP_START_DATE, None),
          'endDate': feed_item.get(FieldMap.PLACEMENT_GROUP_END_DATE, None),
          'pricingType': feed_item.get(FieldMap.PLACEMENT_GROUP_PRICING_TYPE, None)
        }
    }

## [/task/traffic/feed.py](/task/traffic/feed.py)

Handles interactions with the Buldozer feed.

This module has all the column name mappings, reads and writes data to the
Google Sheet that represents the Bulkdozer feed, and



## class FieldMap:


  Contains static maps of column names and enumerations.

  This class maps user friendly field names with API enumeration values, it also
  maps Bulkdozer feed column names to constants so those can be referenced
  indirectly.
  


## class Feed:


  Maps Bulkdozer feed items to and from dictionaries.

  
  Maps of internal feed names and Bulkdozer feed tabs.

  Each value is a list because if the first options is not found, it falls back
  to the subsequent one. E.g. lading_page_feed will first try to find a tab
  called "Landing Page", if that isn't found it will use the "Campaign" feed
  isntead, this allows end users to customize the tool behavior by adding or
  removing certain tabs.
  


###   _get_feed(self):


    Fetches the feed based on initialization parameters.

    Returns:
      List of lists that represents the rows and columns of the feed. If the
      feed isn't found returns a list with an empty list.
    


###   __init__(self, auth, trix_id, feed_name, parse=True, spreadsheet=None):


    Initializes the feed with parameters.

    Args:
      auth: The authentication scheme to use based on the json configuration
        file.
      trix_id: Unique identifier of the Google Sheet that represents the
        Bulkdozer feed.
      feed_name: The name of the feed to initialize.
      spreadsheet: Optional, the spreadsheet object representing the Bulkdozer
        feed spreadsheet, useful to limit calls to the sheets API and allow
        multiple Feed objects to use the same spreadsheet instance. This is used
        to determine which tabs exist in the feed so the correct one can be
        selected for the entity this Feed object represents.
    


###   update(self):


    Updates the related Bulkdozer feed item with the values in this object.

    


###   _convert_int(self, value):


    Converts a value into a integer.

    Args:
      value: String representation of a field from the Bulkdozer feed.

    Returns:
      If possible to convert value into an integer, returns the integer
      representation, otherwise None.
    


###   _feed_to_dict(self, parse=True):


    Turns a raw feed from Google Sheets into a list of dictionaries.

    Args:
      raw_feed: List of list of strings representing the feed from Google
        Sheets.

    Returns:
      List of dictionaries with the data from the feed
    


###   _convert_date(self, value):


    Converts dates into a Bulkdozer specific format to be written back to the Feed.

    Args:
      value: String representation of the date.

    Returns:
      Bulkdozer string representation of a date. Returns null if the value
      cannot be parsed into a date.
    


###   _parse_value(self, value):


    Parses a string value into a type specific value infering the correct type based on the data.

    Args:
      value: The value to parse.

    Returns:
      The representation of the value in the correct data type.
    


###   _convert_float(self, value):


    Conversta a value into a float.

    


###   _dict_to_feed(self, parse=True):


    Turns a feed into a list of strings to be written back to the feed.

    Args:
      feed: Dictionary list to convert into a list of lists of strings.

    Returns:
     List of list of strings representing the values of the feed.

    

## [/task/traffic/dynamic_targeting_key.py](/task/traffic/dynamic_targeting_key.py)

Handles creation and updates of dynamic targeting keys.

from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.feed import FieldMap


class DynamicTargetingKeyDAO(BaseDAO):
  Landing page data access object.
  

  def __init__(self, auth, profile_id):
    Initializes DynamicTargetingKeyDAO with profile id and authentication scheme.


###   process(self, feed_item):


    Processes a Bulkdozer feed item.

    This method identifies if the dyanmic targeting key already exists in CM, if
    it doesn't it creates it associated with the advertiser, and then inserts an
    association with the identified object.

    Args:
      feed_item: Bulkdozer feed item to process.

    Returns:
      Newly created or updated CM object.
    

## [/task/traffic/logger.py](/task/traffic/logger.py)

Handles logging actions back to the Bulkdozer feed Log tab.




## class Logger

  Logger class responsible for logging data into the Bulkdozer feed's Log tab.

  


###   __init__(self, flush_threshold=10):


    Initializes the logger object.

    This object is a signleton, and therefore when the application starts and
    reads the configuration of which sheet ID to use for the Bulkdozer feed, the
    trix_id and auth fields need to be updated.
    


###   clear(self):


    Clears the log tab in the Bulkdozer feed, useful when a new execution is starting.

    


###   log(self, message):


    Logs a message to the Bulkdozer feed's Log tab.

    Args:
      message: The message to log to the feed, it will be appended at the bottom
        of the log, after the last message that was written.
    


###   flush(self):


    Flushes the message buffer writing buffered messages to the sheet.

    


## class Timer

  Timer class responsible for measuring run time for performance profiling and optimization.
  


###   __init__(self):


    Constructor.
    


###   check_timer(self, timer_name):


    Checks and prints the elapsed time of a given timer.

    Args:
      timer_name: Name of the timer to check and print, it must have been initialized with start_timer.
    


###   start_timer(self, timer_name):


    Initializes a new timer.

    Args:
      timer_name: name of the timer to initialize, if not unique will reset existing timer.
    

## [/task/traffic/campaign.py](/task/traffic/campaign.py)

Handles creation and updates of Ads.




## class CampaignDAO

  Campaign data access object.

  Inherits from BaseDAO and implements campaign specific logic for creating and
  updating campaigns.
  


###   __init__(self, auth, profile_id):


    Initializes CampaignDAO with profile id and authentication scheme.
    super(CampaignDAO, self).__init__(auth, profile_id)

    self.landing_page_dao = LandingPageDAO(auth, profile_id)
    self._id_field = FieldMap.CAMPAIGN_ID
    self._search_field = FieldMap.CAMPAIGN_NAME
    self._list_name = 'campaigns'

    self._parent_filter_name = None
    self._parent_filter_field_name = None

    self._entity = 'CAMPAIGN'
    self._service = self.service.campaigns()

  def _process_update(self, item, feed_item):
    Updates a campaign based on the values from the feed.
    
    lp = self.landing_page_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_ID] = lp['id']
    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME] = lp['name']

    item['startDate'] = StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.CAMPAIGN_START_DATE, None))
    item['endDate'] = StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.CAMPAIGN_END_DATE, None))
    item['name'] = feed_item.get(FieldMap.CAMPAIGN_NAME, None)
    item['defaultLandingPageId'] = lp['id']

  def _process_new(self, feed_item):
    Creates a new campaign DCM object from a feed item representing a campaign from the Bulkdozer feed.
    
    lp = self.landing_page_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_ID] = lp['id']
    feed_item[FieldMap.CAMPAIGN_LANDING_PAGE_NAME] = lp['name']

    return {
        'advertiserId': feed_item.get(FieldMap.ADVERTISER_ID, None),
        'name': feed_item.get(FieldMap.CAMPAIGN_NAME, None),
        'startDate': StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.CAMPAIGN_START_DATE, None)),
        'endDate': StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.CAMPAIGN_END_DATE, None)),
        'defaultLandingPageId': lp['id']
    }


## [/task/traffic/creative.py](/task/traffic/creative.py)

Handles creation and updates of Creatives.




## class CreativeDAO

  Creative data access object.

  Inherits from BaseDAO and implements creative specific logic for creating and
  updating creatives.
  


###   __init__(self, auth, profile_id):


    Initializes CreativeDAO with profile id and authentication scheme.
    super(CreativeDAO, self).__init__(auth, profile_id)

    self._entity = 'CREATIVE'

    self._parent_filter_name = 'advertiserId'
    self._parent_filter_field_name = FieldMap.ADVERTISER_ID

    self._service = self.service.creatives()
    self._id_field = FieldMap.CREATIVE_ID
    self._search_field = FieldMap.CREATIVE_NAME
    self._list_name = 'creatives'
    self._parent_dao = None

    self.creative_asset_dao = CreativeAssetDAO(auth, profile_id, None)

  def _assignment_matches(self, item, assignment):
    if item.get(FieldMap.CREATIVE_ID, None) and assignment.get(FieldMap.CREATIVE_ID, None):
      return item.get(FieldMap.CREATIVE_ID, None) == assignment.get(FieldMap.CREATIVE_ID, None)
    else:
      return item.get(FieldMap.CREATIVE_NAME, '1') == assignment.get(FieldMap.CREATIVE_NAME, '2')

  def map_creative_third_party_url_feeds(self, creative_feed,
                                         third_party_url_feed):
    Maps third party url feed to the corresponding creative.
    
    for creative in creative_feed:
      creative['third_party_urls'] = [
          third_party_url for third_party_url in third_party_url_feed
          if self._assignment_matches(creative, third_party_url)
      ]

  def map_creative_and_association_feeds(self, creative_feed,
                                         creative_association_feed):
    Maps creative association feed to the corresponding creative.
    
    for creative in creative_feed:
      creative['associations'] = [
          association for association in creative_association_feed
          if self._assignment_matches(creative, association)
      ]

  def _associate_third_party_urls(self, feed_item, creative):
    Associate third party urls with the respective creative DCM object.
    
    third_party_urls = []
    for third_party_url in feed_item.get('third_party_urls', []):
      third_party_url_type = FieldMap.THIRD_PARTY_URL_TYPE_MAP.get(
          third_party_url.get(FieldMap.THIRD_PARTY_URL_TYPE, None))
      if third_party_url_type:
        third_party_urls.append({
            'thirdPartyUrlType': third_party_url_type,
            'url': third_party_url.get(FieldMap.THIRD_PARTY_URL, None)
        })

    if third_party_urls:
      creative['thirdPartyUrls'] = third_party_urls

  def _process_update(self, item, feed_item):
    Updates a creative based on the values from the feed.
    
    item['name'] = feed_item.get(FieldMap.CREATIVE_NAME, None)
    self._associate_third_party_urls(feed_item, item)

  def _process_new(self, feed_item):
    Creates a new creative DCM object from a feed item representing an creative from the Bulkdozer feed.
    
    creative = {
        'advertiserId': feed_item.get(FieldMap.ADVERTISER_ID, None),
        'name': feed_item.get(FieldMap.CREATIVE_NAME, None),
        'active': True
    }

    self._associate_third_party_urls(feed_item, creative)

    if feed_item.get(FieldMap.CREATIVE_TYPE, None) == 'VIDEO':
      creative['type'] = 'INSTREAM_VIDEO'

      for association in feed_item.get('associations', []):
        identifier = self.creative_asset_dao.get_identifier(association, self._creative_asset_feed)

        creative['creativeAssets'] = [{
            'assetIdentifier': identifier,
            'role': 'PARENT_VIDEO'
        }]

      del creative['active']
    else:
      raise Exception('Only video is supported at the moment!')
    # (mauriciod@): I didn't pull the display creative stuff from jeltz in here,
    # because I am splitting things up differently, and the backup image will
    # have to be uploaded in the creative_assets dao

    return creative

  def map_assets_feed(self, creative_asset_feed):
    self._creative_asset_feed = creative_asset_feed

  def _post_process(self, feed_item, new_item):
    Maps ids and names of related entities so they can be updated in the Bulkdozer feed.
    
    # TODO loop through 3p urls and update the feed
    for third_party_url in feed_item.get('third_party_urls', []):
      third_party_url[FieldMap.CREATIVE_ID] = new_item['id']
      third_party_url[FieldMap.CREATIVE_NAME] = new_item['name']

    for association in feed_item.get('associations', []):
      association[FieldMap.CREATIVE_ID] = self.get(association)['id']

      dcm_association = self.creative_asset_dao.get(association, required=True)
      if dcm_association:
        association[FieldMap.CREATIVE_ASSET_ID] = dcm_association.get(
            'id', None)

## [/task/traffic/creative_assets.py](/task/traffic/creative_assets.py)

Handles creation and updates of creative assets.




## class CreativeAssetDAO

  Creative asset data access object.

  Inherits from BaseDAO and implements ad specific logic for creating and
  updating ads.
  


###   __init__(self, auth, profile_id, gc_project):


    Initializes CreativeAssetDAO with profile id and authentication scheme.
    super(CreativeAssetDAO, self).__init__(auth, profile_id)

    self._entity = 'CREATIVE_ASSET'
    self._service = self.service.creativeAssets()
    self.gc_project = gc_project
    self._list_name = ''
    self._id_field = FieldMap.CREATIVE_ASSET_ID
    self._search_field = None
    self.auth = auth

    self._parent_filter_name = None
    self._parent_filter_field_name = None

  def pre_fetch(self, feed):
    Pre-fetches all required items to be update into the cache.
    
    pass

  def _process_update(self, item, feed_item):
    Handles updates to the creative asset object.
    
    pass

  def _insert(self, new_item, feed_item):
    Handles the upload of creative assets to DCM and the creation of the associated entity.
    
    local_file = os.path.join('/tmp', feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None))

    self._download_from_gcs(
        feed_item.get(FieldMap.CREATIVE_ASSET_BUCKET_NAME, None),
        feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None),
        local_file,
        auth=self.auth)

    media = http.MediaFileUpload(local_file)

    if not media.mimetype():
      mimetype = 'application/zip' if asset_type == 'HTML' else 'application/octet-stream'
      media = http.MediaFileUpload(asset_file, mimetype)

    result = self._retry(
        self._service.insert(
            profileId=self.profile_id,
            advertiserId=feed_item.get(FieldMap.ADVERTISER_ID, None),
            media_body=media,
            body=new_item))

    os.remove(local_file)

    return result

  def _get(self, feed_item):
    Retrieves an item from DCM or the local cache.
    
    result = store.get(self._entity, feed_item.get(FieldMap.CREATIVE_ASSET_ID, None))

    if not result:
      result = {
          'id': feed_item.get(FieldMap.CREATIVE_ASSET_ID, None),
          'assetIdentifier': {
              'name': feed_item.get(FieldMap.CREATIVE_ASSET_NAME, None),
              'type': feed_item.get(FieldMap.CREATIVE_TYPE, None)
          }
      }

      store.set(self._entity, [feed_item.get(FieldMap.CREATIVE_ASSET_ID, None)], result)

    return result

  def _update(self, item, feed_item):
    Performs an update in DCM.
    
    pass

  def _process_new(self, feed_item):
    Creates a new creative asset DCM object from a feed item representing a creative asset from the Bulkdozer feed.
    
    return {
        'assetIdentifier': {
            'name': feed_item.get(FieldMap.CREATIVE_ASSET_FILE_NAME, None),
            'type': feed_item.get(FieldMap.CREATIVE_TYPE, None)
        }
    }

  def _post_process(self, feed_item, item):
    Maps ids and names of related entities so they can be updated in the Bulkdozer feed.
    
    if item['assetIdentifier']['name']:
      feed_item[FieldMap.CREATIVE_ASSET_NAME] = item['assetIdentifier']['name']

  def _download_from_gcs(self, bucket, object_name, local_file, auth='user'):
    Downloads assets from Google Cloud Storage locally to be uploaded to DCM.
    
    object_download(self.gc_project, bucket, object_name, local_file, auth=auth)

  def get_identifier(self, association, feed):
    asset_ids = (association.get(FieldMap.CREATIVE_ASSET_ID, None), store.translate(self._entity, association[FieldMap.CREATIVE_ASSET_ID]))

    for creative_asset in feed.feed:
      if str(creative_asset[FieldMap.CREATIVE_ASSET_ID]) in asset_ids:
        return {
            'name': creative_asset.get(FieldMap.CREATIVE_ASSET_NAME, None),
            'type': creative_asset.get(FieldMap.CREATIVE_TYPE, None)
        }

    return None

## [/task/traffic/creative_association.py](/task/traffic/creative_association.py)

Handles creation and updates of creative asset association.




## class CreativeAssociationDAO

  Creative Association data access object.

  Inherits from BaseDAO and implements creative association specific logic for
  creating and
  updating creative association.
  


###   __init__(self, auth, profile_id):


    Initializes CreativeAssociationDAO with profile id and authentication scheme.
    super(CreativeAssociationDAO, self).__init__(auth, profile_id)

    self._service = self.service.campaignCreativeAssociations()
    self._id_field = FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID

    self.campaign_dao = CampaignDAO(auth, profile_id)
    self.creative_dao = CreativeDAO(auth, profile_id)

    self._parent_filter_name = None
    self._parent_filter_field_name = None

  def get(self, feed_item):
    It is not possible to retrieve creative associations from DCM,
    
    return None

  def process(self, feed_item):
    Processes a feed item by creating the creative association in DCM.
    
    if not feed_item.get(FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID, None):
      campaign = self.campaign_dao.get(feed_item, required=True)
      creative = self.creative_dao.get(feed_item, required=True)

      if campaign and creative:
        if campaign:
          feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
          feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

        association = {'creativeId': creative['id']}

        result = self._retry(
            self._service.insert(
                profileId=self.profile_id,
                campaignId=campaign['id'],
                body=association))

        feed_item[FieldMap.CAMPAIGN_CREATIVE_ASSOCIATION_ID] = '%s|%s' % (
            campaign['id'], creative['id'])

        return result

    return None

## [/task/traffic/placement.py](/task/traffic/placement.py)

Handles creation and updates of Placements.




## class PlacementDAO

  Placement data access object.

  Inherits from BaseDAO and implements placement specific logic for creating and
  updating placement.
  


###   __init__(self, auth, profile_id):


    Initializes PlacementDAO with profile id and authentication scheme.
    super(PlacementDAO, self).__init__(auth, profile_id)

    self._entity = 'PLACEMENT'

    self.campaign_dao = CampaignDAO(auth, profile_id)
    self.video_format_dao = VideoFormatDAO(auth, profile_id)
    self.placement_group_dao = PlacementGroupDAO(auth, profile_id)

    self._service = self.service.placements()
    self._id_field = FieldMap.PLACEMENT_ID
    self._search_field = FieldMap.PLACEMENT_NAME

    self._parent_filter_name = 'campaignIds'
    self._parent_filter_field_name = FieldMap.CAMPAIGN_ID
    self._parent_dao = self.campaign_dao


    self._list_name = 'placements'

    self.cache = PlacementDAO.cache

  def _process_skipability(self, feed_item, item):
    Process skipability settings.
    
    if feed_item.get(FieldMap.PLACEMENT_SKIPPABLE, False):
      if not 'videoSettings' in item:
        item['videoSettings'] = {}

      item['videoSettings']['skippableSettings'] = {
        'skippable': feed_item.get(FieldMap.PLACEMENT_SKIPPABLE, False),
        'skipOffset': {},
        'progressOffset': {}
      }

      skippable_settings = item['videoSettings']['skippableSettings']

      if feed_item.get(FieldMap.PLACEMENT_SKIP_OFFSET_SECONDS, None):
        skippable_settings['skipOffset']['offsetSeconds']= feed_item.get(FieldMap.PLACEMENT_SKIP_OFFSET_SECONDS, None)

      if feed_item.get(FieldMap.PLACEMENT_SKIP_OFFSET_PERCENTAGE, None):
        skippable_settings['skipOffset']['offsetPercentage'] = feed_item.get(FieldMap.PLACEMENT_SKIP_OFFSET_PERCENTAGE, None)

      if feed_item.get(FieldMap.PLACEMENT_PROGRESS_OFFSET_SECONDS, None):
        skippable_settings['progressOffset']['offsetSeconds']= feed_item.get(FieldMap.PLACEMENT_SKIP_OFFSET_SECONDS, None)

      if feed_item.get(FieldMap.PLACEMENT_PROGRESS_OFFSET_PERCENTAGE, None):
        skippable_settings['progressOffset']['offsetPercentage'] = feed_item.get(FieldMap.PLACEMENT_SKIP_OFFSET_PERCENTAGE, None)
    else:
      if 'skippableSettings' in item and 'videoSettings' in item:
        del item['videoSettings']['skippableSettings']

  def _process_active_view_and_verification(self, placement, feed_item):
    Updates / creates active view and verification settings.
    

    if FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION in feed_item:
      if feed_item.get(FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION, None) == 'ON':
        placement['vpaidAdapterChoice'] = 'HTML5'
        placement['videoActiveViewOptOut'] = False
      elif feed_item.get(FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION, None) == 'OFF':
        placement['vpaidAdapterChoice'] = 'DEFAULT'
        placement['videoActiveViewOptOut'] = True
      elif feed_item[
          FieldMap.
          PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION] == 'LET_DCM_DECIDE' or feed_item[
              FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION] == '':
        placement['vpaidAdapterChoice'] = 'DEFAULT'
        placement['videoActiveViewOptOut'] = False
      else:
        raise Exception(
            '%s is not a valid value for the placement Active View and Verification field'
            % feed_item.get(FieldMap.PLACEMENT_ACTIVE_VIEW_AND_VERIFICATION, None))

  def _process_pricing_schedule(self, item, feed_item):
    Updates / creates pricing schedule settings.
    
    if 'pricing_schedule' in feed_item and feed_item['pricing_schedule']:
      if not 'pricingSchedule' in item:
        item['pricingSchedule'] = {}

      item['pricingSchedule']['pricingPeriods'] = []

      for pricing_schedule in feed_item['pricing_schedule']:
        item['pricingSchedule']['pricingPeriods'].append({
            'endDate':
                pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_END, None),
            'startDate':
                pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_START, None),
            'rateOrCostNanos':
                float(pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_RATE)) *
                1000000000,
            'units':
                pricing_schedule.get(FieldMap.PLACEMENT_PERIOD_UNITS),
        })

  def _process_update(self, item, feed_item):
    Updates an placement based on the values from the feed.
    

    if feed_item.get(FieldMap.CAMPAIGN_ID, '') == '':
      feed_item[FieldMap.CAMPAIGN_ID] = item['campaignId']

    campaign = self.campaign_dao.get(feed_item, required=True)
    placement_group = self.placement_group_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    if placement_group:
      feed_item[FieldMap.PLACEMENT_GROUP_ID] = placement_group['id']
      feed_item[FieldMap.PLACEMENT_GROUP_NAME] = placement_group['name']
      item['placementGroupId'] = placement_group['id']
    else:
      item['placementGroupId'] = None

    self._process_skipability(feed_item, item)

    item['pricingSchedule']['startDate'] = (StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_START_DATE, None)) 
        if feed_item.get(FieldMap.PLACEMENT_START_DATE, '')
        else item['pricingSchedule']['startDate'])

    item['pricingSchedule']['endDate'] = (StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_END_DATE, None)) 
      if feed_item.get(FieldMap.PLACEMENT_END_DATE, '') 
      else item['pricingSchedule']['endDate'])

    item['pricingSchedule']['pricingType'] = feed_item.get(
        FieldMap.PLACEMENT_PRICING_SCHEDULE_COST_STRUCTURE,
        None) if feed_item.get(
            FieldMap.PLACEMENT_PRICING_SCHEDULE_COST_STRUCTURE,
            '') else item['pricingSchedule']['pricingType']

    if feed_item.get(FieldMap.PLACEMENT_PRICING_TESTING_START, None):
      item['pricingSchedule']['testingStartDate'] = feed_item.get(FieldMap.PLACEMENT_PRICING_TESTING_START , None)

    item['name'] = feed_item.get(FieldMap.PLACEMENT_NAME,
                                 None) if feed_item.get(FieldMap.PLACEMENT_NAME,
                                                        '') else item['name']
    item['archived'] = feed_item.get(
        FieldMap.PLACEMENT_ARCHIVED, None) if feed_item.get(
            FieldMap.PLACEMENT_ARCHIVED, '') else item['archived']
    item['adBlockingOptOut'] = feed_item.get(FieldMap.PLACEMENT_AD_BLOCKING,
                                             False)

    self._process_transcode(item, feed_item)
    self._process_active_view_and_verification(item, feed_item)
    self._process_pricing_schedule(item, feed_item)

    if feed_item.get(FieldMap.PLACEMENT_ADDITIONAL_KEY_VALUES, None):
      if not 'tagSetting' in item:
        item['tagSetting'] = {}

      item['tagSetting']['additionalKeyValues'] = feed_item.get(FieldMap.PLACEMENT_ADDITIONAL_KEY_VALUES, None)

  def _process_transcode(self, item, feed_item):
    Updates / creates transcode configuration for the placement.
    
    if 'transcode_config' in feed_item:

      if not 'videoSettings' in item:
        item['videoSettings'] = {}

      if not 'transcodeSettings' in item['videoSettings']:
        item['videoSettings']['transcodeSettings'] = {}

      item['videoSettings']['transcodeSettings'][
          'enabledVideoFormats'] = self.video_format_dao.translate_transcode_config(
              feed_item['transcode_config'])

      if not item['videoSettings']['transcodeSettings']['enabledVideoFormats']:
        raise Exception(
            'Specified transcode profile did not match any placement level transcode settings in Campaign Manager'
        )

  def get_sizes(self, width, height):
    Retrieves a creative sizes from DCM.
    
    # TODO (mauriciod): this could potentially be in a separate SizesDAO,
    # but since we don't use it anywhere else it is probably fine.
    # May need to do it in case it becomes necessary for other entities when
    # we implement display
    return self._retry(self.service.sizes().list(
        profileId=self.profile_id, height=height, width=width))

  def _process_new(self, feed_item):
    Creates a new placement DCM object from a feed item representing an placement from the Bulkdozer feed.
    
    campaign = self.campaign_dao.get(feed_item, required=True)
    placement_group = self.placement_group_dao.get(feed_item, required=True)

    feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']
    feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']

    if placement_group:
      feed_item[FieldMap.PLACEMENT_GROUP_ID] = placement_group['id']
      feed_item[FieldMap.PLACEMENT_GROUP_NAME] = placement_group['name']

    result = {
        'name':
            feed_item.get(FieldMap.PLACEMENT_NAME, None),
        'adBlockingOptOut':
            feed_item.get(FieldMap.PLACEMENT_AD_BLOCKING, False),
        'campaignId':
            campaign['id'],
        'placementGroupId':
            placement_group['id'] if placement_group else None,
        'archived':
            feed_item.get(FieldMap.PLACEMENT_ARCHIVED, None),
        'siteId':
            feed_item.get(FieldMap.SITE_ID, None),
        'paymentSource':
            'PLACEMENT_AGENCY_PAID',
        'pricingSchedule': {
            'startDate':
                StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_START_DATE, None)),
            'endDate':
                StringExtensions.convertDateTimeStrToDateStr(feed_item.get(FieldMap.PLACEMENT_END_DATE, None)),
            'pricingType':
                feed_item.get(FieldMap.PLACEMENT_PRICING_SCHEDULE_COST_STRUCTURE, None) or 'PRICING_TYPE_CPM',
            'pricingPeriods': [{
                'startDate':
                    feed_item.get(FieldMap.PLACEMENT_START_DATE, None),
                'endDate':
                    feed_item.get(FieldMap.PLACEMENT_END_DATE, None)
            }]
        }
    }

    self._process_skipability(feed_item, result)

    if feed_item.get(FieldMap.PLACEMENT_ADDITIONAL_KEY_VALUES, None):
      result['tagSetting'] = {
        'additionalKeyValues': feed_item.get(FieldMap.PLACEMENT_ADDITIONAL_KEY_VALUES, None)
      }

    if feed_item.get(FieldMap.PLACEMENT_PRICING_TESTING_START, None):
      result['pricingSchedule']['testingStartDate'] = feed_item.get(FieldMap.PLACEMENT_PRICING_TESTING_START , None)

    self._process_active_view_and_verification(result, feed_item)

    if feed_item.get(FieldMap.PLACEMENT_TYPE, None) == 'VIDEO' or feed_item[
        FieldMap.PLACEMENT_TYPE] == 'IN_STREAM_VIDEO':
      result['compatibility'] = 'IN_STREAM_VIDEO'
      result['size'] = {'width': '0', 'height': '0'}
      result['tagFormats'] = ['PLACEMENT_TAG_INSTREAM_VIDEO_PREFETCH']
    else:
      result['compatibility'] = 'DISPLAY'
      width = 1
      height = 1
      raw_size = feed_item.get(FieldMap.ASSET_SIZE,
                                    '0x0')
      if(raw_size and 'x' in raw_size):
        width, height = raw_size.strip().lower().split('x')

      sizes = self.get_sizes(int(width), int(height))['sizes']
      if sizes:
        result['size'] = {'id': sizes[0]['id']}
      else:
        result['size'] = {'width': int(width), 'height': int(height)}

      result['tagFormats'] = [
          'PLACEMENT_TAG_STANDARD', 'PLACEMENT_TAG_JAVASCRIPT',
          'PLACEMENT_TAG_IFRAME_JAVASCRIPT', 'PLACEMENT_TAG_IFRAME_ILAYER',
          'PLACEMENT_TAG_INTERNAL_REDIRECT', 'PLACEMENT_TAG_TRACKING',
          'PLACEMENT_TAG_TRACKING_IFRAME', 'PLACEMENT_TAG_TRACKING_JAVASCRIPT'
      ]

    self._process_transcode(result, feed_item)
    self._process_pricing_schedule(result, feed_item)

    return result

  def _post_process(self, feed_item, item):

    for pricing_schedule in feed_item.get('pricing_schedule', []):
      placement = self.get(pricing_schedule)

      if placement:
        feed_item[FieldMap.PLACEMENT_ID] = placement['id']


  def map_placement_transcode_configs(
      self, placement_feed, transcode_configs_feed, pricing_schedule_feed):
    Maps sub feeds with the parent feed based on placement id.
    

    for placement in placement_feed:
      placement['pricing_schedule'] = []

      for pricing_schedule in pricing_schedule_feed:
        if placement.get(FieldMap.PLACEMENT_ID,
                         '') == pricing_schedule.get(FieldMap.PLACEMENT_ID, None):
          placement['pricing_schedule'].append(pricing_schedule)

      transcode_id = placement.get(FieldMap.TRANSCODE_ID, '')
      if transcode_id:
        for transcode_config in transcode_configs_feed:
          if transcode_id == transcode_config.get(FieldMap.TRANSCODE_ID, None):
            placement['transcode_config'] = transcode_config
            break

## [/task/traffic/dao.py](/task/traffic/dao.py)

Module that centralizes all CM data access.




## class BaseDAO

  Parent class to all data access objects.

  Centralizes all common logic to all classes that access CM to create or update
  entities.
  
  Version of the CM API to use.
  API_VERSION = 'v3.2'

  def __init__(self, auth, profile_id):
    Initializes the object with a specific CM profile ID and an authorization scheme.
    
    self.service = get_service('dfareporting', self.API_VERSION, auth)
    self.profile_id = profile_id
    self._entity = 'UNDEFINED'
    self._metrics = {}

  def _clean(self, item):
    Removes null keys from the item.
    
    # Write code here to remove all null fields from item
    null_keys = []
    for key in item:
      if item[key] == None:
        null_keys.append(key)

    for key in null_keys:
      del item[key]

    return item

  def _get(self, feed_item):
    Fetches an item from CM.
    
    print 'hitting the api to get %s, %s' % (self._entity, feed_item[self._id_field])
    return self._retry(
        self._service.get(
            profileId=self.profile_id, id=feed_item[self._id_field]))

  def get(self, feed_item, required=False):
    Retrieves an item.
    
    result = None
    keys = []
    id_value = feed_item.get(self._id_field, None)

    if not id_value and self._search_field and feed_item.get(self._search_field, None):
      store_key = feed_item[self._search_field]

      if self._parent_filter_name:
        if feed_item.get(self._parent_filter_field_name, None):
          store_key = str(feed_item.get(self._parent_filter_field_name, None)) + store_key

      result = store.get(self._entity, store_key)

      if not result:
        result, key = self._get_by_name(feed_item)
        keys.append(key)

      if not result and required:
        raise Exception('ERROR: Could not find %s with name %s' % (self._entity, feed_item[self._search_field]))
    elif id_value:
      if type(id_value) in (str, unicode) and id_value.startswith('ext'):
        keys.append(id_value)
        id_value = store.translate(self._entity, id_value)

        if id_value:
          feed_item[self._id_field] = id_value

      if id_value:
        keys.append(id_value)
        result = store.get(self._entity, id_value)

        if not result:
          result = self._get(feed_item)

        if not result and required:
          raise Exception('ERROR: Could not find %s with id %s' % (self._entity, id_value))

    store.set(self._entity, keys, result)

    return result

  def _get_base_search_args(self, search_string):
    return {
      'profileId': self.profile_id,
      'searchString': search_string,
      'sortField': 'NAME',
      'maxResults': 2
    }

  def _get_by_name(self, feed_item):
    Searches CM for an item of name defined in the search field of the DAO class.
    
    key = ''
    if self._search_field:
      key = feed_item[self._search_field].strip()

      search_string = feed_item[self._search_field].strip()
      args = self._get_base_search_args(search_string)

      if self._parent_filter_name:
        if feed_item.get(self._parent_filter_field_name, None):
          args[self._parent_filter_name] = feed_item.get(self._parent_filter_field_name, None)
        elif self._parent_dao:
          parent = self._parent_dao.get(feed_item, required=True)
          if parent:
            args[self._parent_filter_name] = parent.get('id', None)

        key = str(args.get(self._parent_filter_name, '')) + key

      print 'hitting the api to search for %s, %s' % (self._entity, search_string)
      search_result = self._retry(
          self._service.list(**args))

      items = search_result[self._list_name]

      if items and len(items) > 0:
        item = items[0]

        if search_string == item['name']:
          if len(items) > 1 and items[1]['name'] == search_string:
            raise Exception('ERROR: More than one item found with %s %s' % (self._search_field, feed_item[self._search_field]))
          else:
            return item, key

    return None, key


  def _insert(self, item, feed_item):
    Inserts a new item into CM.
    
    return self._retry(
        self._service.insert(profileId=self.profile_id, body=item))

  def _update(self, item, feed_item):
    Updates a new item in CM.
    
    self._retry(self._service.update(profileId=self.profile_id, body=item))

  def _chunk(self, l, chunk_size):
    result = []
    start = 0

    while start < len(l):
      result.append(l[start:start + chunk_size - 1])
      start += chunk_size

    return result

  def pre_fetch(self, feed):
    Pre-fetches all required items to be update into the cache.
    
    if hasattr(self, '_list_name') and self._list_name and self._id_field:
      print 'pre fetching %s' % self._list_name
      ids = [feed_item[self._id_field] for feed_item in feed if isinstance(feed_item[self._id_field], int)]

      if ids:
        for chunk_ids in self._chunk(ids, 500):
          result = self._retry(
              self._service.list(profileId=self.profile_id, ids=chunk_ids))

          while result.get(self._list_name, []):
            for item in result[self._list_name]:
              store.set(self._entity, [item['id']], item)

            result = self._retry(
                self._service.list(profileId=self.profile_id, pageToken=result['nextPageToken']))

  def process(self, feed_item):
    Processes a Bulkdozer feed item.
    
    item = self.get(feed_item)

    if item:
      self._process_update(item, feed_item)

      self._clean(item)

      self._update(item, feed_item)
    else:
      new_item = self._process_new(feed_item)

      self._clean(new_item)

      item = self._insert(new_item, feed_item)

      if self._id_field and feed_item.get(self._id_field, '').startswith('ext'):
        store.map(self._entity, feed_item.get(self._id_field), item['id'])
        store.set(self._entity, [feed_item[self._id_field]], item)

      if self._search_field and feed_item.get(self._search_field, ''):
        store.map(self._entity, feed_item.get(self._search_field), item['id'])
        store.set(self._entity, [feed_item[self._search_field]], item)

    if item:
      feed_item[self._id_field] = item['id']
      store.set(self._entity, [item['id']], item)

    self._post_process(feed_item, item)

    return item

  def _post_process(self, feed_item, item):
    Provides an opportunity for sub classes to perform any required operations after the item has been processed.
    
    pass

  def _retry(self, job, retries=6, wait=2):
    Handles required logic to ensure robust interactions with the CM API.
    
    try:
      data = job.execute()
      return data
    except http.HttpError, e:
      stack = traceback.format_exc()
      print stack

      msg = str(e)
      match = re.search(r'"(.*)"', msg)

      if e.resp.status in [403, 429, 500, 503]:
        if retries > 0:
          time.sleep(wait)
          return self._retry(job, retries - 1, wait * 2)

      if match:
        raise Exception('ERROR: %s' % match.group(0))
      else:
        logger.log(msg)

      raise

## [/task/traffic/ad.py](/task/traffic/ad.py)

Handles creation and updates of Ads.

import time
import json

from starthinker.task.traffic.campaign import CampaignDAO
from starthinker.task.traffic.class_extensions import StringExtensions
from starthinker.task.traffic.creative import CreativeDAO
from starthinker.task.traffic.dao import BaseDAO
from starthinker.task.traffic.event_tag import EventTagDAO
from starthinker.task.traffic.feed import FieldMap
from starthinker.task.traffic.landing_page import LandingPageDAO
from starthinker.task.traffic.placement import PlacementDAO
from starthinker.task.traffic.store import store


class AdDAO(BaseDAO):
  Ad data access object.
  

  def __init__(self, auth, profile_id):
    Initializes AdDAO with profile id and authentication scheme.


###   _process_assignments(self, feed_item, creative_assignments,


    Updates the ad by setting the values of child objects based on secondary feeds.

    Args:
      feed_item: Feed item representing the ad from the Bulkdozer feed.
      creative_assignments: Feed items representing creative assignments related
        with the current ad.
      placement_assignments: Feed items representing placement assignments
        related with the current ad.
      event_tag_assignments: Feed items representing event tag assignments
        related with the current ad.
    


###   map_feeds(self, ad_feed, ad_creative_assignment, ad_placement_assignment,


    Maps subfeeds to the corresponding ad.

    The Ad is an object that has several other dependent entities, they could be
    other entities like creative assignment, or complex sub objects in the ad
    entity like the placement assignment. This function maps those feeds by ID
    and injects the child feeds into the feed item representing the ad.

    Also, the ad level is where placement event tag profiles are assigned, and
    therefore this function is also responsible to determining if the placement
    event tag profile should be used, or if the direct event tag assignment in
    the ad should be used.

    Args:
      ad_feed: Ad feed.
      ad_creative_assignment: Ad creative assignment feed.
      ad_placement_assignment: Ad placement assignment feed.
      placement_feed: Placement feed.
      event_tag_profile_feed: Event tag profile feed.
    


###   _process_landing_page(self, item, feed_item):


    Configures ad landing page.

    Args:
      item: DCM ad object to update.
      feed_item: Feed item representing the ad from the Bulkdozer feed
    


###   _process_new(self, feed_item):


    Creates a new ad DCM object from a feed item representing an ad from the Bulkdozer feed.

    This function simply creates the object to be inserted later by the BaseDAO
    object.

    Args:
      feed_item: Feed item representing the ad from the Bulkdozer feed.

    Returns:
      An ad object ready to be inserted in DCM through the API.

    


###   _process_update(self, item, feed_item):


    Updates an ad based on the values from the feed.

    Args:
      item: Object representing the ad to be updated, this object is updated
        directly.
      feed_item: Feed item representing ad values from the Bulkdozer feed.
    


###   _wait_creative_activation(self, creative_id, timeout=128):


    Waits for a creative to become active.

    This function checks the if the creative is active in intervals that
    increase exponentially (exponential backoff).

    Args:
      creative_id: Creative identifier.
      timeout: Optional parameter, determines how many seconds to wait for the
        activation.

    Raises:
      Exception: In case the creative doesn't activate within the specified
      timeout

    


###   _wait_all_creative_activation(self, feed_item, timeout=128):


    Waits for activation of all creatives that should be associated to the feed item that represents an ad.

    Args:
      feed_item: Feed item representing an Ad from the Bulkdozer feed.
      timeout: Optional parameter identifying how long to wait for all creatives
        to be activated in seconds.

    Raises:
      Exception: In case one or more creatives do not get activated within the
      specified timeout.

    


###   _post_process(self, feed_item, item):


    Maps ids and names of related entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    ad feed.

    Args:
      feed_item: Feed item representing the ad from the Bulkdozer feed.
      item: The DCM ad being updated or created.
    


###   _sub_entity_map(self, assignments, item, campaign):


    Maps ids and names of sub entities so they can be updated in the Bulkdozer feed.

    When Bulkdozer is done processing an item, it writes back the updated names
    and ids of related objects, this method makes sure those are updated in the
    ad feed.

    Args:
      assignments: List of child feeds to map.
      item: The DCM ad object that was updated or created.
      campaign: The campaign object associated with the ad.
    


###   _setup_rotation_strategy(self, creative_rotation, feed_item):


    Analyzes the feed and sets up rotation strategy for the ad.

    For better user experience, the creative rotaion values that come from the
    feed map directly to values in the UI, this function is responsible for
    translating that to API specific values for the creative rotation objects
    under the ad.

    Args:
      creative_rotation: Feed item representing the creative rotation setup from
        the feed.
      feed_item: Feed item representing the ad.
    

## [/task/traffic/event_tag.py](/task/traffic/event_tag.py)

Handles creation and updates of Ads.




## class EventTagDAO

  Event Tag data access object.

  Inherits from BaseDAO and implements Event Tag specific logic for creating and
  updating Event Tags.
  


###   __init__(self, auth, profile_id):


    Initializes EventTagDAO with profile id and authentication scheme.
    super(EventTagDAO, self).__init__(auth, profile_id)

    self._id_field = FieldMap.EVENT_TAG_ID

    # This causes the dao to search event tag by name, but
    # to do so it is required to pass campaign or advertiser id
    # self._search_field = FieldMap.EVENT_TAG_NAME
    #self._search_field = FieldMap.EVENT_TAG_NAME
    self._search_field = None

    self._list_name = 'eventTags'
    self._entity = 'EVENT_TAGS'
    self._parent_filter_name = 'advertiserId'
    self._parent_dao = None
    self._parent_filter_field_name = FieldMap.ADVERTISER_ID
    self._campaign_dao = CampaignDAO(auth, profile_id)
    self._service = self.service.eventTags()

  def pre_fetch(self, feed):
    Pre-fetches all required items to be update into the cache.
    
    pass

  def _get_base_search_args(self, search_string):
    return {
      'profileId': self.profile_id,
      'searchString': search_string,
      'sortField': 'NAME'
    }

  def _process_update(self, item, feed_item):
    Processes the update of an Event Tag
    
    item['name'] = feed_item.get(FieldMap.EVENT_TAG_NAME, None)
    item['status'] = feed_item.get(FieldMap.EVENT_TAG_STATUS, None)
    item['type'] = feed_item.get(FieldMap.EVENT_TAG_TYPE, None)
    item['url'] = feed_item.get(FieldMap.EVENT_TAG_URL, None)

  def _process_new(self, feed_item):
    Creates a new event tag DCM object from a feed item representing a event tag from the Bulkdozer feed.
    
    campaign = self._campaign_dao.get(feed_item, required=True)

    return {
        'advertiserId':
            feed_item.get(FieldMap.ADVERTISER_ID, None),
        'campaignId':
            campaign.get('id', None) if campaign else None,
        'enabledByDefault':
            feed_item.get(FieldMap.EVENT_TAG_ENABLED_BY_DEFAULT, False),
        'name':
            feed_item.get(FieldMap.EVENT_TAG_NAME, None),
        'status':
            feed_item.get(FieldMap.EVENT_TAG_STATUS, None),
        'type':
            feed_item.get(FieldMap.EVENT_TAG_TYPE, None),
        'url':
            feed_item.get(FieldMap.EVENT_TAG_URL, None)
    }

  def _post_process(self, feed_item, item):
    Updates the feed item with ids and names of related object so those can be updated in the Bulkdozer feed.
    
    campaign = self._campaign_dao.get(feed_item, required=True)

    if campaign:
      feed_item[FieldMap.CAMPAIGN_NAME] = campaign['name']
      feed_item[FieldMap.CAMPAIGN_ID] = campaign['id']

## [/task/traffic/video_format.py](/task/traffic/video_format.py)

Handles creation and updates of video formats.




## class VideoFormatDAO

  Video format data access object.

  Inherits from BaseDAO and implements video format specific logic for creating
  and
  updating video format.
  


###   __init__(self, auth, profile_id):


    Initializes VideoFormatDAO with profile id and authentication scheme.
    super(VideoFormatDAO, self).__init__(auth, profile_id)

    self.profile_id = profile_id
    self._service = self.service.videoFormats()

    self._video_formats = None

  def get_video_formats(self):
    Fetches video formats from CM.
    

    if not self._video_formats:
      self._video_formats = self._retry(self._service.list(
          profileId=self.profile_id))['videoFormats']

    return self._video_formats

  def translate_transcode_config(self, transcode_config):
    Given a transcode config, returns the CM transcodes that match the config.
    
    result = []

    try:
      min_width = int(transcode_config.get(FieldMap.TRANSCODE_MIN_WIDTH, 0))
      min_height = int(transcode_config.get(FieldMap.TRANSCODE_MIN_HEIGHT, 0))
      min_bitrate = int(transcode_config.get(FieldMap.TRANSCODE_MIN_BITRATE, 0))

      max_width = int(transcode_config.get(FieldMap.TRANSCODE_MAX_WIDTH, sys.maxint))
      max_height = int(transcode_config.get(FieldMap.TRANSCODE_MAX_HEIGHT, sys.maxint))
      max_bitrate = int(transcode_config.get(FieldMap.TRANSCODE_MAX_BITRATE, sys.maxint))
    except:
      return result

    file_types = [
        file_type for file_type in FieldMap.TRANSCODE_FILE_TYPES
        if transcode_config.get(file_type, False)
    ]

    for video_format in self.get_video_formats():
      if min_width <= video_format['resolution']['width'] and \
          video_format['resolution']['width'] <= max_width \
          and min_height <= video_format['resolution']['height'] \
          and video_format['resolution']['height'] <= max_height \
          and min_bitrate <= video_format['targetBitRate'] \
          and video_format['targetBitRate'] <= max_bitrate \
          and video_format['fileType'] in file_types:
        result.append(video_format['id'])

    return result

# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Ftask%2Ftraffic%2FREADME.md)
