from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_world() -> str:
    return "Hello, World!"


@app.get("/echo")
async def echo(message: str | None = None) -> str:
    if message is None:
        return f"Test echo with /echo?message=<message>"
    else:
        return f"echo: {message}"
