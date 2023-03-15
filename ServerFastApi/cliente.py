import requests
import random
from math import pow
import threading
import time
import hashlib

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
registered_client = requests.post("http://127.0.0.1:8000/client/check", json={"name": name}).json()

if (registered_client["registered"]):
	password = input("Enter Your Password: ")
else:
	password = input("Create Your Password: ")

cliente_json = {"name": name, "password": hashlib.sha256(password.encode('utf-8')).hexdigest(), "key": public_key}

login = False
response = requests.post("http://127.0.0.1:8000/client/register", json=cliente_json)
if (response.status_code == 200):
	print(response.json()["message"])
	login = True
else:
	login = False

#password = input("Digite sua senha (se já cadastrado): ")
#cliente_json = {"name": name, "password_hash": hashlib.sha256(password.encode('utf-8')).hexdigest(), "key": public_key}
#response = requests.post("http://127.0.0.1:8000/client", json=cliente_json)
#print(response.json())

messages_history = []
def receive_messages():
	while(login):
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

contatos = []

while(login):

	# Receber todas as mensagens (em segundo plano)
	receive_thread = threading.Thread(target=receive_messages)
	receive_thread.start()

	message_input = input()
	
	# Verificar autenticidade
	password = input("Enter Your Password: ")
	cliente_json = {"name": name, "password": hashlib.sha256(password.encode('utf-8')).hexdigest(), "key": public_key}
	response = requests.post("http://127.0.0.1:8000/client/register", json=cliente_json)
	if (response.status_code == 200):
		login = True
	else:
		login = False

	# Atualizar chaves públicas salvas
	clients = requests.get("http://127.0.0.1:8000/clients")
	for client in clients.json():
		client_name = client["name"]
		if(client_name != name):
			if (len(contatos) > 0):
				for contato in contatos:
					if(client_name == contato["name"]):
						contato["key"] = client["key"]
					else:
						contatos.append(client)
			else:
				contatos.append(client)
	print(contatos)

	# Enviar uma mensagem

	for contato in contatos:
		key = contato["key"]
		en_msg, p = encrypt(message_input, int(key.split(" ")[0]), int(key.split(" ")[1]), int(key.split(" ")[2]))
		message_json = {"sender": name, "message": en_msg, "p": p, "key": key}
		response = requests.post("http://127.0.0.1:8000/message", json=message_json)