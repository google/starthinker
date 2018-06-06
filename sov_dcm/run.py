###########################################################################
#
#  Copyright 2017 Google Inc.
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


from util.project import project 
from util.dcm import parse_account
from util.bigquery import query_to_table, query_to_rows
from util.sheets import sheets_tab_copy, sheets_read


SOV_TABLE = '[plx.google:starthinker.xfa_reporting.SOV_DCM.all]'

SOV_QUERY = '''
SELECT 
  base_event_utc_event_date AS Report_Day,
  REGEXP_REPLACE(CAST(base_event_utc_event_date AS STRING), r'(\d\d\d\d)(\d\d)\d\d', r'\\1-\\2') AS Year_Month,
  "%(Advertiser_Type)s" AS Advertiser_Type,
  CASE
     WHEN device_platform_type == 30000 THEN 'Desktop'
     WHEN device_platform_type == 30001 THEN 'Mobile'
     WHEN device_platform_type == 30002 THEN 'Tablet'
     WHEN device_platform_type == 30003 THEN 'Feature Phone'
     WHEN device_platform_type == 30004 THEN 'Connected TV'
     ELSE 'Unknown'
  END AS Platform_Type,
  CASE
    WHEN ad_creative_type == 0 THEN 'Image'
    WHEN ad_creative_type == 3 THEN 'Internal Redirect'
    WHEN ad_creative_type == 5 THEN 'Tracking'
    WHEN ad_creative_type == 7 THEN 'Interstitial internal redirect' 
    WHEN ad_creative_type == 11 THEN 'Tracking Image'
    WHEN ad_creative_type == 12 THEN 'Tracking HTML'
    WHEN ad_creative_type == 29 THEN 'Streaming Real'
    WHEN ad_creative_type == 30 THEN 'Streaming Windows'
    WHEN ad_creative_type == 31 THEN 'Streaming Flash'
    WHEN ad_creative_type == 32 THEN 'In-Stream Tracking'
    WHEN ad_creative_type == 41 THEN 'Streaming Silverlight'  
    WHEN ad_creative_type == 46 THEN 'Flash in-page'
    WHEN ad_creative_type == 47 THEN 'In-Stream Video'
    WHEN ad_creative_type == 101 THEN 'HTML5 Banner'
    WHEN ad_creative_type == 104 THEN 'Video Redirect'
    WHEN ad_creative_type == 105 THEN 'In-Stream Audio'
    WHEN ad_creative_type == 1 THEN 'Display redirect'
    WHEN ad_creative_type == 2 THEN 'Custom display'
    WHEN ad_creative_type == 6 THEN 'Custom display interstitial'  
    WHEN ad_creative_type == 15 THEN 'Rich Media display banner' 
    WHEN ad_creative_type == 18 THEN 'Rich Media display banner with floating' 
    WHEN ad_creative_type == 19 THEN 'Rich Media IM expand' 
    WHEN ad_creative_type == 22 THEN 'Rich Media display expanding' 
    WHEN ad_creative_type == 23 THEN 'Rich Media mobile in-app'
    WHEN ad_creative_type == 24 THEN 'Rich Media display interstitial' 
    WHEN ad_creative_type == 27 THEN 'Rich Media display multi-floating interstitial' 
    WHEN ad_creative_type == 100 THEN 'Rich Media peel-down' 
    WHEN ad_creative_type == 50 THEN 'VPAID linear video'
    WHEN ad_creative_type == 51 THEN 'VPAID non-linear video'
    WHEN ad_creative_type == 102 THEN 'Display'
    WHEN ad_creative_type == 103 THEN 'Display image gallery'
    ELSE 'Unknown'
  END AS Creative_Type,
  geo_state AS State_Region,
  CASE
    WHEN geo_dma_id == 2 THEN 'Portland-Auburn ME'
    WHEN geo_dma_id == 3 THEN 'New York NY'
    WHEN geo_dma_id == 4 THEN 'Binghamton NY'
    WHEN geo_dma_id == 5 THEN 'Macon GA'
    WHEN geo_dma_id == 6 THEN 'Philadelphia PA'
    WHEN geo_dma_id == 7 THEN 'Detroit MI'
    WHEN geo_dma_id == 8 THEN 'Boston MA-Manchester NH'
    WHEN geo_dma_id == 9 THEN 'Savannah GA'
    WHEN geo_dma_id == 10 THEN 'Pittsburgh PA'
    WHEN geo_dma_id == 11 THEN 'Ft. Wayne IN'
    WHEN geo_dma_id == 12 THEN 'Cleveland-Akron (Canton) OH'
    WHEN geo_dma_id == 13 THEN 'Washington DC (Hagerstown MD)'
    WHEN geo_dma_id == 14 THEN 'Baltimore MD'
    WHEN geo_dma_id == 15 THEN 'Flint-Saginaw-Bay City MI'
    WHEN geo_dma_id == 16 THEN 'Buffalo NY'
    WHEN geo_dma_id == 17 THEN 'Cincinnati OH'
    WHEN geo_dma_id == 18 THEN 'Erie PA'
    WHEN geo_dma_id == 19 THEN 'Charlotte NC'
    WHEN geo_dma_id == 20 THEN 'Greensboro-High Point-Winston Salem NC'
    WHEN geo_dma_id == 21 THEN 'Charleston SC'
    WHEN geo_dma_id == 22 THEN 'Augusta GA'
    WHEN geo_dma_id == 23 THEN 'Providence RI-New Bedford MA'
    WHEN geo_dma_id == 24 THEN 'Columbus GA'
    WHEN geo_dma_id == 25 THEN 'Burlington VT-Plattsburgh NY'
    WHEN geo_dma_id == 26 THEN 'Atlanta GA'
    WHEN geo_dma_id == 27 THEN 'Albany GA'
    WHEN geo_dma_id == 28 THEN 'Utica NY'
    WHEN geo_dma_id == 29 THEN 'Indianapolis IN'
    WHEN geo_dma_id == 30 THEN 'Miami-Ft. Lauderdale FL'
    WHEN geo_dma_id == 31 THEN 'Louisville KY'
    WHEN geo_dma_id == 32 THEN 'Tallahassee FL-Thomasville GA'
    WHEN geo_dma_id == 33 THEN 'Tri-Cities TN-VA'
    WHEN geo_dma_id == 34 THEN 'Albany-Schenectady-Troy NY'
    WHEN geo_dma_id == 35 THEN 'Hartford & New Haven CT'
    WHEN geo_dma_id == 36 THEN 'Orlando-Daytona Beach-Melbourne FL'
    WHEN geo_dma_id == 37 THEN 'Columbus OH'
    WHEN geo_dma_id == 38 THEN 'Youngstown OH'
    WHEN geo_dma_id == 39 THEN 'Bangor ME'
    WHEN geo_dma_id == 40 THEN 'Rochester NY'
    WHEN geo_dma_id == 41 THEN 'Tampa-St. Petersburg (Sarasota) FL'
    WHEN geo_dma_id == 42 THEN 'Traverse City-Cadillac MI'
    WHEN geo_dma_id == 43 THEN 'Lexington KY'
    WHEN geo_dma_id == 44 THEN 'Dayton OH'
    WHEN geo_dma_id == 45 THEN 'Springfield-Holyoke MA'
    WHEN geo_dma_id == 46 THEN 'Norfolk-Portsmouth-Newport News VA'
    WHEN geo_dma_id == 47 THEN 'Greenville-New Bern-Washington NC'
    WHEN geo_dma_id == 48 THEN 'Columbia SC'
    WHEN geo_dma_id == 49 THEN 'Toledo OH'
    WHEN geo_dma_id == 50 THEN 'West Palm Beach-Ft. Pierce FL'
    WHEN geo_dma_id == 51 THEN 'Watertown NY'
    WHEN geo_dma_id == 52 THEN 'Wilmington NC'
    WHEN geo_dma_id == 53 THEN 'Lansing MI'
    WHEN geo_dma_id == 54 THEN 'Presque Isle ME'
    WHEN geo_dma_id == 55 THEN 'Marquette MI'
    WHEN geo_dma_id == 56 THEN 'Wheeling WV-Steubenville OH'
    WHEN geo_dma_id == 57 THEN 'Syracuse NY'
    WHEN geo_dma_id == 58 THEN 'Richmond-Petersburg VA'
    WHEN geo_dma_id == 59 THEN 'Knoxville TN'
    WHEN geo_dma_id == 60 THEN 'Lima OH'
    WHEN geo_dma_id == 61 THEN 'Bluefield-Beckley-Oak Hill WV'
    WHEN geo_dma_id == 62 THEN 'Raleigh-Durham (Fayetteville) NC'
    WHEN geo_dma_id == 63 THEN 'Jacksonville FL'
    WHEN geo_dma_id == 64 THEN 'Grand Rapids-Kalamazoo-Battle Creek MI'
    WHEN geo_dma_id == 65 THEN 'Charleston-Huntington WV'
    WHEN geo_dma_id == 66 THEN 'Elmira NY'
    WHEN geo_dma_id == 67 THEN 'Harrisburg-Lancaster-Lebanon-York PA'
    WHEN geo_dma_id == 68 THEN 'Greenville-Spartanburg SC-Asheville NC-Anderson SC'
    WHEN geo_dma_id == 69 THEN 'Harrisonburg VA'
    WHEN geo_dma_id == 70 THEN 'Florence-Myrtle Beach SC'
    WHEN geo_dma_id == 71 THEN 'Ft. Myers-Naples FL'
    WHEN geo_dma_id == 72 THEN 'Roanoke-Lynchburg VA'
    WHEN geo_dma_id == 73 THEN 'Johnstown-Altoona PA'
    WHEN geo_dma_id == 74 THEN 'Chattanooga TN'
    WHEN geo_dma_id == 75 THEN 'Salisbury MD'
    WHEN geo_dma_id == 76 THEN 'Wilkes Barre-Scranton PA'
    WHEN geo_dma_id == 77 THEN 'Terre Haute IN'
    WHEN geo_dma_id == 78 THEN 'Lafayette IN'
    WHEN geo_dma_id == 79 THEN 'Alpena MI'
    WHEN geo_dma_id == 80 THEN 'Charlottesville VA'
    WHEN geo_dma_id == 81 THEN 'South Bend-Elkhart IN'
    WHEN geo_dma_id == 82 THEN 'Gainesville FL'
    WHEN geo_dma_id == 83 THEN 'Zanesville OH'
    WHEN geo_dma_id == 84 THEN 'Parkersburg WV'
    WHEN geo_dma_id == 85 THEN 'Clarksburg-Weston WV'
    WHEN geo_dma_id == 86 THEN 'Corpus Christi TX'
    WHEN geo_dma_id == 87 THEN 'Chicago IL'
    WHEN geo_dma_id == 88 THEN 'Joplin MO-Pittsburg KS'
    WHEN geo_dma_id == 89 THEN 'Columbia-Jefferson City MO'
    WHEN geo_dma_id == 90 THEN 'Topeka KS'
    WHEN geo_dma_id == 91 THEN 'Dothan AL'
    WHEN geo_dma_id == 92 THEN 'St. Louis MO'
    WHEN geo_dma_id == 93 THEN 'Rockford IL'
    WHEN geo_dma_id == 94 THEN 'Rochester MN-Mason City IA-Austin MN'
    WHEN geo_dma_id == 95 THEN 'Shreveport LA'
    WHEN geo_dma_id == 96 THEN 'Minneapolis-St. Paul MN'
    WHEN geo_dma_id == 97 THEN 'Kansas City MO'
    WHEN geo_dma_id == 98 THEN 'Milwaukee WI'
    WHEN geo_dma_id == 99 THEN 'Houston TX'
    WHEN geo_dma_id == 100 THEN 'Springfield MO'
    WHEN geo_dma_id == 101 THEN 'New Orleans LA'
    WHEN geo_dma_id == 102 THEN 'Dallas-Ft. Worth TX'
    WHEN geo_dma_id == 103 THEN 'Sioux City IA'
    WHEN geo_dma_id == 104 THEN 'Waco-Temple-Bryan TX'
    WHEN geo_dma_id == 105 THEN 'Victoria TX'
    WHEN geo_dma_id == 106 THEN 'Wichita Falls TX & Lawton OK'
    WHEN geo_dma_id == 107 THEN 'Monroe LA-El Dorado AR'
    WHEN geo_dma_id == 108 THEN 'Birmingham AL'
    WHEN geo_dma_id == 109 THEN 'Ottumwa IA-Kirksville MO'
    WHEN geo_dma_id == 110 THEN 'Paducah KY-Cape Girardeau MO-Harrisburg-Mount Vernon IL'
    WHEN geo_dma_id == 111 THEN 'Odessa-Midland TX'
    WHEN geo_dma_id == 112 THEN 'Amarillo TX'
    WHEN geo_dma_id == 113 THEN 'Austin TX'
    WHEN geo_dma_id == 114 THEN 'Harlingen-Weslaco-Brownsville-McAllen TX'
    WHEN geo_dma_id == 115 THEN 'Cedar Rapids-Waterloo-Iowa City & Dubuque IA'
    WHEN geo_dma_id == 116 THEN 'St. Joseph MO'
    WHEN geo_dma_id == 117 THEN 'Jackson TN'
    WHEN geo_dma_id == 118 THEN 'Memphis TN'
    WHEN geo_dma_id == 119 THEN 'San Antonio TX'
    WHEN geo_dma_id == 120 THEN 'Lafayette LA'
    WHEN geo_dma_id == 121 THEN 'Lake Charles LA'
    WHEN geo_dma_id == 122 THEN 'Alexandria LA'
    WHEN geo_dma_id == 123 THEN 'Greenwood-Greenville MS'
    WHEN geo_dma_id == 124 THEN 'Champaign & Springfield-Decatur,IL'
    WHEN geo_dma_id == 125 THEN 'Evansville IN'
    WHEN geo_dma_id == 126 THEN 'Oklahoma City OK'
    WHEN geo_dma_id == 127 THEN 'Lubbock TX'
    WHEN geo_dma_id == 128 THEN 'Omaha NE'
    WHEN geo_dma_id == 129 THEN 'Panama City FL'
    WHEN geo_dma_id == 130 THEN 'Sherman TX-Ada OK'
    WHEN geo_dma_id == 131 THEN 'Green Bay-Appleton WI'
    WHEN geo_dma_id == 132 THEN 'Nashville TN'
    WHEN geo_dma_id == 133 THEN 'San Angelo TX'
    WHEN geo_dma_id == 134 THEN 'Abilene-Sweetwater TX'
    WHEN geo_dma_id == 135 THEN 'Madison WI'
    WHEN geo_dma_id == 136 THEN 'Ft. Smith-Fayetteville-Springdale-Rogers AR'
    WHEN geo_dma_id == 137 THEN 'Tulsa OK'
    WHEN geo_dma_id == 138 THEN 'Columbus-Tupelo-West Point MS'
    WHEN geo_dma_id == 139 THEN 'Peoria-Bloomington IL'
    WHEN geo_dma_id == 140 THEN 'Duluth MN-Superior WI'
    WHEN geo_dma_id == 141 THEN 'Wichita-Hutchinson KS'
    WHEN geo_dma_id == 142 THEN 'Des Moines-Ames IA'
    WHEN geo_dma_id == 143 THEN 'Davenport IA-Rock Island-Moline IL'
    WHEN geo_dma_id == 144 THEN 'Mobile AL-Pensacola (Ft. Walton Beach) FL'
    WHEN geo_dma_id == 145 THEN 'Minot-Bismarck-Dickinson(Williston) ND'
    WHEN geo_dma_id == 146 THEN 'Huntsville-Decatur (Florence) AL'
    WHEN geo_dma_id == 147 THEN 'Beaumont-Port Arthur TX'
    WHEN geo_dma_id == 148 THEN 'Little Rock-Pine Bluff AR'
    WHEN geo_dma_id == 149 THEN 'Montgomery (Selma) AL'
    WHEN geo_dma_id == 150 THEN 'La Crosse-Eau Claire WI'
    WHEN geo_dma_id == 151 THEN 'Wausau-Rhinelander WI'
    WHEN geo_dma_id == 152 THEN 'Tyler-Longview(Lufkin & Nacogdoches) TX'
    WHEN geo_dma_id == 153 THEN 'Hattiesburg-Laurel MS'
    WHEN geo_dma_id == 154 THEN 'Meridian MS'
    WHEN geo_dma_id == 155 THEN 'Baton Rouge LA'
    WHEN geo_dma_id == 156 THEN 'Quincy IL-Hannibal MO-Keokuk IA'
    WHEN geo_dma_id == 157 THEN 'Jackson MS'
    WHEN geo_dma_id == 158 THEN 'Lincoln & Hastings-Kearney NE'
    WHEN geo_dma_id == 159 THEN 'Fargo-Valley City ND'
    WHEN geo_dma_id == 160 THEN 'Sioux Falls(Mitchell) SD'
    WHEN geo_dma_id == 161 THEN 'Jonesboro AR'
    WHEN geo_dma_id == 162 THEN 'Bowling Green KY'
    WHEN geo_dma_id == 163 THEN 'Mankato MN'
    WHEN geo_dma_id == 164 THEN 'North Platte NE'
    WHEN geo_dma_id == 165 THEN 'Anchorage AK'
    WHEN geo_dma_id == 166 THEN 'Honolulu HI'
    WHEN geo_dma_id == 167 THEN 'Fairbanks AK'
    WHEN geo_dma_id == 168 THEN 'Biloxi-Gulfport MS'
    WHEN geo_dma_id == 169 THEN 'Juneau AK'
    WHEN geo_dma_id == 170 THEN 'Laredo TX'
    WHEN geo_dma_id == 171 THEN 'Denver CO'
    WHEN geo_dma_id == 172 THEN 'Colorado Springs-Pueblo CO'
    WHEN geo_dma_id == 173 THEN 'Phoenix AZ'
    WHEN geo_dma_id == 174 THEN 'Butte-Bozeman MT'
    WHEN geo_dma_id == 175 THEN 'Great Falls MT'
    WHEN geo_dma_id == 176 THEN 'Billings MT'
    WHEN geo_dma_id == 177 THEN 'Boise ID'
    WHEN geo_dma_id == 178 THEN 'Idaho Falls-Pocatello ID'
    WHEN geo_dma_id == 179 THEN 'Cheyenne WY-Scottsbluff NE'
    WHEN geo_dma_id == 180 THEN 'Twin Falls ID'
    WHEN geo_dma_id == 181 THEN 'Missoula MT'
    WHEN geo_dma_id == 182 THEN 'Rapid City SD'
    WHEN geo_dma_id == 183 THEN 'El Paso TX'
    WHEN geo_dma_id == 184 THEN 'Helena MT'
    WHEN geo_dma_id == 185 THEN 'Casper-Riverton WY'
    WHEN geo_dma_id == 186 THEN 'Salt Lake City UT'
    WHEN geo_dma_id == 187 THEN 'Yuma AZ-El Centro CA'
    WHEN geo_dma_id == 188 THEN 'Grand Junction-Montrose CO'
    WHEN geo_dma_id == 189 THEN 'Tucson (Sierra Vista) AZ'
    WHEN geo_dma_id == 190 THEN 'Albuquerque-Santa Fe NM'
    WHEN geo_dma_id == 191 THEN 'Glendive MT'
    WHEN geo_dma_id == 192 THEN 'Bakersfield CA'
    WHEN geo_dma_id == 193 THEN 'Eugene OR'
    WHEN geo_dma_id == 194 THEN 'Eureka CA'
    WHEN geo_dma_id == 195 THEN 'Los Angeles CA'
    WHEN geo_dma_id == 196 THEN 'Palm Springs CA'
    WHEN geo_dma_id == 197 THEN 'San Francisco-Oakland-San Jose CA'
    WHEN geo_dma_id == 198 THEN 'Yakima-Pasco-Richland-Kennewick WA'
    WHEN geo_dma_id == 199 THEN 'Reno NV'
    WHEN geo_dma_id == 200 THEN 'Medford-Klamath Falls OR'
    WHEN geo_dma_id == 201 THEN 'Seattle-Tacoma WA'
    WHEN geo_dma_id == 202 THEN 'Portland OR'
    WHEN geo_dma_id == 203 THEN 'Bend OR'
    WHEN geo_dma_id == 204 THEN 'San Diego CA'
    WHEN geo_dma_id == 205 THEN 'Monterey-Salinas CA'
    WHEN geo_dma_id == 206 THEN 'Las Vegas NV'
    WHEN geo_dma_id == 207 THEN 'Santa Barbara-Santa Maria-San Luis Obispo CA'
    WHEN geo_dma_id == 208 THEN 'Sacramento-Stockton-Modesto CA'
    WHEN geo_dma_id == 209 THEN 'Fresno-Visalia CA'
    WHEN geo_dma_id == 210 THEN 'Chico-Redding CA'
    WHEN geo_dma_id == 211 THEN 'Spokane WA'
    ELSE 'Unknown'
  END AS Designated_Market_Area,
  CASE
    WHEN geo_dma_id == 2 THEN 200500
    WHEN geo_dma_id == 3 THEN 200501
    WHEN geo_dma_id == 4 THEN 200502
    WHEN geo_dma_id == 5 THEN 200503
    WHEN geo_dma_id == 6 THEN 200504
    WHEN geo_dma_id == 7 THEN 200505
    WHEN geo_dma_id == 8 THEN 200506
    WHEN geo_dma_id == 9 THEN 200507
    WHEN geo_dma_id == 10 THEN 200508
    WHEN geo_dma_id == 11 THEN 200509
    WHEN geo_dma_id == 12 THEN 200510
    WHEN geo_dma_id == 13 THEN 200511
    WHEN geo_dma_id == 14 THEN 200512
    WHEN geo_dma_id == 15 THEN 200513
    WHEN geo_dma_id == 16 THEN 200514
    WHEN geo_dma_id == 17 THEN 200515
    WHEN geo_dma_id == 18 THEN 200516
    WHEN geo_dma_id == 19 THEN 200517
    WHEN geo_dma_id == 20 THEN 200518
    WHEN geo_dma_id == 21 THEN 200519
    WHEN geo_dma_id == 22 THEN 200520
    WHEN geo_dma_id == 23 THEN 200521
    WHEN geo_dma_id == 24 THEN 200522
    WHEN geo_dma_id == 25 THEN 200523
    WHEN geo_dma_id == 26 THEN 200524
    WHEN geo_dma_id == 27 THEN 200525
    WHEN geo_dma_id == 28 THEN 200526
    WHEN geo_dma_id == 29 THEN 200527
    WHEN geo_dma_id == 30 THEN 200528
    WHEN geo_dma_id == 31 THEN 200529
    WHEN geo_dma_id == 32 THEN 200530
    WHEN geo_dma_id == 33 THEN 200531
    WHEN geo_dma_id == 34 THEN 200532
    WHEN geo_dma_id == 35 THEN 200533
    WHEN geo_dma_id == 36 THEN 200534
    WHEN geo_dma_id == 37 THEN 200535
    WHEN geo_dma_id == 38 THEN 200536
    WHEN geo_dma_id == 39 THEN 200537
    WHEN geo_dma_id == 40 THEN 200538
    WHEN geo_dma_id == 41 THEN 200539
    WHEN geo_dma_id == 42 THEN 200540
    WHEN geo_dma_id == 43 THEN 200541
    WHEN geo_dma_id == 44 THEN 200542
    WHEN geo_dma_id == 45 THEN 200543
    WHEN geo_dma_id == 46 THEN 200544
    WHEN geo_dma_id == 47 THEN 200545
    WHEN geo_dma_id == 48 THEN 200546
    WHEN geo_dma_id == 49 THEN 200547
    WHEN geo_dma_id == 50 THEN 200548
    WHEN geo_dma_id == 51 THEN 200549
    WHEN geo_dma_id == 52 THEN 200550
    WHEN geo_dma_id == 53 THEN 200551
    WHEN geo_dma_id == 54 THEN 200552
    WHEN geo_dma_id == 55 THEN 200553
    WHEN geo_dma_id == 56 THEN 200554
    WHEN geo_dma_id == 57 THEN 200555
    WHEN geo_dma_id == 58 THEN 200556
    WHEN geo_dma_id == 59 THEN 200557
    WHEN geo_dma_id == 60 THEN 200558
    WHEN geo_dma_id == 61 THEN 200559
    WHEN geo_dma_id == 62 THEN 200560
    WHEN geo_dma_id == 63 THEN 200561
    WHEN geo_dma_id == 64 THEN 200563
    WHEN geo_dma_id == 65 THEN 200564
    WHEN geo_dma_id == 66 THEN 200565
    WHEN geo_dma_id == 67 THEN 200566
    WHEN geo_dma_id == 68 THEN 200567
    WHEN geo_dma_id == 69 THEN 200569
    WHEN geo_dma_id == 70 THEN 200570
    WHEN geo_dma_id == 71 THEN 200571
    WHEN geo_dma_id == 72 THEN 200573
    WHEN geo_dma_id == 73 THEN 200574
    WHEN geo_dma_id == 74 THEN 200575
    WHEN geo_dma_id == 75 THEN 200576
    WHEN geo_dma_id == 76 THEN 200577
    WHEN geo_dma_id == 77 THEN 200581
    WHEN geo_dma_id == 78 THEN 200582
    WHEN geo_dma_id == 79 THEN 200583
    WHEN geo_dma_id == 80 THEN 200584
    WHEN geo_dma_id == 81 THEN 200588
    WHEN geo_dma_id == 82 THEN 200592
    WHEN geo_dma_id == 83 THEN 200596
    WHEN geo_dma_id == 84 THEN 200597
    WHEN geo_dma_id == 85 THEN 200598
    WHEN geo_dma_id == 86 THEN 200600
    WHEN geo_dma_id == 87 THEN 200602
    WHEN geo_dma_id == 88 THEN 200603
    WHEN geo_dma_id == 89 THEN 200604
    WHEN geo_dma_id == 90 THEN 200605
    WHEN geo_dma_id == 91 THEN 200606
    WHEN geo_dma_id == 92 THEN 200609
    WHEN geo_dma_id == 93 THEN 200610
    WHEN geo_dma_id == 94 THEN 200611
    WHEN geo_dma_id == 95 THEN 200612
    WHEN geo_dma_id == 96 THEN 200613
    WHEN geo_dma_id == 97 THEN 200616
    WHEN geo_dma_id == 98 THEN 200617
    WHEN geo_dma_id == 99 THEN 200618
    WHEN geo_dma_id == 100 THEN 200619
    WHEN geo_dma_id == 101 THEN 200622
    WHEN geo_dma_id == 102 THEN 200623
    WHEN geo_dma_id == 103 THEN 200624
    WHEN geo_dma_id == 104 THEN 200625
    WHEN geo_dma_id == 105 THEN 200626
    WHEN geo_dma_id == 106 THEN 200627
    WHEN geo_dma_id == 107 THEN 200628
    WHEN geo_dma_id == 108 THEN 200630
    WHEN geo_dma_id == 109 THEN 200631
    WHEN geo_dma_id == 110 THEN 200632
    WHEN geo_dma_id == 111 THEN 200633
    WHEN geo_dma_id == 112 THEN 200634
    WHEN geo_dma_id == 113 THEN 200635
    WHEN geo_dma_id == 114 THEN 200636
    WHEN geo_dma_id == 115 THEN 200637
    WHEN geo_dma_id == 116 THEN 200638
    WHEN geo_dma_id == 117 THEN 200639
    WHEN geo_dma_id == 118 THEN 200640
    WHEN geo_dma_id == 119 THEN 200641
    WHEN geo_dma_id == 120 THEN 200642
    WHEN geo_dma_id == 121 THEN 200643
    WHEN geo_dma_id == 122 THEN 200644
    WHEN geo_dma_id == 123 THEN 200647
    WHEN geo_dma_id == 124 THEN 200648
    WHEN geo_dma_id == 125 THEN 200649
    WHEN geo_dma_id == 126 THEN 200650
    WHEN geo_dma_id == 127 THEN 200651
    WHEN geo_dma_id == 128 THEN 200652
    WHEN geo_dma_id == 129 THEN 200656
    WHEN geo_dma_id == 130 THEN 200657
    WHEN geo_dma_id == 131 THEN 200658
    WHEN geo_dma_id == 132 THEN 200659
    WHEN geo_dma_id == 133 THEN 200661
    WHEN geo_dma_id == 134 THEN 200662
    WHEN geo_dma_id == 135 THEN 200669
    WHEN geo_dma_id == 136 THEN 200670
    WHEN geo_dma_id == 137 THEN 200671
    WHEN geo_dma_id == 138 THEN 200673
    WHEN geo_dma_id == 139 THEN 200675
    WHEN geo_dma_id == 140 THEN 200676
    WHEN geo_dma_id == 141 THEN 200678
    WHEN geo_dma_id == 142 THEN 200679
    WHEN geo_dma_id == 143 THEN 200682
    WHEN geo_dma_id == 144 THEN 200686
    WHEN geo_dma_id == 145 THEN 200687
    WHEN geo_dma_id == 146 THEN 200691
    WHEN geo_dma_id == 147 THEN 200692
    WHEN geo_dma_id == 148 THEN 200693
    WHEN geo_dma_id == 149 THEN 200698
    WHEN geo_dma_id == 150 THEN 200702
    WHEN geo_dma_id == 151 THEN 200705
    WHEN geo_dma_id == 152 THEN 200709
    WHEN geo_dma_id == 153 THEN 200710
    WHEN geo_dma_id == 154 THEN 200711
    WHEN geo_dma_id == 155 THEN 200716
    WHEN geo_dma_id == 156 THEN 200717
    WHEN geo_dma_id == 157 THEN 200718
    WHEN geo_dma_id == 158 THEN 200722
    WHEN geo_dma_id == 159 THEN 200724
    WHEN geo_dma_id == 160 THEN 200725
    WHEN geo_dma_id == 161 THEN 200734
    WHEN geo_dma_id == 162 THEN 200736
    WHEN geo_dma_id == 163 THEN 200737
    WHEN geo_dma_id == 164 THEN 200740
    WHEN geo_dma_id == 165 THEN 200743
    WHEN geo_dma_id == 166 THEN 200744
    WHEN geo_dma_id == 167 THEN 200745
    WHEN geo_dma_id == 168 THEN 200746
    WHEN geo_dma_id == 169 THEN 200747
    WHEN geo_dma_id == 170 THEN 200749
    WHEN geo_dma_id == 171 THEN 200751
    WHEN geo_dma_id == 172 THEN 200752
    WHEN geo_dma_id == 173 THEN 200753
    WHEN geo_dma_id == 174 THEN 200754
    WHEN geo_dma_id == 175 THEN 200755
    WHEN geo_dma_id == 176 THEN 200756
    WHEN geo_dma_id == 177 THEN 200757
    WHEN geo_dma_id == 178 THEN 200758
    WHEN geo_dma_id == 179 THEN 200759
    WHEN geo_dma_id == 180 THEN 200760
    WHEN geo_dma_id == 181 THEN 200762
    WHEN geo_dma_id == 182 THEN 200764
    WHEN geo_dma_id == 183 THEN 200765
    WHEN geo_dma_id == 184 THEN 200766
    WHEN geo_dma_id == 185 THEN 200767
    WHEN geo_dma_id == 186 THEN 200770
    WHEN geo_dma_id == 187 THEN 200771
    WHEN geo_dma_id == 188 THEN 200773
    WHEN geo_dma_id == 189 THEN 200789
    WHEN geo_dma_id == 190 THEN 200790
    WHEN geo_dma_id == 191 THEN 200798
    WHEN geo_dma_id == 192 THEN 200800
    WHEN geo_dma_id == 193 THEN 200801
    WHEN geo_dma_id == 194 THEN 200802
    WHEN geo_dma_id == 195 THEN 200803
    WHEN geo_dma_id == 196 THEN 200804
    WHEN geo_dma_id == 197 THEN 200807
    WHEN geo_dma_id == 198 THEN 200810
    WHEN geo_dma_id == 199 THEN 200811
    WHEN geo_dma_id == 200 THEN 200813
    WHEN geo_dma_id == 201 THEN 200819
    WHEN geo_dma_id == 202 THEN 200820
    WHEN geo_dma_id == 203 THEN 200821
    WHEN geo_dma_id == 204 THEN 200825
    WHEN geo_dma_id == 205 THEN 200828
    WHEN geo_dma_id == 206 THEN 200839
    WHEN geo_dma_id == 207 THEN 200855
    WHEN geo_dma_id == 208 THEN 200862
    WHEN geo_dma_id == 209 THEN 200866
    WHEN geo_dma_id == 210 THEN 200868
    WHEN geo_dma_id == 211 THEN 200881
    ELSE NULL
  END AS Metro_Code,
  %(Client_Impressions)s AS Client_Impressions,
  %(Peer_Impressions)s AS Peer_Impressions
FROM %(Table)s
WHERE %(Where)s
GROUP BY
  1,2,3,4,5,6,7,8
'''


PEER_ANALYSIS_QUERY = '''
SELECT
  Advertiser_Id,
  RATIO_TO_REPORT(Impressions) OVER () AS Percent
FROM (
  SELECT
    ad_advertiser_id AS Advertiser_Id,
    SUM(ad_metrics_impressions) AS Impressions
  FROM %(Table)s
  WHERE %(Where)s
  GROUP BY 1
)
'''


def sov_query_where(dcm_accounts):
  query = ''
  first = True

  # assemble all accounts using OR to combine multiple networks and advertisers
  for account in dcm_accounts:
    network, advertiser, profile = parse_account(project.task['auth'], account)
    if network and advertiser:
      query += '%s ( base_event_network_id = %d AND ad_advertiser_id = %d ) ' % ('' if first else 'OR', network, advertiser)
      first = False
    elif network:
      query += '%s base_event_network_id = %d ' % ('' if first else 'OR', network)
      first = False
    
  # prevent query all by omission
  if query == '': raise Exception('Missing DCM accounts!')

  return query


def sov_accounts():
  if project.verbose: print "CLIENT:", project.task['dataset']

  # make sure tab exists in sheet
  sheets_tab_copy(project.task['auth'], project.task['sheet']['template']['url'], project.task['sheet']['template']['tab'], project.task['sheet']['url'], project.task['sheet']['template']['tab'])

  # read peers from sheet
  rows = sheets_read(project.task['auth'], project.task['sheet']['url'], project.task['sheet']['template']['tab'], project.task['sheet']['range'])

  # CHECK: If minimum number of peers met
  if len(rows) < 5:
    raise Exception('Need at least 5 DCM accounts in the sheet to ensure anonymity!')

  # assemble accounts for the peers ( given in sheet ), make account_id:advertiser_id@profile_id
  peers = [r[0] + ((':%s' % r[1]) if len(r) > 1 else '') + (('@%s' % r[2]) if len(r) > 2 else '')  for r in rows]

  # assemble accounts for the client ( given in JSON )
  clients = project.task['dcm_accounts']

  # names are used to fetch the report
  return clients, peers


def sov():
  # 1 - get client and peer ids
  client_accounts, peer_accounts = sov_accounts()

  # 2 - Check if peer weights are correct
  query = PEER_ANALYSIS_QUERY % {
    'Table':SOV_TABLE,
    'Where':sov_query_where(peer_accounts)
  }

  rows = query_to_rows(
    project.task['auth'],
    project.id,
    project.task['dataset'],
    query
  )

  warnings = []
  errors = []
  advertiser_count = 0
  for row in rows:
    advertiser_count += 1
    if row[1] == 0: warnings.append('Advertiser %s has no impressions, change it out!' % row[0])
    elif row[1] > 0.5: errors.append('Advertiser %s share %d%% > 50%%, add more peers!' % (row[0], row[1] * 100))

  # check if enough peers ( ignore peers without impressions until it affects the required minimum )
  if advertiser_count < 5:
    errors.extend(warnings)
    errors.append('Need at least 5 DCM advertisers with impressions to ensure anonymity!')

  # STOP IF WRONG MIX, raise all errors at once so user can clean up multiple issues at once
  if errors: raise Exception('\n'.join(errors))


  # 3 - Write client data to table
  query = SOV_QUERY % {
    'Advertiser_Type':'Client',
    'Client_Impressions':'SUM(ad_metrics_impressions)',
    'Peer_Impressions':'0',
    'Table':SOV_TABLE,
    'Where':sov_query_where(client_accounts)
  }

  query_to_table(
    project.task['auth'],
    project.id,
    project.task['dataset'],
    project.task['table'],
    query,
  )

  # 4 - Append peer data to table
  query = SOV_QUERY % {
    'Advertiser_Type':'Peer',
    'Client_Impressions':'0',
    'Peer_Impressions':'SUM(ad_metrics_impressions)',
    'Table':SOV_TABLE,
    'Where':sov_query_where(peer_accounts)
  }

  query_to_table(
    project.task['auth'],
    project.id,
    project.task['dataset'],
    project.task['table'],
    query,
    'WRITE_APPEND'
  )


if __name__ == "__main__":
  project.load('sov_dcm')
  sov()
