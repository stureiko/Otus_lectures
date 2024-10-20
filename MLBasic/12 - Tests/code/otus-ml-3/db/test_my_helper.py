# from .db_helper import User


def test_mock(otus_user):
    # user = User(username)
    username, inst = otus_user
    # print(username, inst)
    assert inst.username == username
