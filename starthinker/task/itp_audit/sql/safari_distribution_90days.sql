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
  `{{project_id}}.{{dataset}}.z_DV360_Browser_Report_Clean`
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