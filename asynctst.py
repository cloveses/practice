import asyncio
from datetime import datetime
async def work(x):
    while 1:
        print('pause...')
        await asyncio.sleep(x)
        print('Stop...')

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def time_kick():
    pass

start = datetime.now()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop,args=(new_loop,))
t.start()

asyncio.run_coroutine_threadsafe(work(3),new_loop)
asyncio.run_coroutine_threadsafe(work(6),new_loop)
