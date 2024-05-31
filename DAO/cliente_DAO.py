import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.database_access import database_access

class cliente_DAO:

    def __init__(self):
        self.database_access_dao = database_access()
        self.db = None
        self.cursor = None

    def cadastrar(self, request):

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

        self.database_access_dao.execute_query(query)

    def check_login(self, request):
        email = request.form['email']
        senha = request.form['senha']

        query = f'''
        SELECT *
        FROM cliente
        WHERE email = '{email}' AND senha = '{senha}'
    '''
        user = self.database_access_dao.fetch(query)
        return user
    
    def get_client_by_id(self, id):
        query = f'''
        SELECT *
        FROM cliente
        WHERE id_cliente = {id}
    '''

        user = self.database_access_dao.fetch(query)[0]
        print(user)

        if user and (user[5]!=0):
            return user
        else:
            return None

    def get_cliente_by_nome(self, nome):

        query = f'''
        SELECT *
        FROM cliente
        WHERE nome = '{nome}'
    '''

        user = self.database_access_dao.fetch(query)[0]

        if user:
            return user
        else:
            return None

    def get_cliente_by_email(self, email):
        print("email: "+email)
        query = f'''
        SELECT *
        FROM cliente
        WHERE email = '{email}';
    '''
        
        user = self.database_access_dao.fetch(query)[0]

        if user and (user[5]!=0):
            return user
        else:
            return None
    
    def atualizar_cliente(self, id, request):
        novo_nome = request.form['nome']
        novo_email = request.form ['email']
        novo_telefone = request.form ['telefone']
        
        user = self.get_client_by_id(id)

        if not user:
            return False

        query = f'''
        UPDATE cliente
        SET nome = '{novo_nome}', email = '{novo_email}', telefone = '{novo_telefone}'
        WHERE id_cliente = {id}
    '''
        self.database_access_dao.execute_query(query)

        return True
    
    def desativar_cliente(self, id):
        #CLIENTE EXISTE?
        cliente = self.get_client_by_id(id)

        #CLIENTE EXISTE?
        if not cliente:
            return False
        else:
            #DO CONTRÁRIO:
            query = f'''UPDATE cliente SET ativo = 0 WHERE id_cliente = {id}'''
            self.database_access_dao.execute_query(query)

        return True