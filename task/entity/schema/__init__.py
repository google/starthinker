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

from ExchangeSettings import ExchangeSettings_Schema
from UniversalChannel import UniversalChannel_Schema
from CostTrackingPixel import CostTrackingPixel_Schema
from PartnerRevenueModel import PartnerRevenueModel_Schema
from CustomAffinity import CustomAffinity_Schema
from UniversalSite import UniversalSite_Schema
from FrequencyCap import FrequencyCap_Schema
from Creative import Creative_Schema
from LineItem import LineItem_Schema
from Pixel import Pixel_Schema
from EntityCommonData import EntityCommonData_Schema
from UserList import UserList_Schema
from InventorySource import InventorySource_Schema
from FreeFormTarget import FreeFormTarget_Schema
from DeviceCriteria import DeviceCriteria_Schema
from SupportedExchange import SupportedExchange_Schema
from DataPartner import DataPartner_Schema
from UserListPricing import UserListPricing_Schema
from TargetUnion import TargetUnion_Schema
from Target import Target_Schema
from Language import Language_Schema
from ApprovalStatus import ApprovalStatus_Schema
from InsertionOrder import InsertionOrder_Schema
from Budget import Budget_Schema
from UserListAdvertiserPricing import UserListAdvertiserPricing_Schema
from Browser import Browser_Schema
from Advertiser import Advertiser_Schema
from PartnerCosts import PartnerCosts_Schema
from Campaign import Campaign_Schema
from GeoLocation import GeoLocation_Schema
from SelectionTarget import SelectionTarget_Schema
from Isp import Isp_Schema
from Partner import Partner_Schema
from TargetList import TargetList_Schema

Entity_Schema_Lookup = {
  'ExchangeSettings':ExchangeSettings_Schema,
  'UniversalChannel':UniversalChannel_Schema,
  'CostTrackingPixel':CostTrackingPixel_Schema,
  'PartnerRevenueModel':PartnerRevenueModel_Schema,
  'CustomAffinity':CustomAffinity_Schema,
  'UniversalSite':UniversalSite_Schema,
  'FrequencyCap':FrequencyCap_Schema,
  'Creative':Creative_Schema,
  'LineItem':LineItem_Schema,
  'Pixel':Pixel_Schema,
  'EntityCommonData':EntityCommonData_Schema,
  'UserList':UserList_Schema,
  'InventorySource':InventorySource_Schema,
  'FreeFormTarget':FreeFormTarget_Schema,
  'DeviceCriteria':DeviceCriteria_Schema,
  'SupportedExchange':SupportedExchange_Schema,
  'DataPartner':DataPartner_Schema,
  'UserListPricing':UserListPricing_Schema,
  'TargetUnion':TargetUnion_Schema,
  'Target':Target_Schema,
  'Language':Language_Schema,
  'ApprovalStatus':ApprovalStatus_Schema,
  'InsertionOrder':InsertionOrder_Schema,
  'Budget':Budget_Schema,
  'UserListAdvertiserPricing':UserListAdvertiserPricing_Schema,
  'Browser':Browser_Schema,
  'Advertiser':Advertiser_Schema,
  'PartnerCosts':PartnerCosts_Schema,
  'Campaign':Campaign_Schema,
  'GeoLocation':GeoLocation_Schema,
  'SelectionTarget':SelectionTarget_Schema,
  'Isp':Isp_Schema,
  'Partner':Partner_Schema,
  'TargetList':TargetList_Schema,
}
