import os
import pandas as pd
from tinkoff.invest import Client, InstrumentStatus
from sqlalchemy import create_engine

TOKEN = os.environ["INVEST_TOKEN"]


def connect_to_postgres(user:str = 'otus_user',
                        password: str='otus_password',
                        db_name: str='otus_db'):
    conn_string = f'postgresql://{user}:{password}@127.0.0.1/{db_name}'
    db = create_engine(conn_string)
    return db

def main():
    with Client(TOKEN) as client:
        shares = client.instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE)
        shares_df = pd.DataFrame(shares.instruments)

        shares_df = shares_df[['figi', 'ticker', 'class_code','first_1min_candle_date', 'currency', 'name']]
        # будем загружать только те акции, которые торгуются в рублях
        shares_df = shares_df[shares_df['currency']=='rub'].reset_index(drop=True)
        engine = connect_to_postgres()

        with engine.connect() as conn:
            shares_df.to_sql('stocks_info', conn, if_exists='replace',
                      schema='metadata', index=False)

if __name__ == "__main__":
    main()