from fastapi import FastAPI

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
