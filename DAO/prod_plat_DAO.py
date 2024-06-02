import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.database_access import database_access

class prod_plat_DAO:

    def __init__(self):
        self.database_access_dao = database_access()

    def create_prod_plat(self, id_produto, id_plataforma):

        try:
            query = f'''
            INSERT
            INTO prod_plat (fk_id_produto, fk_id_plataforma)
            VALUES ('{id_produto}', '{id_plataforma}')
            '''

            self.database_access_dao.execute_query(query)

            return True
        except:
            return False
        
    def get_prod_plat(self, id_produto, id_plataforma):

        query = f'''
        SELECT *
        FROM prod_plat
        WHERE fk_id_produto = '{id_produto}' AND fk_id_plataforma = '{id_plataforma}';
'''
        
        prod_plat = self.database_access_dao.fetch(query)

        if prod_plat:
            return prod_plat
        else:
            return None
        
    def update_prod_plat(self, id_plataforma, id):
        print(id)

        existe = self.database_access_dao.fetch(f'SELECT * FROM prod_plat WHERE id_prod_plat = {id}')

        if existe:
            try:
                query = f'''
                UPDATE prod_plat
                SET fk_id_plataforma = '{id_plataforma}'
                WHERE id_prod_plat = '{id}'
        '''
                
                self.database_access_dao.execute_query(query)

                return True
            except:
                return False