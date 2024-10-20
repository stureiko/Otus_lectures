import sys
import helpers as hlp
from utils import load_from_csv
from pathlib import Path

# ROOT = Path(__file__).resolve().parent.parent.parent
# # print(ROOT)
# sys.path.append(str(ROOT))

# import some_module

# print(sys.path)

print('started')

f_content = load_from_csv('user.csv')
hlp.parse_user_data(f_content)

print('finished')
