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
      `{dataset}.DV360_Browser_Report_Clean`
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
      Browser_detail as Browser_Detail,
      Environment,
      Device,
      CASE
        when Line_Item_Type = "TrueView" THEN "TrueView"
        ELSE Concat(Device,"-",Environment)
      END AS Device_Environment,
      Week,
      Month,
      Year,
      Week_start,
      Line_Item_Type,
      Segment1,
      Segment2,
      Segment3,
      SUM(Impressions) AS Impressions,
      SUM(Total_Conversions) AS Total_Conversions,
      SUM(Post_Click_Conversions) AS Post_Click_Conversions,
      SUM(Post_View_Conversions) AS Post_View_Conversions,
      SUM(Revenue_Adv_Currency) AS Revenue_Adv_Currency,
      SUM(Media_Cost_Advertiser_Currency) AS Media_Cost_Advertiser_Currency,
      SUM(CM_Post_View_Revenue) AS CM_Post_View_Revenue,
      SUM(CM_Post_Click_Revenue) AS CM_Post_Click_Revenue
    FROM
      `{dataset}.z_DV360_Browser_Report_Clean`
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
      Week,
      Month,
      Year,
      Line_Item_Type,
      Segment1,
      Segment2,
      Segment3,
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
        IF(UPPER(browser)='SAFARI', SUM(Impressions), 0) AS safari_imps,
        Line_Item_Type,
        Advertiser,
        Advertiser_ID,
        Campaign,
        Insertion_Order,
        Device_Environment,
        Week_start
      FROM `{dataset}.DV3_Browser`
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
      SUM(sbt.imps) AS impressions,
      SUM(sbt.safari_imps) AS safari_impressions,
      sbt.Line_Item_Type as Line_Item_Type,
      sbt.browser as Browser,
      sbt.Advertiser as Advertiser,
      sbt.Advertiser_ID as Advertiser_ID,
      sbt.Campaign as Campaign,
      sbt.Insertion_Order as Insertion_Order,
      sbt.Device_Environment as Device_Environment,
      sbt.Week_start as Week_start
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
      Env.Environment_clean AS Environment,
      Dev.Device_Type AS Device_Type,
      Dev.Device AS Device,
      seg.Segment1 AS Segment1,
      seg.Segment2 AS Segment2,
      seg.Segment3 AS Segment3,
      DV3_reporting.Week,
      CAST(PARSE_DATE('%Y/%m/%d', SPLIT(DV3_reporting.Week,'-')[OFFSET(0)]) AS DATE) AS Week_start,
      DV3_reporting.Month,
      DV3_reporting.Year,
      DV3_reporting.Line_Item_Type,
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
      `{dataset}.z_Dv360_Browser_Report_Dirty` AS DV3_reporting
    LEFT JOIN
      `{dataset}.z_Browser` AS Bro
    ON
      DV3_reporting.Browser = Bro.Browser_Platform
    LEFT JOIN
      `{dataset}.z_Environment` AS Env
    ON
      DV3_reporting.Environment = Env.Environment
    LEFT JOIN
      `{dataset}.z_Device_Type` AS Dev
    ON
      DV3_reporting.Device_Type = Dev.Device_Type
    LEFT JOIN
      `{dataset}.z_Custom_Segments` AS seg
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
      seg.Segment3
  """

  cm_floodlight_join = """
    SELECT
      Flood.Floodlight_Attribution_Type AS Floodlight_Attribution_Type,
      Att.Attribution_Type AS Attribution_Type,
      CMBrowser.Browser_Platform AS Browser_Platform,
      CMBrowser.Browser_Platform_detail AS Browser_Platform_detail,
      CMBrowser.Browser_Platform_clean AS Browser_Platform_clean,
      SUM(Total_Conversions) AS Total_Conversions,
      SUM(Click_Through_Conversions) AS Click_Through_Conversions,
      SUM(View_Through_Conversions) AS View_Through_Conversions
    FROM
      `{dataset}.z_Floodlight_CM_Report` AS Flood
    JOIN
      `{dataset}.z_Floodlight_Attribution` AS Att
    ON
      Flood.Floodlight_Attribution_Type = Att.Floodlight_Attribution_Type
    LEFT JOIN
      `{dataset}.z_CM_Browser_lookup` AS CMBrowser
    ON
      Flood.Browser_Platform = CMBrowser.Browser_Platform
    GROUP BY
      Flood.Floodlight_Attribution_Type,
      Att.Attribution_Type,
      Browser_Platform,
      Browser_Platform_detail,
      Browser_Platform_clean
  """

  cm_floodlight_multichart = """
    WITH
    attrtype_browser_total AS
    (
      SELECT
        IFNULL(att.Attribution_Type, '[missing]') as attribution_type,
        IFNULL(cm_br.Browser_Platform_clean, '[missing]') as browser_platform,
        SUM(fl.Total_Conversions) as convs
      FROM `{dataset}.z_CM_Floodlight` fl
      LEFT OUTER JOIN `{dataset}.z_Floodlight_Attribution` AS att USING(Floodlight_Attribution_Type)
      LEFT OUTER JOIN `{dataset}.z_CM_Browser_lookup` AS cm_br USING(Browser_Platform_clean)
      WHERE cm_br.Browser_Platform_clean IN ('Chrome', 'Safari', 'FF', 'MSFT')
      GROUP BY 1, 2
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
      SAFE_DIVIDE(SUM(abt.convs), ANY_VALUE(gt.convs)) share_of_floodlight_conversions
    FROM attrtype_browser_total abt
    CROSS JOIN grand_total gt
    GROUP BY 1
    ORDER BY 4 DESC
  """

  cm_segmentation = """
    SELECT
      CONCAT(CM.Advertiser," - ",CAST(CM.Advertiser_Id AS STRING)) AS Advertiser,
      CONCAT(CM.Campaign," - ",CAST(CM.Campaign_Id AS STRING)) AS Campaign,
      CM.Site_Dcm,
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
      `{dataset}.z_CM_Browser_Report_Dirty` AS CM
    LEFT JOIN
      `{dataset}.z_CM_Site_Segmentation` AS SiteSeg
    ON
      CM.Site_Dcm = SiteSeg.Site_Dcm
    LEFT JOIN
      `{dataset}.z_CM_Browser_lookup` AS CMBrowser
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
    r.Site_Dcm,
    Sum(r.Impressions) AS Impressions,
    s.Site_Type
    FROM `{dataset}.z_CM_Browser_Report_Dirty` as r
    left join `{dataset}.z_CM_Site_Segmentation_Sheet` as s
    on r.Site_Dcm = s.Site_Dcm
    Group By
    Site_Dcm,
    Site_Type
    Order By
    Impressions desc
  """

  dv360_custom_segments = """
    SELECT DISTINCT
      c.Advertiser,
      c.Advertiser_Id,
      c.Campaign,
      c.Campaign_Id,
      c.Insertion_Order,
      c.Insertion_Order_Id,
      c.Line_Item,
      c.Line_Item_Id,
      c.Line_Item_Type,
      sum(c.Impressions),
      s.Segment1,
      s.Segment2,
      s.Segment3
    from
      `{dataset}.z_Dv360_Browser_Report_Dirty` as c
    left join
      `{dataset}.z_Custom_Segments_Sheet` as s
    on
      c.Line_Item_Id = s.Line_Item_Id
    where
      c.Line_Item_Type != "TrueView"
    Group By
      c.Advertiser,
      c.Advertiser_Id,
      c.Campaign,
      c.Campaign_Id,
      c.Insertion_Order,
      c.Insertion_Order_Id,
      c.Line_Item,
      c.Line_Item_Id,
      c.Line_Item_Type,
      s.Segment1,
      s.Segment2,
      s.Segment3
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
        WHEN Browser_detail="Safari" THEN "Safari 12+13"
        WHEN Browser_detail="Safari 12" THEN "Safari 12+13"
        WHEN Browser_detail="Safari 11" THEN "Safari 11"
      ELSE
      "Other Safari"
      END
        AS Browser_Rollup,
        SUM(Impressions) AS Impressions
      FROM
        `{dataset}.z_DV360_Browser_Report_Clean`
      WHERE
        Browser = 'Safari'
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
      `{dataset}.SDF_campaign` AS C
    LEFT JOIN
      `{dataset}.SDF_insertion_order` AS IO
    ON
      C.Campaign_Id = IO.Campaign_Id
    LEFT JOIN
      `{dataset}.SDF_line_item` AS LI
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
