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
      Segment1,
      Segment2,
      Segment3,
      SegmentAutoGen,
      Anonymous_Inventory_Modeling,

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
      Segment1,
      Segment2,
      Segment3,
      SegmentAutoGen,
      Anonymous_Inventory_Modeling,
      Week_start
  """

  browser_share_multichart = """
    WITH
    filtered AS
    (
      SELECT
        segment1,
        segment2,
        segment3,
        browser,
        sum(Impressions) AS imps,
        IF(UPPER(browser)='SAFARI/IOS', SUM(Impressions), 0) AS safari_imps,
        Line_Item_Type,
        Advertiser,
        Advertiser_ID,
        Campaign,
        Insertion_Order,
        Device_Environment,
        Week_start
      FROM `{{dataset}}.DV3_Browser`
      GROUP BY
        segment1,
        segment2,
        segment3,
        browser,
        Line_Item_Type,
        Advertiser,
        Advertiser_ID,
        Campaign,
        Insertion_Order,
        Device_Environment,
        Week_start
    ),

    subtotals AS
    (
      SELECT
        1 AS segment_number,
        segment1 AS segment,
        browser,
        SUM(imps) AS imps,
        SUM(safari_imps) AS safari_imps,
        Line_Item_Type,
        Advertiser,
        Advertiser_ID,
        Campaign,
        Insertion_Order,
        Device_Environment,
        Week_start
      FROM filtered
      WHERE segment1 IS NOT NULL
      GROUP BY 1, 2, 3, Line_Item_Type, Advertiser, Advertiser_ID, Campaign,Insertion_Order,Device_Environment, Week_start
      UNION ALL
      SELECT
        2 AS segment_number,
        segment2 AS segment,
        browser,
        SUM(imps) AS segment_browser_imps,
        SUM(safari_imps) AS safari_imps,
        Line_Item_Type,
        Advertiser,
        Advertiser_ID,
        Campaign,
        Insertion_Order,
        Device_Environment,
        Week_start
      FROM filtered
      WHERE Segment2 IS NOT NULL
      GROUP BY 1, 2, 3, Line_Item_Type, Advertiser, Advertiser_ID, Campaign,Insertion_Order,Device_Environment, Week_start
      UNION ALL
      SELECT
        3 AS segment_number,
        segment3 AS segment,
        browser,
        SUM(imps) AS segment_browser_imps,
        SUM(safari_imps) AS safari_imps,
        Line_Item_Type,
        Advertiser,
        Advertiser_ID,
        Campaign,
        Insertion_Order,
        Device_Environment,
        Week_start
      FROM filtered
      WHERE Segment3 IS NOT NULL
      GROUP BY 1, 2, 3, Line_Item_Type, Advertiser, Advertiser_ID, Campaign,Insertion_Order,Device_Environment,Week_start
    ),


    grand_total AS
    (
      SELECT
        segment_number,
        SUM(imps) AS imps
      FROM subtotals
      GROUP BY 1
    )

    SELECT
      segment_number,
      segment,
      sbt.Line_Item_Type as Line_Item_Type,
      sbt.browser as Browser,
      sbt.Advertiser as Advertiser,
      sbt.Advertiser_ID as Advertiser_ID,
      sbt.Campaign as Campaign,
      sbt.Insertion_Order as Insertion_Order,
      sbt.Device_Environment as Device_Environment,
      sbt.Week_start as Week_start,
      Sum(sbt.imps) as Impressions,
      Sum(case when Browser = "Chrome/Android" then sbt.imps else 0 end) as Chrome_Impressions,
      Sum(case when Browser = "Safari/iOS" then sbt.imps else 0 end) as Safari_Impressions,
      Sum(case when Browser = "IE/Edge" then sbt.imps else 0 end) as IE_Impressions,
      Sum(case when Browser = "Firefox" then sbt.imps else 0 end) as Firefox_Impressions,
      Sum(case when Browser = "TrueView" then sbt.imps else 0 end) as TrueView_Impressions,
      Sum(case when Browser = "Other" then sbt.imps else 0 end) as Other_Impressions,
      Sum(case when Browser is null then sbt.imps else 0 end) as Null_Impressions,
      SUM(sbt.safari_imps) AS safari_impressions2
    FROM `subtotals` sbt
    LEFT OUTER JOIN `grand_total` AS gt USING (segment_number)
    GROUP BY 1, 2, Line_Item_Type, Browser, Advertiser, Advertiser_ID, Campaign,Insertion_Order,Device_Environment,Week_start
    ORDER BY 1, 2
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
      seg.Segment1 AS Segment1,
      seg.Segment2 AS Segment2,
      seg.Segment3 AS Segment3,
      seg.SegmentAutoGen as SegmentAutoGen,
      DV3_reporting.Anonymous_Inventory_Modeling as Anonymous_Inventory_Modeling,
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
    LEFT JOIN
      `{{dataset}}.z_Custom_Segments` AS seg
    ON
      DV3_reporting.Line_Item_Id = seg.Line_Item_Id
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
      Week_start,
      seg.Segment1,
      seg.Segment2,
      seg.Segment3,
      seg.SegmentAutoGen,
      DV3_reporting.Anonymous_Inventory_Modeling
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

  dv360_custom_segments = """
    with sheet_update as
    (
      select
        seg.Advertiser as Advertiser,
        seg.Advertiser_Id as Advertiser_Id,
        seg.Campaign as Campaign,
        seg.Campaign_Id as Campaign_Id,
        seg.Insertion_Order as Insertion_Order,
        seg.Insertion_Order_Id as Insertion_Order_Id,
        seg.Line_Item as Line_Item,
        seg.Line_Item_Id as Line_Item_Id,
        case
          when seg.Line_Item_Type = "YouTube & partners" then "TrueView"
          else seg.Line_Item_Type
        end as Line_Item_Type,
        sum(b.Impressions) as Impressions,
        case
          when
            sdf.Audience_Targeting_Similar_Audiences = "True" then "Similar Audience"
          when
            sdf.Combined_Audience_Targeting is not null then "Combo Audience"
          when
            sdf.Audience_Targeting_Include is not null then "1/3P Audience"
          when sdf.Affinity_In_Market_Targeting_Include is not null
            or sdf.Custom_List_Targeting is not null
            then "Google Audience"
          when
            sdf.Site_Targeting_Include is not null
            or sdf.App_Targeting_Include is not null
            or sdf.App_Collection_Targeting_Include is not null
            or sdf.Category_Targeting_Include is not null
            or sdf.Keyword_Targeting_Include is not null
            or sdf.Channel_Targeting_Include is not null
            then "Contextual"
          when
            sdf.Demographic_Targeting_Gender is not null
            or sdf.Demographic_Targeting_Age is not null
            or sdf.Demographic_Targeting_Household_Income is not null
            or sdf.Demographic_Targeting_Parental_Status is not null
            then "Demographic"
          when
            sdf.Geography_Targeting_Include is not null
            or sdf.Geography_Regional_Location_List_Targeting_Include is not null
            then "Geography"
          when
            sdf.Daypart_Targeting is not null
            or sdf.Daypart_Targeting_Time_Zone is not null
            or sdf.Environment_Targeting is not null
            or sdf.Viewability_Targeting_Active_View is not null
            then "OpenRTB"
          else "Archived"
        end as SegmentAutoGen,
        seg.Segment1 as Segment1,
        seg.Segment2 as Segment2,
        seg.Segment3 as Segment3
      from `{{dataset}}.z_Custom_Segments_Sheet` as seg
      left join
        `{{dataset}}.z_Dv360_Browser_Report_Dirty` as b
      on seg.Line_Item_Id = b.Line_Item_Id
      left join
        `{{dataset}}.SDF_LineItems` as sdf
      on seg.Line_Item_Id = sdf.Line_Item_Id
      Group By
      Advertiser,
      Advertiser_Id,
      Campaign,
      Campaign_Id,
      Insertion_Order,
      Insertion_Order_Id,
      Line_Item,
      Line_Item_Id,
      Line_Item_Type,
      SegmentAutoGen,
      Segment1,
      Segment2,
      Segment3
    ),



    new_report_fields as
    (
      select
        b.Advertiser as Advertiser,
        b.Advertiser_Id as Advertiser_Id,
        b.Campaign as Campaign,
        b.Campaign_Id as Campaign_Id,
        b.Insertion_Order as Insertion_Order,
        b.Insertion_Order_Id as Insertion_Order_Id,
        b.Line_Item as Line_Item,
        b.Line_Item_Id as Line_Item_Id,
        case
          when
            li.Audience_Targeting_Similar_Audiences = "True" then "Similar Audience"
          when b.Line_Item_Type = "YouTube & partners" then "TrueView"
          else b.Line_Item_Type
        end as Line_Item_Type,
        sum(b.Impressions) as Impressions,
        case
          when
            li.Audience_Targeting_Include is not null then "1/3P Audience"
          when li.Affinity_In_Market_Targeting_Include is not null
            or li.Custom_List_Targeting is not null
            then "Google Audience"
          when
            li.Site_Targeting_Include is not null
            or li.App_Targeting_Include is not null
            or li.App_Collection_Targeting_Include is not null
            or li.Category_Targeting_Include is not null
            or li.Keyword_Targeting_Include is not null
            or li.Channel_Targeting_Include is not null
            then "Contextual"
          when
            li.Demographic_Targeting_Gender is not null
            or li.Demographic_Targeting_Age is not null
            or li.Demographic_Targeting_Household_Income is not null
            or li.Demographic_Targeting_Parental_Status is not null
            then "Demographic"
          when
            li.Geography_Targeting_Include is not null
            or li.Geography_Regional_Location_List_Targeting_Include is not null
            then "Geography"
          when
            li.Daypart_Targeting is not null
            or li.Daypart_Targeting_Time_Zone is not null
            or li.Environment_Targeting is not null
            or li.Viewability_Targeting_Active_View is not null
            then "OpenRTB"
          else "Archived"
        end as SegmentAutoGen,
        cast(null as String) as Segment1,
        cast(null as String) as Segment2,
        cast(null as String) as Segment3
      from
        `{{dataset}}.z_Dv360_Browser_Report_Dirty` as b
      left join
        `{{dataset}}.SDF_LineItems` as li
      on
        b.Line_Item_Id = li.Line_Item_Id
      left join
        `{{dataset}}.SDF_InsertionOrders` as io
      on
        b.Insertion_Order_Id = io.Io_Id
      left join
        `{{dataset}}.SDF_Campaigns` as c
      on
        b.Campaign_Id = c.Campaign_Id
      left join
        `{{dataset}}.z_Custom_Segments_Sheet` as seg
      on
        seg.Line_Item_Id = b.Line_Item_Id
      where
        seg.Line_Item_Id is null
      Group By
      Advertiser,
      Advertiser_Id,
      Campaign,
      Campaign_Id,
      Insertion_Order,
      Insertion_Order_Id,
      Line_Item,
      Line_Item_Id,
      Line_Item_Type,
      SegmentAutoGen,
      Segment1,
      Segment2,
      Segment3
    )


    select * from sheet_update
    union all
    select * from new_report_fields
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

  sdf_feature_flags = """
    SELECT
      c.Advertiser_Id as Advertiser_Id,
      c.Name as Campaign,
      c.Campaign_Id as Campaign_Id,
      io.Name as Insertion_Order,
      io.Io_Id as Insertion_Order_Id,
      li.Name as Line_Item,
      li.Line_Item_Id as Line_Item_Id,
      CASE
        When li.Audience_Targeting_Include is Null
          Then FALSE
        ELSE TRUE
      END as Audience_Targeting_Include,
      CASE
        When li.Audience_Targeting_Exclude is Null
          Then FALSE
        ELSE TRUE
      END as Audience_Targeting_Exclude,
      CASE
        when io.Browser_Targeting_Include is null then FALSE
        else TRUE
      END as Io_Browser_Targeting_Include,
      CASE
        when io.Browser_Targeting_Exclude is null then FALSE
        else TRUE
      END as Io_Browser_Targeting_Exclude,
      CASE
        when '3' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '3' in UNNEST(SPLIT(io.Browser_Targeting_Exclude, ';')) then FALSE
        else null
      end as Io_Chrome_Browser_Targeting_Include,
      CASE
        when '6' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '7' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '10' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '17' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '18' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '19' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '20' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '22' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '23' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '24' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '25' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '26' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '27' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        when '28' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        else FALSE
      end as Io_Safari_Browser_Targeting_Include,
      CASE
        when '2' in UNNEST(SPLIT(io.Browser_Targeting_Include, ';')) then TRUE
        else FALSE
      end as Io_FF_Browser_Targeting_Include,
      CASE
        when li.Browser_Targeting_Include is null then FALSE
        else TRUE
      END as Li_Browser_Targeting_Include,
      CASE
        when li.Browser_Targeting_Exclude is null then FALSE
        else TRUE
      END as Li_Browser_Targeting_Exclude,
      CASE
        when '3' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        else FALSE
      end as Li_Chrome_Browser_Targeting_Include,
      CASE
        when '6' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '7' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '10' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '17' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '18' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '19' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '20' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '22' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '23' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '24' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '25' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '26' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '27' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        when '28' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        else FALSE
      end as Li_Safari_Browser_Targeting_Include,
      CASE
        when '2' in UNNEST(SPLIT(li.Browser_Targeting_Include, ';')) then TRUE
        else FALSE
      end as Li_FF_Browser_Targeting_Include,
      io.Environment_Targeting as Io_Environment_Targeting,
      li.Environment_Targeting as Li_Environment_Targeting,
      io.Device_Targeting_Include as Io_Device_Targeting_Include,
      io.Device_Targeting_Exclude as Io_Device_Targeting_Exclude,
      li.Device_Targeting_Include as Li_Device_Targeting_Include,
      li.Device_Targeting_Exclude as Li_Device_Targeting_Exclude,
      CASE
        When li.Affinity_In_Market_Targeting_Include is Null
          Then FALSE
        ELSE TRUE
      END as Google_Audience_Targeting_Include,
      CASE
        When li.Affinity_In_Market_Targeting_Exclude is Null
          Then FALSE
        ELSE TRUE
      END as Google_Audience_Targeting_Exclude,
      CASE
        When li.Geography_Targeting_Include is Null and li.Geography_Regional_Location_List_Targeting_Include is Null
          Then FALSE
        ELSE TRUE
      END as Geography_Targeting_Include,
      CASE
        When li.Geography_Targeting_Exclude is Null and li.Geography_Regional_Location_List_Targeting_Exclude is Null
          Then FALSE
        ELSE TRUE
      END as Geography_Targeting_Exclude,
      CASE
        When li.Channel_Targeting_Include is Null
          and li.Site_Targeting_Include is Null
          and li.App_Targeting_Include is Null
          and li.App_Collection_Targeting_Include is Null
          and li.Category_Targeting_Include is Null
          and li.Keyword_Targeting_Include is Null
          Then FALSE
        ELSE TRUE
      END as Contextual_Targeting_Include,
      CASE
        When li.Channel_Targeting_Exclude is Null
          and li.Site_Targeting_Exclude is Null
          and li.App_Targeting_Exclude is Null
          and li.App_Collection_Targeting_Exclude is Null
          and li.Category_Targeting_Exclude is Null
          and li.Keyword_Targeting_Exclude is Null
          and li.Keyword_List_Targeting_Exclude is Null
          Then FALSE
        ELSE TRUE
      END as Contextual_Targeting_Exclude,
      li.Type as Line_Item_Type,
      li.Bid_Strategy_Type as Bid_Strategy_Type,
      li.Bid_Strategy_Unit as Bid_Strategy_Unit,
      li.Trueview_Bid_Strategy_Type as Trueview_Bid_Strategy_Type,
      li.Budget_Type as Budget_Type,
      li.Conversion_Counting_Type as Conversion_Counting_Type,
      io.Frequency_Enabled as Io_Frequency_Management,
      li.Frequency_Enabled as Li_Frequency_Management
    FROM
      `{{dataset}}.SDF_LineItems` as li
    LEFT JOIN
      `{{dataset}}.SDF_InsertionOrders` as io
    ON
      io.Io_Id = li.Io_Id
    LEFT join
      `{{dataset}}.SDF_Campaigns` as c
    on
      c.Campaign_Id = io.Campaign_Id
  """

  sdf_join = """
    SELECT
      C.Campaign_Id as Campaign_Id,
      C.Advertiser_Id as Advertiser_Id,
      C.Name as Campaign_Name,
      IO.Io_Id as IO_Id,
      IO.Name as IO_Name,
      IO.Io_Type as IO_Type,
      IO.Pacing as IO_Pacing,
      IO.Performance_Goal_Type as IO_Performance_Goal_Type,
      IO.Performance_Goal_Value as IO_Performance_Goal_Value,
      IO.Budget_Type as IO_Budget_Type,
      IO.Budget_Segments as IO_Budget_Segments,
      IO.Auto_Budget_Allocation as IO_Auto_Budget_Allocation,
      LI.Line_Item_Id as LI_Id,
      LI.Type as LI_Type,
      LI.Subtype as LI_Subtype,
      LI.Name as LI_Name,
      LI.Budget_Type as LI_Budget_Type,
      LI.Budget_Amount as LI_Budget_Amount,
      LI.Pacing as LI_Pacing,
      LI.Pacing_Rate as LI_Pacing_Rate,
      LI.Bid_Strategy_Type as LI_Bid_Strategy_Type,
      LI.Bid_Strategy_Do_Not_Exceed as LI_Bid_Strategy_Do_Not_Exceed,
      LI.Geography_Targeting_Include as LI_Geography_Targeting_Include,
      LI.Geography_Targeting_Exclude as LI_Geography_Targeting_Exclude,
      LI.Device_Targeting_Include as LI_Device_Targeting_Include,
      LI.Device_Targeting_Exclude as LI_Device_Targeting_Exclude,
      LI.Browser_Targeting_Include as LI_Browser_Targeting_Include,
      LI.Browser_Targeting_Exclude as LI_Browser_Targeting_Exclude,

      LI.Third_Party_Verification_Services as LI_Third_Party_Verification_Services,
      LI.Third_Party_Verification_Labels as LI_Third_Party_Verification_Labels,
      LI.Channel_Targeting_Include as LI_Channel_Targeting_Include,
      LI.Channel_Targeting_Exclude as LI_Channel_Targeting_Exclude,
      LI.Site_Targeting_Include as LI_Site_Targeting_Include,
      LI.Site_Targeting_Exclude as LI_Site_Targeting_Exclude,
      LI.App_Targeting_Include as LI_App_Targeting_Include,
      LI.App_Targeting_Exclude as LI_App_Targeting_Exclude,
      LI.App_Collection_Targeting_Include as LI_App_Collection_Targeting_Include,
      LI.App_Collection_Targeting_Exclude as LI_App_Collection_Targeting_Exclude,
      LI.Category_Targeting_Include as LI_Category_Targeting_Include,
      LI.Category_Targeting_Exclude as LI_Category_Targeting_Exclude,
      LI.Keyword_Targeting_Include as LI_Keyword_Targeting_Include,
      LI.Keyword_Targeting_Exclude as LI_Keyword_Targeting_Exclude,
      LI.Keyword_List_Targeting_Exclude as LI_Keyword_List_Targeting_Exclude,
      LI.Audience_Targeting_Similar_Audiences as LI_Audience_Targeting_Similar_Audiences,
      LI.Audience_Targeting_Include as LI_Audience_Targeting_Include,
      LI.Audience_Targeting_Exclude as LI_Audience_Targeting_Exclude,
      LI.Affinity_In_Market_Targeting_Include as LI_Affinity_In_Market_Targeting_Include,
      LI.Affinity_In_Market_Targeting_Exclude as LI_Affinity_In_Market_Targeting_Exclude,
      LI.Custom_List_Targeting as LI_Custom_List_Targeting,
      LI.Daypart_Targeting as LI_Daypart_Targeting,
      LI.Daypart_Targeting_Time_Zone as LI_Daypart_Targeting_Time_Zone,
      LI.Environment_Targeting as LI_Environment_Targeting,
      LI.Demographic_Targeting_Gender as LI_Demographic_Targeting_Gender,
      LI.Demographic_Targeting_Age as LI_Demographic_Targeting_Age,
      LI.Demographic_Targeting_Household_Income as LI_Demographic_Targeting_Household_Income,
      LI.Demographic_Targeting_Parental_Status as LI_Demographic_Targeting_Parental_Status

      FROM
        `{{dataset}}.SDF_campaign` AS C
      LEFT JOIN
        `{{dataset}}.SDF_insertion_order` AS IO
      ON
        C.Campaign_Id = IO.Campaign_Id
      LEFT JOIN
        `{{dataset}}.SDF_line_item` AS LI
      ON
        IO.Io_Id = LI.Io_Id
      GROUP BY
      Campaign_Id,
      Advertiser_Id,
      Campaign_Name,
      IO_Id,
      IO_Name,
      IO_Type,
      IO_Pacing,
      IO_Performance_Goal_Type,
      IO_Performance_Goal_Value,
      IO_Budget_Type,
      IO_Budget_Segments,
      IO_Auto_Budget_Allocation,
      LI_Id,
      LI_Type,
      LI_Subtype,
      LI_Name,
      LI_Budget_Type,
      LI_Budget_Amount,
      LI_Pacing,
      LI_Pacing_Rate,
      LI_Bid_Strategy_Type,
      LI_Bid_Strategy_Do_Not_Exceed,
      LI_Geography_Targeting_Include,
      LI_Geography_Targeting_Exclude,
      LI_Device_Targeting_Include,
      LI_Device_Targeting_Exclude,
      LI_Browser_Targeting_Include,
      LI_Browser_Targeting_Exclude,
      LI_Third_Party_Verification_Services,
      LI_Third_Party_Verification_Labels,
      LI_Channel_Targeting_Include,
      LI_Channel_Targeting_Exclude,
      LI_Site_Targeting_Include,
      LI_Site_Targeting_Exclude,
      LI_App_Targeting_Include,
      LI_App_Targeting_Exclude,
      LI_App_Collection_Targeting_Include,
      LI_App_Collection_Targeting_Exclude,
      LI_Category_Targeting_Include,
      LI_Category_Targeting_Exclude,
      LI_Keyword_Targeting_Include,
      LI_Keyword_Targeting_Exclude,
      LI_Keyword_List_Targeting_Exclude,
      LI_Audience_Targeting_Similar_Audiences,
      LI_Audience_Targeting_Include,
      LI_Audience_Targeting_Exclude,
      LI_Affinity_In_Market_Targeting_Include,
      LI_Affinity_In_Market_Targeting_Exclude,
      LI_Custom_List_Targeting,
      LI_Daypart_Targeting,
      LI_Daypart_Targeting_Time_Zone,
      LI_Environment_Targeting,
      LI_Demographic_Targeting_Gender,
      LI_Demographic_Targeting_Age,
      LI_Demographic_Targeting_Household_Income,
      LI_Demographic_Targeting_Parental_Status
  """

  sdf_li_scores = """
    SELECT
      f.Advertiser_Id,
      f.Campaign,
      f.Campaign_Id,
      f.Insertion_Order,
      f.Insertion_Order_Id,
      f.Line_Item,
      f.Line_Item_Id,
      f.Line_Item_Type,
      f.Audience_Targeting_Include,
      f.Google_Audience_Targeting_Include,
      f.Contextual_Targeting_Include,
      f.Conversion_Bid_Optimization,
      f.Browser_Targeting_Include,
      f.Chrome_Browser_Targeting_Include,
      f.Safari_Browser_Targeting_Include,
      f.FF_Browser_Targeting_Include,
      f.View_Through_Enabled,
      s.Whole_Attribution_Score as Attribution_Score,
      s.Safari_Attribution_Score,
      s.Safari_Reach_Score,
      s.Comment,
      Sum(clean.Impressions) as Impressions
    FROM
      `{{dataset}}.z_sdf_scoring` as f
    left join
      `{{dataset}}.z_dv360_scoring_matrix` as s
      on
        f.Audience_Targeting_Include = s.Audience_Targeting_Include
        and f.Google_Audience_Targeting_Include = s.Google_Audience_Include
        and f.Contextual_Targeting_Include = s.Contextual_Targeting_Include
        and f.Conversion_Bid_Optimization = s.Conversion_Bid_Optimization
        and f.Browser_Targeting_Include = s.Browser_Targeting_Include
        and f.Chrome_Browser_Targeting_Include = s.Chrome_Browser_Targeting_Include
        and f.Safari_Browser_Targeting_Include = s.Safari_Browser_Targeting_Include
        and f.FF_Browser_Targeting_Include = s.FF_Browser_Targeting_Include
        and f.View_Through_Enabled = s.View_Through_Enabled
    left join
      `{{dataset}}.z_DV360_Browser_Report_Clean` as clean
    on
      clean.Line_Item_Id = f.Line_Item_Id
    group by
      Advertiser_Id,
      Campaign,
      Campaign_Id,
      Insertion_Order,
      Insertion_Order_Id,
      Line_Item,
      Line_Item_Id,
      Line_Item_Type,
      Audience_Targeting_Include,
      Google_Audience_Targeting_Include,
      Contextual_Targeting_Include,
      Conversion_Bid_Optimization,
      Browser_Targeting_Include,
      Chrome_Browser_Targeting_Include,
      Safari_Browser_Targeting_Include,
      FF_Browser_Targeting_Include,
      View_Through_Enabled,
      Attribution_Score,
      Safari_Attribution_Score,
      Safari_Reach_Score,
      Comment
  """
  sdf_scoring = """
    SELECT
      Advertiser_Id,
      Campaign,
      Campaign_Id,
      Insertion_Order,
      Insertion_Order_Id,
      Line_Item,
      Line_Item_Id,
      Line_Item_Type,
      Audience_Targeting_Include,
      Google_Audience_Targeting_Include,
      Contextual_Targeting_Include,
      case
        when Bid_Strategy_Type in ("Beat","Minimize","Maximize") and Bid_Strategy_Unit in ("CPA","INCREMENTAL_CONVERSIONS") THEN True
        ELSE False
      end
      as Conversion_Bid_Optimization,
      Li_Browser_Targeting_Include as Browser_Targeting_Include,
      Conversion_Counting_Type != "Count post-click" as View_Through_Enabled,
      Li_Chrome_Browser_Targeting_Include as Chrome_Browser_Targeting_Include,
      Li_Safari_Browser_Targeting_Include as Safari_Browser_Targeting_Include,
      Li_FF_Browser_Targeting_Include as FF_Browser_Targeting_Include,
    FROM
      `{{dataset}}.z_sdf_feature_flags`
  """
