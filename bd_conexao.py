import mysql.connector

def conectarBd():
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='crm_impulse_bd')
    return conexao

