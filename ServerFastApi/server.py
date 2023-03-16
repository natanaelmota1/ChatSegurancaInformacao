from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import hashlib
import secrets

app = FastAPI()

class Message(BaseModel):
    sender: str
    message: list
    p: int
    key: str

class Client(BaseModel):
    name: str
    password: str
    key: str

class ClientName(BaseModel):
    name: str

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

def findClientByName(name):
    for client in clients:
        if client.name == name:
            return client
    return None

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

@app.post("/client/check")
async def check_client(client_name: ClientName):
    client = findClientByName(client_name.name)
    if client:
        return {"registered": True}
    else:
        return {"registered": False}

@app.post("/client/register")
async def register_client(client: Client):
    existing_client = findClientByName(client.name)
    if existing_client:
        if not existing_client.password:
            existing_client.password = client.password
            return {"message": "Senha cadastrada com sucesso"}
        elif existing_client.password != client.password:
            raise HTTPException(status_code=400, detail="Senha incorreta")
        else:
            existing_client.key = client.key
            return {"message": "Senha correta"}
    else:
        clients.append(client)
        return {"message": "Cliente criado com sucesso"}
    
@app.post("/client/auth")
async def auth_client(client: Client):
    existing_client = findClientByName(client.name)
    if existing_client:
        if not existing_client.password:
            raise HTTPException(status_code=400, detail="Senha incorreta")
        elif existing_client.password != client.password or existing_client.key != client.key:
            raise HTTPException(status_code=400, detail="Senha incorreta")
        else:
            return {"message": "Senha correta"}

@app.get("/clients")
async def get_clients():
    contatos = []
    for client in clients:
        contatos.append({"name":client.name, "key":client.key})
    return contatos


