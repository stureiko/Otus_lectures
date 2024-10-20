# import math, random, itertools
import math
import random
import itertools

from utils import load_from_csv
# from math import *
# from utils import *
# from utils import (
#     load_from_csv, load_from_json,
#     load_from_pickle, load_from_blob
# )

# from numpy import *


import helpers as hlp

print('started')

f_content = load_from_csv('user.csv')
hlp.parse_user_data(f_content)
print(min([0, 15]))
# hlp.parse_product_data(f_content)
# hlp.parse_storage_data(f_content)

print('finished')
