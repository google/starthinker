###########################################################################
#
#  Copyright 2020 Google LLC
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
#
#  This code generated (see starthinker/scripts for possible source):
#    - Command: "python starthinker_ui/manage.py airflow"
#
###########################################################################

'''
--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer ( recommended ):

    From Release: pip install starthinker
    From Open Source: pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory ( if pushing local code changes ):

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

  If any recipe task has "auth" set to "user" add user credentials:

    1. Ensure an RECIPE['setup']['auth']['user'] = [User Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_user", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/deploy_commandline.md#optional-setup-user-credentials

--------------------------------------------------------------

  If any recipe task has "auth" set to "service" add service credentials:

    1. Ensure an RECIPE['setup']['auth']['service'] = [Service Credentials JSON]

  OR

    1. Visit Airflow UI > Admin > Connections.
    2. Add an Entry called "starthinker_service", fill in the following fields. Last step paste JSON from authentication.
      - Conn Type: Google Cloud Platform
      - Project: Get from https://github.com/google/starthinker/blob/master/tutorials/cloud_project.md
      - Keyfile JSON: Get from: https://github.com/google/starthinker/blob/master/tutorials/cloud_service.md

--------------------------------------------------------------

CM360 Oculi

Export CM360 Creatives into BigQuery, process them with the Vision API, and generate a breakdown of each creative asset mapped back to its parent. Also generate a series of views to flatten the data.

  - Wait for <b>BigQuery->->->Oculi_...</b> to be created.
  - Then use the data for analysis.
  - Or give these intructions to the client.

--------------------------------------------------------------

This StarThinker DAG can be extended with any additional tasks from the following sources:
  - https://google.github.io/starthinker/
  - https://github.com/google/starthinker/tree/master/dags

'''

from starthinker.airflow.factory import DAG_Factory

INPUTS = {
  'auth_cm':'user',  # CM360 read credentials.
  'auth_bigquery':'service',  # BigQuery read/ write credentials.
  'account':'',  # CM360 Account Identifier
  'limit':1000,  # Number of creatives to pull.
  'recipe_slug':'',  # name of dataset in BigQuery.
}

RECIPE = {
  'tasks':[
    {
      'dataset':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
      }
    },
    {
      'google_api':{
        '__comment__':'Download all creatives, limit set to 20K for 4 hour processing time, and up to maximum 80K to prevent triggering 500 Error in API.',
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'user','description':'CM360 read credentials.'}},
        'api':'dfareporting',
        'version':'v3.4',
        'function':'creatives.list',
        'kwargs':{
          'accountId':{'field':{'name':'account','kind':'integer','order':3,'default':'','description':'CM360 Account Identifier'}},
          'sortField':'ID',
          'sortOrder':'DESCENDING'
        },
        'iterate':True,
        'limit':{'field':{'name':'limit','kind':'integer','order':4,'default':1000,'description':'Number of creatives to pull.','choices':[1000,5000,10000,20000,40000,80000]}},
        'results':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
            'table':'CM_Creatives'
          }
        }
      }
    },
    {
      'url':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'status':True,
        'read':True,
        'urls':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
            'query':"WITH             URL_PARTS AS (               SELECT                 C.id,                 CAST(C.AdvertiserId AS STRING) AS AdvertiserId,                 CA.assetIdentifier.name AS Name               FROM `CM_Creatives` AS C, UNNEST(creativeAssets) AS CA               WHERE REPLACE(RIGHT(CA.assetIdentifier.name, 4), '.', '') IN ('jpg', 'png', 'gif', 'jpeg','html','htm')               AND CA.size.width >1 and CA.size.height > 1             )             SELECT FORMAT('https://s0.2mdn.net/%s/%s', AdvertiserId, REPLACE(Name, ' ', '%20')) AS URL, id AS URI FROM URL_PARTS             UNION ALL             SELECT  FORMAT('https://s0.2mdn.net/sadbundle/%s', REPLACE(Name, ' ', '%20')) AS URL, id AS URI FROM URL_PARTS             UNION ALL             SELECT FORMAT('https://s0.2mdn.net/simgad/%s', REPLACE(Name, ' ', '%20')) AS URL, id AS URI FROM URL_PARTS           ",
            'legacy':False
          }
        },
        'to':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
            'table':'Creative_URLs'
          }
        }
      }
    },
    {
      'vision_api':{
        'auth':{'field':{'name':'auth_cm','kind':'authentication','order':1,'default':'user','description':'CM360 read credentials.'}},
        'requests':{
          'bigquery':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
            'query':"             SELECT             STRUCT(               Read AS content,               STRUCT(                 URI AS imageUri               ) AS source             ) AS image,             [               STRUCT(                 'TEXT_DETECTION' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               ),               STRUCT(                 'IMAGE_PROPERTIES' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               ),               STRUCT(                 'SAFE_SEARCH_DETECTION' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               ),               STRUCT(                 'LABEL_DETECTION' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               ),               STRUCT(                 'LOGO_DETECTION' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               ),               STRUCT(                 'FACE_DETECTION' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               ),               STRUCT(                 'OBJECT_LOCALIZATION' AS type,                 10 AS maxResults,                 'builtin/stable' AS model               )             ] AS features             FROM `Creative_URLs`             WHERE Status=200           ",
            'legacy':False
          }
        },
        'responses':{
          'bigquery':{
            'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
            'table':'Vision_Creatives'
          }
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'query':'SELECT           C.*,           VC.*           FROM `{dataset}.CM_Creatives` AS C           LEFT JOIN `{dataset}.Vision_Creatives` AS VC           ON C.Id=CAST(VC.imageUri AS INT64)         ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_Creatives'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'query':'SELECT           CAST(imageUri AS INT64) AS creativeID,           description AS label,           score         FROM           `{dataset}.Vision_Creatives`, UNNEST( labelAnnotations)         ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_labelAnnotations'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'query':"WITH Creative_Sizes AS (           SELECT             Id AS creativeId,             MAX(size.width) AS width,             MAX(size.height) AS height,           FROM `{dataset}.CM_Creatives`           GROUP BY 1         )          SELECT           CAST(VC.imageUri AS INT64) AS creativeId,           LOWER(T.description) AS word,           SAFE_DIVIDE(MAX(V.x) - MIN(v.x), ANY_VALUE(width)) * SAFE_DIVIDE(MAX(V.y) - MIN(v.y), ANY_VALUE(height)) AS area_fraction           FROM             `{dataset}.Vision_Creatives` AS VC             JOIN UNNEST(textAnnotations) AS T             JOIN UNNEST(boundingPoly.vertices) AS V             JOIN Creative_Sizes AS CS             ON CAST(VC.imageUri AS INT64) = CS.creativeId           WHERE             /* Exclude small and common words */             LENGTH(description) > 2             AND LOWER(description) NOT IN ('for', 'the')           GROUP BY 1,2         ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_textAnnotations'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'function':'RGB To HSV',
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'query':'SELECT             CAST(VC.imageUri AS INT64) AS creativeId,             LOWER(LO.name) AS name,             (MAX(V.x) - MIN(v.x)) * (MAX(V.y) - MIN(v.y)) AS areaFraction           FROM `{dataset}.Vision_Creatives` AS VC             JOIN UNNEST(localizedObjectAnnotations) AS LO             JOIN UNNEST(boundingPoly.normalizedVertices) AS V           GROUP BY 1,2         ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_localizedObjectAnnotations'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'query':"WITH Vision_Colors AS (           SELECT             CAST(VC.imageUri AS INT64) AS creativeId,             STRUCT(               CAST(C.color.red AS INT64) AS r,               CAST(C.color.green AS INT64) AS g,               CAST(C.color.blue AS INT64) AS b             ) as rgb,             STRUCT(               FORMAT('%02X', CAST(C.color.red AS INT64)) as r,               FORMAT('%02X', CAST(C.color.green AS INT64)) as g,               FORMAT('%02X', CAST(C.color.blue AS INT64)) as b             ) as html,             `{dataset}`.rgb_to_hsv(C.color.red, C.color.green, C.color.blue) AS hsv,             (0.2126*C.color.red + 0.7152*C.color.green + 0.0722*C.color.blue) / 255.0 AS percievedBrightness,             C.score,             C.pixelFraction AS areaFraction           FROM             `{dataset}.Vision_Creatives` AS VC             JOIN UNNEST(imagePropertiesAnnotation.dominantColors.colors) AS C          )           SELECT            *,            CASE              WHEN hsv.h < 90 THEN (90 - hsv.h) / 90              WHEN hsv.h < 270 THEN 0              ELSE (hsv.h - 270) / 90            END AS warmness,            CASE              WHEN hsv.h < 90 THEN 0              WHEN hsv.h < 270 THEN ( 90 - ABS(180 - hsv.h)) / 90              ELSE 0            END AS coldness          FROM Vision_Colors;         ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_imagePropertiesAnnotation'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'query':'           WITH Creative_Sizes AS (             SELECT               Id AS creativeId,               MAX(size.width) AS width,               MAX(size.height) AS height,             FROM `{dataset}.CM_Creatives`             GROUP BY 1           )            SELECT             CAST(VC.imageUri AS INT64) AS creativeId,             F.angerLikelihood,             F.headwearLikelihood,             F.surpriseLikelihood,             F.sorrowLikelihood,             F.joyLikelihood,             F.blurredLikelihood,             F.panAngle,             F.rollAngle,             F.tiltAngle,             detectionConfidence AS score,             SAFE_DIVIDE(MAX(v.x) - MIN(v.x), ANY_VALUE(width)) * SAFE_DIVIDE(MAX(v.y) - MIN(v.y), ANY_VALUE(height)) AS area_fraction           FROM             `{dataset}.Vision_Creatives` AS VC             JOIN UNNEST(faceAnnotations ) AS F             JOIN UNNEST(boundingPoly.vertices) AS V             JOIN Creative_Sizes AS CS             ON CAST(VC.imageUri AS INT64) = CS.creativeId           GROUP BY 1,2,3,4,5,6,7,8,9,10,11         ',
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_faceAnnotations'
        }
      }
    },
    {
      'bigquery':{
        'auth':{'field':{'name':'auth_bigquery','kind':'authentication','order':3,'default':'service','description':'BigQuery read/ write credentials.'}},
        'from':{
          'query':"           WITH Creative_Sizes AS (             SELECT               Id AS creativeId,               MAX(size.width) AS width,               MAX(size.height) AS height,             FROM `{dataset}.CM_Creatives`             GROUP BY 1           ),           Creative_Faces AS (           SELECT             CAST(VC.imageUri AS INT64) AS creativeId,             description AS logo,             score,             SAFE_DIVIDE((MAX(v.x) + MIN(v.x)) / 2, ANY_VALUE(width)) AS x_fraction,             SAFE_DIVIDE((MAX(v.y) + MIN(v.y)) / 2, ANY_VALUE(height)) AS y_fraction,             SAFE_DIVIDE(MAX(v.x) - MIN(v.x), ANY_VALUE(width)) * SAFE_DIVIDE(MAX(v.y) - MIN(v.y), ANY_VALUE(height)) AS area_fraction           FROM             `{dataset}.Vision_Creatives` AS VC             JOIN UNNEST(logoAnnotations ) AS L             JOIN UNNEST(boundingPoly.vertices) AS V             JOIN Creative_Sizes AS CS             ON CAST(VC.imageUri AS INT64) = CS.creativeId           GROUP BY 1,2,3           )            SELECT           *,           score * area_fraction AS prominenceScore,           RANK() OVER (PARTITION BY creativeId ORDER BY score * area_fraction DESC) AS prominenceRank,           CASE             WHEN x_fraction < 0.33 AND y_fraction < 0.33 THEN 'TOP LEFT'             WHEN x_fraction > 0.66 AND y_fraction < 0.33 THEN 'TOP RIGHT'             WHEN x_fraction < 0.33 AND y_fraction > 0.66 THEN 'BOTTOM LEFT'             WHEN x_fraction > 0.66 AND y_fraction > 0.66 THEN 'BOTTOM RIGHT'             WHEN y_fraction < 0.33 THEN 'TOP CENTER'             WHEN y_fraction > 0.66 THEN 'BOTTOM CENTER'             WHEN X_fraction > 0.66 THEN 'RIGHT CENTER'             WHEN x_fraction < 0.33 THEN 'LEFT CENTER'             ELSE 'CENTER'           END AS position           FROM Creative_Faces;         ",
          'parameters':{
            'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}}
          },
          'legacy':False
        },
        'to':{
          'dataset':{'field':{'name':'recipe_slug','kind':'string','order':5,'default':'','description':'name of dataset in BigQuery.'}},
          'view':'Oculi_logoAnnotations'
        }
      }
    }
  ]
}

dag_maker = DAG_Factory('cm360_oculi', RECIPE, INPUTS)
dag = dag_maker.generate()

if __name__ == "__main__":
  dag_maker.print_commandline()
