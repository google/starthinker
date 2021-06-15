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

from datetime import datetime

from starthinker.util.dv import report_file, report_get, report_clean, report_to_rows, DBM_CHUNKSIZE, report_to_list
from starthinker.util.bigquery import rows_to_table, make_schema
from starthinker.util.sdf import get_single_sdf_rows
from starthinker.util.data import put_rows

BUDGET_SEGMENTS = 'Budget Segments'
IO_ID = 'Io Id'
CHANGES_SCHEMA = ['Io Id', 'Category', 'Old Value', 'Delta', 'New Value']


def monthly_budget_mover(config, task):
  if config.verbose:
    print('MONTHLY BUDGET MOVER')

  # Get Spend report
  r = report_get(config, task['auth'], name=task['report_name'])

  report_id = report_get(
      config, task['auth'], name=task['report_name'])['queryId']
  #report = report_to_list(task['auth'], report_id)

  # Get Insertion Order SDF
  # sdf = list(get_single_sdf_rows(
  #     task['auth'],
  #     task['sdf']['version'],
  #     task['sdf']['partner_id'],
  #     task['sdf']['file_types'],
  #     task['sdf']['filter_type'],
  #     task['sdf']['read']['filter_ids'],
  #    'InsertionOrders'))

  # print('sdf============================================================')
  # print(sdf)
  # print('sdf============================================================')

  sdf = [
      [
          'Io Id', 'Campaign Id', 'Name', 'Timestamp', 'Status', 'Io Type',
          'Billable Outcome', 'Fees', 'Integration Code', 'Details', 'Pacing',
          'Pacing Rate', 'Pacing Amount', 'Frequency Enabled',
          'Frequency Exposures', 'Frequency Period', 'Frequency Amount',
          'Performance Goal Type', 'Performance Goal Value', 'Measure DAR',
          'Measure DAR Channel', 'Budget Type', 'Budget Segments',
          'Auto Budget Allocation', 'Geography Targeting - Include',
          'Geography Targeting - Exclude', 'Language Targeting - Include',
          'Language Targeting - Exclude', 'Device Targeting - Include',
          'Device Targeting - Exclude', 'Browser Targeting - Include',
          'Browser Targeting - Exclude', 'Digital Content Labels - Exclude',
          'Brand Safety Sensitivity Setting', 'Brand Safety Custom Settings',
          'Third Party Verification Services',
          'Third Party Verification Labels', 'Channel Targeting - Include',
          'Channel Targeting - Exclude', 'Site Targeting - Include',
          'Site Targeting - Exclude', 'App Targeting - Include',
          'App Targeting - Exclude', 'App Collection Targeting - Include',
          'App Collection Targeting - Exclude', 'Category Targeting - Include',
          'Category Targeting - Exclude', 'Keyword Targeting - Include',
          'Keyword Targeting - Exclude', 'Keyword List Targeting - Exclude',
          'Audience Targeting - Similar Audiences',
          'Audience Targeting - Include', 'Audience Targeting - Exclude',
          'Affinity & In Market Targeting - Include',
          'Affinity & In Market Targeting - Exclude', 'Custom List Targeting',
          'Inventory Source Targeting - Authorized Seller Options',
          'Inventory Source Targeting - Include',
          'Inventory Source Targeting - Exclude',
          'Inventory Source Targeting - Target New Exchanges',
          'Daypart Targeting', 'Daypart Targeting Time Zone',
          'Environment Targeting', 'Viewability Targeting Active View',
          'Position Targeting - Display On Screen',
          'Position Targeting - Video On Screen',
          'Position Targeting - Display Position In Content',
          'Position Targeting - Video Position In Content',
          'Position Targeting - Audio Position In Content',
          'Video Player Size Targeting', 'Demographic Targeting Gender',
          'Demographic Targeting Age', 'Demographic Targeting Household Income',
          'Demographic Targeting Parental Status', 'Connection Speed Targeting',
          'Carrier Targeting - Include', 'Carrier Targeting - Exclude',
          'Insertion Order Optimization', 'Bid Strategy Unit',
          'Bid Strategy Do Not Exceed', 'Apply Floor Price For Deals',
          'Algorithm Id'
      ],
      [
          '3489402', '294948', 'Audit_creas_Mustang',
          '2020-03-06T22:04:11.821000', 'Paused', 'Standard', 'Impression',
          '(Media; 0.0; Display & Video 360 Fee; True;);', '', '', 'Flight',
          'Even', '0', 'True', '1', 'Lifetime', '0', 'None', '0', 'False', '',
          'Amount',
          '(12000.0; 05/01/2020; 05/31/2020;);(12000.0; 06/01/2020; 06/30/2020;);',
          'False', '', '', '', '', '2; 502; 202; 302;', '', '', '', '',
          'Use custom',
          'Adult; Alcohol; Derogatory; Downloads & Sharing; Drugs; Gambling; '
          'Profanity; Religion; Sensitive social issues; Suggestive; Tobacco; '
          'Tragedy; Transportation Accidents; Violence; Weapons;',
          'None', '', '',
          '2203109; 2998109; 2998110; 2998111; 2998112; 2998113; 2998114;', '',
          '', '', '', '', '', '', '', '', '', '', 'False', '', '', '', '', '',
          'Authorized and Non-Participating Publisher',
          '1; 6; 8; 9; 10; 2; 11; 12; 13; 16; 17; 19; 20; 21; 23; 27; 31; 34; '
          '36; 37; 38; 41; 42; 43; 50; 52; 60;',
          '', 'True', '', '', 'Web; App;', '', '', '', '', '', '', '', '', '',
          '', '', '', '', '', 'False', '', '', '', ''
      ],
      [
          '3502002', '294948', 'FR_Mindshare_Ford_Mustang_CTX_VOL_Avril17',
          '2020-03-06T12:07:04.366000', 'Paused', 'Standard', 'Impression',
          '(Media; 0.0; Display & Video 360 Fee; True;);', '', '', 'Flight',
          'Even', '0', 'False', '0', 'Minutes', '0', 'None', '0', 'False', '',
          'Amount',
          '(12000.0; 05/01/2020; 05/31/2020;);(12000.0; 06/01/2020; 06/30/2020;);',
          'False', '2250;', '', '', '', '2;', '502; 202; 302;', '', '', '',
          'Use custom',
          'Adult; Alcohol; Derogatory; Downloads & Sharing; Drugs; Gambling; '
          'Politics; Profanity; Religion; Sensitive social issues; Suggestive;'
          ' Tobacco; Tragedy; Transportation Accidents; Violence; Weapons;',
          'None', '', '',
          '2203109; 2998109; 2998110; 2998111; 2998112; 2998113; 2998114;', '',
          '', '', '', '', '', '', '', '', '', '', 'False', '', '', '', '', '',
          'Authorized and Non-Participating Publisher',
          '1; 6; 8; 9; 10; 2; 11; 12; 13; 16; 17; 19; 20; 21; 23; 27; 31; 34; '
          '36; 37; 38; 41; 42; 43; 50; 52; 60;',
          '', 'True', '', '', 'Web; App;', '', '', '', '', '', '', '', '', '',
          '', '', '', '', '', 'False', '', '', '', ''
      ],
      [
          '3522675', '294948', 'FR_Mindshare_Ford_Sales_Juin_CTX_VOL_Juin17',
          '2020-03-06T10:44:48.709000', 'Paused', 'Standard', 'Impression',
          '(Media; 0.0; Display & Video 360 Fee; True;);', '', '', 'Flight',
          'Ahead', '0', 'False', '0', 'Minutes', '0', 'None', '0', 'False', '',
          'Amount',
          '(12000.0; 05/01/2020; 05/31/2020;);(12000.0; 06/01/2020; 06/30/2020;);',
          'False', '2250;', '', '', '', '2;', '502; 202; 302;', '', '', '',
          'Use custom',
          'Adult; Alcohol; Derogatory; Downloads & Sharing; Drugs; Gambling; '
          'Profanity; Religion; Sensitive social issues; Suggestive; Tobacco; '
          'Tragedy; Transportation Accidents; Violence; Weapons;',
          'None', '', '',
          '2203109; 2998109; 2998110; 2998111; 2998112; 2998113; 2998114;', '',
          '', '', '', '', '', '', '', '', '', '', 'False', '', '', '', '', '',
          'Authorized and Non-Participating Publisher',
          '1; 6; 8; 9; 10; 2; 11; 12; 13; 16; 17; 19; 20; 21; 23; 27; 31; 34; '
          '36; 37; 38; 41; 42; 43; 50; 52; 60;',
          '', 'True', '', '', 'Web; App;', '', '', '', '', '', '', '', '', '',
          '', '', '', '', '', 'False', '', '', '', ''
      ]
  ]

  report = [[
      'Advertiser_Currency', 'Insertion_Order_Id', 'Revenue_Adv_Currency'
  ], ['EUR', '3489402', '893.195881'], ['EUR', '3502002', '14893.195881'],
            ['EUR', '3522675', '893.195881']]
  print('report============================================================')
  print(report)
  print('report============================================================')

  # Prep out blocks depending on where the outputs should be stored
  if task['is_colab']:
    task['out_old_sdf'].pop('bigquery')
    task['out_new_sdf'].pop('bigquery')
    task['out_changes'].pop('bigquery')

  else:
    task['out_old_sdf'].pop('file')
    task['out_new_sdf'].pop('file')
    task['out_changes'].pop('file')

    # Build Schemas
    schema = make_schema(sdf[0])
    schema_changes = make_schema(CHANGES_SCHEMA)
    task['out_old_sdf']['bigquery']['schema'] = schema
    task['out_new_sdf']['bigquery']['schema'] = schema
    task['out_changes']['bigquery']['schema'] = schema_changes

  # Write old sdf to table
  put_rows(config, task['auth'], task['out_old_sdf'], (n for n in sdf))

  # Categorize the IOs to be aggregated together
  if (task['budget_categories'] != {} and
      task['budget_categories'] != '' and
      task['budget_categories'] != None):

    categories = remove_excluded_ios_from_categories(
        task['budget_categories'], task['excluded_ios'])

    categories_spend = aggregate_io_spend_to_categories(report, categories)

    categories_budget = aggregate_io_budget_to_categories(sdf, categories)

    category_budget_deltas = calc_budget_spend_deltas(categories_budget,
                                                      categories_spend,
                                                      categories)

    new_sdf, changes = apply_category_budgets(sdf, category_budget_deltas,
                                              categories)

  # Don't split up the IOs by categories
  else:
    report_dict = convert_report_to_dict(report)
    new_sdf, changes = calc_new_sdf_no_categories(sdf, report_dict,
                                                  task['excluded_ios'])

  if task['is_colab']:
    changes.insert(0, CHANGES_SCHEMA)

  # Write new sdf to table
  put_rows(config, task['auth'], task['out_new_sdf'],
           (n for n in new_sdf))

  # Write log file to table
  put_rows(config, task['auth'], task['out_changes'],
           (n for n in changes))


""" Convert the spend report into an dictionary: key=>io_id, value=>spend

Args: * report=> DV360 report containing spend data for every IO in the
categories list

Returns:
  * a dictionary: key=>io_id, value=>spend for the previous month
"""


def convert_report_to_dict(report):
  spend_dict = {}

  # Read header to get correct columns then remove header
  report_spend_column = report[0].index('Revenue_Adv_Currency')
  report_io_id_column = report[0].index('Insertion_Order_Id')
  report.pop(0)

  for row in report:
    spend_dict[row[report_io_id_column]] = row[report_spend_column]

  return spend_dict


""" Create new SDF when no categories are provided

Args: * report dictionary=> DV360 report dictionary with io_id and spend amount

Returns:
  * sdf -> updated budget segments
  *changes -> what sort of changes happened to the budget
"""


def calc_new_sdf_no_categories(sdf, report, excluded_ios):
  changes = []
  new_sdf = []

  # Read sdf header for values
  sdf_io_id_column = sdf[0].index(IO_ID)
  sdf_budget_segments_column = sdf[0].index(BUDGET_SEGMENTS)
  is_first = True

  for row in sdf:
    if is_first:
      new_sdf.append(row)
      is_first = False
      continue

    # If Io is in exclude then just add the current
    io_id = row[sdf_io_id_column]
    if io_id in excluded_ios:
      new_sdf.append(row)
      continue

    budget_segment = convert_budget_segment_to_obj(
        row[sdf_budget_segments_column])
    current_month_idx = get_current_month_idx_in_budget_segment(
        budget_segment, str(io_id))

    # Calculate the budget delta from the previous month
    prev_spend = 0
    if io_id in report:
      prev_spend = report[io_id]

    prev_budget = get_prev_month_budget(row[sdf_budget_segments_column], io_id)

    prev_delta = float(prev_budget) - float(prev_spend)

    old_budget = float(budget_segment[current_month_idx][0])
    new_budget = old_budget + prev_delta
    budget_segment[current_month_idx][0] = '{:0.2f}'.format(new_budget)

    # Insert new budget segment information into the row
    new_budget_segment = convert_budget_segment_obj_to_string(budget_segment)
    row[sdf_budget_segments_column] = new_budget_segment

    # Log the change to be written to BQ
    changes.append([io_id, '', old_budget, prev_delta, new_budget])

    new_sdf.append(row)

  return new_sdf, changes


""" Aggregates all the io spend into their categories

Args: * report=> DV360 report containing spend data for every IO in the
categories list * categories => dictionary with categories as the key, and a
list of ios under that category as the value

Returns:
  * a dictionary with the category as the key, and the aggregated spend for the
  IOs in that category as the value
"""


def aggregate_io_spend_to_categories(report, categories):
  processed_ios = {}
  categories_spend = {}

  # Read header to get correct columns and remove header
  spend_column = report[0].index('Revenue (Adv Currency)')
  io_id_column = report[0].index('Insertion Order ID')
  report.pop(0)

  # Aggregate io spend into bigger categories
  for row in report:
    io_id = row[io_id_column]
    io_spend = row[spend_column]

    for key, val in categories.iteritems():
      if val == None:
        continue
      if int(io_id) in val:
        # Add io to the list of processed ios
        if processed_ios.has_key(key):
          processed_ios[key].append(io_id)
        else:
          processed_ios[key] = [io_id]

        # Aggregate category spend
        if categories_spend.has_key(key):
          categories_spend[key] = categories_spend[key] + float(io_spend)
        else:
          categories_spend[key] = float(io_spend)

        break

  validate_all_ios_processed(categories, processed_ios, 'Spend Report')

  return categories_spend


""" Aggregate io budget up to the category level

Args: * sdf => the current sdf for the desired filter ids * categories =>
dictionary with categories as the key, and a list of ios under that category as
the value

Returns:
  * dictionary with the category as the key, and the aggregated budget for that
  category as the value
"""


def aggregate_io_budget_to_categories(sdf, categories):
  processed_ios = {}
  categories_budget = {}

  # Read header to get correct columns and remove header
  header = sdf[0]
  io_id_idx = header.index(IO_ID)
  budget_segments_idx = header.index(BUDGET_SEGMENTS)

  # Aggregate io budget into bigger categories
  for row in sdf:
    if sdf.index(row) == 0:
      continue
    io_id = row[io_id_idx]
    budget_segments = row[budget_segments_idx]

    for key, val in categories.iteritems():
      if int(io_id) in val:
        # Get budget amount from budget segment
        budget = get_prev_month_budget(budget_segments, io_id)

        # Add IO to the list of processed ios
        if processed_ios.has_key(key):
          processed_ios[key].append(io_id)
        else:
          processed_ios[key] = [io_id]

        # Aggregate category budget
        if categories_budget.has_key(key):
          categories_budget[key] = categories_budget[key] + budget
        else:
          categories_budget[key] = budget

  validate_all_ios_processed(categories, processed_ios, 'SDF')

  return categories_budget


""" Removes the ios from the excluded list from the categories list

Args: * categories => dictionary with categories as the key, and a list of ios
under that category as the value * excluded_ios => list of ios to be excluded
from the calculations

Returns:
  * The new dictionary of categories with the necessary ios excluded from the
  list

"""


def remove_excluded_ios_from_categories(categories, excluded_ios):

  for io in excluded_ios:
    for key, value in categories.iteritems():
      if io in value:
        categories[key].remove(io)
        break

  return categories


""" Apply the new calculated budget deltas to the sdf under the budget segments portion

Args: * sdf => the current sdf file to be editted * category_budget_deltas => a
dictionary with category as the key, and the value of the budget - spend for
that category as the value * categories => dictionary with categories as the
key, and a list of ios under that category as the value

Returns:
  * new_sdf => the new sdf in list format with the updated budget segment
  strings inputted
        * changes => a list of changes that occured including: Io_Id, Category,
        Old_Value, Delta, New_Value
"""


def apply_category_budgets(sdf, category_budget_deltas, categories):
  changes = []
  new_sdf = []
  first = True
  io_id_idx = -1
  budget_segments_idx = -1

  for row in sdf:
    # Do not process the header and get the idx for Io Id and
    if first:
      io_id_idx = row.index(IO_ID)
      budget_segments_idx = row.index(BUDGET_SEGMENTS)
      if io_id_idx < 0:
        raise Exception('IO Id column was not found in SDF.')
      if budget_segments_idx < 0:
        raise Exception('Budget Segment column was not found in SDF.')
      new_sdf.append(row)
      first = False
      continue

    # Update budget segments with the new values
    io_id = row[io_id_idx]
    budget_segment = row[budget_segments_idx]
    category = None

    # figure out which category the current IO is in
    for key, val in categories.iteritems():
      if int(io_id) in val:
        category = key

    # Only update the row if the IO has been applied to a category
    if category != None:
      # Get the current budget to be updated
      budget_segment_obj = convert_budget_segment_to_obj(budget_segment)
      current_month_idx = get_current_month_idx_in_budget_segment(
          budget_segment_obj, str(io_id))

      # Apply the budget delta to the budget segment object
      if category in category_budget_deltas and current_month_idx != None:
        old_budget = float(budget_segment_obj[current_month_idx][0])
        budget_segment_obj[current_month_idx][0] = '{:0.2f}'.format(
            old_budget + category_budget_deltas[category])

        # Insert new budget segment information into the row
        new_budget_segment = convert_budget_segment_obj_to_string(
            budget_segment_obj)
        row[budget_segments_idx] = new_budget_segment

        # Log the change to be written to BQ
        changes.append([
            io_id, category, old_budget, category_budget_deltas[category],
            budget_segment_obj[current_month_idx][0]
        ])

    new_sdf.append(row)

  return new_sdf, changes


""" Converts the list of budget segment objects to the string format needed by the SDF

Args: * budget_segment_obj => A list of budget segment objects. [{budget,
start_date, end_date},{...}]

Returns:
  * A string representing the budget segment in the format required by sdfs.
        (#; MM/DD/YYYY; MM/DD/YYYY;); (#; MM/DD/YYYY; MM/DD/YYYY;);
"""


def convert_budget_segment_obj_to_string(budget_segment_obj):
  budget_segment_str = ''
  for segment in budget_segment_obj:
    budget_segment_str += '(' + str(
        segment[0]) + '; ' + segment[1] + '; ' + segment[2] + ';); '

  return budget_segment_str


""" Find the index for the current months budget in the budget segments obj

Args:
  * budget_obj: list of budget_objs

Returns:
  * Index of the current month's budget information in the budget obj
"""


def get_current_month_idx_in_budget_segment(budget_objs, io_id):
  # Seperate budget_string into a list of budget objs
  today = datetime.today()
  month = str(today.month)
  if len(month) == 1:
    month = '0' + month

  # Find correct month in the budget_obj
  for monthly_budget in budget_objs:
    if monthly_budget[1][:2] == month and monthly_budget[1][-4:] == str(
        today.year):
      return budget_objs.index(monthly_budget)

  raise Exception('The current monthly budget is not available ' + month +
                  '. Io Id => ' + io_id)


""" Calculate the deltas between the category budget and spend amount

Args: * categories_budget => dictionary with the category as the key, and the
aggregated budget for that category as the value * categories_spend =>
dictionary with the category as the key, and the aggregated spend from the
previous month as the * categories => dictionary with categories as the key, and
a list of ios under that category as the value

Returns:
  * new_sdf => the new sdf in list format with the updated budget segment
  strings inputted
        * changes => a list of changes that occured including: Io_Id, Category,
        Old_Value, Delta, New_Value
"""


def calc_budget_spend_deltas(categories_budget, categories_spend, categories):
  budget_deltas = {}

  for key, budget in categories_budget.iteritems():
    delta = budget - categories_spend[key]
    budget_deltas[key] = delta / len(categories[key])

  return budget_deltas


""" Gets the budget allocated for the previous month

Args: * budget_string => the budget segment string from the sdf (#; MM/DD/YYYY;
MM/DD/YYYY;); (#; MM/DD/YYYY; MM/DD/YYYY;);

Returns:
  * a float that represents the budget for the previous month
"""


def get_prev_month_budget(budget_string, io_id):
  # Seperate budget_string into a list of budget objs
  budget_obj = convert_budget_segment_to_obj(budget_string)

  # Calculate previous month, with two characters
  cur_year = str(datetime.today().year)
  cur_month = datetime.today().month
  prev_month_int = int(cur_month) - 1
  if (prev_month_int == 0):
    prev_month_int = 12
    cur_year = str(int(cur_year) - 1)
  prev_month = str(prev_month_int)
  if (len(prev_month) == 1):
    prev_month = '0' + prev_month

  # Find correct month in the budget_obj
  for monthly_budget in budget_obj:
    if monthly_budget[1][:2] == prev_month and monthly_budget[1][
        -4:] == cur_year:
      return float(monthly_budget[0])

  raise Exception(
      io_id +
      ' does not have budget set for the previous month(month number = ' +
      prev_month + ')')


""" Helper to split the budget segment string from the sdf into a list of budget objects

Args: * budget_string => string from the SDF that represents the budget segment
Format of the string =>

Returns:
  * List of budget objects => [{budget, start_date, end_date},...]
        budget_string format => "(#; MM/DD/YYYY; MM/DD/YYYY;); (#; MM/DD/YYYY;
        MM/DD/YYYY;);"

"""


def convert_budget_segment_to_obj(budget_string):
  budget_obj = []

  one_month_per_item = budget_string.replace('(', '').replace(' ',
                                                              '').split(';);')

  for val in one_month_per_item:
    budget_obj.append(val.split(';'))

  return budget_obj[:-1]


""" Go through the list of ios that were found from the source and verify there are no missing ios from the categories list

Args: * categories => dictionary with categories as the key, and a list of ios
under that category as the value * processed_ios => a dictionary with a list of
ios that were found in the source and aggregated * source => where the
aggregation was happening => Spend Report or SDF

Returns:
  * Nothing, but throws an exception if any un processed ios are found in the
  categories list
"""


def validate_all_ios_processed(categories, processed_ios, source):
  not_processed = []

  for key, value in categories.iteritems():
    for io_id in value:
      if str(io_id) not in processed_ios[key]:
        not_processed.append(io_id)

  if len(not_processed) > 0:
    not_processed_str = ''
    for io in not_processed:
      not_processed_str += str(io) + ', '

    raise Exception('The following ios were not found in the ' + source +
                    ':  ' + not_processed_str)
