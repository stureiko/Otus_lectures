import asyncio
import aiohttp
from tqdm import tqdm

async def fetch_data(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        return await response.json()

async def main(url: str = 'http://localhost:5002'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url + '/total') as response:
            total = await response.json()
            total = total['total']
            
        tasks = []
        for index in range(total):
            tasks.append(
                asyncio.create_task(fetch_data(session, f'{url}/texts/{index}'))
            )
        res = [
            await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))
        ]

if __name__ == '__main__':
    asyncio.run(main())