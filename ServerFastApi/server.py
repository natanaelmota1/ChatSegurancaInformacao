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

def findMessageClient(client_key):
    for message in messages:
        key = message.key
        if (key == client_key):
            message_client = message
            messages.remove(message)
            return message_client
    return ""

@app.post("/message")
async def send_message(message: Message):
    messages.append(message)
    return {"message": message}

@app.post("/messages")
async def get_messages(client: Client):
    message = findMessageClient(client.key)
    if (message == ""):
        return ""
    else:
        return message

@app.post("/client")
async def send_client(client: Client):
    print(client.name, client.key)
    clients.append(client)
    return {"message": "Cliente criado com sucesso"}

@app.get("/clients")
async def get_clients():
    return clients
