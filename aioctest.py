import asyncio
import aiohttp
 
async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as r:
            print(r.status)
            # print(await r.text())
 
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch())
loop.close()