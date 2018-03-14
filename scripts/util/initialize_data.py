import pandas as pd
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
e_records_df = pd.merge(
    profiles_df,
    preactions_df,
    on=['EmployeeNumber', 'EducationField']
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


def randomize_termination(month, year=2017):
    fday, day = monthrange(year, month)
    return date(year, month, day)


termination_date_list = [
    randomize_termination(month) if separated else None
    for month, separated in zip(
        np.random.randint(10, 13, count),
        e_records_df['Separated']
    )
]

promotion_date_list = [
    get_relative_date(year, records_date) for year in
    e_records_df['YearsSinceLastPromotion']
]

promotion_days = [
    (records_date - date).days
    for date in promotion_date_list
]

hiring_date_list = [
    get_relative_date(year, termination_date) if termination_date
    else get_relative_date(year, last_hire_date) for year, termination_date in
    zip(e_records_df['YearsAtCompany'], termination_date_list)
]

e_records_df['promotion_date'] = promotion_date_list
e_records_df['hiring_date'] = hiring_date_list
