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

# Field types for Schema Lookup
SDF_Field_Lookup = {
    # Campaign
    'Campaign Id': 'INTEGER',
    'Advertiser Id': 'INTEGER',
    'Name': 'STRING',
    'Timestamp': 'STRING',
    'Status': 'STRING',
    'Campaign Goal': 'STRING',
    'Campaign Goal KPI': 'STRING',
    'Creative Types': 'STRING',
    'Campaign Budget': 'FLOAT',
    'Campaign Start Date': 'STRING',
    'Campaign End Date': 'STRING',
    'Frequency Enabled': 'STRING',
    'Frequency Exposures': 'INTEGER',
    'Frequency Period': 'STRING',
    'Frequency Amount': 'INTEGER',
    'Demographic Targeting Gender': 'STRING',
    'Demographic Targeting Age': 'STRING',
    'Demographic Targeting Household Income': 'STRING',
    'Demographic Targeting Parental Status': 'STRING',
    'Geography Targeting - Include': 'STRING',
    'Geography Targeting - Exclude': 'STRING',
    'Language Targeting - Include': 'STRING',
    'Language Targeting - Exclude': 'STRING',
    'Brand Safety Labels': 'STRING',
    'Brand Safety Sensitivity Setting': 'STRING',
    'Brand Safety Custom Settings': 'STRING',
    'Third Party Services': 'STRING',
    'Third Party Verification Labels': 'STRING',
    'Viewability Targeting Active View': 'STRING',
    'Viewability Targeting Ad Position - Include': 'STRING',
    'Viewability Targeting Ad Position - Exclude': 'STRING',
    'Inventory Source Targeting - Authorized Seller Only': 'STRING',
    'Inventory Source Targeting - Include': 'STRING',
    'Inventory Source Targeting - Exclude': 'STRING',
    'Inventory Source Targeting - Target New Exchanges': 'STRING',
    'Environment Targeting': 'STRING',
    # Insertion Order
    'Io Id': 'INTEGER',
    'Io Type': 'STRING',
    'Fees': 'STRING',
    'Integration Code': 'STRING',
    'Details': 'STRING',
    'Pacing': 'STRING',
    'Pacing Rate': 'STRING',
    'Pacing Amount': 'FLOAT',
    'Performance Goal Type': 'STRING',
    'Performance Goal Value': 'STRING',
    'Measure DAR': 'STRING',
    'Measure DAR Channel': 'INTEGER',
    'Budget': 'STRING',
    'Budget Segments': 'STRING',
    'Auto Budget Allocation': 'STRING',
    'Device Targeting - Include': 'STRING',
    'Device Targeting - Exclude': 'STRING',
    'Browser Targeting - Include': 'STRING',
    'Browser Targeting - Exclude': 'STRING',
    'Brand Safety Labels': 'STRING',
    'Brand Safety Sensitivity Setting': 'STRING',
    'Brand Safety Custom Settings': 'STRING',
    'Third Party Verification Services': 'STRING',
    'Third Party Verification Labels': 'STRING',
    'Channel Targeting - Include': 'STRING',
    'Channel Targeting - Exclude': 'STRING',
    'Site Targeting - Include': 'STRING',
    'Site Targeting - Exclude': 'STRING',
    'App Targeting - Exclude': 'STRING',
    'App Collection Targeting - Include': 'STRING',
    'App Collection Targeting - Exclude': 'STRING',
    'Category Targeting - Include': 'STRING',
    'Category Targeting - Exclude': 'STRING',
    'Keyword Targeting - Include': 'STRING',
    'Keyword Targeting - Exclude': 'STRING',
    'Keyword List Targeting - Exclude': 'STRING',
    'Audience Targeting - Similar Audiences': 'STRING',
    'Audience Targeting - Include': 'STRING',
    'Audience Targeting - Exclude': 'STRING',
    'Affinity & In Market Targeting - Include': 'STRING',
    'Affinity & In Market Targeting - Exclude': 'STRING',
    'Custom List Targeting': 'STRING',
    'Inventory Source Targeting - Authorized Seller Only': 'STRING',
    'Inventory Source Targeting - Include': 'STRING',
    'Inventory Source Targeting - Exclude': 'STRING',
    'Inventory Source Targeting - Target New Exchanges': 'STRING',
    'Daypart Targeting': 'STRING',
    'Daypart Targeting Time Zone': 'STRING',
    'Environment Targeting': 'STRING',
    # Line Items
    'Line Item Id': 'INTEGER',
    'Budget Amount': 'FLOAT',
    'TrueView View Frequency Exposures': 'INTEGER',
    'Partner Revenue Amount': 'FLOAT',
    'Conversion Counting Pct': 'FLOAT',
    'Bid Strategy Value': 'FLOAT',
    'Bid Strategy Do Not Exceed': 'FLOAT',
    'TrueView Bid Strategy Value': 'FLOAT',
    'Bid Strategy Do Not Exceed': 'FLOAT',
    'TrueView Mobile Bid Adjustment Percentage': 'INTEGER',
    'TrueView Desktop Bid Adjustment Percentage': 'INTEGER',
    'TrueView Tablet Bid Adjustment Percentage': 'INTEGER',
    # Inventory Source
    'Rate': 'FLOAT',
    'Units Purchased': 'INTEGER',
    # Media Product
    'Product Id': 'INTEGER',
    'Plan Id': 'INTEGER',
    'Campaign Id': 'INTEGER',
    'Budget': 'FLOAT',
    'Frequency Exposures': 'INTEGER',
    'Frequency Amount': 'INTEGER',
    # Ad Group
    'Ad Group Id': 'INTEGER',
    'Line Item Id': 'INTEGER',
    'Bid Cost': 'FLOAT',
    'Popular Videos Bid Adjustment': 'INTEGER',
    # Ad
    'Ad Id': 'INTEGER',
    'Ad Group Id': 'INTEGER',
    'DCM Tracking - Placement Id': 'INTEGER',
    'DCM Tracking - Ad Id': 'INTEGER',
    'DCM Tracking - Creative Id': 'INTEGER'
}

SDF_COLUMNS = ('Line_Item_Id, Io_Id, Type, Subtype, Name, Timestamp, Status, '
               'Start_Date, End_Date, Budget_Type, Budget_Amount, Pacing, '
               'Pacing_Rate, Pacing_Amount, Frequency_Enabled, '
               'Frequency_Exposures, Frequency_Period, Frequency_Amount, '
               'Trueview_View_Frequency_Enabled, '
               'Trueview_View_Frequency_Exposures, '
               'Trueview_View_Frequency_Period, Partner_Revenue_Model, '
               'Partner_Revenue_Amount, Conversion_Counting_Type, '
               'Conversion_Counting_Pct, Conversion_Pixel_Ids, Fees, '
               'Integration_Code, Details, Bid_Strategy_Type, '
               'Bid_Strategy_Value, Bid_Strategy_Unit, '
               'Bid_Strategy_Do_Not_Exceed, Creative_Assignments, '
               'Geography_Targeting_Include, Geography_Targeting_Exclude, '
               'Language_Targeting_Include, Language_Targeting_Exclude, '
               'Device_Targeting_Include, Device_Targeting_Exclude, '
               'Browser_Targeting_Include, Browser_Targeting_Exclude, '
               'Brand_Safety_Labels, Brand_Safety_Sensitivity_Setting, '
               'Brand_Safety_Custom_Settings, '
               'Third_Party_Verification_Services, '
               'Third_Party_Verification_Labels, Channel_Targeting_Include, '
               'Channel_Targeting_Exclude, Site_Targeting_Include, '
               'Site_Targeting_Exclude, App_Targeting_Include, '
               'App_Targeting_Exclude, Category_Targeting_Include, '
               'Category_Targeting_Exclude, Keyword_Targeting_Include, '
               'Keyword_Targeting_Exclude, '
               'Audience_Targeting_Similar_Audiences, '
               'Audience_Targeting_Include, Audience_Targeting_Exclude, '
               'Affinity_In_Market_Targeting_Include, '
               'Affinity_In_Market_Targeting_Exclude, '
               'Custom_Affinity_Targeting, Inventory_Source_Targeting_Include, '
               'Inventory_Source_Targeting_Exclude, Daypart_Targeting, '
               'Environment_Targeting, Viewability_Targeting_Active_View, '
               'Viewability_Targeting_Ad_Position_Include, '
               'Viewability_Targeting_Ad_Position_Exclude, '
               'Video_Ad_Position_Targeting, Video_Player_Size_Targeting, '
               'Demographic_Targeting_Gender, Demographic_Targeting_Age, '
               'Connection_Speed_Targeting, Carrier_Targeting_Include, '
               'Carrier_Targeting_Exclude, '
               'Trueview_Mobile_Bid_Adjustment_Option, '
               'Trueview_Mobile_Bid_Adjustment_Percentage, '
               'Trueview_Category_Exclusions_Targeting, '
               'Trueview_Inventory_Source_Targeting')

SDF_FILE_TYPE_COLUMNS = {
    'AD': [
        'Line_Item_Id', 'Io_Id', 'Type', 'Subtype', 'Name', 'Timestamp',
        'Status', 'Start_Date', 'End_Date', 'Budget_Type', 'Budget_Amount',
        'Pacing', 'Pacing_Rate', 'Pacing_Amount', 'Frequency_Enabled',
        'Frequency_Exposures', 'Frequency_Period', 'Frequency_Amount',
        'Trueview_View_Frequency_Enabled', 'Trueview_View_Frequency_Exposures',
        'Trueview_View_Frequency_Period', 'Partner_Revenue_Model',
        'Partner_Revenue_Amount', 'Conversion_Counting_Type',
        'Conversion_Counting_Pct', 'Conversion_Pixel_Ids', 'Fees',
        'Integration_Code', 'Details', 'Bid_Strategy_Type',
        'Bid_Strategy_Value', 'Bid_Strategy_Unit', 'Bid_Strategy_Do_Not_Exceed',
        'Creative_Assignments', 'Geography_Targeting_Include',
        'Geography_Targeting_Exclude', 'Language_Targeting_Include',
        'Language_Targeting_Exclude', 'Device_Targeting_Include',
        'Device_Targeting_Exclude', 'Browser_Targeting_Include',
        'Browser_Targeting_Exclude', 'Brand_Safety_Labels',
        'Brand_Safety_Sensitivity_Setting', 'Brand_Safety_Custom_Settings',
        'Third_Party_Verification_Services', 'Third_Party_Verification_Labels',
        'Channel_Targeting_Include', 'Channel_Targeting_Exclude',
        'Site_Targeting_Include', 'Site_Targeting_Exclude',
        'App_Targeting_Include', 'App_Targeting_Exclude',
        'Category_Targeting_Include', 'Category_Targeting_Exclude',
        'Keyword_Targeting_Include', 'Keyword_Targeting_Exclude',
        'Audience_Targeting_Similar_Audiences', 'Audience_Targeting_Include',
        'Audience_Targeting_Exclude', 'Affinity_In_Market_Targeting_Include',
        'Affinity_In_Market_Targeting_Exclude', 'Custom_Affinity_Targeting',
        'Inventory_Source_Targeting_Include',
        'Inventory_Source_Targeting_Exclude', 'Daypart_Targeting',
        'Environment_Targeting', 'Viewability_Targeting_Active_View',
        'Viewability_Targeting_Ad_Position_Include',
        'Viewability_Targeting_Ad_Position_Exclude',
        'Video_Ad_Position_Targeting', 'Video_Player_Size_Targeting',
        'Demographic_Targeting_Gender', 'Demographic_Targeting_Age',
        'Connection_Speed_Targeting', 'Carrier_Targeting_Include',
        'Carrier_Targeting_Exclude', 'Trueview_Mobile_Bid_Adjustment_Option',
        'Trueview_Mobile_Bid_Adjustment_Percentage',
        'Trueview_Category_Exclusions_Targeting',
        'Trueview_Inventory_Source_Targeting'
    ],
    'AD_GROUP': [],
    'CAMPAIGN': [],
    'INSERTION_ORDER': [],
    'LINE_ITEM': [
        'Line_Item_Id', 'Io_Id', 'Type', 'Subtype', 'Name', 'Timestamp',
        'Status', 'Start_Date', 'End_Date', 'Budget_Type', 'Budget_Amount',
        'Pacing', 'Pacing_Rate', 'Pacing_Amount', 'Frequency_Enabled',
        'Frequency_Exposures', 'Frequency_Period', 'Frequency_Amount',
        'Trueview_View_Frequency_Enabled', 'Trueview_View_Frequency_Exposures',
        'Trueview_View_Frequency_Period', 'Partner_Revenue_Model',
        'Partner_Revenue_Amount', 'Conversion_Counting_Type',
        'Conversion_Counting_Pct', 'Conversion_Pixel_Ids', 'Fees',
        'Integration_Code', 'Details', 'Bid_Strategy_Type',
        'Bid_Strategy_Value', 'Bid_Strategy_Unit', 'Bid_Strategy_Do_Not_Exceed',
        'Creative_Assignments', 'Geography_Targeting_Include',
        'Geography_Targeting_Exclude', 'Language_Targeting_Include',
        'Language_Targeting_Exclude', 'Device_Targeting_Include',
        'Device_Targeting_Exclude', 'Browser_Targeting_Include',
        'Browser_Targeting_Exclude', 'Brand_Safety_Labels',
        'Brand_Safety_Sensitivity_Setting', 'Brand_Safety_Custom_Settings',
        'Third_Party_Verification_Services', 'Third_Party_Verification_Labels',
        'Channel_Targeting_Include', 'Channel_Targeting_Exclude',
        'Site_Targeting_Include', 'Site_Targeting_Exclude',
        'App_Targeting_Include', 'App_Targeting_Exclude',
        'Category_Targeting_Include', 'Category_Targeting_Exclude',
        'Keyword_Targeting_Include', 'Keyword_Targeting_Exclude',
        'Audience_Targeting_Similar_Audiences', 'Audience_Targeting_Include',
        'Audience_Targeting_Exclude', 'Affinity_In_Market_Targeting_Include',
        'Affinity_In_Market_Targeting_Exclude', 'Custom_Affinity_Targeting',
        'Inventory_Source_Targeting_Include',
        'Inventory_Source_Targeting_Exclude', 'Daypart_Targeting',
        'Environment_Targeting', 'Viewability_Targeting_Active_View',
        'Viewability_Targeting_Ad_Position_Include',
        'Viewability_Targeting_Ad_Position_Exclude',
        'Video_Ad_Position_Targeting', 'Video_Player_Size_Targeting',
        'Demographic_Targeting_Gender', 'Demographic_Targeting_Age',
        'Connection_Speed_Targeting', 'Carrier_Targeting_Include',
        'Carrier_Targeting_Exclude', 'Trueview_Mobile_Bid_Adjustment_Option',
        'Trueview_Mobile_Bid_Adjustment_Percentage',
        'Trueview_Category_Exclusions_Targeting',
        'Trueview_Inventory_Source_Targeting'
    ],
}
