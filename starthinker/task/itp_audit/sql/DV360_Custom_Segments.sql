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
	`{{project_id}}.{{dataset}}.z_Dv360_Browser_Report_Dirty` as c
left join
	`{{project_id}}.{{dataset}}.z_Custom_Segments_Sheet` as s
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
