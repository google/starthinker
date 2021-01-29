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

from starthinker.task.entity.schema.ExchangeSettings import ExchangeSettings_Schema
from starthinker.task.entity.schema.UniversalChannel import UniversalChannel_Schema
from starthinker.task.entity.schema.CostTrackingPixel import CostTrackingPixel_Schema
from starthinker.task.entity.schema.PartnerRevenueModel import PartnerRevenueModel_Schema
from starthinker.task.entity.schema.CustomAffinity import CustomAffinity_Schema
from starthinker.task.entity.schema.UniversalSite import UniversalSite_Schema
from starthinker.task.entity.schema.FrequencyCap import FrequencyCap_Schema
from starthinker.task.entity.schema.Creative import Creative_Schema
from starthinker.task.entity.schema.LineItem import LineItem_Schema
from starthinker.task.entity.schema.Pixel import Pixel_Schema
from starthinker.task.entity.schema.EntityCommonData import EntityCommonData_Schema
from starthinker.task.entity.schema.UserList import UserList_Schema
from starthinker.task.entity.schema.InventorySource import InventorySource_Schema
from starthinker.task.entity.schema.FreeFormTarget import FreeFormTarget_Schema
from starthinker.task.entity.schema.DeviceCriteria import DeviceCriteria_Schema
from starthinker.task.entity.schema.SupportedExchange import SupportedExchange_Schema
from starthinker.task.entity.schema.DataPartner import DataPartner_Schema
from starthinker.task.entity.schema.UserListPricing import UserListPricing_Schema
from starthinker.task.entity.schema.TargetUnion import TargetUnion_Schema
from starthinker.task.entity.schema.Target import Target_Schema
from starthinker.task.entity.schema.Language import Language_Schema
from starthinker.task.entity.schema.ApprovalStatus import ApprovalStatus_Schema
from starthinker.task.entity.schema.InsertionOrder import InsertionOrder_Schema
from starthinker.task.entity.schema.Budget import Budget_Schema
from starthinker.task.entity.schema.UserListAdvertiserPricing import UserListAdvertiserPricing_Schema
from starthinker.task.entity.schema.Browser import Browser_Schema
from starthinker.task.entity.schema.Advertiser import Advertiser_Schema
from starthinker.task.entity.schema.PartnerCosts import PartnerCosts_Schema
from starthinker.task.entity.schema.Campaign import Campaign_Schema
from starthinker.task.entity.schema.GeoLocation import GeoLocation_Schema
from starthinker.task.entity.schema.SelectionTarget import SelectionTarget_Schema
from starthinker.task.entity.schema.Isp import Isp_Schema
from starthinker.task.entity.schema.Partner import Partner_Schema
from starthinker.task.entity.schema.TargetList import TargetList_Schema

Entity_Schema_Lookup = {
    'ExchangeSettings': ExchangeSettings_Schema,
    'UniversalChannel': UniversalChannel_Schema,
    'CostTrackingPixel': CostTrackingPixel_Schema,
    'PartnerRevenueModel': PartnerRevenueModel_Schema,
    'CustomAffinity': CustomAffinity_Schema,
    'UniversalSite': UniversalSite_Schema,
    'FrequencyCap': FrequencyCap_Schema,
    'Creative': Creative_Schema,
    'LineItem': LineItem_Schema,
    'Pixel': Pixel_Schema,
    'EntityCommonData': EntityCommonData_Schema,
    'UserList': UserList_Schema,
    'InventorySource': InventorySource_Schema,
    'FreeFormTarget': FreeFormTarget_Schema,
    'DeviceCriteria': DeviceCriteria_Schema,
    'SupportedExchange': SupportedExchange_Schema,
    'DataPartner': DataPartner_Schema,
    'UserListPricing': UserListPricing_Schema,
    'TargetUnion': TargetUnion_Schema,
    'Target': Target_Schema,
    'Language': Language_Schema,
    'ApprovalStatus': ApprovalStatus_Schema,
    'InsertionOrder': InsertionOrder_Schema,
    'Budget': Budget_Schema,
    'UserListAdvertiserPricing': UserListAdvertiserPricing_Schema,
    'Browser': Browser_Schema,
    'Advertiser': Advertiser_Schema,
    'PartnerCosts': PartnerCosts_Schema,
    'Campaign': Campaign_Schema,
    'GeoLocation': GeoLocation_Schema,
    'SelectionTarget': SelectionTarget_Schema,
    'Isp': Isp_Schema,
    'Partner': Partner_Schema,
    'TargetList': TargetList_Schema,
}
