import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.database_access import database_access

class categoria_DAO:

    db = None
    cursor = None

    def __init__(self):
        self.database_access_dao = database_access()
        
    def create_categoria(self, request):
        nome = request.form['nome']

        categoria = self.get_categoria_by_nome(nome)

        if not categoria:

            query = f'''
            INSERT INTO categoria
            (nome)
            VALUES
            ('{nome}')
        '''
            
            self.database_access_dao.execute_query(query)

            return True
        else:
            return False

    def get_categoria_by_id(self, id):
        query = f'''
        SELECT *
        FROM categoria
        WHERE id_categoria = '{id}'
'''

        categoria = self.database_access_dao.fetch(query)[0]

        if categoria and (categoria[2]!=0):
            return categoria
        else:
            return None


    def get_categoria_by_nome(self, nome):
        query = f'''
        SELECT *
        FROM categoria
        WHERE nome = '{nome}'
        '''

        categoria = self.database_access_dao.fetch(query)[0]

        if categoria and (categoria[2] != 0):
            return categoria
        else:
            return None
        
    def update_categoria(self, id, request):
        
        categoria = self.get_categoria_by_id(id)

        if categoria:
            nome = request.form['nome']

            query = f'''
            UPDATE categoria
            SET nome = '{nome}'
            WHERE id_categoria = '{id}'
'''
            self.database_access_dao.execute_query(query)

            return True
        else:
            return False
        
    def delete_categoria(self, id):
        
        categoria = self.get_categoria_by_id(id)

        if categoria:
            query = f'''
            UPDATE categoria
            SET ativo = 0
            WHERE id_categoria = '{id}'
'''
            self.database_access_dao.execute_query(query)

            return True
        else:
            return False