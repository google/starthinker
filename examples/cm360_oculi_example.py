###########################################################################
#
#  Copyright 2021 Google LLC
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
#  This code generated (see scripts folder for possible source):
#    - Command: "python starthinker_ui/manage.py example"
#
###########################################################################

import argparse
import textwrap

from starthinker.util.configuration import Configuration
from starthinker.task.dataset.run import dataset
from starthinker.task.google_api.run import google_api
from starthinker.task.url.run import url
from starthinker.task.vision_api.run import vision_api
from starthinker.task.bigquery.run import bigquery


def recipe_cm360_oculi(config, auth_cm, auth_bigquery, account, limit, recipe_slug):
  """Export CM360 Creatives into BigQuery, process them with the Vision API, and
     generate a breakdown of each creative asset mapped back to its parent. Also
     generate a series of views to flatten the data.

     Args:
       auth_cm (authentication) - CM360 read credentials.
       auth_bigquery (authentication) - BigQuery read/ write credentials.
       account (integer) - CM360 Account Identifier
       limit (integer) - Number of creatives to pull.
       recipe_slug (string) - name of dataset in BigQuery.
  """

  dataset(config, {
    'auth':auth_bigquery,
    'dataset':recipe_slug
  })

  google_api(config, {
    '__comment__':'Download all creatives, limit set to 20K for 4 hour processing time, and up to maximum 80K to prevent triggering 500 Error in API.',
    'auth':auth_cm,
    'api':'dfareporting',
    'version':'v3.4',
    'function':'creatives.list',
    'kwargs':{
      'accountId':account,
      'sortField':'ID',
      'sortOrder':'DESCENDING'
    },
    'iterate':True,
    'limit':limit,
    'results':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'CM_Creatives'
      }
    }
  })

  url(config, {
    'auth':auth_bigquery,
    'status':True,
    'read':True,
    'urls':{
      'bigquery':{
        'dataset':recipe_slug,
        'query':'''WITH
           URL_PARTS AS (
             SELECT
               C.id,
               CAST(C.AdvertiserId AS STRING) AS AdvertiserId,
               CA.assetIdentifier.name AS Name
             FROM `CM_Creatives` AS C, UNNEST(creativeAssets) AS CA
             WHERE REPLACE(RIGHT(CA.assetIdentifier.name, 4), '.', '') IN ('jpg', 'png', 'gif', 'jpeg','html','htm')
             AND CA.size.width >1 and CA.size.height > 1
           )
           SELECT FORMAT('https://s0.2mdn.net/%s/%s', AdvertiserId, REPLACE(Name, ' ', '%20')) AS URL, id AS URI FROM URL_PARTS
           UNION ALL
           SELECT  FORMAT('https://s0.2mdn.net/sadbundle/%s', REPLACE(Name, ' ', '%20')) AS URL, id AS URI FROM URL_PARTS
           UNION ALL
           SELECT FORMAT('https://s0.2mdn.net/simgad/%s', REPLACE(Name, ' ', '%20')) AS URL, id AS URI FROM URL_PARTS           ''',
        'legacy':False
      }
    },
    'to':{
      'bigquery':{
        'dataset':recipe_slug,
        'table':'Creative_URLs'
      }
    }
  })

  vision_api(config, {
    'auth':auth_cm,
    'requests':{
      'bigquery':{
        'dataset':recipe_slug,
        'query':'''
           SELECT
           STRUCT(
             Read AS content,
             STRUCT(
               URI AS imageUri
             ) AS source
           ) AS image,
           [
             STRUCT(
               'TEXT_DETECTION' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             ),
             STRUCT(
               'IMAGE_PROPERTIES' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             ),
             STRUCT(
               'SAFE_SEARCH_DETECTION' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             ),
             STRUCT(
               'LABEL_DETECTION' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             ),
             STRUCT(
               'LOGO_DETECTION' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             ),
             STRUCT(
               'FACE_DETECTION' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             ),
             STRUCT(
               'OBJECT_LOCALIZATION' AS type,
               10 AS maxResults,
               'builtin/stable' AS model
             )
           ] AS features
           FROM `Creative_URLs`
           WHERE Status=200           ''',
        'legacy':False
      }
    },
    'responses':{
      'bigquery':{
        'auth':auth_bigquery,
        'dataset':recipe_slug,
        'table':'Vision_Creatives'
      }
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'query':'''SELECT
         C.*,
         VC.*
         FROM `{dataset}.CM_Creatives` AS C
         LEFT JOIN `{dataset}.Vision_Creatives` AS VC
         ON C.Id=CAST(VC.imageUri AS INT64)         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_Creatives'
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'query':'''SELECT
         CAST(imageUri AS INT64) AS creativeID,
         description AS label,
         score         FROM
         `{dataset}.Vision_Creatives`, UNNEST( labelAnnotations)         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_labelAnnotations'
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'query':'''WITH Creative_Sizes AS (
         SELECT
           Id AS creativeId,
           MAX(size.width) AS width,
           MAX(size.height) AS height,
         FROM `{dataset}.CM_Creatives`
         GROUP BY 1         )          SELECT
         CAST(VC.imageUri AS INT64) AS creativeId,
         LOWER(T.description) AS word,
         SAFE_DIVIDE(MAX(V.x) - MIN(v.x), ANY_VALUE(width)) * SAFE_DIVIDE(MAX(V.y) - MIN(v.y), ANY_VALUE(height)) AS area_fraction
         FROM
           `{dataset}.Vision_Creatives` AS VC
           JOIN UNNEST(textAnnotations) AS T
           JOIN UNNEST(boundingPoly.vertices) AS V
           JOIN Creative_Sizes AS CS
           ON CAST(VC.imageUri AS INT64) = CS.creativeId
         WHERE
           /* Exclude small and common words */
           LENGTH(description) > 2
           AND LOWER(description) NOT IN ('for', 'the')
         GROUP BY 1,2         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_textAnnotations'
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'function':'RGB To HSV',
    'to':{
      'dataset':recipe_slug
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'query':'''SELECT
           CAST(VC.imageUri AS INT64) AS creativeId,
           LOWER(LO.name) AS name,
           (MAX(V.x) - MIN(v.x)) * (MAX(V.y) - MIN(v.y)) AS areaFraction           FROM `{dataset}.Vision_Creatives` AS VC
           JOIN UNNEST(localizedObjectAnnotations) AS LO
           JOIN UNNEST(boundingPoly.normalizedVertices) AS V           GROUP BY 1,2         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_localizedObjectAnnotations'
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'dataset':recipe_slug,
      'query':'''WITH Vision_Colors AS (
         SELECT
           CAST(VC.imageUri AS INT64) AS creativeId,
           STRUCT(
             CAST(C.color.red AS INT64) AS r,
             CAST(C.color.green AS INT64) AS g,
             CAST(C.color.blue AS INT64) AS b
           ) as rgb,
           STRUCT(
             FORMAT('%02X', CAST(C.color.red AS INT64)) as r,
             FORMAT('%02X', CAST(C.color.green AS INT64)) as g,
             FORMAT('%02X', CAST(C.color.blue AS INT64)) as b
           ) as html,
           `{dataset}`.rgb_to_hsv(C.color.red, C.color.green, C.color.blue) AS hsv,
           (0.2126*C.color.red + 0.7152*C.color.green + 0.0722*C.color.blue) / 255.0 AS percievedBrightness,
           C.score,
           C.pixelFraction AS areaFraction
         FROM
           `{dataset}.Vision_Creatives` AS VC
           JOIN UNNEST(imagePropertiesAnnotation.dominantColors.colors) AS C          )
         SELECT
          *,
          CASE
            WHEN hsv.h < 90 THEN (90 - hsv.h) / 90
            WHEN hsv.h < 270 THEN 0
            ELSE (hsv.h - 270) / 90
          END AS warmness,
          CASE
            WHEN hsv.h < 90 THEN 0
            WHEN hsv.h < 270 THEN ( 90 - ABS(180 - hsv.h)) / 90
            ELSE 0
          END AS coldness          FROM Vision_Colors;         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_imagePropertiesAnnotation'
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'query':'''
         WITH Creative_Sizes AS (
           SELECT
             Id AS creativeId,
             MAX(size.width) AS width,
             MAX(size.height) AS height,
           FROM `{dataset}.CM_Creatives`
           GROUP BY 1
         )
          SELECT
           CAST(VC.imageUri AS INT64) AS creativeId,
           F.angerLikelihood,
           F.headwearLikelihood,
           F.surpriseLikelihood,
           F.sorrowLikelihood,
           F.joyLikelihood,
           F.blurredLikelihood,
           F.panAngle,
           F.rollAngle,
           F.tiltAngle,
           detectionConfidence AS score,
           SAFE_DIVIDE(MAX(v.x) - MIN(v.x), ANY_VALUE(width)) * SAFE_DIVIDE(MAX(v.y) - MIN(v.y), ANY_VALUE(height)) AS area_fraction
         FROM
           `{dataset}.Vision_Creatives` AS VC
           JOIN UNNEST(faceAnnotations ) AS F
           JOIN UNNEST(boundingPoly.vertices) AS V
           JOIN Creative_Sizes AS CS
           ON CAST(VC.imageUri AS INT64) = CS.creativeId
         GROUP BY 1,2,3,4,5,6,7,8,9,10,11         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_faceAnnotations'
    }
  })

  bigquery(config, {
    'auth':auth_bigquery,
    'from':{
      'query':'''
         WITH Creative_Sizes AS (
           SELECT
             Id AS creativeId,
             MAX(size.width) AS width,
             MAX(size.height) AS height,
           FROM `{dataset}.CM_Creatives`
           GROUP BY 1
         ),
         Creative_Faces AS (
         SELECT
           CAST(VC.imageUri AS INT64) AS creativeId,
           description AS logo,
           score,
           SAFE_DIVIDE((MAX(v.x) + MIN(v.x)) / 2, ANY_VALUE(width)) AS x_fraction,
           SAFE_DIVIDE((MAX(v.y) + MIN(v.y)) / 2, ANY_VALUE(height)) AS y_fraction,
           SAFE_DIVIDE(MAX(v.x) - MIN(v.x), ANY_VALUE(width)) * SAFE_DIVIDE(MAX(v.y) - MIN(v.y), ANY_VALUE(height)) AS area_fraction
         FROM
           `{dataset}.Vision_Creatives` AS VC
           JOIN UNNEST(logoAnnotations ) AS L
           JOIN UNNEST(boundingPoly.vertices) AS V
           JOIN Creative_Sizes AS CS
           ON CAST(VC.imageUri AS INT64) = CS.creativeId
         GROUP BY 1,2,3
         )
          SELECT
         *,
         score * area_fraction AS prominenceScore,
         RANK() OVER (PARTITION BY creativeId ORDER BY score * area_fraction DESC) AS prominenceRank,
         CASE
           WHEN x_fraction < 0.33 AND y_fraction < 0.33 THEN 'TOP LEFT'
           WHEN x_fraction > 0.66 AND y_fraction < 0.33 THEN 'TOP RIGHT'
           WHEN x_fraction < 0.33 AND y_fraction > 0.66 THEN 'BOTTOM LEFT'
           WHEN x_fraction > 0.66 AND y_fraction > 0.66 THEN 'BOTTOM RIGHT'
           WHEN y_fraction < 0.33 THEN 'TOP CENTER'
           WHEN y_fraction > 0.66 THEN 'BOTTOM CENTER'
           WHEN X_fraction > 0.66 THEN 'RIGHT CENTER'
           WHEN x_fraction < 0.33 THEN 'LEFT CENTER'
           ELSE 'CENTER'
         END AS position
         FROM Creative_Faces;         ''',
      'parameters':{
        'dataset':recipe_slug
      },
      'legacy':False
    },
    'to':{
      'dataset':recipe_slug,
      'view':'Oculi_logoAnnotations'
    }
  })



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""
      Export CM360 Creatives into BigQuery, process them with the Vision API, and generate a breakdown of each creative asset mapped back to its parent. Also generate a series of views to flatten the data.

      1. Wait for BigQuery->->->Oculi_... to be created.
      2. Then use the data for analysis.
      3. Or give these intructions to the client.
  """))

  parser.add_argument("-project", help="Cloud ID of Google Cloud Project.", default=None)
  parser.add_argument("-key", help="API Key of Google Cloud Project.", default=None)
  parser.add_argument("-client", help="Path to CLIENT credentials json file.", default=None)
  parser.add_argument("-user", help="Path to USER credentials json file.", default=None)
  parser.add_argument("-service", help="Path to SERVICE credentials json file.", default=None)
  parser.add_argument("-verbose", help="Print all the steps as they happen.", action="store_true")

  parser.add_argument("-auth_cm", help="CM360 read credentials.", default='user')
  parser.add_argument("-auth_bigquery", help="BigQuery read/ write credentials.", default='service')
  parser.add_argument("-account", help="CM360 Account Identifier", default='')
  parser.add_argument("-limit", help="Number of creatives to pull.", default=1000)
  parser.add_argument("-recipe_slug", help="name of dataset in BigQuery.", default='')


  args = parser.parse_args()

  config = Configuration(
    project=args.project,
    user=args.user,
    service=args.service,
    client=args.client,
    key=args.key,
    verbose=args.verbose
  )

  recipe_cm360_oculi(config, args.auth_cm, args.auth_bigquery, args.account, args.limit, args.recipe_slug)
