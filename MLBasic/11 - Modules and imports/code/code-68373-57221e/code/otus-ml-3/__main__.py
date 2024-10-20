import helpers as hlp
from utils import load_from_csv

print('started')

f_content = load_from_csv('user.csv')
hlp.parse_user_data(f_content)

print('finished')
