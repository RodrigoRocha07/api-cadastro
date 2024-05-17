import requests
import json
from bd_conexao import conectarBd
from models import User

def send_sms(phone, text):
    url = 'https://api.zenvia.com/v2/channels/sms/messages'
    headers = {
        'X-API-TOKEN': 'Tpa4jd0v5nAkkgOIA7WUxO1zyiDhA7mvD9Ju',
        'content-type': 'application/json'
    }
    data = {
        'from': 'calico-colossus',
        'to': phone,
        'contents': [{
            'type': 'text',
            'text': text,
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)





#SIG-IN / SIGN-UP
def salvar_user_db(user: User):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = f'INSERT INTO users ( name, password, email) VALUES ("{user.username}","{user.password}","{user.email}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def get_username():
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT name FROM users'
    cursor.execute(comando)
    lista_nomes = [nome[0] for nome in cursor.fetchall()]
    conexao.close()
    return lista_nomes

def get_email():
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT email FROM users'
    cursor.execute(comando)
    lista_emails = [nome[0] for nome in cursor.fetchall()]
    conexao.close()
    return lista_emails

def checar_senha(email, senha_digitada):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = f'SELECT password FROM users WHERE email = "{email}"'
    cursor.execute(comando)
    senha_original = cursor.fetchone()[0]
    conexao.close()
    if senha_original == senha_digitada:
        return True
    else:
        return False
    
def checar_email(email):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT email FROM users'
    cursor.execute(comando)
    lista_emails = [nome[0] for nome in cursor.fetchall()]
    conexao.close()
    if email in lista_emails:
        return True
    else:
        return False

def salvar_token(email, token):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = f'UPDATE users SET token = "{token}" WHERE email = "{email}"'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()


#MANIPULAÇÃO CSV
def salvar_csv_db(matriz):
    pass