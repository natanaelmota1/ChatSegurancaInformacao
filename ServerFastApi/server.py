from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
# import uvicorn


app = FastAPI()

class Message(BaseModel):
    sender: str
    message: list
    p: int
    key: str

class Client(BaseModel):
    name: str
    key: str

messages = [
    "test message",
    "another"
]
clients = []

@app.post("/message")
async def send_message(message: Message):
    messages.append(message)
    return {"message": message}

@app.get("/messages")
async def get_messages() -> dict:
    return { "data": messages }

@app.post("/client")
async def send_client(client: Client):
    print(client.name, client.key)
    clients.append(client)
    return {"message": "Cliente criado com sucesso"}

@app.get("/clients")
async def get_clients():
    return clients


# if __name__ == "__main__":
    # uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)