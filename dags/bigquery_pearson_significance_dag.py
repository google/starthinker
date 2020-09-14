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
"""--------------------------------------------------------------

Before running this Airflow module...

  Install StarThinker in cloud composer from open source:

    pip install git+https://github.com/google/starthinker

  Or push local code to the cloud composer plugins directory:

    source install/deploy.sh
    4) Composer Menu
    l) Install All

--------------------------------------------------------------

Pearson Correlation Significance Function

Add function to dataset for checking if correlation is significant.

Specify the dataset, and the function will be added and available.

"""

from starthinker_airflow.factory import DAG_Factory

# Add the following credentials to your Airflow configuration.
USER_CONN_ID = 'starthinker_user'  # The connection to use for user authentication.
GCP_CONN_ID = 'starthinker_service'  # The connection to use for service authentication.

INPUTS = {
    'auth': 'service',  # Credentials used for writing data.
    'dataset': '',  # Existing BigQuery dataset.
}

TASKS = [{
    'bigquery': {
        'auth': {
            'field': {
                'name': 'auth',
                'kind': 'authentication',
                'order': 0,
                'default': 'service',
                'description': 'Credentials used for writing data.'
            }
        },
        'run': {
            'query':
                "           CREATE FUNCTION IF NOT EXISTS "
                "[PARAMETER].pearson_significance_test(correlation FLOAT64, "
                "population INT64, percent FLOAT64, threshold FLOAT64)"
                "             RETURNS INT64             LANGUAGE js AS"
                "             '''               /* correlation = value from "
                "CORR function. */               /* population = number of "
                "mesurements. */               /* percent = 80, 90, 98, 99, "
                "99.5, 99.95 certainty ( aka sigma ). */               /* "
                "threshold = usually 0.5, the minimum correlation value to be "
                "considered significant. */               /* returns = -1 for "
                "negative significant correlation, 0 for no significant "
                "correlation ( null hypothesis), and 1 for positive "
                "siginificant correlation. */               /* Example: SELECT"
                " pearson_significance_test(Impression_Correlation, "
                "Data_Point_Count, 95, 0.5) AS Female_Impression_Significant "
                "FROM ... */               if (Math.abs(correlation) < "
                "threshold) { return 0; }               var dt_lookup = ["
                "                 [1, .9511, .9877, .9969, .9995, .9999, "
                ".9999], /* 0 */                 [2, .8000, .9000, .9500, "
                ".9800, .9900, .9990], /* 1 */                 [3, .6870, "
                ".8054, .8783, .9343, .9587, .9911], /* 2 */                 "
                "[4, .6084, .7293, .8114, .8822, .9172, .9741], /* 3 */"
                "                 [5, .5509, .6694, .7545, .8329, .8745, "
                ".9509], /* 4 */                 [6, .5067, .6215, .7067, "
                ".7887, .8343, .9249], /* 5 */                 [7, .4716, "
                ".5822, .6664, .7498, .7977, .8983], /* 6 */                 "
                "[8, .4428, .5494, .6319, .7155, .7646, .8721], /* 7 */"
                "                 [9, .4187, .5214, .6021, .6851, .7348, "
                ".8470], /* 8 */                 [10, .3981, .4973, .5760, "
                ".6581, .7079, .8233], /* 9 */                 [11, .3802, "
                ".4762, .5529, .6339, .6835, .8010], /* 10 */                 "
                "[12, .3646, .4575, .5324, .6120, .6614, .7800], /* 11 */"
                "                 [13, .3507, .4409, .5140, .5923, .6411, "
                ".7604], /* 12 */                 [14, .3383, .4259, .4973, "
                ".5742, .6226, .7419], /* 13 */                 [15, .3271, "
                ".4124, .4821, .5577, .6055, .7247], /* 14 */                 "
                "[16, .3170, .4000, .4683, .5425, .5897, .7084], /* 15 */"
                "                 [17, .3077, .3887, .4555, .5285, .5751, "
                ".6932], /* 16 */                 [18, .2992, .3783, .4438, "
                ".5155, .5614, .6788], /* 17 */                 [19, .2914, "
                ".3687, .4329, .5034, .5487, .6652], /* 18 */                 "
                "[20, .2841, .3598, .4227, .4921, .5368, .6524], /* 29 */"
                "                 [21, .2774, .3515, .4132, .4815, .5256, "
                ".6402], /* 20 */                 [22, .2711, .3438, .4044, "
                ".4716, .5151, .6287], /* 21 */                 [23, .2653, "
                ".3365, .3961, .4622, .5052, .6178], /* 22 */                 "
                "[24, .2598, .3297, .3882, .4534, .4958, .6074], /* 23 */"
                "                 [25, .2546, .3233, .3809, .4451, .4869, "
                ".5974], /* 24 */                 [30, .2327, .2960, .3494, "
                ".4093, .4487, .5541], /* 25 */                 [35, .2156, "
                ".2746, .3246, .3810, .4182, .5189], /* 26 */                 "
                "[40, .2018, .2573, .3044, .3578, .3932, .4896], /* 27 */"
                "                 [50, .1806, .2306, .2732, .3218, .3542, "
                ".4432], /* 28 */                 [60, .1650, .2108, .2500, "
                ".2948, .3248, .4079], /* 29 */                 [70, .1528, "
                ".1954, .2319, .2737, .3017, .3798], /* 30 */                 "
                "[80, .1430, .1829, .2172, .2565, .2830, .3568], /* 31 */"
                "                 [90, .1348, .1726, .2050, .2422, .2673, "
                ".3375], /* 32 */                 [100, .1279, .1638, .1946, "
                ".2301, .2540, .3211], /* 33 */                 [150, .1045, "
                ".1339, .1593, .1886, .2084, .2643], /* 34 */                 "
                "[300, .0740, .0948, .1129, .1338, .1480, .1884], /* 35 */"
                "                 [500, .0573, .0735, .0875, .1038, .1149, "
                ".1464], /* 36 */                 [1000, .0405, .0520, .0619, "
                ".0735, .0813, .1038] /* 37 */               ]               "
                "populatuion = population - 2;               var dt_low = 0;"
                "               var dt_high = 0;               var dt_sigma = "
                "0;               if (percent == 80) { dt_sigma = 1; }"
                "               else if (percent == 90) { dt_sigma = 2; }"
                "               else if (percent == 95) { dt_sigma = 3; }"
                "               else if (percent == 98) { dt_sigma = 4; }"
                "               else if (percent == 99.5) { dt_sigma = 5; }"
                "               else if (percent == 99.95) { dt_sigma = 6; }"
                "               else { dt_sigma = 5; }               if "
                "(population >= 1000) { dt_low = 37; dt_high = 37; }"
                "               else if (population >= 500) { dt_low = 36; "
                "dt_high = 37; }               else if (population >= 300) { "
                "dt_low = 35; dt_high = 36; }               else if "
                "(population >= 150) { dt_low = 34; dt_high = 35; }"
                "               else if (population >= 100) { dt_low = 33; "
                "dt_high = 34; }               else if (population >= 90) { "
                "dt_low = 32; dt_high = 33; }               else if "
                "(population >= 80) { dt_low = 31; dt_high = 32; }"
                "               else if (population >= 70) { dt_low = 30; "
                "dt_high = 31; }               else if (population >= 60) { "
                "dt_low = 29; dt_high = 30; }               else if "
                "(population >= 50) { dt_low = 28; dt_high = 29; }"
                "               else if (population >= 40) { dt_low = 27; "
                "dt_high = 28; }               else if (population >= 35) { "
                "dt_low = 26; dt_high = 27; }               else if "
                "(population >= 30) { dt_low = 25; dt_high = 26; }"
                "               else if (population > 25) { dt_low = 24; "
                "dt_high = 25; }               else if (population > 0) { "
                "dt_low = population; dt_high = population; }               "
                "else { return 0; }               if (dt_low == dt_high) {"
                "                 if (Math.abs(correlation) > "
                "dt_lookup[dt_low][dt_sigma] ) { return "
                "Math.sign(correlation); }                 else { return 0; }"
                "                  } else {                 if "
                "(Math.abs(correlation) > dt_lookup[dt_low][dt_sigma] + "
                "((dt_lookup[dt_high][dt_sigma] - dt_lookup[dt_low][dt_sigma])"
                " * ((population - dt_lookup[dt_low][0]) / "
                "(dt_lookup[dt_high][0] - dt_lookup[dt_low][0])))) { return "
                "Math.sign(correlation); }                 else { return 0; }"
                "                }             ''';         ",
            'legacy':
                False,
            'parameters': [{
                'field': {
                    'name': 'dataset',
                    'kind': 'string',
                    'order': 1,
                    'default': '',
                    'description': 'Existing BigQuery dataset.'
                }
            }]
        }
    }
}]

DAG_FACTORY = DAG_Factory('bigquery_pearson_significance', {'tasks': TASKS},
                          INPUTS)
DAG_FACTORY.apply_credentails(USER_CONN_ID, GCP_CONN_ID)
DAG = DAG_FACTORY.execute()

if __name__ == '__main__':
  DAG_FACTORY.print_commandline()
