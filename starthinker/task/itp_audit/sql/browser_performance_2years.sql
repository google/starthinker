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
  `{{project_id}}.{{dataset}}.z_DV360_Browser_Report_Clean`
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
