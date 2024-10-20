import helpers as hlp
# from utils.csv import load_from_csv
from utils import load_from_csv
from utils.json import load_from_stream

print('started')

f_content = load_from_csv('user.csv')
hlp.parse_user_data(f_content)

print('finished')
