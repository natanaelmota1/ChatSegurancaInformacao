import random
from math import pow

a=random.randint(2,10)

# Função para encontrar o máximo divisor comum
def maxDivComum(a,b):
    if a<b:
        return maxDivComum(b,a)
    elif a%b==0:
        return b
    else:
        return maxDivComum(b,a%b)

# Função para geração uma chave aleatória
def gen_key(q):
    key= random.randint(pow(10,20),q)
    
    # Dando a garantia de que o máximo divisor comum entre 'key' e 'q' seja 1, para a segurança do algoritmo
    while maxDivComum(q,key)!=1:
        key=random.randint(pow(10,20),q)
    return key

# Função para fazer uma exponenciação rápida
def expo(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c
        y=(y*y)%c
        b=int(b/2)
    return x%c

# Função que encriptografa a mensagem
def encryption(msg,q,h,g):
    ct=[]
    k=gen_key(q)
    s=expo(h,k,q)
    p=expo(g,k,q)
    for i in range(0,len(msg)):
        ct.append(msg[i])
    for i in range(0,len(ct)):
        ct[i]=s*ord(ct[i])
    return ct,p

# Função que descriptografa a mensagem
def decryption(ct,p,key,q):
    pt=[]
    h=expo(p,key,q)
    for i in range(0,len(ct)):
        pt.append(chr(int(ct[i]/h)))
    return pt

msg=input("Enter message.")
q=random.randint(pow(10,20),pow(10,50))
g=random.randint(2,q)
key=gen_key(q)
h=expo(g,key,q)
ct,p=encryption(msg,q,h,g)
print("Original Message=",msg)
print("Encrypted Maessage=",ct)
pt=decryption(ct,p,key,q)
d_msg=''.join(pt)
print("Decryted Message=",d_msg)