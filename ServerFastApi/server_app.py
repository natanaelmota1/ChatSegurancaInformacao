import asyncio
import websockets
from WebSocket import  websockets
from fastapi import FastAPI, HTTPException
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
clients = set()

def findMessageClient(client_key):
    for message in messages:
        key = message.key
        if (key == client_key):
            message_client = message
            messages.remove(message)
            return message_client
    return ""

@app.websocket("/ws")
async def websocket_endpoint(websocket: websockets.webSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        async for message in websocket:
            # Handle incoming messages
            message = Message.parse_raw(message)
            messages.append(message)

            # Send messages to clients
            for client in clients:
                await client.send(message.json())
    finally:
        clients.remove(websocket)

@app.post("/client")
async def send_client(client: Client):
    clients.add(client.key)
    return {"message": "Cliente criado com sucesso"}

@app.get("/clients")
async def get_clients():
    return list(clients)
