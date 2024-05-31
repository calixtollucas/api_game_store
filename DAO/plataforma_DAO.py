import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.database_access import database_access

class plataforma_DAO:

    db = None
    cursor = None

    def __init__(self):
        self.database_access_dao = database_access()
        
        
    def create_plataforma(self, request):
        nome = request.form['nome']

        plataforma = self.get_plataforma_by_nome(nome)

        if not plataforma:

            query = f'''
            INSERT INTO plataforma
            (nome)
            VALUES
            ('{nome}')
        '''
            
            self.database_access_dao.execute_query(query)

            return True
        else:
            return False
        
    def get_all_plataforma(self):
        query = f'''
        SELECT *
        FROM plataforma;
'''
        
        plataformas = self.database_access_dao.fetch(query)

        return plataformas

    def get_plataforma_by_nome(self, nome):
        query = f'''
        SELECT *
        FROM plataforma
        WHERE nome = '{nome}'
        '''

        plataforma = self.database_access_dao.fetch(query)

        if plataforma:
            return plataforma
        else:
            return None
        
    def get_plataforma_by_id(self, id):
        query = f'''
        SELECT *
        FROM plataforma
        WHERE id_plataforma = '{id}'
'''
        
        plataforma = self.database_access_dao.fetch(query)[0]

        return plataforma
    
    def update_plataforma(self, request, id):

        nome = request.form['nome']

        plataforma = self.get_plataforma_by_id(id)

        if plataforma:

            query = f'''
            UPDATE plataforma
            SET nome = '{nome}'
            WHERE id_plataforma = '{id}';
'''
            self.database_access_dao.execute_query(query)

            return True
        else:
            return False
        
    def delete_plataforma(self, id):

        plataforma = self.get_plataforma_by_id(id)

        if plataforma:
            query = f'''
            UPDATE plataforma
            SET ativo = 0
            WHERE id_plataforma = '{id}'
'''
            self.database_access_dao.execute_query(query)

            return True
        else:
            return False
        