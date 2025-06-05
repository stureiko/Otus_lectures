from sqlalchemy import create_engine
import os

def connect_to_postgres(user:str = 'otus_user',
                        password: str='otus_password',
                        db_name: str='otus_db'):
    conn_string = f'postgresql://{user}:{password}@127.0.0.1/{db_name}'
    db = create_engine(conn_string)
    return db
#

TOKEN = os.environ["INVEST_TOKEN"]
