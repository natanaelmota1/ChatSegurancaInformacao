import asyncio
import json
import random
import threading
from typing import List
import websockets


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

q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
private_key = random.randint(2, q-1)

h = pow(g, private_key, q)

uri = 'ws://localhost:8000/ws/'
clientId = str(random.randint(2, 1000))

public_key = str(q) + " " + str(h) + " " + str(g)

name = input("Enter your name: ")

async def receive_messages():
	async with websockets.connect(uri + clientId) as websocket:
		while True:
			message_json = await websocket.recv()
			message = json.load(message_json)
			print(message.message)
			print(decrypt(message.message, message.p, private_key, q))

async def send_message(message: str, recipients: List[str], private_key: int, q: int, g: int):
	async with websockets.connect(uri + clientId) as websocket:
		await websocket.send(json.dumps(message))
		for recipient in recipients:
			q_key, h_key, g_key = map(int, recipient.split())
			en_msg, p = encrypt(message, q_key, h_key, g_key)
			message_json = {"sender": name, "message": en_msg, "p": p, "key": recipient}
			await websocket.send(json.dumps(message_json))

async def handle_client():
	async with websockets.connect(uri + clientId) as websocket:
		client_json = {"name": name, "key": public_key}
		await websocket.send(json.dumps(client_json))
		await receive_messages()

asyncio.run(handle_client())

