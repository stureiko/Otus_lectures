URL = "sqlite:///:memory:"


class User:
    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return self.username

    def delete(self):
        print("deleted user", self)
        return True


class Engine:
    def __init__(self, url: str):
        self.url = url

    def init_connection(self):
        ...

    def destroy_connection(self):
        ...


class Connection:
    def __init__(self, engine: Engine):
        self.engine = engine

    def init_conn(self):
        self.engine.init_connection()

    def get_user_from_conn(self, username: str) -> User:
        pass
        # print("conn get username", username)
        return User(username)


def get_engine(url=URL):
    return Engine(url)


def get_connection(engine=None):
    pass
    # if engine is None:
    #     engine = get_engine()
    #
    # return Connection(engine)


def get_user(username: str):
    conn = get_connection()  # -> ???
    # conn = get_connection(engine='hello')
    # conn = Connection(get_engine())
    # conn.get_user(username)
    return conn.get_user_from_conn(username)
    # return conn.get_user(username.upper())
    # return User('hello')
