import sys

print(sys.path)

# from .utils import MAX_USER_AGE
from users.utils import MAX_USER_AGE
# from .. import schemas
import schemas


def get_by_id(user_id):
    schemas.valdate_user(user_id)
    print(f'get data for user {user_id}, {MAX_USER_AGE}')


if __name__ == '__main__':
    print(dir(globals()))
    print(globals())
    print(__doc__)
    print('__name__', __name__)
