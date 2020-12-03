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
  `{{project_id}}.{{dataset}}.z_Floodlight_CM_Report` AS Flood
JOIN
  `{{project_id}}.{{dataset}}.z_Floodlight_Attribution` AS Att
ON
  Flood.Floodlight_Attribution_Type = Att.Floodlight_Attribution_Type
LEFT JOIN
  `{{project_id}}.{{dataset}}.z_CM_Browser_lookup` AS CMBrowser
ON
  Flood.Browser_Platform = CMBrowser.Browser_Platform
GROUP BY
  Flood.Floodlight_Attribution_Type,
  Att.Attribution_Type,
  Browser_Platform,
  Browser_Platform_detail,
  Browser_Platform_clean