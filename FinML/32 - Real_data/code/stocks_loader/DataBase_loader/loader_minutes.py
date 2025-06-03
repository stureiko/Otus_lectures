import asyncio
import os
from datetime import timedelta
import pandas as pd
from tinkoff.invest import AsyncClient, CandleInterval
from tinkoff.invest.utils import now
import asyncpg
import time
from sqlalchemy import create_engine

TOKEN = os.environ["INVEST_TOKEN"]
DATABASE_URL = "postgresql://otus_user:otus_password@localhost/otus_db" # Your database connection string
TABLE_NAME = "test_table"

async def store_candle_data(conn, candle, figi, ticker):
    """Stores a single candle's data in the database."""
    try:
        await conn.execute(
            f"""
            INSERT INTO active_shares.{ticker} (figi,  time, open, close, high, low, volume)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            figi,
            candle.time,
            float(str(candle.open.units) + '.' + str(candle.open.nano)),
            float(str(candle.high.units) + '.' + str(candle.high.nano)),
            float(str(candle.low.units) + '.' + str(candle.low.nano)),
            float(str(candle.close.units) + '.' + str(candle.close.nano)),
            candle.volume
        )
    except asyncpg.exceptions.UniqueViolationError:
        print(f"Duplicate candle data detected, skipping: {candle.time}")
    except Exception as e:
        print(f"Error storing candle data: {e}")


async def download_tickers(figi, ticker_name):

    async with AsyncClient(TOKEN) as client:


        conn = await asyncpg.connect(DATABASE_URL)

        print(ticker_name)
        # Create table if it doesn't exist (only run once)
        await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS active_shares.{ticker_name} (
                figi TEXT NOT NULL,
                time TIMESTAMP WITH TIME ZONE NOT NULL PRIMARY KEY,
                open NUMERIC,
                close NUMERIC,
                high NUMERIC,
                low NUMERIC,
                volume INTEGER
            );
        """)
        async for candle in client.get_all_candles(
            figi=figi,
            from =now() - timedelta(days=7),
            to = now(),
            interval = CandleInterval.CANDLE_INTERVAL_HOUR,
        ):
            await store_candle_data(conn, candle, figi, ticker_name)
            print(f"Stored candle data for {ticker_name}")
        await conn.close()
        time.sleep(secs=10)



def connect_to_postgres(user:str = 'otus_user',
                        password: str='otus_password',
                        db_name: str='otus_db'):
    conn_string = f'postgresql://{user}:{password}@127.0.0.1/{db_name}'
    db = create_engine(conn_string)
    return db
#
async def main():
    loop = asyncio.get_running_loop()
    engine = connect_to_postgres()
    with engine.connect() as conn:
        figies = pd.read_sql('SELECT DISTINCT figi, ticker from metadata.active_metadata', conn)
        # print(figies)
    tasks = [loop.create_task(download_tickers(figi, ticker_name )) for figi, ticker_name in zip(figies['figi'], figies['ticker'])]
    # print(tasks)
    await asyncio.gather(*tasks, return_exceptions=True)
if __name__ == "__main__":
    asyncio.run(main())
