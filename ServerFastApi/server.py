from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel


app = FastAPI()

class Message(BaseModel):
    sender: str
    message: list
    p: int
    key: str

class Client(BaseModel):
    name: str
    key: str

messages = []
clients = []

@app.post("/message")
async def send_message(message: Message):
    messages.append(message)
    return {"message": message}

@app.get("/messages")
async def get_messages():
    print(messages)
    return messages

@app.post("/client")
async def send_client(client: Client):
    print(client.name, client.key)
    clients.append(client)
    return {"message": "Cliente criado com sucesso"}

@app.get("/clients")
async def get_clients():
    return clients
