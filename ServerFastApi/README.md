# Para instalar as dependências: 
pip3 install -r requirements.txt

# PARA RODAR O SERVIDOR:
python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# PARA PARAR SERVIDOR EM SEGUNDO PLANO
sudo fuser -k 8000/tcp
