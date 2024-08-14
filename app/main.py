from fastapi import FastAPI
from .network import routes_api
from typing import MutableSequence
from google.maps.routing_v2 import RouteLegStep

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


# @app.get("/compute_routes")
# async def compute_routes() -> MutableSequence[RouteLegStep]:
#     stepsList = await routes_api.sample_compute_routes()
#     return stepsList
