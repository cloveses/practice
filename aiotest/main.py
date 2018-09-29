from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.json_response({'status':0,'data':{'a':1,'b':1}})

app = web.Application()
app.add_routes(routes)
web.run_app(app)