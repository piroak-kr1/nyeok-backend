from fastapi import APIRouter, FastAPI, Response
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Coordinate
from .network import routes_api

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def hello_world() -> str:
    return "Hello, world!"


@api_router.get("/echo")
async def echo(message: str | None = None) -> str:
    if message is None:
        return f"Test echo with /echo?message=<message>"
    else:
        print(f"Received message: {message}")
        return f"{message}"


@api_router.get("/compute_routes_sample")
async def compute_routes_sample() -> Response:
    resultJson: str = await routes_api.sample_compute_routes()
    return Response(content=resultJson, media_type="application/json")


class RouteRequest(BaseModel):
    origin: Coordinate
    destination: Coordinate


@api_router.post("/compute_routes")
async def compute_routes(request: RouteRequest) -> Response:
    origin: Coordinate = request.origin
    destination: Coordinate = request.destination
    resultJson: str = await routes_api.compute_routes(
        origin=origin, destination=destination
    )
    return Response(content=resultJson, media_type="application/json")


app = FastAPI()
app.include_router(api_router)
