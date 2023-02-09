import tkinter as tk
import requests
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

q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
private_key = gen_key(q)# Private key for receiver
h = power(g, private_key, q)

public_key = str(q) + " " + str(h) + " " + str(g)

# Criar a janela principal
root = tk.Tk()
root.title("Secure Chat")

# Variáveis globais
#name = ""
keys = []
messages_history = []

# Função para enviar uma mensagem
def send_message(message):
    for key in keys:
        en_msg, p = encrypt(message, int(key.split(" ")[0]), int(key.split(" ")[1]), int(key.split(" ")[2]))
        message_json = {"sender": name, "message": en_msg, "p": p, "key": key}
        response = requests.post("http://127.0.0.1:8000/message", json=message_json)
    message_text.insert(tk.END, name + ": " + message + "\n")

# Função para atualizar as mensagens recebidas
def update_messages():
	messages = requests.get("http://127.0.0.1:8000/messages")
	for message in messages.json():
		key = message["key"]	
		p = message["p"]
		if (key == public_key and p not in messages_history):
			message_text.insert(tk.END, message["sender"] + ": " + str(decrypt(message["message"], message["p"], private_key, q)) + "\n")
	root.after(1000, update_messages)

# Função para atualizar as chaves públicas
def update_keys():
    clients = requests.get("http://127.0.0.1:8000/clients")
    for client in clients.json():
        key = client["key"]
        if(key != public_key and key not in keys):
            keys.append(key)

# Criar um campo de texto para o usuário digitar o nome
name_label = tk.Label(root, text="Nome:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Botão para enviar o nome
send_name_button = tk.Button(root, text="Enviar Nome", command=lambda: set_name(name_entry.get()))
send_name_button.pack()

def set_name(entry):
	global name
	name = entry
	public_key, private_key, q
	cliente_json = {"name": name, "key": public_key}
	print(cliente_json)
	response = requests.post("http://127.0.0.1:8000/client", json=cliente_json)
	update_keys()

# Criar um campo de texto para o usuário digitar a mensagem
message_entry = tk.Entry(root)
message_entry.pack()

# Botão para enviar a mensagem
send_message_button = tk.Button(root, text="Enviar Mensagem", command=lambda: send_message(message_entry.get()))
send_message_button.pack()

# Área de texto para exibir as mensagens
message_text = tk.Text(root)
message_text.pack()

# Atualizar as mensagens periodicamente
#root.after(1000, update_messages())
update_messages()

# Iniciar o loop de eventos do Tkinter
root.mainloop()

