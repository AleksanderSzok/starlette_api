from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def json_to_xml(request):
    pass


app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/to_xml', json_to_xml, methods=["POST"])
])