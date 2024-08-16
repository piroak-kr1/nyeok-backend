import os, sys

# Ensure import from source code root directory. ex) `from main`
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
from fastapi import FastAPI, Response
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Coordinate
from network import routes_api


app = FastAPI()


@app.get("/")
async def hello_world() -> str:
    return "Hello, world!"


@app.get("/echo")
async def echo(message: str | None = None) -> str:
    if message is None:
        return f"Test echo with /echo?message=<message>"
    else:
        print(f"Received message: {message}")
        return f"{message}"


@app.get("/compute_routes_sample")
async def compute_routes_sample() -> Response:
    resultJson: str = await routes_api.sample_compute_routes()
    return Response(content=resultJson, media_type="application/json")


class RouteRequest(BaseModel):
    origin: Coordinate
    destination: Coordinate


@app.post("/compute_routes")
async def compute_routes(request: RouteRequest) -> Response:
    origin: Coordinate = request.origin
    destination: Coordinate = request.destination
    resultJson: str = await routes_api.compute_routes(
        origin=origin, destination=destination
    )
    return Response(content=resultJson, media_type="application/json")


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find('"GET /readiness HTTP/1.1" 200') == -1


# Filter out /readiness
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@app.get("/readiness")
async def readiness():
    return {"status": "ok"}
