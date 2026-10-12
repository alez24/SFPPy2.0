import asyncio
from starlette.requests import Request

from survey.app.main import app, current_family


def build_request():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "client": ("testclient", 50000),
        "root_path": "",
        "http_version": "1.1",
        "app": app,
    }
    return Request(scope)


def test_family_editor_template_renders():
    request = build_request()
    response = asyncio.run(__import__("survey.app.main", fromlist=["home"]).home(request))
    assert response.status_code == 200
    body = response.body.decode("utf-8")
    assert "SFPPy Family Editor" in body


def test_simulator_template_renders():
    request = build_request()
    response = asyncio.run(__import__("survey.app.simulator", fromlist=["home"]).home(request))
    assert response.status_code == 200
    body = response.body.decode("utf-8")
    assert "SFPPy Survey Simulator" in body
