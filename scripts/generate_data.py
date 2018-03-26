from util.regression_promotion_days import lamb
from util.initialize_data import *
from util.models import Employee, Actions
from datetime import timedelta, datetime as dt
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

        temp_df.loc[:, year_column_list] = (temp_df[year_column_list] - 1)

        temp_df = temp_df.loc[
            (temp_df['yearsatcompany'] >= 0) &
            (temp_df['yearsincurrentrole'] >= 0) &
            (temp_df['yearssincelastpromotion'] >= 0) &
            (temp_df['yearswithcurrmanager'] >= 0)
        ]
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

simulated_employees_df = pd.DataFrame(simulated_employees)

main_e_records_df = pd.concat([e_records_df, simulated_employees_df])

main_e_records_df['record_year'] = main_e_records_df['termination_date'].apply(
    lambda x: x.year if x is not None else '2017'
)

main_e_records_df['record_date'] = main_e_records_df['record_year'].apply(
    lambda x: date(int(x), 12, 31)
)

main_e_records_df.sort_values('hiring_date', ascending=True, inplace=True)
main_e_records_df.drop('employeenumber', axis=1, inplace=True)
main_e_records_df.reset_index(drop=True, inplace=True)
main_e_records_df.reset_index(inplace=True)
main_e_records_df.rename(columns={'index': 'employeenumber'}, inplace=True)
main_e_records_df['employeenumber'] += 1

# days since last promotion

main_last_promotion_date_list = [
    get_relative_date(year, date) for year, date in
    zip(
        main_e_records_df['yearssincelastpromotion'],
        main_e_records_df['record_date']
    )
]

main_promotion_days = [
    (record_date - date).days for date, record_date in
    zip(
        main_last_promotion_date_list,
        main_e_records_df['record_date'].tolist()
    )
]

main_hiring_promotion_list = [
    (hiring_promotion_diff(
        promotion_date,
        record.hiring_date
    )).days for promotion_date, record in
    zip(
        main_last_promotion_date_list,
        main_e_records_df.itertuples())
]

promotion_dict = {
    idx: {'count': min(
        level - 1,
        np.random.poisson(lamb * promotion_range)
    )} for idx, level, promotion_range in
    zip(
        main_e_records_df.index,
        main_e_records_df['joblevel'],
        main_hiring_promotion_list
    )
}

for key, delta in zip(promotion_dict.keys(), main_hiring_promotion_list):
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

for delta, hiring in zip(temp_delta, main_e_records_df['hiring_date'].values):
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
        main_e_records_df.drop(
            ['hiring_date', 'promotion_date','termination_date', 'record_year', 'record_date'], axis=1
        ).iloc[key].to_dict()
    )

    print(f"{key} >>> Employee Number: {temp_employee.employeenumber} of Job Level {temp_employee.joblevel} was promoted {promotion_dict[key]['count']} times")
    actions = temp_employee.demote_n(
        promotion_dict[key]['promotion_dates'],
        promotion_dict[key]['count']
    )

    temp_actions_list.append(actions)

promotion_df = pd.concat(temp_actions_list)

terminations_list = []

hirings_promoted_df = promotion_df.sort_values('date').groupby('employeenumber', as_index=False).first()

hirings_promoted_df.loc[:, 'roleto'] = ''
hirings_promoted_df.loc[:, 'joblevelto'] = ''

hirings_promoted_df = hirings_promoted_df.merge(main_e_records_df[['hiring_date', 'employeenumber']], how='left', on = 'employeenumber')

hirings_promoted_df.rename(columns={
    'joblevelfrom': 'joblevelto',
    'joblevelto': 'joblevelfrom',
    'rolefrom': 'roleto',
    'roleto': 'rolefrom',
}, inplace=True)

hirings_promoted_df.drop('date', axis=1, inplace=True)
hirings_promoted_df.rename(columns={'hiring_date': 'date'}, inplace=True)
hirings_promoted_df.loc[:,'action_type'] = 'hiring'

hirings_no_promotion_df = main_e_records_df.loc[~main_e_records_df['employeenumber'].isin(hirings_promoted_df['employeenumber'])]
to_retain = ['employeenumber', 'department', 'jobrole', 'joblevel', 'hiring_date']
hirings_no_promotion_df = hirings_no_promotion_df[to_retain]
hirings_no_promotion_df.rename(
    columns = {
        'jobrole': 'jobroleto',
        'joblevel': 'joblevelto',
        'hiring_date': 'date'
    },
    inplace=True
)

hirings_no_promotion_df.loc[:,'rolefrom'] = ''
hirings_no_promotion_df.loc[:,'joblevelfrom'] = ''
hirings_no_promotion_df.loc[:,'actions_id'] = ''
hirings_no_promotion_df.loc[:,'salary'] = ''
hirings_no_promotion_df.loc[:,'supervisornumber'] = ''
hirings_no_promotion_df.loc[:,'action_type'] = 'hiring'

for e in main_e_records_df.loc[~main_e_records_df['termination_date'].isnull()][['employeenumber', 'termination_date', 'jobrole', 'joblevel', 'department']].itertuples():
    terminations_list.append(Actions({
        'date': e.termination_date,
        'employeenumber': e.employeenumber,
        'rolefrom': e.jobrole,
        'joblevelfrom': e.joblevel,
        'department': e.department,
        'action_type': 'termination'
    }))

terminations_df = pd.DataFrame([t.to_series() for t in terminations_list])

actions_df = pd.concat([
    hirings_promoted_df,
    hirings_no_promotion_df,
    terminations_df,
    promotion_df
])

actions_df.drop('actions_id', inplace=True, axis=1)
actions_df.sort_values(['date', 'employeenumber'], ascending=[True, True], inplace=True)
actions_df.reset_index(drop=True, inplace=True)
actions_df.reset_index(inplace=True)
actions_df.rename(columns={'index': 'actions_id'}, inplace=True)
actions_df.actions_id += 1

today = dt.today().strftime('%Y-%m-%d %H%M')
actions_df.to_csv(data_dir + f'{today} {seed} actions log.csv')
main_e_records_df.to_csv(data_dir + f'{today} {seed} employee db.csv')
