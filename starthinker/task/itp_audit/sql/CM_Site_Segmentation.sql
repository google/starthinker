SELECT
r.Site_Dcm,
Sum(r.Impressions) AS Impressions,
s.Site_Type
FROM `{{project_id}}.{{dataset}}.z_CM_Browser_Report_Dirty` as r
left join `{{project_id}}.{{dataset}}.z_CM_Site_Segmentation_Sheet` as s
on r.Site_Dcm = s.Site_Dcm
Group By
Site_Dcm,
Site_Type
Order By
Impressions desc