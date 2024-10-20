from pytest import fixture

from db_helper import User


# @fixture(scope='module')
@fixture
def otus_user():
    username = 'Otus'
    return username, User(username=username)
