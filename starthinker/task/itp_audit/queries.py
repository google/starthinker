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

class Queries:
  browser_env_90 = """
    SELECT
      Partner,
      Advertiser,
      Advertiser_Id,
      Insertion_Order,
      Insertion_Order_Id,
      Campaign,
      Campaign_Id,
      CASE
        when Line_Item_Type = "TrueView" THEN "TrueView"
        when Line_Item_Type != "TrueView" and Browser_Detail = "Other" THEN "Other"
        ELSE Browser
      END AS Browser,
      Environment,
      Device,
      CASE
        when Line_Item_Type = "TrueView" THEN "TrueView"
        ELSE Concat(Device,"-",Environment)
      END AS Device_Environment,
      Line_item_type,
      Week_start,
      SUM(Impressions) AS Impressions
    FROM
      `{{dataset}}.DV360_Browser_Report_Clean`
    WHERE
      DATE_DIFF(CURRENT_DATE(), Week_start, WEEK) < 12
    GROUP BY
      Partner,
      Advertiser,
      Advertiser_Id,
      Insertion_Order,
      Insertion_Order_Id,
      Campaign,
      Campaign_Id,
      Browser,
      Environment,
      Device,
      Device_Environment,
      Week_start,
      Line_item_type
  """

  browser_2_year = """
    SELECT
      Partner,
      Advertiser,
      Advertiser_ID,
      Campaign,
      Insertion_Order,
      CASE
        when Line_Item_Type = "TrueView" THEN "TrueView"
        when Line_Item_Type != "TrueView" and Browser_Detail = "Other" THEN "Other"
        ELSE Browser
      END AS Browser,

      CASE
        WHEN Browser_detail="Safari" THEN "Safari 12+13"
        WHEN Browser_detail="Safari 12" THEN "Safari 12+13"
        WHEN Browser_detail="Safari 11" THEN "Safari 11"
        when Browser_detail like '%Safari%' Then "Other Safari"
        else Browser_detail
      END AS Browser_Rollup,
      Browser_detail as Browser_Detail,
      Environment,
      Device,
      CASE
        when Line_Item_Type = "TrueView" THEN "TrueView"
        ELSE Concat(Device,"-",Environment)
      END AS Device_Environment,
      Operating_System,
      Week,
      Month,
      Year,
      Week_start,
      Line_Item_Type,
      Sum(Impressions) as Impressions,
      Sum(case when Browser = "Chrome/Android" then Impressions else 0 end) as Chrome_Impressions,
      Sum(case when Browser = "Safari/iOS" then Impressions else 0 end) as Safari_Impressions,
      Sum(case when Browser = "IE/Edge" then Impressions else 0 end) as IE_Impressions,
      Sum(case when Browser = "Firefox" then Impressions else 0 end) as Firefox_Impressions,
      Sum(case when Browser = "TrueView" then Impressions else 0 end) as TrueView_Impressions,
      Sum(case when Browser = "Other" then Impressions else 0 end) as Other_Impressions,
      Sum(case when Browser is null then Impressions else 0 end) as Null_Impressions,

      Sum(Total_Conversions) as Total_Conversions,
      Sum(case when Browser = "Chrome/Android" then Total_Conversions else 0 end) as Chrome_Total_Conversions,
      Sum(case when Browser = "Safari/iOS" then Total_Conversions else 0 end) as Safari_Total_Conversions,
      Sum(case when Browser = "IE/Edge" then Total_Conversions else 0 end) as IE_Total_Conversions,
      Sum(case when Browser = "Firefox" then Total_Conversions else 0 end) as Firefox_Total_Conversions,
      Sum(case when Browser = "TrueView" then Total_Conversions else 0 end) as TrueView_Total_Conversions,
      Sum(case when Browser = "Other" then Total_Conversions else 0 end) as Other_Total_Conversions,
      Sum(case when Browser is null then Total_Conversions else 0 end) as Null_Total_Conversions,

      Sum(Post_Click_Conversions) as Post_Click_Conversions,
      Sum(case when Browser = "Chrome/Android" then Post_Click_Conversions else 0 end) as Chrome_Post_Click_Conversions,
      Sum(case when Browser = "Safari/iOS" then Post_Click_Conversions else 0 end) as Safari_Post_Click_Conversions,
      Sum(case when Browser = "IE/Edge" then Post_Click_Conversions else 0 end) as IE_Post_Click_Conversions,
      Sum(case when Browser = "Firefox" then Post_Click_Conversions else 0 end) as Firefox_Post_Click_Conversions,
      Sum(case when Browser = "TrueView" then Post_Click_Conversions else 0 end) as TrueView_Post_Click_Conversions,
      Sum(case when Browser = "Other" then Post_Click_Conversions else 0 end) as Other_Post_Click_Conversions,
      Sum(case when Browser is null then Post_Click_Conversions else 0 end) as Null_Post_Click_Conversions,

      Sum(Post_View_Conversions) as Post_View_Conversions,
      Sum(case when Browser = "Chrome/Android" then Post_View_Conversions else 0 end) as Chrome_Post_View_Conversions,
      Sum(case when Browser = "Safari/iOS" then Post_View_Conversions else 0 end) as Safari_Post_View_Conversions,
      Sum(case when Browser = "IE/Edge" then Post_View_Conversions else 0 end) as IE_Post_View_Conversions,
      Sum(case when Browser = "Firefox" then Post_View_Conversions else 0 end) as Firefox_Post_View_Conversions,
      Sum(case when Browser = "TrueView" then Post_View_Conversions else 0 end) as TrueView_Post_View_Conversions,
      Sum(case when Browser = "Other" then Post_View_Conversions else 0 end) as Other_Post_View_Conversions,
      Sum(case when Browser is null then Post_View_Conversions else 0 end) as Null_Post_View_Conversions,

      Sum(Revenue_Adv_Currency) as Revenue_Adv_Currency,
      Sum(case when Browser = "Chrome/Android" then Revenue_Adv_Currency else 0 end) as Chrome_Revenue_Adv_Currency,
      Sum(case when Browser = "Safari/iOS" then Revenue_Adv_Currency else 0 end) as Safari_Revenue_Adv_Currency,
      Sum(case when Browser = "IE/Edge" then Revenue_Adv_Currency else 0 end) as IE_Revenue_Adv_Currency,
      Sum(case when Browser = "Firefox" then Revenue_Adv_Currency else 0 end) as Firefox_Revenue_Adv_Currency,
      Sum(case when Browser = "TrueView" then Revenue_Adv_Currency else 0 end) as TrueView_Revenue_Adv_Currency,
      Sum(case when Browser = "Other" then Revenue_Adv_Currency else 0 end) as Other_Revenue_Adv_Currency,
      Sum(case when Browser is null then Revenue_Adv_Currency else 0 end) as Null_Revenue_Adv_Currency,

      Sum(Media_Cost_Advertiser_Currency) as Media_Cost_Advertiser_Currency,
      Sum(case when Browser = "Chrome/Android" then Media_Cost_Advertiser_Currency else 0 end) as Chrome_Media_Cost_Advertiser_Currency,
      Sum(case when Browser = "Safari/iOS" then Media_Cost_Advertiser_Currency else 0 end) as Safari_Media_Cost_Advertiser_Currency,
      Sum(case when Browser = "IE/Edge" then Media_Cost_Advertiser_Currency else 0 end) as IE_Media_Cost_Advertiser_Currency,
      Sum(case when Browser = "Firefox" then Media_Cost_Advertiser_Currency else 0 end) as Firefox_Media_Cost_Advertiser_Currency,
      Sum(case when Browser = "TrueView" then Media_Cost_Advertiser_Currency else 0 end) as TrueView_Media_Cost_Advertiser_Currency,
      Sum(case when Browser = "Other" then Media_Cost_Advertiser_Currency else 0 end) as Other_Media_Cost_Advertiser_Currency,
      Sum(case when Browser is null then Media_Cost_Advertiser_Currency else 0 end) as Null_Media_Cost_Advertiser_Currency,

      Sum(CM_Post_View_Revenue) as CM_Post_View_Revenue,
      Sum(case when Browser = "Chrome/Android" then CM_Post_View_Revenue else 0 end) as Chrome_CM_Post_View_Revenue,
      Sum(case when Browser = "Safari/iOS" then CM_Post_View_Revenue else 0 end) as Safari_CM_Post_View_Revenue,
      Sum(case when Browser = "IE/Edge" then CM_Post_View_Revenue else 0 end) as IE_CM_Post_View_Revenue,
      Sum(case when Browser = "Firefox" then CM_Post_View_Revenue else 0 end) as Firefox_CM_Post_View_Revenue,
      Sum(case when Browser = "TrueView" then CM_Post_View_Revenue else 0 end) as TrueView_CM_Post_View_Revenue,
      Sum(case when Browser = "Other" then CM_Post_View_Revenue else 0 end) as Other_CM_Post_View_Revenue,
      Sum(case when Browser is null then CM_Post_View_Revenue else 0 end) as Null_CM_Post_View_Revenue,

      Sum(CM_Post_Click_Revenue) as CM_Post_Click_Revenue,
      Sum(case when Browser = "Chrome/Android" then CM_Post_Click_Revenue else 0 end) as Chrome_CM_Post_Click_Revenue,
      Sum(case when Browser = "Safari/iOS" then CM_Post_Click_Revenue else 0 end) as Safari_CM_Post_Click_Revenue,
      Sum(case when Browser = "IE/Edge" then CM_Post_Click_Revenue else 0 end) as IE_CM_Post_Click_Revenue,
      Sum(case when Browser = "Firefox" then CM_Post_Click_Revenue else 0 end) as Firefox_CM_Post_Click_Revenue,
      Sum(case when Browser = "TrueView" then CM_Post_Click_Revenue else 0 end) as TrueView_CM_Post_Click_Revenue,
      Sum(case when Browser = "Other" then CM_Post_Click_Revenue else 0 end) as Other_CM_Post_Click_Revenue,
      Sum(case when Browser is null then CM_Post_Click_Revenue else 0 end) as Null_CM_Post_Click_Revenue
    FROM
      `{{dataset}}.z_DV360_Browser_Report_Clean`
    GROUP BY
      Partner,
      Advertiser,
      Advertiser_ID,
      Campaign,
      Insertion_Order,
      Browser,
      Browser_detail,
      Environment,
      Device,
      Device_Environment,
      Operating_System,
      Week,
      Month,
      Year,
      Line_Item_Type,
      Week_start
  """

  clean_browser_report = """
    SELECT
      DV3_reporting.Partner AS Partner_clean,
      DV3_reporting.Partner_Id,
      CONCAT(DV3_reporting.Partner," - ",CAST(DV3_reporting.Partner_Id AS STRING)) AS Partner,
      DV3_reporting.Advertiser AS Advertiser_clean,
      DV3_reporting.Advertiser_Id,
      CONCAT(DV3_reporting.Advertiser," - ",CAST(DV3_reporting.Advertiser_Id AS STRING)) AS Advertiser,
      DV3_reporting.Advertiser_Currency,
      DV3_reporting.Insertion_Order AS Insertion_Order_clean,
      DV3_reporting.Insertion_Order_Id,
      CONCAT(DV3_reporting.Insertion_Order," - ",CAST(DV3_reporting.Insertion_Order_Id AS STRING)) AS Insertion_Order,
      DV3_reporting.Campaign AS Campaign_clean,
      DV3_reporting.Campaign_Id,
      CONCAT(DV3_reporting.Campaign," - ",CAST(DV3_reporting.Campaign_Id AS STRING)) AS Campaign,
      DV3_reporting.Line_Item AS Line_Item_clean,
      DV3_reporting.Line_Item_Id,
      CONCAT(DV3_reporting.Line_Item," - ",CAST(DV3_reporting.Line_Item AS STRING)) AS Line_Item,
      DV3_reporting.Browser AS Browser_Detail,
      Bro.Browser_Platform_clean AS Browser,
      DV3_reporting.Environment AS Environment_Detail,
      DV3_reporting.Operating_System as Operating_System,
      Env.Environment_clean AS Environment,
      Dev.Device_Type AS Device_Type,
      Dev.Device AS Device,
      DV3_reporting.Week,
      CAST(PARSE_DATE('%Y/%m/%d', SPLIT(DV3_reporting.Week,'-')[OFFSET(0)]) AS DATE) AS Week_start,
      DV3_reporting.Month,
      DV3_reporting.Year,
      case
        when DV3_reporting.Line_Item_Type = "YouTube & partners" then "TrueView"
        else DV3_reporting.Line_Item_Type
      end as Line_Item_Type,
      SUM(DV3_reporting.Impressions) AS Impressions,
      SUM(DV3_reporting.Clicks) AS Clicks,
      SUM(DV3_reporting.Total_Conversions) AS Total_Conversions,
      SUM(DV3_reporting.Post_Click_Conversions) AS Post_Click_Conversions,
      SUM(DV3_reporting.Post_View_Conversions) AS Post_View_Conversions,
      SUM(DV3_reporting.CM_Post_View_Revenue) AS CM_Post_View_Revenue,
      SUM(DV3_reporting.CM_Post_Click_Revenue) AS CM_Post_Click_Revenue,
      SUM(DV3_reporting.Revenue_Adv_Currency) AS Revenue_Adv_Currency,
      SUM(DV3_reporting.Media_Cost_Advertiser_Currency) AS Media_Cost_Advertiser_Currency,
      SAFE_DIVIDE(SUM(DV3_reporting.Revenue_Adv_Currency), SAFE_DIVIDE(SUM(DV3_reporting.Impressions), 1000)) AS CPM,
      SAFE_DIVIDE(SUM(DV3_reporting.Revenue_Adv_Currency), SUM(DV3_reporting.Total_Conversions)) AS CPA,
      SAFE_DIVIDE(SUM(DV3_reporting.CM_Post_View_Revenue + DV3_reporting.CM_Post_Click_Revenue), SUM(DV3_reporting.Revenue_Adv_Currency)) AS ROAS_Total,
      SAFE_DIVIDE(SUM(DV3_reporting.CM_Post_View_Revenue), SUM(DV3_reporting.Revenue_Adv_Currency)) AS ROAS_View,
      SAFE_DIVIDE(SUM(DV3_reporting.CM_Post_Click_Revenue), SUM(DV3_reporting.Revenue_Adv_Currency)) AS ROAS_Click
    FROM
      `{{dataset}}.z_Dv360_Browser_Report_Dirty` AS DV3_reporting
    LEFT JOIN
      `{{dataset}}.z_Browser` AS Bro
    ON
      DV3_reporting.Browser = Bro.Browser_Platform
    LEFT JOIN
      `{{dataset}}.z_Environment` AS Env
    ON
      DV3_reporting.Environment = Env.Environment
    LEFT JOIN
      `{{dataset}}.z_Device_Type` AS Dev
    ON
      DV3_reporting.Device_Type = Dev.Device_Type
    GROUP BY
      DV3_reporting.Partner,
      DV3_reporting.Partner_Id,
      DV3_reporting.Advertiser,
      DV3_reporting.Advertiser_Id,
      DV3_reporting.Advertiser_Currency,
      DV3_reporting.Insertion_Order,
      DV3_reporting.Insertion_Order_Id,
      DV3_reporting.Campaign,
      DV3_reporting.Campaign_Id,
      DV3_reporting.Line_Item,
      DV3_reporting.Line_Item_Id,
      DV3_reporting.Browser,
      Bro.Browser_Platform_clean,
      DV3_reporting.Environment,
      DV3_reporting.Operating_System,
      Env.Environment_clean,
      DV3_reporting.Week,
      DV3_reporting.Month,
      DV3_reporting.Year,
      DV3_reporting.Line_Item_Type,
      Dev.Device,
      Device_Type,
      Week_start
  """

  cm_floodlight_join = """
    SELECT
      Flood.Floodlight_Attribution_Type AS Floodlight_Attribution_Type,
      Flood.Floodlight_Configuration as Floodlight_Configuration,
      Att.Attribution_Type AS Attribution_Type,
      CMBrowser.Browser_Platform AS Browser_Platform,
      CMBrowser.Browser_Platform_detail AS Browser_Platform_detail,
      CMBrowser.Browser_Platform_clean AS Browser_Platform_clean,
      SUM(Total_Conversions) AS Total_Conversions,
      SUM(Click_Through_Conversions) AS Click_Through_Conversions,
      SUM(View_Through_Conversions) AS View_Through_Conversions
    FROM
      `{{dataset}}.z_Floodlight_CM_Report` AS Flood
    JOIN
      `{{dataset}}.z_Floodlight_Attribution` AS Att
    ON
      Flood.Floodlight_Attribution_Type = Att.Floodlight_Attribution_Type
    LEFT JOIN
      `{{dataset}}.z_CM_Browser_lookup` AS CMBrowser
    ON
      Flood.Browser_Platform = CMBrowser.Browser_Platform
    GROUP BY
      Flood.Floodlight_Attribution_Type,
      Flood.Floodlight_Configuration,
      Att.Attribution_Type,
      CMBrowser.Browser_Platform,
      CMBrowser.Browser_Platform_detail,
      CMBrowser.Browser_Platform_clean
  """

  cm_floodlight_multichart = """
    WITH
    attrtype_browser_total AS
    (
      SELECT
        IFNULL(att.Attribution_Type, '[missing]') as attribution_type,
        IFNULL(cm_br.Browser_Platform_clean, '[missing]') as browser_platform,
        SUM(fl.Total_Conversions) as convs,
        fl.Floodlight_Configuration as Floodlight_Configuration
      FROM `{{dataset}}.z_CM_Floodlight` fl
      LEFT OUTER JOIN `{{dataset}}.z_Floodlight_Attribution` AS att USING(Floodlight_Attribution_Type)
      LEFT OUTER JOIN `{{dataset}}.z_CM_Browser_lookup` AS cm_br USING(Browser_Platform_clean)
      WHERE cm_br.Browser_Platform_clean IN ('Chrome/Android', 'Safari/iOS', 'Firefox', 'IE/Edge')
      GROUP BY 1, 2,4
    ),


    grand_total AS
    (
      SELECT SUM(convs) AS convs
      FROM attrtype_browser_total
    )


    SELECT
      browser_platform,
      SAFE_DIVIDE(SUM(IF(UPPER(attribution_type)='ATTRIBUTED', abt.convs, 0)),
                  SUM(abt.convs)) AS percent_attributed,
      SAFE_DIVIDE(SUM(IF(UPPER(attribution_type)='UNATTRIBUTED', abt.convs, 0)),
                  SUM(abt.convs)) AS percent_unattributed,
      SAFE_DIVIDE(SUM(abt.convs), ANY_VALUE(gt.convs)) as share_of_floodlight_impressions,
      SUM(IF(UPPER(attribution_type)='ATTRIBUTED', abt.convs, 0)) AS attributed_conv,
      SUM(IF(UPPER(attribution_type)='UNATTRIBUTED', abt.convs, 0)) AS unattributed_conv,
      sum(abt.convs) as total_convs,
      max(gt.convs) as grand_total_convs,
      abt.Floodlight_Configuration as Floodlight_Configuration
    FROM attrtype_browser_total abt
    CROSS JOIN grand_total gt
    GROUP BY 1,9
    ORDER BY 9 DESC
  """

  cm_segmentation = """
    SELECT
      CONCAT(CM.Advertiser," - ",CAST(CM.Advertiser_Id AS STRING)) AS Advertiser,
      CONCAT(CM.Campaign," - ",CAST(CM.Campaign_Id AS STRING)) AS Campaign,
      CM.Site_Cm360 as Site_Dcm,
      CM.Browser_Platform AS Browser_Platform,
      CMBrowser.Browser_Platform_detail AS Browser_Platform_detail,
      CMBrowser.Browser_Platform_clean AS Browser_Platform_clean,
      Platform_Type,
      SiteSeg.Site_Type AS Site_Type,
      CAST(Week AS DATE) AS Week,
      SUM(CM.Impressions) AS Impressions,
      SUM(Clicks) AS Clicks,
      SUM(Total_Conversions) AS Total_Conversions,
      SUM(Click_Through_Conversions) AS Click_Through_Conversions,
      SUM(View_Through_Conversions) AS View_Through_Conversions
    FROM
      `{{dataset}}.z_CM_Browser_Report_Dirty` AS CM
    LEFT JOIN
      `{{dataset}}.z_CM_Site_Segmentation` AS SiteSeg
    ON
      CM.Site_Cm360 = SiteSeg.Site_Dcm
    LEFT JOIN
      `{{dataset}}.z_CM_Browser_lookup` AS CMBrowser
    ON
      CM.Browser_Platform = CMBrowser.Browser_Platform
    GROUP BY
      Advertiser,
      Campaign,
      Site_Dcm,
      Browser_Platform,
      Browser_Platform_detail,
      Browser_Platform_clean,
      Platform_Type,
      Site_Type,
      Week
  """

  cm_site_segmentation = """
    SELECT
    r.Site_Cm360 as Site_Dcm,
    Sum(r.Impressions) AS Impressions,
    s.Site_Type
    FROM `{{dataset}}.z_CM_Browser_Report_Dirty` as r
    left join `{{dataset}}.z_CM_Site_Segmentation_Sheet` as s
    on r.Site_Cm360 = s.Site_Dcm
    Group By
    Site_Dcm,
    Site_Type
    Order By
    Impressions desc
  """

  safari_distribution_90days = """
    SELECT
      Partner,
      Advertiser,
      Campaign,
      Environment,
      Device,
      CASE
        when Line_Item_Type = "TrueView" THEN "TrueView"
        ELSE Concat(Device,"-",Environment)
      END AS Device_Environment,
      Week_start,
      Line_item_type,
      CASE
        WHEN Operating_System like "iOS 14" THEN "Safari 14"
        WHEN Browser_detail="Safari" THEN "Safari 12+13"
        WHEN Browser_detail="Safari 12" THEN "Safari 12+13"
        WHEN Browser_detail="Safari 11" THEN "Safari 11"
      ELSE
      "Other Safari"
    END
      AS Browser_Rollup,
      SUM(Impressions) AS Impressions
    FROM
      `{{dataset}}.z_DV360_Browser_Report_Clean`
    WHERE
      Browser = 'Safari/iOS'
      AND
      DATE_DIFF(CURRENT_DATE(),Week_start,WEEK)<12
    GROUP BY
      Browser_Rollup,
      Partner,
      Advertiser,
      Campaign,
      Environment,
      Device,
      Device_Environment,
      Line_item_type,
      Week_start
    ORDER BY
      Impressions DESC
  """
