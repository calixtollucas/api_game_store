import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)

class plataforma_DAO:

    db = None
    cursor = None

    # função para conectar com o banco de dados
    def connect_database(self):
    # OBS: talvez seja preciso mudar as credenciais para usar no seu mysql workbench. De preferência, utilizar a mesma senha
        print("Conectando no banco")
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

    def open_cursor(self):
        print("Abrindo cursor")
        if (self.db is None) or not self.db.is_connected():
            self.connect_database()
            return self.db.cursor(buffered=True)
        else:
            return self.db.cursor(buffered=True)
        
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
            
            cursor = self.open_cursor()

            cursor.execute(query)
            self.db.commit()

            cursor.close()
            self.db.close()

            return True
        else:
            return False

    def get_plataforma_by_nome(self, nome):
        query = f'''
        SELECT *
        FROM plataforma
        WHERE nome = '{nome}'
        '''

        cursor = self.open_cursor()
        plataforma = cursor.execute(query)

        cursor.close()
        self.db.close()

        if plataforma:
            return plataforma
        else:
            return None