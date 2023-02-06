import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_app():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.post(url="/to_xml", data='{"a": "1"}')
        assert response.status_code == 200
        assert response.text == '<?xml version="1.0" ?>\n<root>\n   <a>1</a>\n</root>\n'
