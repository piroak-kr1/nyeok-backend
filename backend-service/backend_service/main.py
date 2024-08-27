import logging
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from geoalchemy2 import Geometry
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Coordinate
from sqlalchemy import Row, Select, select, cast
from geoalchemy2.functions import ST_X, ST_Y
from sqlalchemy.orm import Session


from .outbound import routes_api
from .models import Place
from database_core import db
from database_core.tables import Place as DBPlace


app = FastAPI()

db.setup(
    username="superuser",
    password="wrongpassword",
    hostname="localhost",
    port=5432,
    databasename="database",
)


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


@app.get("/places_sample", response_model=Place)
def places_sample(session: Session = Depends(db.get_session_yield)):
    # cast Geography to Geometry (ST_X, ST_Y only works with Geometry)
    statement: Select[tuple[DBPlace, float, float]] = select(
        DBPlace,
        ST_X(cast(DBPlace.coordinate, Geometry("POINT", srid=4326))),
        ST_Y(cast(DBPlace.coordinate, Geometry("POINT", srid=4326))),
    )

    single_record: Row[tuple[DBPlace, float, float]] | None = session.execute(
        statement
    ).first()
    if single_record is None:
        raise ValueError("No records found")

    dbPlace, longitude, latitude = single_record
    return Place.from_sqlalchemy_model(dbPlace, longitude, latitude)


@app.get("/compute_routes_sample")
async def compute_routes_sample() -> JSONResponse:
    resultJson: str = await routes_api.sample_compute_routes()
    return JSONResponse(content=resultJson, media_type="application/json")


class RouteRequest(BaseModel):
    origin: Coordinate
    destination: Coordinate


@app.post("/compute_routes")
async def compute_routes(request: RouteRequest) -> JSONResponse:
    origin: Coordinate = request.origin
    destination: Coordinate = request.destination
    resultJson: str = await routes_api.compute_routes(
        origin=origin, destination=destination
    )
    return JSONResponse(content=resultJson, media_type="application/json")


@app.get("/readiness")
async def readiness():
    return {"status": "ok"}


# Filter out /readiness
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find('"GET /readiness HTTP/1.1" 200') == -1


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
