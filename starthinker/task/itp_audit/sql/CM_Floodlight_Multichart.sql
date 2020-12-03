WITH
attrtype_browser_total AS
(
  SELECT
    IFNULL(att.Attribution_Type, '[missing]') as attribution_type,
    IFNULL(cm_br.Browser_Platform_clean, '[missing]') as browser_platform,
    SUM(fl.Total_Conversions) as convs
  FROM `{{project_id}}.{{dataset}}.z_CM_Floodlight` fl
  LEFT OUTER JOIN `{{project_id}}.{{dataset}}.z_Floodlight_Attribution` AS att USING(Floodlight_Attribution_Type)
  LEFT OUTER JOIN `{{project_id}}.{{dataset}}.z_CM_Browser_lookup` AS cm_br USING(Browser_Platform_clean)
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