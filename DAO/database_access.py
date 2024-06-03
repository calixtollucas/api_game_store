from uu import Error
import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)

class database_access:

    db = None

    # função para conectar com o banco de dados
    def get_connection(self):
    # OBS: talvez seja preciso mudar as credenciais para usar no seu mysql workbench. De preferência, utilizar a mesma senha
        print("Conectando no banco")

        if self.db is None or not (self.db.is_connected()):
            try:
                self.db = mysql.connector.connect(
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

    def execute_query(self, query):

        self.get_connection()

        try:
            self.db.start_transaction()

            cursor = self.db.cursor(buffered=True)
            cursor.execute(query)
            self.db.commit()
            cursor.close()
            self.close_connection()
            return True
        except:
            self.db.rollback()
            return False
        finally:
            cursor.close()
            self.db.close()

    def fetch(self, query):
        self.get_connection()

        cursor = self.db.cursor(buffered=True)
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result

    def close_connection(self):
        if self.db is not None or self.db.is_connected():
            self.db.close()
            self.db = None

    def call_procedure(self, nome_procedure, args):
        self.get_connection()

        try:
            cursor = self.db.cursor(buffered=True)
            cursor.callproc(nome_procedure, args)
            self.db.commit()
            return True
        except Error as err:
            print(err)
            self.db.rollback()
            return False