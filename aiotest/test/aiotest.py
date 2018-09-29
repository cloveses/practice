import asyncio
import aiohttp


async def fetch_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            print(r.status)
            print(await r.json())

base_url = 'http://localhost:8080/'

req_lsts = [
    (fetch_get,base_url),
    (fetch_get,base_url,{'a':3}),

    ]

async def fetch_gets():
    for req_lst in req_lsts:
        if len(req_lst) == 2:
            await req_lst[0](req_lst[1])
        else:
            await req_lst[0](req_lst[1],data=req_lst[2])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_gets())
    loop.close()

# cookies = {}

# async def fetch():
#     async with aiohttp.ClientSession(cookies=cookies) as session:
#         async with session.get('https://api.github.com/events',params=params) as r:
#             print(r.status)
#             # print(await r.text(encodeing='utf-8'))
#             # r.read()
#             # r.json()
#             # r.content.read(10) 响应内容太大时，使用的流式响应内容

#             # verify_ssl=False 不验证ssl证书

#         #session.post(url,data=data,headers=headers)
#         # data 是字典形式是发送的是表单形式，是字符串会直接发送出去，是文件对象会以流式上传
