# import accounts
import accounts as acc
import users

# import numpy as np
# import pandas as pd
# import matplotlib.plot as plt
# from math import sin, asin, cos, acos, tan, atan, pi, inf, cosh
from math import *  # bad practice
from math import (
    sin, asin, cos,
    acos, tan, atan,
    pi, inf,
)

# from accounts import get_by_id
# from users import get_by_id
# from accounts import *
# from users import *

if __name__ == '__main__':
    print('I am __main__')
    users.get_by_id(123)
    acc.get_by_id(123)
    # accounts.get_by_id(123)
    # get_by_id(123)


