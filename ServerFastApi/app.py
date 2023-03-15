import asyncio
import json
import websockets
from typing import List
import random
from math import pow

a = random.randint(2, 10)

def gcd(a, b):
	if a < b:
		return gcd(b, a)
	elif a % b == 0:
		return b
	else:
		return gcd(b, a % b)

# Generating large random numbers
def gen_key(q):

	key = random.randint(pow(10, 20), q)
	while gcd(q, key) != 1:
		key = random.randint(pow(10, 20), q)

	return key

# Modular exponentiation
def power(a, b, c):
	x = 1
	y = a

	while b > 0:
		if b % 2 != 0:
			x = (x * y) % c
		y = (y * y) % c
		b = int(b / 2)

	return x % c

# Asymmetric encryption
def encrypt(msg, q, h, g):

	en_msg = []

	k = gen_key(q)# Private key for sender
	s = power(h, k, q)
	p = power(g, k, q)
	
	for i in range(0, len(msg)):
		en_msg.append(msg[i])

	for i in range(0, len(en_msg)):
		en_msg[i] = s * ord(en_msg[i])

	return en_msg, p

def decrypt(en_msg, p, key, q):

	dr_msg = ""
	h = power(p, key, q)
	for i in range(0, len(en_msg)):
		dr_msg = dr_msg + chr(int(en_msg[i]/h))
		
	return dr_msg



name = input("Enter your name: ")
q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
private_key = gen_key(q)
h = power(g, private_key, q)
public_key = str(q) + " " + str(h) + " " + str(g)
keys = []
messages_history = []

async def receive_messages(websocket: websockets.WebSocketClientProtocol, name: str, private_key: int, messages_history: List[str]):
    while True:
        message = await websocket.recv()
        message_dict = json.loads(message)
        key = message_dict["key"]
        if key == public_key:
            message_decrypted = message_dict["sender"] + ": " + str(decrypt(message_dict["message"], message_dict["p"], private_key, q))
            if message_decrypted not in messages_history:
                messages_history.append(message_decrypted)
                print(message_decrypted)


async def send_messages(websocket: websockets.WebSocketClientProtocol, name: str, public_key: str, private_key: int):
    while True:
        message_input = input()
        clients_json = await websocket.recv()
        clients = json.loads(clients_json)
        keys = [client["key"] for client in clients if client["key"] != public_key]

        for key in keys:
            en_msg, p = encrypt(message_input, int(key.split(" ")[0]), int(key.split(" ")[1]), int(key.split(" ")[2]))
            message_dict = {"sender": name, "message": en_msg, "p": p, "key": key}
            await websocket.send(json.dumps(message_dict))


async def main():

    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        # Envia o nome do cliente e chave pública
        client_json = {"name": name, "key": public_key}
        await websocket.send(json.dumps(client_json))

        # Recebe todas as mensagens em background
        receive_task = asyncio.create_task(receive_messages(websocket, name, private_key, messages_history))

        # Envia mensagens enquanto o usuário digita
        await send_messages(websocket, name, public_key, private_key)

        # Espera a tarefa de receber terminar
        await receive_task


if __name__ == "__main__":
    asyncio.run(main())
