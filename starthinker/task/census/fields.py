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

'''
  Fields to pull from Census and use in all transforms.

  Commented out fields DO NOT meet Google Personalized Advertising Policy.
  See: https://support.google.com/adspolicy/answer/143465?hl=en
'''

CENSUS_FIELDS = [{
    'category': None,
    'denominator': None,
    'columns': ['geo_id', 'total_pop']
}, {
    'category': 'gender',
    'denominator': 'total_pop',
    'columns': [
        'female_pop',
        'male_pop',
    ]
}, {
    'category':
        'age',
    'denominator':
        'total_pop',
    'columns': [
#        'population_1_year_and_over',
#        'population_3_years_over',
#        'pop_5_years_over',
#        'pop_15_and_over',
#        'pop_16_over',
        'pop_25_years_over',
        'pop_25_64',
    ]
}, {
    'category':
        'male age',
    'denominator':
        'total_pop',
    'columns': [
#        'male_5_to_9',
#        'male_10_to_14',
#        'male_15_to_17',
        'male_18_to_19',
        'male_20',
        'male_21',
        'male_22_to_24',
        'male_25_to_29',
        'male_30_to_34',
        'male_35_to_39',
        'male_40_to_44',
        'male_45_to_49',
        'male_50_to_54',
        'male_55_to_59',
        'male_65_to_66',
        'male_67_to_69',
        'male_70_to_74',
        'male_75_to_79',
        'male_80_to_84',
        'male_85_and_over',
    ]
}, {
    'category':
        'female age',
    'denominator':
        'total_pop',
    'columns': [
        #'female_5_to_9',
        #'female_10_to_14',
        #'female_15_to_17',
        'female_18_to_19',
        'female_20',
        'female_21',
        'female_22_to_24',
        'female_25_to_29',
        'female_30_to_34',
        'female_35_to_39',
        'female_40_to_44',
        'female_45_to_49',
        'female_50_to_54',
        'female_55_to_59',
        'female_65_to_66',
        'female_67_to_69',
        'female_70_to_74',
        'female_75_to_79',
        'female_80_to_84',
        'female_85_and_over',
    ]
#}, {
#    'category':
#        'race',
#    'denominator':
#        'total_pop',
#    'columns': [
#        'white_pop',
#        'black_pop',
#        'asian_pop',
#        'hispanic_pop',
#        'amerindian_pop',
#        'other_race_pop',
#        'two_or_more_races_pop',
#        'hispanic_any_race',
#        'not_hispanic_pop',
#    ]
#}, {
#    'category':
#        'race age',
#    'denominator':
#        'total_pop',
#    'columns': [
#        'asian_male_45_54',
#        'asian_male_55_64',
#        'black_male_45_54',
#        'black_male_55_64',
#        'hispanic_male_45_54',
#        'hispanic_male_55_64',
#        'white_male_45_54',
#        'white_male_55_64',
#    ]
}, {
    'category':
        'income',
    'denominator':
        'total_pop',
    'columns': [
        'income_less_10000',
        'income_10000_14999',
        'income_15000_19999',
        'income_20000_24999',
        'income_25000_29999',
        'income_30000_34999',
        'income_35000_39999',
        'income_40000_44999',
        'income_45000_49999',
        'income_50000_59999',
        'income_60000_74999',
        'income_75000_99999',
        'income_100000_124999',
        'income_125000_149999',
        'income_150000_199999',
        'income_200000_or_more',
    ]
#}, {
#    'category': 'poverty',
#    'denominator': None,
#    'columns': [
#        'poverty',
#        'gini_index',
#    ]
}, {
    'category':
        'housing type',
    'denominator':
        'housing_units',
    'columns': [
        'occupied_housing_units',
        'housing_units_renter_occupied',
        'vacant_housing_units',
        'vacant_housing_units_for_rent',
        'vacant_housing_units_for_sale',
        'owner_occupied_housing_units',
        'million_dollar_housing_units',
        'mortgaged_housing_units',
    ]
}, {
    'category':
        'housing size',
    'denominator':
        'housing_units',
    'columns': [
        'dwellings_1_units_detached',
        'dwellings_1_units_attached',
        'dwellings_2_units',
        'dwellings_3_to_4_units',
        'dwellings_5_to_9_units',
        'dwellings_10_to_19_units',
        'dwellings_20_to_49_units',
        'dwellings_50_or_more_units',
        'mobile_homes',
        'group_quarters',
    ]
}, {
    'category':
        'housing age',
    'denominator':
        'housing_units',
    'columns': [
        'housing_built_2005_or_later',
        'housing_built_2000_to_2004',
        'housing_built_1939_or_earlier',
    ]
}, {
    'category':
        'housing rent',
    'denominator':
        'housing_units',
    'columns': [
        'rent_over_50_percent',
        'rent_40_to_50_percent',
        'rent_35_to_40_percent',
        'rent_30_to_35_percent',
        'rent_25_to_30_percent',
        'rent_20_to_25_percent',
        'rent_15_to_20_percent',
        'rent_10_to_15_percent',
        'rent_under_10_percent',
        'rent_burden_not_computed',
    ]
}, {
    'category': 'housing rent',
    'denominator': 'housing_units',
    'columns': ['percent_income_spent_on_rent',]
#}, {
#    'category':
#        'housing mobility',
#    'denominator':
#        'housing_units',
#    'columns': [
#        'different_house_year_ago_different_city',
#        'different_house_year_ago_same_city'
#    ]
}, {
    'category':
        'family',
    'denominator':
        'households',
    'columns': [
        'married_households',
        'nonfamily_households',
        'family_households',
#        'households_public_asst_or_food_stamps',
        'male_male_households',
        'female_female_households',
        'children',
#        'children_in_single_female_hh',
        'families_with_young_children',
        'two_parent_families_with_young_children',
        'two_parents_in_labor_force_families_with_young_children',
        'two_parents_father_in_labor_force_families_with_young_children',
        'two_parents_mother_in_labor_force_families_with_young_children',
        'two_parents_not_in_labor_force_families_with_young_children',
#        'one_parent_families_with_young_children',
#        'father_one_parent_families_with_young_children',
#        'father_in_labor_force_one_parent_families_with_young_children',
    ]
}, {
    'category':
        'cars owned',
    'denominator':
        'total_pop',
    'columns': [
        'no_car',
        'one_car',
        'two_cars',
        'three_cars',
        'four_more_cars',
    ]
}, {
    'category':
        'commuter time',
    'denominator':
        'total_pop',
    'columns': [
        'commute_less_10_mins',
        'commute_10_14_mins',
        'commute_15_19_mins',
        'commute_20_24_mins',
        'commute_25_29_mins',
        'commute_30_34_mins',
        'commute_35_44_mins',
        'commute_45_59_mins',
    ]
}, {
    'category': 'commuter age',
    'denominator': 'total_pop',
    'columns': ['commuters_16_over',]
}, {
    'category':
        'commuter method',
    'denominator':
        'total_pop',
    'columns': [
        'worked_at_home',
        'walked_to_work',
        'commuters_by_public_transportation',
        'commuters_by_bus',
        'commuters_by_car_truck_van',
        'commuters_by_carpool',
        'commuters_by_subway_or_elevated',
        'commuters_drove_alone',
    ]
}, {
    'category':
        'education degree',
    'denominator':
        'total_pop',
    'columns': [
        'associates_degree',
        'bachelors_degree',
        'bachelors_degree_2',
        'bachelors_degree_or_higher_25_64',
        'high_school_diploma',
        'high_school_including_ged',
        'less_one_year_college',
        'masters_degree',
        'one_year_more_college',
        'less_than_high_school_graduate',
        'graduate_professional_degree',
        'some_college_and_associates_degree',
    ]
#}, {
#    'category':
#        'education grade',
#    'denominator':
#        'total_pop',
#    'columns': [
#        'in_school',
#        'in_grades_1_to_4',
#        'in_grades_5_to_8',
#        'in_grades_9_to_12',
#        'in_undergrad_college',
#    ]
}, {
    'category':
        'education male age',
    'denominator':
        'total_pop',
    'columns': [
        'male_45_64_associates_degree',
        'male_45_64_bachelors_degree',
        'male_45_64_graduate_degree',
        'male_45_64_less_than_9_grade',
        'male_45_64_grade_9_12',
        'male_45_64_high_school',
        'male_45_64_some_college',
    ]
}, {
    'category':
        'labor status',
    'denominator':
        'total_pop',
    'columns': [
        'employed_pop',
#        'unemployed_pop',
        'pop_in_labor_force',
        'not_in_labor_force',
        'civilian_labor_force',
        'armed_forces',
        'workers_16_and_over',
    ]
}, {
    'category':
        'labor occupation',
    'denominator':
        'total_pop',
    'columns': [
        'employed_agriculture_forestry_fishing_hunting_mining',
        'employed_arts_entertainment_recreation_accommodation_food',
        'employed_construction',
        'employed_education_health_social',
        'employed_finance_insurance_real_estate',
        'employed_information',
        'employed_manufacturing',
        'employed_other_services_not_public_admin',
        'employed_public_administration',
        'employed_retail_trade',
        'employed_science_management_admin_waste',
        'employed_transportation_warehousing_utilities',
        'employed_wholesale_trade',
        'occupation_management_arts',
        'occupation_natural_resources_construction_maintenance',
        'occupation_production_transportation_material',
        'occupation_sales_office',
        'occupation_services',
        'management_business_sci_arts_employed',
        'sales_office_employed',
    ]
#}, {
#    'category':
#        'language',
#    'denominator':
#        'total_pop',
#    'columns': [
#        'speak_only_english_at_home',
#        'speak_spanish_at_home',
#        'speak_spanish_at_home_low_english',
#    ]
}]
