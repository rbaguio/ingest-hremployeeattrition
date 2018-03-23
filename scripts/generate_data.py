from util.regression_promotion_days import lamb
from util.initialize_data import *
from util.models import Employee
from datetime import timedelta
import numpy as np
import pandas as pd

np.random.seed(seed)


def create_employee_class(idx):
    return Employee(
        e_records_df.drop(
            ['promotion_date', 'hiring_date', 'termination_date'],
            axis=1).iloc[idx].to_dict()
    )


def hiring_promotion_diff(promotion_date, hiring_date):
    return max(
        promotion_date - hiring_date - timedelta(days=180),
        timedelta(180)
    )


hiring_promotion_list = [
    (hiring_promotion_diff(
        promotion_date,
        record.hiring_date
    )).days for promotion_date, record in
    zip(last_promotion_date_list, e_records_df.itertuples())
]

promotion_dict = {
    idx: {'count': min(
        level - 1,
        np.random.poisson(lamb * promotion_range)
    )} for idx, level, promotion_range in
    zip(
        e_records_df.index,
        e_records_df['joblevel'],
        hiring_promotion_list
    )
}

for key, delta in zip(promotion_dict.keys(), hiring_promotion_list):
    promotion_dict[key]['delta'] = delta

temp_delta = []
for k, v in promotion_dict.items():
    loopy = True
    # deltas = []
    while loopy:
        temp = np.random.exponential(1 / lamb, v['count']).round(0)
        simulated_delta = sum(temp)
        if simulated_delta <= v['delta']:
            # deltas.extend(temp.tolist())
            temp_delta.append(temp.tolist())
            loopy = False

promotion_dates_list = []

for delta, hiring in zip(temp_delta, hiring_date_list):
    temp = hiring
    temp_date_list = []
    for i in range(len(delta)):
        temp += timedelta(days=delta[i])
        temp_date_list.append(temp.strftime('%Y-%m-%d'))

    promotion_dates_list.append(temp_date_list)


for key, l in zip(promotion_dict.keys(), promotion_dates_list):
    promotion_dict[key]['promotion_dates'] = l[::-1]

temp_actions_list = []

for key in promotion_dict.keys():
    temp_employee = Employee(
        e_records_df.drop(
            ['hiring_date', 'termination_date'], axis=1
        ).iloc[key].to_dict()
    )

    print(f"{key} >>> Employee Number: {temp_employee.employeenumber} of Job Level {temp_employee.joblevel} was promoted {promotion_dict[key]['count']} times")
    actions = temp_employee.demote_n(
        promotion_dict[key]['promotion_dates'],
        promotion_dict[key]['count']
    )

    temp_actions_list.append(actions)

temp_actions_df = pd.concat(temp_actions_list)

actions_df = pd.concat([actions_df, temp_actions_df]).reset_index(drop=True)

# Determine attrition rates since first hire by the company

rate_2017 = sum(e_records_df['separated']) / len(e_records_df)

magnitude = 0.4
adjustment = - 0.18
periodicity = np.radians(3)

attrition_history = pd.DataFrame(
    {'attrition':
        [magnitude * np.sin((y * periodicity)) + adjustment
         for y in range(0, 41)],
     'year': [1977 + a for a in range(0, 41)]}
).sort_values('year', ascending=False)

start_employment = len(e_records_df)

simulated_employees = []

temp_df = e_records_df

for item in attrition_history.itertuples():
    if item.year < 2017 and item.year > 1977:
        print(item.year)
        # print(temp_df)
        temp_df = temp_df.loc[
            e_records_df['hiring_date'].map(
                lambda x: x.year
            ) < item.year
        ]

        year_column_list = [
            'yearsatcompany',
            'yearsincurrentrole',
            'yearssincelastpromotion',
            'yearswithcurrmanager'
        ]

        temp_df.loc[:,year_column_list] = (temp_df[year_column_list] - 1).clip(lower=0)

        count_sim_employees = int(
            len(temp_df) * item.attrition / (1 - item.attrition)
        )

        print(count_sim_employees)

        # print(count_sim_employees)
        sim_employees = [
            Employee().randomize(df=temp_df, yearsfrom=item.year).to_series()
            for i in range(count_sim_employees)
        ]

        simulated_employees.extend(sim_employees)

        temp_df = temp_df.append(pd.DataFrame(sim_employees))
