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
  FROM `{{project_id}}.{{dataset}}.DV3_Browser`
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