import requests
import random
from math import pow
import threading
import time

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
private_key = gen_key(q)# Private key for receiver
h = power(g, private_key, q)

public_key = str(q) + " " + str(h) + " " + str(g)

name = input("Enter your name: ")
cliente_json = {"name": name, "key": public_key}
response = requests.post("http://127.0.0.1:8000/client", json=cliente_json)
#print(response.json())

messages_history = []
def receive_messages():
	while(True):
		time.sleep(20)
		message = requests.post("http://127.0.0.1:8000/messages", json=cliente_json).json()
		if (message != ""):
			print(message)
			key = message["key"]
			if (key == public_key):
				message_save = message["sender"] + ": " + str(decrypt(message["message"], message["p"], private_key, q))
				if (message_save not in messages_history):
					messages_history.append(message_save)
					print(message["sender"] + ": " + str(message["message"]))
					print(message_save)

keys = []

while(True):

	# Receber todas as mensagens (em segundo plano)
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    message_input = input()

    # Atualizar chaves públicas salvas
    clients = requests.get("http://127.0.0.1:8000/clients")
    for client in clients.json():
        key = client["key"]
        if(key != public_key and key not in keys):
            keys.append(key)
    #print(keys)

    # Enviar uma mensagem
    for key in keys:
        en_msg, p = encrypt(message_input, int(key.split(" ")[0]), int(key.split(" ")[1]), int(key.split(" ")[2]))
        message_json = {"sender": name, "message": en_msg, "p": p, "key": key}
        response = requests.post("http://127.0.0.1:8000/message", json=message_json)
        #print(response.json())