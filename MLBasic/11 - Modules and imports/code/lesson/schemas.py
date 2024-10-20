import os

print(os.name)

if os.name == 'posix':
    print('unix import')
else:
    print('non unix import')

try:
    from pydantic import json
    # logger.info('using v1')
except ImportError:
    from pydantic.v1 import json
    # logger.info('using v2')

print('hello')


def valdate_user(user):
    print('valdate_user')
