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

def list_users():
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT * FROM users'
    cursor.execute(comando)
    usuarios = cursor.fetchall()
    conexao.close()
    print(type(usuarios[0]))
    return usuarios

def salvar_token_publico(name, token):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = f'INSERT INTO public_tokens ( name, token) VALUES ("{name}","{token}")'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_keys_db():
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT * FROM bases'
    cursor.execute(comando)
    keys = cursor.fetchall()
    conexao.close()
    return keys


def salvar_keys(name, keys):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = f'INSERT INTO bases (`name`,`chaves`) VALUES ("{name}","{keys}")'
    cursor.execute(comando)
    conexao.commit()                                                                            
    return cursor.lastrowid


#json.dumps(dict, ensure_ascii=False, indent=4)
def salvarInfos(listDict, base_id):
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = f'INSERT INTO infos (`infos`,`base_id`) VALUES ("{listDict}",{base_id})'
    cursor.execute(comando)
    conexao.commit()                                                                            



def listar_infos_bd():
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT infos FROM infos'
    cursor.execute(comando)
    lista_infos = [info[0] for info in cursor.fetchall()]
    conexao.close()
    return lista_infos
 


def listar_infos_bd_formatada():
    conexao = conectarBd()
    cursor = conexao.cursor()
    comando = 'SELECT infos FROM infos'
    cursor.execute(comando)
    lista_infos = [info[0] for info in cursor.fetchall()]
    conexao.close()
    #FORMATACAO 
    lista_infos_formatada = []
    for info in lista_infos:
        info = info.replace("'", '')
        info = info.replace("{", '')
        info = info.replace("}", '')
        infos = info.split(',')
        infos_formatados = []
        for info in infos:
            info = info.split(':')
            info = {info[0]: info[1]}
            infos_formatados.append(info)

        dicionario_unico = {}

        for item in infos_formatados:
            chave, valor = next(iter(item.items()))
            dicionario_unico[chave.strip()] = valor.strip()
        infos = dicionario_unico

        lista_infos_formatada.append(infos)
    return lista_infos_formatada




#FORMATAR  A  MENSAGEM  DE ACORDO COM AS CHAVES E VALORES QUE VIRAM DO FRONT
mensagem = "Oi [nome], como voce esta?"

variavel = 'nome'

dicionario = {
    "nome":"Rodrigo",
    "idade": "25"
}

chaves = []

for chave in dicionario:
    chaves.append(chave)


mensagem = mensagem.split(' ')

for palavra in mensagem:
    if palavra == "":
        print(palavra)