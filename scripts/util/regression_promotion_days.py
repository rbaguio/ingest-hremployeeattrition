import numpy as np
from scipy import stats
import pandas as pd
from util.initialize_data import promotion_days
# from matplotlib import pyplot as plt

promotion_series = pd.Series(promotion_days)
x = [np.log(1 - (n / 100)) for n in range(1, 100)]
y = [np.percentile(promotion_series, n) for n in range(1, 100)]

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# plt.plot(x,y,'o', label='original_data')
# plt.plot(x, [intercept + slope * z for z in x], 'r', label = 'fitted line')

# plt.show()

lamb = -1 / slope
