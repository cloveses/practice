from aiohttp import web
import aiohttp_mako
import logging

access_log = logging.getLogger('aiohttp.access')
logging.basicConfig(level=logging.DEBUG)
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

@aiohttp_mako.template('index.html')
@routes.get('/mako')
async def mako_test(request):
    return {'aa':'22'}

app = web.Application(debug=True)
app.add_routes(routes)
# for rsrc in app.router.resources():
#     print(rsrc)
lookup = aiohttp_mako.setup(app, input_encoding='utf-8',
    output_encoding='utf-8',
    default_filters=['decode.utf8'])
lookup.put_string('index.html','''<html><body><h1>${aa}</h1>${aa}</body></html>''')
web.run_app(app)