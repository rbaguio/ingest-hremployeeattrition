import os
import platform


wd = os.getcwd()

if 'Windows' in platform.platform():
    split = '\\'

else:
    split = '/'

data_dir = '/'.join(
    wd.split(split)[:-1] + ['data/']
)
