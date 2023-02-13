import asyncio
import json
import logging

from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from app.json_to_xml_converter import JsonToXml


async def homepage(request):
    return JSONResponse({"hello": "world"})


async def receive_xml_from_json(request):
    try:
        data = await request.json()
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Wrong json format, exception: \n{e}")
        data = json.dumps({"error": "wrong json format", "exception": str(e)})
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
