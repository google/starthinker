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

from starthinker.task.dcm_api.schema.account import account_Schema
from starthinker.task.dcm_api.schema.accountActiveAdSummary import accountActiveAdSummary_Schema
from starthinker.task.dcm_api.schema.accountPermission import accountPermission_Schema
from starthinker.task.dcm_api.schema.accountPermissionGroup import accountPermissionGroup_Schema
from starthinker.task.dcm_api.schema.accountPermissionGroupsListResponse import accountPermissionGroupsListResponse_Schema
from starthinker.task.dcm_api.schema.accountPermissionsListResponse import accountPermissionsListResponse_Schema
from starthinker.task.dcm_api.schema.accountUserProfile import accountUserProfile_Schema
from starthinker.task.dcm_api.schema.accountUserProfilesListResponse import accountUserProfilesListResponse_Schema
from starthinker.task.dcm_api.schema.accountsListResponse import accountsListResponse_Schema
from starthinker.task.dcm_api.schema.activities import activities_Schema
from starthinker.task.dcm_api.schema.ad import ad_Schema
from starthinker.task.dcm_api.schema.adBlockingConfiguration import adBlockingConfiguration_Schema
from starthinker.task.dcm_api.schema.adSlot import adSlot_Schema
from starthinker.task.dcm_api.schema.adsListResponse import adsListResponse_Schema
from starthinker.task.dcm_api.schema.advertiser import advertiser_Schema
from starthinker.task.dcm_api.schema.advertiserGroup import advertiserGroup_Schema
from starthinker.task.dcm_api.schema.advertiserGroupsListResponse import advertiserGroupsListResponse_Schema
from starthinker.task.dcm_api.schema.advertiserLandingPagesListResponse import advertiserLandingPagesListResponse_Schema
from starthinker.task.dcm_api.schema.advertisersListResponse import advertisersListResponse_Schema
from starthinker.task.dcm_api.schema.audienceSegment import audienceSegment_Schema
from starthinker.task.dcm_api.schema.audienceSegmentGroup import audienceSegmentGroup_Schema
from starthinker.task.dcm_api.schema.browser import browser_Schema
from starthinker.task.dcm_api.schema.browsersListResponse import browsersListResponse_Schema
from starthinker.task.dcm_api.schema.campaign import campaign_Schema
from starthinker.task.dcm_api.schema.campaignCreativeAssociation import campaignCreativeAssociation_Schema
from starthinker.task.dcm_api.schema.campaignCreativeAssociationsListResponse import campaignCreativeAssociationsListResponse_Schema
from starthinker.task.dcm_api.schema.campaignsListResponse import campaignsListResponse_Schema
from starthinker.task.dcm_api.schema.changeLog import changeLog_Schema
from starthinker.task.dcm_api.schema.changeLogsListResponse import changeLogsListResponse_Schema
from starthinker.task.dcm_api.schema.citiesListResponse import citiesListResponse_Schema
from starthinker.task.dcm_api.schema.city import city_Schema
from starthinker.task.dcm_api.schema.clickTag import clickTag_Schema
from starthinker.task.dcm_api.schema.clickThroughUrl import clickThroughUrl_Schema
from starthinker.task.dcm_api.schema.clickThroughUrlSuffixProperties import clickThroughUrlSuffixProperties_Schema
from starthinker.task.dcm_api.schema.companionClickThroughOverride import companionClickThroughOverride_Schema
from starthinker.task.dcm_api.schema.companionSetting import companionSetting_Schema
from starthinker.task.dcm_api.schema.compatibleFields import compatibleFields_Schema
from starthinker.task.dcm_api.schema.connectionType import connectionType_Schema
from starthinker.task.dcm_api.schema.connectionTypesListResponse import connectionTypesListResponse_Schema
from starthinker.task.dcm_api.schema.contentCategoriesListResponse import contentCategoriesListResponse_Schema
from starthinker.task.dcm_api.schema.contentCategory import contentCategory_Schema
from starthinker.task.dcm_api.schema.conversion import conversion_Schema
from starthinker.task.dcm_api.schema.conversionError import conversionError_Schema
from starthinker.task.dcm_api.schema.conversionStatus import conversionStatus_Schema
from starthinker.task.dcm_api.schema.conversionsBatchInsertRequest import conversionsBatchInsertRequest_Schema
from starthinker.task.dcm_api.schema.conversionsBatchInsertResponse import conversionsBatchInsertResponse_Schema
from starthinker.task.dcm_api.schema.conversionsBatchUpdateRequest import conversionsBatchUpdateRequest_Schema
from starthinker.task.dcm_api.schema.conversionsBatchUpdateResponse import conversionsBatchUpdateResponse_Schema
from starthinker.task.dcm_api.schema.countriesListResponse import countriesListResponse_Schema
from starthinker.task.dcm_api.schema.country import country_Schema
from starthinker.task.dcm_api.schema.creative import creative_Schema
from starthinker.task.dcm_api.schema.creativeAsset import creativeAsset_Schema
from starthinker.task.dcm_api.schema.creativeAssetId import creativeAssetId_Schema
from starthinker.task.dcm_api.schema.creativeAssetMetadata import creativeAssetMetadata_Schema
from starthinker.task.dcm_api.schema.creativeAssetSelection import creativeAssetSelection_Schema
from starthinker.task.dcm_api.schema.creativeAssignment import creativeAssignment_Schema
from starthinker.task.dcm_api.schema.creativeClickThroughUrl import creativeClickThroughUrl_Schema
from starthinker.task.dcm_api.schema.creativeCustomEvent import creativeCustomEvent_Schema
from starthinker.task.dcm_api.schema.creativeField import creativeField_Schema
from starthinker.task.dcm_api.schema.creativeFieldAssignment import creativeFieldAssignment_Schema
from starthinker.task.dcm_api.schema.creativeFieldValue import creativeFieldValue_Schema
from starthinker.task.dcm_api.schema.creativeFieldValuesListResponse import creativeFieldValuesListResponse_Schema
from starthinker.task.dcm_api.schema.creativeFieldsListResponse import creativeFieldsListResponse_Schema
from starthinker.task.dcm_api.schema.creativeGroup import creativeGroup_Schema
from starthinker.task.dcm_api.schema.creativeGroupAssignment import creativeGroupAssignment_Schema
from starthinker.task.dcm_api.schema.creativeGroupsListResponse import creativeGroupsListResponse_Schema
from starthinker.task.dcm_api.schema.creativeOptimizationConfiguration import creativeOptimizationConfiguration_Schema
from starthinker.task.dcm_api.schema.creativeRotation import creativeRotation_Schema
from starthinker.task.dcm_api.schema.creativesListResponse import creativesListResponse_Schema
from starthinker.task.dcm_api.schema.crossDimensionReachReportCompatibleFields import crossDimensionReachReportCompatibleFields_Schema
from starthinker.task.dcm_api.schema.customFloodlightVariable import customFloodlightVariable_Schema
from starthinker.task.dcm_api.schema.customRichMediaEvents import customRichMediaEvents_Schema
from starthinker.task.dcm_api.schema.customViewabilityMetric import customViewabilityMetric_Schema
from starthinker.task.dcm_api.schema.customViewabilityMetricConfiguration import customViewabilityMetricConfiguration_Schema
from starthinker.task.dcm_api.schema.dateRange import dateRange_Schema
from starthinker.task.dcm_api.schema.dayPartTargeting import dayPartTargeting_Schema
from starthinker.task.dcm_api.schema.deepLink import deepLink_Schema
from starthinker.task.dcm_api.schema.defaultClickThroughEventTagProperties import defaultClickThroughEventTagProperties_Schema
from starthinker.task.dcm_api.schema.deliverySchedule import deliverySchedule_Schema
from starthinker.task.dcm_api.schema.dfpSettings import dfpSettings_Schema
from starthinker.task.dcm_api.schema.dimension import dimension_Schema
from starthinker.task.dcm_api.schema.dimensionFilter import dimensionFilter_Schema
from starthinker.task.dcm_api.schema.dimensionValue import dimensionValue_Schema
from starthinker.task.dcm_api.schema.dimensionValueList import dimensionValueList_Schema
from starthinker.task.dcm_api.schema.dimensionValueRequest import dimensionValueRequest_Schema
from starthinker.task.dcm_api.schema.directorySite import directorySite_Schema
from starthinker.task.dcm_api.schema.directorySiteSettings import directorySiteSettings_Schema
from starthinker.task.dcm_api.schema.directorySitesListResponse import directorySitesListResponse_Schema
from starthinker.task.dcm_api.schema.dynamicTargetingKey import dynamicTargetingKey_Schema
from starthinker.task.dcm_api.schema.dynamicTargetingKeysListResponse import dynamicTargetingKeysListResponse_Schema
from starthinker.task.dcm_api.schema.encryptionInfo import encryptionInfo_Schema
from starthinker.task.dcm_api.schema.eventTag import eventTag_Schema
from starthinker.task.dcm_api.schema.eventTagOverride import eventTagOverride_Schema
from starthinker.task.dcm_api.schema.eventTagsListResponse import eventTagsListResponse_Schema
from starthinker.task.dcm_api.schema.file import file_Schema
from starthinker.task.dcm_api.schema.fileList import fileList_Schema
from starthinker.task.dcm_api.schema.flight import flight_Schema
from starthinker.task.dcm_api.schema.floodlightActivitiesGenerateTagResponse import floodlightActivitiesGenerateTagResponse_Schema
from starthinker.task.dcm_api.schema.floodlightActivitiesListResponse import floodlightActivitiesListResponse_Schema
from starthinker.task.dcm_api.schema.floodlightActivity import floodlightActivity_Schema
from starthinker.task.dcm_api.schema.floodlightActivityDynamicTag import floodlightActivityDynamicTag_Schema
from starthinker.task.dcm_api.schema.floodlightActivityGroup import floodlightActivityGroup_Schema
from starthinker.task.dcm_api.schema.floodlightActivityGroupsListResponse import floodlightActivityGroupsListResponse_Schema
from starthinker.task.dcm_api.schema.floodlightActivityPublisherDynamicTag import floodlightActivityPublisherDynamicTag_Schema
from starthinker.task.dcm_api.schema.floodlightConfiguration import floodlightConfiguration_Schema
from starthinker.task.dcm_api.schema.floodlightConfigurationsListResponse import floodlightConfigurationsListResponse_Schema
from starthinker.task.dcm_api.schema.floodlightReportCompatibleFields import floodlightReportCompatibleFields_Schema
from starthinker.task.dcm_api.schema.frequencyCap import frequencyCap_Schema
from starthinker.task.dcm_api.schema.fsCommand import fsCommand_Schema
from starthinker.task.dcm_api.schema.geoTargeting import geoTargeting_Schema
from starthinker.task.dcm_api.schema.inventoryItem import inventoryItem_Schema
from starthinker.task.dcm_api.schema.inventoryItemsListResponse import inventoryItemsListResponse_Schema
from starthinker.task.dcm_api.schema.keyValueTargetingExpression import keyValueTargetingExpression_Schema
from starthinker.task.dcm_api.schema.landingPage import landingPage_Schema
from starthinker.task.dcm_api.schema.language import language_Schema
from starthinker.task.dcm_api.schema.languageTargeting import languageTargeting_Schema
from starthinker.task.dcm_api.schema.languagesListResponse import languagesListResponse_Schema
from starthinker.task.dcm_api.schema.lastModifiedInfo import lastModifiedInfo_Schema
from starthinker.task.dcm_api.schema.listPopulationClause import listPopulationClause_Schema
from starthinker.task.dcm_api.schema.listPopulationRule import listPopulationRule_Schema
from starthinker.task.dcm_api.schema.listPopulationTerm import listPopulationTerm_Schema
from starthinker.task.dcm_api.schema.listTargetingExpression import listTargetingExpression_Schema
from starthinker.task.dcm_api.schema.lookbackConfiguration import lookbackConfiguration_Schema
from starthinker.task.dcm_api.schema.metric import metric_Schema
from starthinker.task.dcm_api.schema.metro import metro_Schema
from starthinker.task.dcm_api.schema.metrosListResponse import metrosListResponse_Schema
from starthinker.task.dcm_api.schema.mobileApp import mobileApp_Schema
from starthinker.task.dcm_api.schema.mobileAppsListResponse import mobileAppsListResponse_Schema
from starthinker.task.dcm_api.schema.mobileCarrier import mobileCarrier_Schema
from starthinker.task.dcm_api.schema.mobileCarriersListResponse import mobileCarriersListResponse_Schema
from starthinker.task.dcm_api.schema.objectFilter import objectFilter_Schema
from starthinker.task.dcm_api.schema.offsetPosition import offsetPosition_Schema
from starthinker.task.dcm_api.schema.omnitureSettings import omnitureSettings_Schema
from starthinker.task.dcm_api.schema.operatingSystem import operatingSystem_Schema
from starthinker.task.dcm_api.schema.operatingSystemVersion import operatingSystemVersion_Schema
from starthinker.task.dcm_api.schema.operatingSystemVersionsListResponse import operatingSystemVersionsListResponse_Schema
from starthinker.task.dcm_api.schema.operatingSystemsListResponse import operatingSystemsListResponse_Schema
from starthinker.task.dcm_api.schema.optimizationActivity import optimizationActivity_Schema
from starthinker.task.dcm_api.schema.order import order_Schema
from starthinker.task.dcm_api.schema.orderContact import orderContact_Schema
from starthinker.task.dcm_api.schema.orderDocument import orderDocument_Schema
from starthinker.task.dcm_api.schema.orderDocumentsListResponse import orderDocumentsListResponse_Schema
from starthinker.task.dcm_api.schema.ordersListResponse import ordersListResponse_Schema
from starthinker.task.dcm_api.schema.pathToConversionReportCompatibleFields import pathToConversionReportCompatibleFields_Schema
from starthinker.task.dcm_api.schema.placement import placement_Schema
from starthinker.task.dcm_api.schema.placementAssignment import placementAssignment_Schema
from starthinker.task.dcm_api.schema.placementGroup import placementGroup_Schema
from starthinker.task.dcm_api.schema.placementGroupsListResponse import placementGroupsListResponse_Schema
from starthinker.task.dcm_api.schema.placementStrategiesListResponse import placementStrategiesListResponse_Schema
from starthinker.task.dcm_api.schema.placementStrategy import placementStrategy_Schema
from starthinker.task.dcm_api.schema.placementTag import placementTag_Schema
from starthinker.task.dcm_api.schema.placementsGenerateTagsResponse import placementsGenerateTagsResponse_Schema
from starthinker.task.dcm_api.schema.placementsListResponse import placementsListResponse_Schema
from starthinker.task.dcm_api.schema.platformType import platformType_Schema
from starthinker.task.dcm_api.schema.platformTypesListResponse import platformTypesListResponse_Schema
from starthinker.task.dcm_api.schema.popupWindowProperties import popupWindowProperties_Schema
from starthinker.task.dcm_api.schema.postalCode import postalCode_Schema
from starthinker.task.dcm_api.schema.postalCodesListResponse import postalCodesListResponse_Schema
from starthinker.task.dcm_api.schema.pricing import pricing_Schema
from starthinker.task.dcm_api.schema.pricingSchedule import pricingSchedule_Schema
from starthinker.task.dcm_api.schema.pricingSchedulePricingPeriod import pricingSchedulePricingPeriod_Schema
from starthinker.task.dcm_api.schema.project import project_Schema
from starthinker.task.dcm_api.schema.projectsListResponse import projectsListResponse_Schema
from starthinker.task.dcm_api.schema.reachReportCompatibleFields import reachReportCompatibleFields_Schema
from starthinker.task.dcm_api.schema.recipient import recipient_Schema
from starthinker.task.dcm_api.schema.region import region_Schema
from starthinker.task.dcm_api.schema.regionsListResponse import regionsListResponse_Schema
from starthinker.task.dcm_api.schema.remarketingList import remarketingList_Schema
from starthinker.task.dcm_api.schema.remarketingListShare import remarketingListShare_Schema
from starthinker.task.dcm_api.schema.remarketingListsListResponse import remarketingListsListResponse_Schema
from starthinker.task.dcm_api.schema.report import report_Schema
from starthinker.task.dcm_api.schema.reportCompatibleFields import reportCompatibleFields_Schema
from starthinker.task.dcm_api.schema.reportList import reportList_Schema
from starthinker.task.dcm_api.schema.reportsConfiguration import reportsConfiguration_Schema
from starthinker.task.dcm_api.schema.richMediaExitOverride import richMediaExitOverride_Schema
from starthinker.task.dcm_api.schema.rule import rule_Schema
from starthinker.task.dcm_api.schema.site import site_Schema
from starthinker.task.dcm_api.schema.siteCompanionSetting import siteCompanionSetting_Schema
from starthinker.task.dcm_api.schema.siteContact import siteContact_Schema
from starthinker.task.dcm_api.schema.siteSettings import siteSettings_Schema
from starthinker.task.dcm_api.schema.siteSkippableSetting import siteSkippableSetting_Schema
from starthinker.task.dcm_api.schema.siteTranscodeSetting import siteTranscodeSetting_Schema
from starthinker.task.dcm_api.schema.siteVideoSettings import siteVideoSettings_Schema
from starthinker.task.dcm_api.schema.sitesListResponse import sitesListResponse_Schema
from starthinker.task.dcm_api.schema.size import size_Schema
from starthinker.task.dcm_api.schema.sizesListResponse import sizesListResponse_Schema
from starthinker.task.dcm_api.schema.skippableSetting import skippableSetting_Schema
from starthinker.task.dcm_api.schema.sortedDimension import sortedDimension_Schema
from starthinker.task.dcm_api.schema.subaccount import subaccount_Schema
from starthinker.task.dcm_api.schema.subaccountsListResponse import subaccountsListResponse_Schema
from starthinker.task.dcm_api.schema.tagData import tagData_Schema
from starthinker.task.dcm_api.schema.tagSetting import tagSetting_Schema
from starthinker.task.dcm_api.schema.tagSettings import tagSettings_Schema
from starthinker.task.dcm_api.schema.targetWindow import targetWindow_Schema
from starthinker.task.dcm_api.schema.targetableRemarketingList import targetableRemarketingList_Schema
from starthinker.task.dcm_api.schema.targetableRemarketingListsListResponse import targetableRemarketingListsListResponse_Schema
from starthinker.task.dcm_api.schema.targetingTemplate import targetingTemplate_Schema
from starthinker.task.dcm_api.schema.targetingTemplatesListResponse import targetingTemplatesListResponse_Schema
from starthinker.task.dcm_api.schema.technologyTargeting import technologyTargeting_Schema
from starthinker.task.dcm_api.schema.thirdPartyAuthenticationToken import thirdPartyAuthenticationToken_Schema
from starthinker.task.dcm_api.schema.thirdPartyTrackingUrl import thirdPartyTrackingUrl_Schema
from starthinker.task.dcm_api.schema.transcodeSetting import transcodeSetting_Schema
from starthinker.task.dcm_api.schema.universalAdId import universalAdId_Schema
from starthinker.task.dcm_api.schema.userDefinedVariableConfiguration import userDefinedVariableConfiguration_Schema
from starthinker.task.dcm_api.schema.userProfile import userProfile_Schema
from starthinker.task.dcm_api.schema.userProfileList import userProfileList_Schema
from starthinker.task.dcm_api.schema.userRole import userRole_Schema
from starthinker.task.dcm_api.schema.userRolePermission import userRolePermission_Schema
from starthinker.task.dcm_api.schema.userRolePermissionGroup import userRolePermissionGroup_Schema
from starthinker.task.dcm_api.schema.userRolePermissionGroupsListResponse import userRolePermissionGroupsListResponse_Schema
from starthinker.task.dcm_api.schema.userRolePermissionsListResponse import userRolePermissionsListResponse_Schema
from starthinker.task.dcm_api.schema.userRolesListResponse import userRolesListResponse_Schema
from starthinker.task.dcm_api.schema.videoFormat import videoFormat_Schema
from starthinker.task.dcm_api.schema.videoFormatsListResponse import videoFormatsListResponse_Schema
from starthinker.task.dcm_api.schema.videoOffset import videoOffset_Schema
from starthinker.task.dcm_api.schema.videoSettings import videoSettings_Schema

DCM_Schema_Lookup = {
    'accounts':
        account_Schema,
    'accountActiveAdSummaries':
        accountActiveAdSummary_Schema,
    'accountPermissions':
        accountPermission_Schema,
    'accountPermissionGroups':
        accountPermissionGroup_Schema,
    'accountPermissionGroupsListResponses':
        accountPermissionGroupsListResponse_Schema,
    'accountPermissionsListResponses':
        accountPermissionsListResponse_Schema,
    'accountUserProfiles':
        accountUserProfile_Schema,
    'accountUserProfilesListResponses':
        accountUserProfilesListResponse_Schema,
    'accountsListResponses':
        accountsListResponse_Schema,
    'activitieses':
        activities_Schema,
    'ads':
        ad_Schema,
    'adBlockingConfigurations':
        adBlockingConfiguration_Schema,
    'adSlots':
        adSlot_Schema,
    'adsListResponses':
        adsListResponse_Schema,
    'advertisers':
        advertiser_Schema,
    'advertiserGroups':
        advertiserGroup_Schema,
    'advertiserGroupsListResponses':
        advertiserGroupsListResponse_Schema,
    'advertiserLandingPagesListResponses':
        advertiserLandingPagesListResponse_Schema,
    'advertisersListResponses':
        advertisersListResponse_Schema,
    'audienceSegments':
        audienceSegment_Schema,
    'audienceSegmentGroups':
        audienceSegmentGroup_Schema,
    'browsers':
        browser_Schema,
    'browsersListResponses':
        browsersListResponse_Schema,
    'campaigns':
        campaign_Schema,
    'campaignCreativeAssociations':
        campaignCreativeAssociation_Schema,
    'campaignCreativeAssociationsListResponses':
        campaignCreativeAssociationsListResponse_Schema,
    'campaignsListResponses':
        campaignsListResponse_Schema,
    'changeLogs':
        changeLog_Schema,
    'changeLogsListResponses':
        changeLogsListResponse_Schema,
    'citiesListResponses':
        citiesListResponse_Schema,
    'cities':
        city_Schema,
    'clickTags':
        clickTag_Schema,
    'clickThroughUrls':
        clickThroughUrl_Schema,
    'clickThroughUrlSuffixPropertieses':
        clickThroughUrlSuffixProperties_Schema,
    'companionClickThroughOverrides':
        companionClickThroughOverride_Schema,
    'companionSettings':
        companionSetting_Schema,
    'compatibleFieldses':
        compatibleFields_Schema,
    'connectionTypes':
        connectionType_Schema,
    'connectionTypesListResponses':
        connectionTypesListResponse_Schema,
    'contentCategoriesListResponses':
        contentCategoriesListResponse_Schema,
    'contentCategories':
        contentCategory_Schema,
    'conversions':
        conversion_Schema,
    'conversionErrors':
        conversionError_Schema,
    'conversionStatuses':
        conversionStatus_Schema,
    'conversionsBatchInsertRequests':
        conversionsBatchInsertRequest_Schema,
    'conversionsBatchInsertResponses':
        conversionsBatchInsertResponse_Schema,
    'conversionsBatchUpdateRequests':
        conversionsBatchUpdateRequest_Schema,
    'conversionsBatchUpdateResponses':
        conversionsBatchUpdateResponse_Schema,
    'countriesListResponses':
        countriesListResponse_Schema,
    'countries':
        country_Schema,
    'creatives':
        creative_Schema,
    'creativeAssets':
        creativeAsset_Schema,
    'creativeAssetIds':
        creativeAssetId_Schema,
    'creativeAssetMetadatas':
        creativeAssetMetadata_Schema,
    'creativeAssetSelections':
        creativeAssetSelection_Schema,
    'creativeAssignments':
        creativeAssignment_Schema,
    'creativeClickThroughUrls':
        creativeClickThroughUrl_Schema,
    'creativeCustomEvents':
        creativeCustomEvent_Schema,
    'creativeFields':
        creativeField_Schema,
    'creativeFieldAssignments':
        creativeFieldAssignment_Schema,
    'creativeFieldValues':
        creativeFieldValue_Schema,
    'creativeFieldValuesListResponses':
        creativeFieldValuesListResponse_Schema,
    'creativeFieldsListResponses':
        creativeFieldsListResponse_Schema,
    'creativeGroups':
        creativeGroup_Schema,
    'creativeGroupAssignments':
        creativeGroupAssignment_Schema,
    'creativeGroupsListResponses':
        creativeGroupsListResponse_Schema,
    'creativeOptimizationConfigurations':
        creativeOptimizationConfiguration_Schema,
    'creativeRotations':
        creativeRotation_Schema,
    'creativesListResponses':
        creativesListResponse_Schema,
    'crossDimensionReachReportCompatibleFieldses':
        crossDimensionReachReportCompatibleFields_Schema,
    'customFloodlightVariables':
        customFloodlightVariable_Schema,
    'customRichMediaEventses':
        customRichMediaEvents_Schema,
    'customViewabilityMetrics':
        customViewabilityMetric_Schema,
    'customViewabilityMetricConfigurations':
        customViewabilityMetricConfiguration_Schema,
    'dateRanges':
        dateRange_Schema,
    'dayPartTargetings':
        dayPartTargeting_Schema,
    'deepLinks':
        deepLink_Schema,
    'defaultClickThroughEventTagPropertieses':
        defaultClickThroughEventTagProperties_Schema,
    'deliverySchedules':
        deliverySchedule_Schema,
    'dfpSettingses':
        dfpSettings_Schema,
    'dimensions':
        dimension_Schema,
    'dimensionFilters':
        dimensionFilter_Schema,
    'dimensionValues':
        dimensionValue_Schema,
    'dimensionValueLists':
        dimensionValueList_Schema,
    'dimensionValueRequests':
        dimensionValueRequest_Schema,
    'directorySites':
        directorySite_Schema,
    'directorySiteSettingses':
        directorySiteSettings_Schema,
    'directorySitesListResponses':
        directorySitesListResponse_Schema,
    'dynamicTargetingKeys':
        dynamicTargetingKey_Schema,
    'dynamicTargetingKeysListResponses':
        dynamicTargetingKeysListResponse_Schema,
    'encryptionInfos':
        encryptionInfo_Schema,
    'eventTags':
        eventTag_Schema,
    'eventTagOverrides':
        eventTagOverride_Schema,
    'eventTagsListResponses':
        eventTagsListResponse_Schema,
    'files':
        file_Schema,
    'fileLists':
        fileList_Schema,
    'flights':
        flight_Schema,
    'floodlightActivitiesGenerateTagResponses':
        floodlightActivitiesGenerateTagResponse_Schema,
    'floodlightActivitiesListResponses':
        floodlightActivitiesListResponse_Schema,
    'floodlightActivities':
        floodlightActivity_Schema,
    'floodlightActivityDynamicTags':
        floodlightActivityDynamicTag_Schema,
    'floodlightActivityGroups':
        floodlightActivityGroup_Schema,
    'floodlightActivityGroupsListResponses':
        floodlightActivityGroupsListResponse_Schema,
    'floodlightActivityPublisherDynamicTags':
        floodlightActivityPublisherDynamicTag_Schema,
    'floodlightConfigurations':
        floodlightConfiguration_Schema,
    'floodlightConfigurationsListResponses':
        floodlightConfigurationsListResponse_Schema,
    'floodlightReportCompatibleFieldses':
        floodlightReportCompatibleFields_Schema,
    'frequencyCaps':
        frequencyCap_Schema,
    'fsCommands':
        fsCommand_Schema,
    'geoTargetings':
        geoTargeting_Schema,
    'inventoryItems':
        inventoryItem_Schema,
    'inventoryItemsListResponses':
        inventoryItemsListResponse_Schema,
    'keyValueTargetingExpressions':
        keyValueTargetingExpression_Schema,
    'landingPages':
        landingPage_Schema,
    'languages':
        language_Schema,
    'languageTargetings':
        languageTargeting_Schema,
    'languagesListResponses':
        languagesListResponse_Schema,
    'lastModifiedInfos':
        lastModifiedInfo_Schema,
    'listPopulationClauses':
        listPopulationClause_Schema,
    'listPopulationRules':
        listPopulationRule_Schema,
    'listPopulationTerms':
        listPopulationTerm_Schema,
    'listTargetingExpressions':
        listTargetingExpression_Schema,
    'lookbackConfigurations':
        lookbackConfiguration_Schema,
    'metrics':
        metric_Schema,
    'metros':
        metro_Schema,
    'metrosListResponses':
        metrosListResponse_Schema,
    'mobileApps':
        mobileApp_Schema,
    'mobileAppsListResponses':
        mobileAppsListResponse_Schema,
    'mobileCarriers':
        mobileCarrier_Schema,
    'mobileCarriersListResponses':
        mobileCarriersListResponse_Schema,
    'objectFilters':
        objectFilter_Schema,
    'offsetPositions':
        offsetPosition_Schema,
    'omnitureSettingses':
        omnitureSettings_Schema,
    'operatingSystems':
        operatingSystem_Schema,
    'operatingSystemVersions':
        operatingSystemVersion_Schema,
    'operatingSystemVersionsListResponses':
        operatingSystemVersionsListResponse_Schema,
    'operatingSystemsListResponses':
        operatingSystemsListResponse_Schema,
    'optimizationActivities':
        optimizationActivity_Schema,
    'orders':
        order_Schema,
    'orderContacts':
        orderContact_Schema,
    'orderDocuments':
        orderDocument_Schema,
    'orderDocumentsListResponses':
        orderDocumentsListResponse_Schema,
    'ordersListResponses':
        ordersListResponse_Schema,
    'pathToConversionReportCompatibleFieldses':
        pathToConversionReportCompatibleFields_Schema,
    'placements':
        placement_Schema,
    'placementAssignments':
        placementAssignment_Schema,
    'placementGroups':
        placementGroup_Schema,
    'placementGroupsListResponses':
        placementGroupsListResponse_Schema,
    'placementStrategiesListResponses':
        placementStrategiesListResponse_Schema,
    'placementStrategies':
        placementStrategy_Schema,
    'placementTags':
        placementTag_Schema,
    'placementsGenerateTagsResponses':
        placementsGenerateTagsResponse_Schema,
    'placementsListResponses':
        placementsListResponse_Schema,
    'platformTypes':
        platformType_Schema,
    'platformTypesListResponses':
        platformTypesListResponse_Schema,
    'popupWindowPropertieses':
        popupWindowProperties_Schema,
    'postalCodes':
        postalCode_Schema,
    'postalCodesListResponses':
        postalCodesListResponse_Schema,
    'pricings':
        pricing_Schema,
    'pricingSchedules':
        pricingSchedule_Schema,
    'pricingSchedulePricingPeriods':
        pricingSchedulePricingPeriod_Schema,
    'projects':
        project_Schema,
    'projectsListResponses':
        projectsListResponse_Schema,
    'reachReportCompatibleFieldses':
        reachReportCompatibleFields_Schema,
    'recipients':
        recipient_Schema,
    'regions':
        region_Schema,
    'regionsListResponses':
        regionsListResponse_Schema,
    'remarketingLists':
        remarketingList_Schema,
    'remarketingListShares':
        remarketingListShare_Schema,
    'remarketingListsListResponses':
        remarketingListsListResponse_Schema,
    'reports':
        report_Schema,
    'reportCompatibleFieldses':
        reportCompatibleFields_Schema,
    'reportLists':
        reportList_Schema,
    'reportsConfigurations':
        reportsConfiguration_Schema,
    'richMediaExitOverrides':
        richMediaExitOverride_Schema,
    'rules':
        rule_Schema,
    'sites':
        site_Schema,
    'siteCompanionSettings':
        siteCompanionSetting_Schema,
    'siteContacts':
        siteContact_Schema,
    'siteSettingses':
        siteSettings_Schema,
    'siteSkippableSettings':
        siteSkippableSetting_Schema,
    'siteTranscodeSettings':
        siteTranscodeSetting_Schema,
    'siteVideoSettingses':
        siteVideoSettings_Schema,
    'sitesListResponses':
        sitesListResponse_Schema,
    'sizes':
        size_Schema,
    'sizesListResponses':
        sizesListResponse_Schema,
    'skippableSettings':
        skippableSetting_Schema,
    'sortedDimensions':
        sortedDimension_Schema,
    'subaccounts':
        subaccount_Schema,
    'subaccountsListResponses':
        subaccountsListResponse_Schema,
    'tagDatas':
        tagData_Schema,
    'tagSettings':
        tagSetting_Schema,
    'tagSettingses':
        tagSettings_Schema,
    'targetWindows':
        targetWindow_Schema,
    'targetableRemarketingLists':
        targetableRemarketingList_Schema,
    'targetableRemarketingListsListResponses':
        targetableRemarketingListsListResponse_Schema,
    'targetingTemplates':
        targetingTemplate_Schema,
    'targetingTemplatesListResponses':
        targetingTemplatesListResponse_Schema,
    'technologyTargetings':
        technologyTargeting_Schema,
    'thirdPartyAuthenticationTokens':
        thirdPartyAuthenticationToken_Schema,
    'thirdPartyTrackingUrls':
        thirdPartyTrackingUrl_Schema,
    'transcodeSettings':
        transcodeSetting_Schema,
    'universalAdIds':
        universalAdId_Schema,
    'userDefinedVariableConfigurations':
        userDefinedVariableConfiguration_Schema,
    'userProfiles':
        userProfile_Schema,
    'userProfileLists':
        userProfileList_Schema,
    'userRoles':
        userRole_Schema,
    'userRolePermissions':
        userRolePermission_Schema,
    'userRolePermissionGroups':
        userRolePermissionGroup_Schema,
    'userRolePermissionGroupsListResponses':
        userRolePermissionGroupsListResponse_Schema,
    'userRolePermissionsListResponses':
        userRolePermissionsListResponse_Schema,
    'userRolesListResponses':
        userRolesListResponse_Schema,
    'videoFormats':
        videoFormat_Schema,
    'videoFormatsListResponses':
        videoFormatsListResponse_Schema,
    'videoOffsets':
        videoOffset_Schema,
    'videoSettingses':
        videoSettings_Schema,
}
