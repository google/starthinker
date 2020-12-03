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
  `{{project_id}}.{{dataset}}.z_Dv360_Browser_Report_Dirty` AS DV3_reporting
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_Browser` AS Bro
ON
  DV3_reporting.Browser = Bro.Browser_Platform
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_Environment` AS Env
ON
  DV3_reporting.Environment = Env.Environment
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_Device_Type` AS Dev
ON
  DV3_reporting.Device_Type = Dev.Device_Type
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_Custom_Segments` AS seg
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