"""
- CRUD CLIENTE
- Create(cadastro e login)
- Read(id, nome, email)
- update
- delete
"""

from errno import errorcode
from flask import Flask, jsonify, request;
import mysql.connector;
from mysql.connector import (errorcode, connection)
from networkx import is_connected

app = Flask(__name__)
db = None
cursor = None
# função para conectar com o banco de dados
def connect_database():
# OBS: talvez seja preciso mudar as credenciais para usar no seu mysql workbench. De preferência, utilizar a mesma senha
    try:
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rukasu",
        database="loja_gamer"
        )
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def open_cursor():
    if db.is_connected:
        cursor = db.cursor()
    else:
        connect_database()
        open_cursor()
        

# teste conexao banco
@app.get("/banco")
def testebanco():
    query = '''
    SELECT * FROM cliente;
'''
    cursor.execute(query)
    result = cursor.fetchone();
    return result



#CREATE (CADASTRO)
@app.route('/cadastrar', methods = ['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']
    ativo = request.form.get('ativo', '1')

    query = ("INSERT INTO cliente (nome, email, senha, telefone, ativo) VALUES (%s, %s, %s, %s, %s)")

    cursor.execute(query, (nome, email, senha, telefone, ativo))

    cursor.close()

    return jsonify({'message': "Cliente cadastrado com sucesso!"}),201


#CREATE (LOGIN)
@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    
    cursor.execute("SELECT * FROM cliente WHERE email = %s AND senha = %s", (email, senha))
    user = cursor.fetchone()
    cursor.close()
    

#READ BY ID
@app.route('/cliente/<int:id>', methods = ['GET'])
def clientes_id(id):

    cursor.execute("SELECT nome, email, telefone, ativo FROM cliente WHERE ID = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        return jsonify({
            'id': id,
            'nome': user[0],
            'email': user[1],
            'telefone': user[2],
            'ativo': user[3]
        }), 200
    else:
        return jsonify({'message': 'Cliente não encontrado via ID'}), 404
    
#READ BY NAME
@app.route('/cliente/nome/<string:nome>', methods = ['GET'])
def cliente_nome(nome):
    conn = mysql.connection 
    cursor.execute("SELECT id, email, telefone, ativo FROM cliente WHERE nome = %s", (nome,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        return jsonify({
            'nome': nome,
            'id': user[0],
            'email': user[1],
            'telefone': user[2],
            'ativo': user[3]
        }), 200
    
    else: 
        return jsonify({'message': 'Cliente não encontrado via nome'}), 404
    
#READ BY EMAIL
@app.route('/cliente/email/<string:email>', methods = ['GET'])
def cliente_email(email):
    conn = mysql.connection
    cursor.execute("SELECT id, nome, telefone, ativo FROM cliente WHERE email = %s ", (email,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    
    if user:
        return jsonify({
            'email': email,
            'id': user[0],
            'nome': user[1],
            'telefone': user[2],
            'ativo': user[3],
        })
    else:
        return jsonify({'message': 'Cliente não encontrado via email'})

#UPDATE 
@app.route('/cliente/atualizar/<int:id>', methods = ['PUT'])
def cliente_atualizar(id):
    novo_nome = request.form['nome']
    novo_email = request.form ['email']
    novo_telefone = request.form ['telefone']
    novo_ativo = request.form ['ativo']
    
    conn = mysql.connection
    cursor.execute("UPDATE cliente SET nome = %s, email = %s, telefone = %s, ativo = %s WHERE ID = %s", (novo_nome, novo_email, novo_telefone, novo_ativo, id))
    mysql.connection.commit()
    db.close() 
    
    return jsonify({'message': 'Cliente atualizado com sucesso'}), 200

#DELETE
@app.route('/cliente/alterar_ativo/<int:id>', methods = ['PUT'])
def cliente_desativar(id):
   #CLIENTE EXISTE?
    cur = mysql.connection.cursor()
    cur.execute("SELECT nome, email, telefone, ativo FROM cliente WHERE ID = %s", (id,))
    cliente = cur.fetchone()
    cur.close()
    
    if not cliente:
        return jsonify({'message': 'Este cliente não existe'}), 404
    
    #DO CONTRÁRIO:
    cur = mysql.connection.cursor()
    cur.execute("UPDATE cliente SET ativo = 0 WHERE ID = %s", (id,))
    mysql.connection.commit()
    cur.close
    
    return jsonify({'message': 'Campo "ativo" alterado com sucesso'}), 200
    
if __name__ == '__main__':
    app.run(debug=True)