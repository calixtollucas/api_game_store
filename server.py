"""
- CRUD CLIENTE
- Create(cadastro e login)
- Read(id, nome, email)
- update
- delete
"""

from errno import errorcode
from sqlite3 import dbapi2
from flask import Flask, jsonify, request;
import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)

app = Flask(__name__)

db = None
cursor = None

# função para conectar com o banco de dados
def connect_database():
# OBS: talvez seja preciso mudar as credenciais para usar no seu mysql workbench. De preferência, utilizar a mesma senha
    print("Conectando no banco")
    try:
        global db
        db = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="rukasu",
        database="loja_gamer",
        )
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Conectado com sucesso!")

def open_cursor():
    print("Abrindo cursor")
    if (db is None) or not db.is_connected():
        connect_database()
        return db.cursor(buffered=True)
    else:
        return db.cursor(buffered=True)
        

# teste conexao banco
@app.get("/banco")
def testebanco():
    query = '''
    SELECT * FROM cliente;
'''
    cursor = open_cursor()
    cursor.execute(query)
    result = cursor.fetchone();
    cursor.close()
    db.close()
    return jsonify(result)



#CREATE (CADASTRO)
@app.route('/cadastrar', methods = ['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    telefone = request.form['telefone']

    query = f'''
    INSERT 
    INTO 
    cliente (nome, email, senha, telefone) 
    VALUES ('{nome}', '{email}', '{senha}', '{telefone}')
    '''

    cursor = open_cursor()
    cursor.execute(query)
    db.commit()

    cursor.close()
    db.close()

    return jsonify({'message': "Cliente cadastrado com sucesso!"}),201


#CREATE (LOGIN)
@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    query = f'''
    SELECT *
    FROM cliente
    WHERE email = '{email}' AND senha = '{senha}'
'''
    cursor = open_cursor()
    cursor.execute(query)
    user = cursor.fetchaone()

    if user:
        cursor.close()
        db.close()
        return jsonify({"Message": "logado com sucesso"}), 200
    else:
        cursor.close()
        db.close()
        return jsonify({"Message": "Este usuário não existe"}), 404

    
    

#READ BY ID
@app.route('/cliente/<int:id>', methods = ['GET'])
def clientes_id(id):

    query = f'''
    SELECT nome, email, telefone, ativo
    FROM cliente
    WHERE id_cliente = {id}
'''

    cursor = open_cursor()
    cursor.execute(query)
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

    query = f'''
    SELECT *
    FROM cliente
    WHERE nome = '{nome}'
'''

    cursor = open_cursor()
    cursor.execute(query)
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

    query = f'''
    SELECT *
    FROM cliente
    WHERE email = '{email}';
'''
    
    cursor = open_cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user[5] == 0:
        return jsonify({"Mensagem": "Este usuário não existe"})
    
    if user:
        return jsonify({
            'email': email,
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'senha': user[3],
            'telefone': user[4],
            'ativo': user[5],
        })
    else:
        return jsonify({'message': 'Cliente não encontrado via email'})

#UPDATE 
@app.route('/cliente/atualizar/<int:id>', methods = ['PUT'])
def cliente_atualizar(id):
    novo_nome = request.form['nome']
    novo_email = request.form ['email']
    novo_telefone = request.form ['telefone']
    
    query = f'''
    UPDATE cliente
    SET nome = '{novo_nome}', email = '{novo_email}', telefone = '{novo_telefone}'
    WHERE id_cliente = {id}
'''

    cursor = open_cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close() 
    
    return jsonify({'message': 'Cliente atualizado com sucesso'}), 200

#DELETE
@app.route('/cliente/alterar_ativo/<int:id>', methods = ['DELETE'])
def cliente_desativar(id):
   
    
    cursor = open_cursor()
    cursor.execute(f'''SELECT nome, email, telefone, ativo FROM cliente WHERE id_cliente = {id}''')
    cliente = cursor.fetchone()

    #CLIENTE EXISTE?
    if not cliente:
        return jsonify({'message': 'Este cliente não existe'}), 404
    else:
        #DO CONTRÁRIO:
        cursor.execute(f'''UPDATE cliente SET ativo = 0 WHERE id_cliente = {id}''')
        db.commit()

    cursor.close()
    db.close()
    
    return jsonify({'message': 'Campo "ativo" alterado com sucesso'}), 200
    
if __name__ == '__main__':
    app.run(debug=True)