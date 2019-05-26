###########################################################################
# 
#  Copyright 2019 Google Inc.
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

from starthinker.util.project import project
from starthinker.util.dbm import report_file, report_clean, report_to_rows, DBM_CHUNKSIZE, sdf_read, report_to_list
from starthinker.util.bigquery import rows_to_table, field_list_to_schema

BUDGET_SEGMENTS = 'Budget Segments'
IO_ID = 'Io Id'


@project.from_parameters
def monthly_budget_mover():
	if project.verbose: print 'MONTHLY BUDGET MOVER'

	report = report_to_list(project.task['auth'], project.task['spend_report_id'])

	categories = remove_excluded_ios_from_categories(project.task['budget_categories'], project.task['excluded_ios'])

	categories_spend = aggregate_io_spend_to_categories(report, categories)

	sdf = list(sdf_read(project.task['auth'], project.task['sdf']['file_types'].split(','), project.task['sdf']['filter_type'], project.task['sdf']['filter_ids']))

	categories_budget = aggregate_io_budget_to_categories(sdf, categories)

	category_budget_deltas = calc_budget_spend_deltas(categories_budget, categories_spend, categories)

	new_sdf,changes = apply_category_budgets(sdf, category_budget_deltas, categories)

	# Set Schemas for BQ tables
	schema = field_list_to_schema(new_sdf[0])
	schema_changes = field_list_to_schema(['Io Id','Category','Old Value','Delta','New Value'])
	
	# Write old sdf to table
	rows_to_table(project.task['auth'], project.id, project.task['out']['dataset'], project.task['out']['old_sdf_table_name'], sdf, schema, skip_rows=1, disposition='WRITE_TRUNCATE')
	
	# Write new sdf to table
	rows_to_table(project.task['auth'], project.id, project.task['out']['dataset'], project.task['out']['new_sdf_table_name'], new_sdf, schema, skip_rows=1, disposition='WRITE_TRUNCATE')
	
	# Write log file to table
	rows_to_table(project.task['auth'], project.id, project.task['out']['dataset'], project.task['out']['changes_table_name'], iter(changes), schema_changes, skip_rows=0, disposition='WRITE_TRUNCATE')


""" Aggregates all the io spend into their categories

Args:
  * report=> DV360 report containing spend data for every IO in the categories list
  * categories => dictionary with categories as the key, and a list of ios under that category as the value

Returns:
  * a dictionary with the category as the key, and the aggregated spend for the IOs in that category as the value
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

		for key,val  in categories.iteritems():
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

Args:
  * sdf => the current sdf for the desired filter ids
  * categories => dictionary with categories as the key, and a list of ios under that category as the value

Returns:
  * dictionary with the category as the key, and the aggregated budget for that category as the value
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
		if sdf.index(row) == 0: continue
		io_id = row[io_id_idx]
		budget_segments = row[budget_segments_idx]

		for key,val in categories.iteritems():
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

Args:
  * categories => dictionary with categories as the key, and a list of ios under that category as the value
  * excluded_ios => list of ios to be excluded from the calculations 
 
Returns:
  * The new dictionary of categories with the necessary ios excluded from the list

"""
def remove_excluded_ios_from_categories(categories, excluded_ios):

	for io in excluded_ios:
		for key,value in categories.iteritems():
			if io in value:
				categories[key].remove(io)
				break

	return categories
	

""" Apply the new calculated budget deltas to the sdf under the budget segments portion

Args:
  * sdf => the current sdf file to be editted
	* category_budget_deltas => a dictionary with category as the key, and the value of the budget - spend for that category as the value
	* categories => dictionary with categories as the key, and a list of ios under that category as the value

Returns:
  * new_sdf => the new sdf in list format with the updated budget segment strings inputted
	* changes => a list of changes that occured including: Io_Id, Category, Old_Value, Delta, New_Value
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
		for key,val in categories.iteritems():
			if int(io_id) in val:
				category = key

		# Only update the row if the IO has been applied to a category
		if category != None:
			# Get the current budget to be updated
			budget_segment_obj = convert_budget_segment_to_obj(budget_segment)
			current_month_idx = get_current_month_idx_in_budget_segment(budget_segment_obj, str(io_id))

			# Apply the budget delta to the budget segment object
			if category in category_budget_deltas and current_month_idx != None:
				old_budget = float(budget_segment_obj[current_month_idx][0])
				budget_segment_obj[current_month_idx][0] = "{:0.2f}".format(old_budget + category_budget_deltas[category])

				# Insert new budget segment information into the row
				new_budget_segment = convert_budget_segment_obj_to_string(budget_segment_obj)
				row[budget_segments_idx] = new_budget_segment

				# Log the change to be written to BQ
				changes.append([
					io_id,
					category,
					old_budget,
					category_budget_deltas[category],
					budget_segment_obj[current_month_idx][0]
					])

		new_sdf.append(row)

	return new_sdf,changes


""" Converts the list of budget segment objects to the string format needed by the SDF

Args:
  * budget_segment_obj => A list of budget segment objects. [{budget, start_date, end_date},{...}]

Returns:
  * A string representing the budget segment in the format required by sdfs.
  	(#; MM/DD/YYYY; MM/DD/YYYY;); (#; MM/DD/YYYY; MM/DD/YYYY;);
"""	
def convert_budget_segment_obj_to_string(budget_segment_obj):
	budget_segment_str = ''
	for segment in budget_segment_obj:
		budget_segment_str += '(' + str(segment[0]) + '; ' + segment[1] + '; ' + segment[2] + ';); '

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
		month = '0'+ month

	# Find correct month in the budget_obj
	for monthly_budget in budget_objs:
		if monthly_budget[1][:2] == month and monthly_budget[1][-4:] == str(today.year):
			return budget_objs.index(monthly_budget)

	raise Exception('The current monthly budget is not available ' +  month + '. Io Id => ' + io_id)

	
""" Calculate the deltas between the category budget and spend amount

Args:
  * categories_budget => dictionary with the category as the key, and the aggregated budget for that category as the value
  * categories_spend => dictionary with the category as the key, and the aggregated spend from the previous month as the 
  * categories => dictionary with categories as the key, and a list of ios under that category as the value

Returns:
  * new_sdf => the new sdf in list format with the updated budget segment strings inputted
	* changes => a list of changes that occured including: Io_Id, Category, Old_Value, Delta, New_Value
"""	
def calc_budget_spend_deltas(categories_budget, categories_spend, categories):
	budget_deltas = {}

	for key,budget in categories_budget.iteritems():
		delta = budget - categories_spend[key]
		budget_deltas[key] = delta / len(categories[key])

	return budget_deltas


""" Gets the budget allocated for the previous month

Args:
  * budget_string => the budget segment string from the sdf
  	(#; MM/DD/YYYY; MM/DD/YYYY;); (#; MM/DD/YYYY; MM/DD/YYYY;);

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
	if(prev_month_int == 0): 
		prev_month_int = 12
		cur_year = str(int(cur_year)-1)
	prev_month = str(prev_month_int)
	if(len(prev_month) == 1): 
		prev_month = '0' + prev_month 

	# Find correct month in the budget_obj
	for monthly_budget in budget_obj:
		if monthly_budget[1][:2] == prev_month and monthly_budget[1][-4:] == cur_year:
			return float(monthly_budget[0])

	raise Exception(io_id + ' does not have budget set for the previous month(month number = ' + prev_month + ')')


""" Helper to split the budget segment string from the sdf into a list of budget objects

Args:
  * budget_string => string from the SDF that represents the budget segment
  	Format of the string => 
 
Returns:
  * List of budget objects => [{budget, start_date, end_date},...]
  	budget_string format => "(#; MM/DD/YYYY; MM/DD/YYYY;); (#; MM/DD/YYYY; MM/DD/YYYY;);"

"""
def convert_budget_segment_to_obj(budget_string):
	budget_obj = []

	one_month_per_item = budget_string.replace('(', '').replace(' ', '').split(';);')

	for val in one_month_per_item:
		budget_obj.append(val.split(';'))


	return budget_obj[:-1]


""" Go through the list of ios that were found from the source and verify there are no missing ios from the categories list

Args:
  * categories => dictionary with categories as the key, and a list of ios under that category as the value
  * processed_ios => a dictionary with a list of ios that were found in the source and aggregated
  * source => where the aggregation was happening => Spend Report or SDF

Returns:
  * Nothing, but throws an exception if any un processed ios are found in the categories list
"""	
def validate_all_ios_processed(categories, processed_ios, source):
	not_processed = []

	for key,value in categories.iteritems():
		for io_id in value:
			if str(io_id) not in processed_ios[key]:
				not_processed.append(io_id)

	if len(not_processed) > 0:
		not_processed_str = ''
		for io in not_processed:
			not_processed_str += str(io) + ', '
		raise Exception('The following ios were not found in the ' + source  + ':  ' + not_processed_str)


if __name__ == "__main__":
  monthly_budget_mover()
