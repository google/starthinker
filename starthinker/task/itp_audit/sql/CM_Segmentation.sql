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
  `{{project_id}}.{{dataset}}.z_CM_Browser_Report_Dirty` AS CM
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_CM_Site_Segmentation` AS SiteSeg
ON
  CM.Site_Dcm = SiteSeg.Site_Dcm
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_CM_Browser_lookup` AS CMBrowser
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