from unittest import mock

from db_helper import get_user, User
# import db_helper
# db_helper.get_connection
# from .conftest import otus_user

# def test_mock(otus_user):
#     username, inst = otus_user
#     print(username, inst)


# @mock.patch("db_helper.get_connection", spec=True)

@mock.patch("db_helper.get_connection")
def test_get_user(mocked_get_connection, otus_user):
    username, user = otus_user

    # mocked_get_connection.return_value = Connection(engine)
    mocker_conn = mocked_get_connection.return_value
    mocked_conn_get_user = mocker_conn.get_user_from_conn
    mocked_conn_get_user.return_value = user

    res = get_user(username)

    assert isinstance(res, User)
    assert res.username == user.username

    mocked_conn_get_user.assert_called()
    mocked_conn_get_user.assert_called_once()
    mocked_conn_get_user.assert_called_once_with(username)

    mocked_get_connection.assert_called_once()
    mocked_get_connection.assert_called_once_with()


# def test_abcde(otus_user):
#     print(otus_user)
   