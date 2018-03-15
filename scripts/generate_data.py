from util.regression_promotion_days import lamb
from util.initialize_data import e_records_df, promotion_date_list
from util.models import Employee
from datetime import timedelta
import numpy as np

np.random.seed(2000)


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
    zip(promotion_date_list, e_records_df.itertuples())
]

count_promotion_dict = {
    employee_number: min(
        level - 1,
        np.random.poisson(lamb * promotion_range)
    ) for employee_number, level, promotion_range in
    zip(
        e_records_df['employeenumber'],
        e_records_df['joblevel'],
        hiring_promotion_list
    )
}
