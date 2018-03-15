from util.regression_promotion_days import lamb
from util.initialize_data import e_records_df, promotion_date_list
from datetime import timedelta
import numpy as np


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

count_promotion_list = [
    min(
        level - 1,
        np.random.poisson(lamb * promotion_range)
    ) for level, promotion_range in
    zip(e_records_df['JobLevel'], hiring_promotion_list)
]
