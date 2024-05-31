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