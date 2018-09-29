from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    print(request.query)
    return web.json_response({'status':0,'data':{'a':1,'b':1}})

@routes.post('/')
async def phello(request):
    data = await request.post()
    print(data)
    return web.json_response({'status':0,'data':{'a':2,'b':2}})


app = web.Application(debug=True)
app.add_routes(routes)
web.run_app(app)