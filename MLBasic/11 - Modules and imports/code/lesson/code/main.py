import accounts
import users

# from users import *
# from users import get

if __name__ == '__main__':
    print('I am main')
    users.get_by_id(123)
    # get.get_by_id(123)
    accounts.get_by_id(123)
