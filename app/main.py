import asyncio

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from app.json_to_xml_converter import JsonToXml


async def homepage(request):
    return JSONResponse({"hello": "world"})


async def receive_xml_from_json(request):
    data = await request.json()
    json_xml = JsonToXml(json_string=data)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, json_xml.json_to_xml)
    return Response(content=str(json_xml), media_type="application/xml")


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/to_xml", receive_xml_from_json, methods=["POST"]),
    ],
)
