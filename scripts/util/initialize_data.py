import pandas as pd
import os
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta, datetime as dt
from util.data import data_dir
from calendar import monthrange

np.random.seed(2000)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

profiles_df = pd.read_csv(data_dir + 'data03_Profiles.csv')
preactions_df = pd.read_csv(data_dir + 'data03_preAction.csv')
roles_df = pd.read_csv(data_dir + 'data03_Roles.csv')
e_records_df = pd.merge(
    profiles_df,
    preactions_df,
    on=['EmployeeNumber', 'EducationField']
)

roles_summary = roles_df.groupby(
    ['Department', 'JobRole', 'JobLevel', 'RoleID']
).count().reset_index().drop('EducationField', axis=1)

hierarchy_dict = {
    ('Human Resources', 'Human Resources'): 1,
    ('Human Resources', 'Manager'): 2,
    ('Research & Development', 'Laboratory Technician'): 1,
    ('Research & Development', 'Research Scientist'): 2,
    ('Research & Development', 'Research Director'): 3,
    ('Research & Development', 'Manufacturing Director'): 3,
    ('Research & Development', 'Healthcare Representative'): 3,
    ('Research & Development', 'Manager'): 4,
    ('Sales', 'Manager'): 3,
    ('Sales', 'Sales Executive'): 2,
    ('Sales', 'Sales Representative'): 1
}

subdepartment_dict = {
    ('Human Resources', 'Human Resources'): 1,
    ('Human Resources', 'Manager'): 1,
    ('Research & Development', 'Laboratory Technician'): 1,
    ('Research & Development', 'Research Scientist'): 1,
    ('Research & Development', 'Research Director'): 1,
    ('Research & Development', 'Manufacturing Director'): 2,
    ('Research & Development', 'Healthcare Representative'): 2,
    ('Research & Development', 'Manager'): 2,
    ('Sales', 'Manager'): 1,
    ('Sales', 'Sales Executive'): 1,
    ('Sales', 'Sales Representative'): 1
}

roles_summary['hierarchy'] = roles_summary.transform(
    lambda df: (df['Department'], df['JobRole']), axis=1
).map(hierarchy_dict)

roles_summary['subdepartment'] = roles_summary.transform(
    lambda df: (df['Department'], df['JobRole']), axis=1
).map(subdepartment_dict)

roles_summary.columns = roles_summary.columns.str.lower()

roles_df['hierarchy'] = roles_df.transform(
    lambda df: (df['Department'], df['JobRole']), axis=1
).map(hierarchy_dict)

roles_df['subdepartment'] = roles_df.transform(
    lambda df: (df['Department'], df['JobRole']), axis=1
).map(subdepartment_dict)

e_records_df = pd.merge(
    e_records_df,
    roles_df,
    on=['EducationField', 'RoleID']
)

last_hire_date = date(2017, 12, 4)
records_date = date(2017, 12, 31)

count = len(e_records_df)


def get_relative_date(years, datefrom, dow=0):
    years_diff = datefrom.year - years
    first_day_of_dec = date(years_diff, 12, 1)
    if first_day_of_dec.weekday() != 0:
        last_hire_date_of_year = date(years_diff, 12, 1) + \
            timedelta(days=(7 - first_day_of_dec.weekday()))
    else:
        last_hire_date_of_year = first_day_of_dec

    day_delta = (last_hire_date_of_year - date(years_diff, 1, 1)).days
    random_day = np.random.randint(1, day_delta)
    est_date = dt.strptime(f'{random_day} {years_diff}', '%j %Y').date()

    return est_date - relativedelta(weekday=dow)


def randomize_termination(hiring_date, year=2017):
    day_start = max(
        1,
        (hiring_date - date(2017, 1, 1)).days
    )
    random_day = np.random.randint(day_start, 338)
    return dt.strptime(f'{random_day} {year}', '%j %Y').date()


promotion_date_list = [
    get_relative_date(year, records_date) for year in
    e_records_df['YearsSinceLastPromotion']
]

promotion_days = [
    (records_date - date).days
    for date in promotion_date_list
]

hiring_date_list = [
    get_relative_date(year, last_hire_date) for year in
    e_records_df['YearsAtCompany']
]

termination_date_list = [
    randomize_termination(hiring_date) if separated else None
    for hiring_date, separated in zip(
        hiring_date_list,
        e_records_df['Separated']
    )
]
e_records_df['promotion_date'] = promotion_date_list
e_records_df['hiring_date'] = hiring_date_list
e_records_df['termination_date'] = termination_date_list

dept_names = ['hr', 'rd', 'rdcore', 'sales']

transition_filenames = [
    x for x in os.listdir(data_dir) if x.startswith('transition')
]

transition_dict = {
    dept: pd.read_csv(data_dir + text, index_col=0)
    for dept, text in zip(dept_names, transition_filenames)
}

for k, v in transition_dict.items():
    v.index.name = 'From'
    v.columns.name = 'To'

transition_dir = {
    'Sales': {1: 'sales'},
    'Research & Development': {
        1: 'rdcore',
        2: 'rd'
    },
    'Human Resources': {1: 'hr'}
}
