from datetime import date
import mysql.connector
import time 
import sys
import stomp
import os
import json
from flask import Flask
from flask_cors import CORS, cross_origin

# servidor web
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# conecta ao servidor mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sistema-sfpd-db"
)

# cria um Listener herdando a stomp.ConnectionListener class
class Listener(stomp.ConnectionListener):

# sobrescreve os metodos on_error and on_message providos pela classe pai
    def on_error(self, message):
        print('received an error "%s"' % message)
# Printa a mensagem recebida
    def on_message(self, message):
        print('received a message "%s"' % message)

# Declara hosts como um array de tuples contendo o ActiveMQ server # IP address ou hostname e a porta
hosts = [('localhost', 61613)]

# Cria conexao
connMq = stomp.Connection(host_and_ports=hosts)

# Diz ao objeto de conexao para ouvir por mensagens usando o Listener criado
connMq.set_listener('', Listener()) 

# Inicia a conexao com as credenciais do ActiveMQ server
# conn.start()
connMq.connect('admin', 'admin', wait=True)

# Registra um consumer com o ActiveMQ. Isto diz ao ActiveMQ para enviar todas as mensagens recebidas na fila setada para o listener
# connMq.subscribe(destination='/queue/fila1', id=1, ack='auto')

def dec_serializer(o):
    if isinstance(o, date):
        return o.strftime("%Y-%m-%d")

def envia_fila_stomp(connmq,row):
    # json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
    djson = json.dumps({'id': row[0], 'arquivoId': row[1], 'arquivoPath': row[2], 'linha': row[3], 'data': row[4]}, separators=(',', ':'), default=dec_serializer)
    connmq.send(body=''.join(djson), destination='/queue/fila1')

mycursor = mydb.cursor()

@app.route("/")
def home():
    return "Hello, World!" 

@cross_origin()
@app.route("/executarRotina")
def executarRotina():
    mycursor.execute("SELECT * FROM arquivos_linhas")
    myresult = mycursor.fetchall()
    print(mycursor.rowcount, "registro(s) selecionado(s)")

    for row in myresult:
        envia_fila_stomp(connMq, row)

    connMq.disconnect();
    return json.dumps({'data' : date.today(), 'executado' : "true", 'status' : "Executando..."}, separators=(',', ':'), default=dec_serializer)

if __name__ == "__main__":
    app.run(debug=True)