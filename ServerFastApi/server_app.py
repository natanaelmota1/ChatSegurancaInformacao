from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    sender: str
    message: str

class Client(BaseModel):
    name: str
    websocket: WebSocket

clients = []

@app.websocket("/ws/{client_name}")
async def websocket_endpoint(client_name: str, websocket: WebSocket):
    await websocket.accept()
    client = Client(name=client_name, websocket=websocket)
    add_client(client)
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(sender=client_name, message=data)
            await send_to_all_clients(message)
    except WebSocketDisconnect:
        remove_client(client)

def add_client(client: Client):
    clients.append(client)

def remove_client(client: Client):
    clients.remove(client)

async def send_to_all_clients(message: Message):
    for client in clients:
        await client.websocket.send_json(message.dict())

@app.get("/clients")
async def get_clients():
    return [client.name for client in clients]