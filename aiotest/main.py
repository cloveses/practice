from aiohttp import web
import logging

# access_log = logging.getLogger('aiohttp.access')
# logging.basicConfig(level=logging.DEBUG)
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    print(request.query)
    # access_log.info('abcc...........')
    return web.json_response({'status':0,'data':{'a':1,'b':1}})

@routes.post('/')
async def phello(request):
    data = await request.post()
    print(data)
    print('aaabb')
    return web.json_response({'status':0,'data':{'a':2,'b':2}})


app = web.Application(debug=True)
app.add_routes(routes)
for rsrc in app.router.resources():
    print(rsrc)
web.run_app(app)