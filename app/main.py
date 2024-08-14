from fastapi import FastAPI, Response
from .network import routes_api

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
