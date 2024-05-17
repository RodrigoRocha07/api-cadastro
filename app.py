from fastapi import FastAPI, Request, HTTPException, Depends,File, UploadFile, Form
from typing import List, Dict
from pydantic import BaseModel
from models import User
from provedores import hash_provider, token_provider
from utils import *
import csv

app = FastAPI()

banco: List[User] = []

#MIDDLEWARE DE AUTENTICACAO
async def token_authentication(request: Request):
    body = await request.json()
    token = body['token']
    if 'token' in body:
        print('Middleware ativada')
        for user in banco:
            if user.token == token:
                print({user.name: 'Autorizado!'})
                return 
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    raise HTTPException(status_code=401, detail="Credenciais não fornecidas")



async def token_authentication_in_header(request: Request):
    header = request.headers
    if 'authorization' in header:
        token = header['authorization'].split(' ')[1]
        if token_provider.verificar_token(token):
            return 
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    raise HTTPException(status_code=401, detail="Credenciais não fornecidas")


@app.post("/signUp")
async def signUp(request: Request, user: User):
    if checar_email(user.email):
        return "Email ja cadastrado! "
    else:
        salvar_user_db(user)
    return 'Cadastrado'



@app.post("/signIn")
async def signIn(request_data: Dict[str, str]):
    users = get_email()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email e senha são necessários para fazer login.")
    if email in users:
        senha_valida = checar_senha(email, password)
        if senha_valida:
            dict = {
                "email":email
            }
            token = token_provider.criar_token(dict)
            salvar_token(email, token)
            return token
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    raise HTTPException(status_code=401, detail="Usuario não encontrado")



@app.post("/verify")
async def verify(dict: Dict):
    token = dict['token']
    valido = token_provider.verificar_token(token)
    time = token_provider.tempo_validade_restante(token)
    if valido:
        return {'Valido':time}
    else:
        return 'Invalido'



@app.post("/send_sms")
async def verify(request_data: Dict[str, str],request: Request, authenticated: None = Depends(token_authentication_in_header)):
    phone = request_data.get('phone')
    text = request_data.get('text')
    send_sms(phone, text)
    return "sms enviado"





@app.post("/upload_csv")
async def upload_csv(name: str = Form(...), csv_file: UploadFile = File(...)):
    if not csv_file.filename.endswith('.csv'):
        return {"error": "O arquivo enviado não é um arquivo CSV."}

    contents = await csv_file.read()

    csv_data = []
    decoded_content = contents.decode('utf-8', errors='ignore').splitlines()
    csv_reader = csv.reader(decoded_content)
    for row in csv_reader:
        csv_data.append(row)
    csv_data = csv_data[0:5]

    keys = csv_data[0][0].split(';')
    matriz = csv_data[1:]
    listDict = list(map(lambda linha:dict(zip(keys, linha[0].split(';'))),matriz))

    return listDict