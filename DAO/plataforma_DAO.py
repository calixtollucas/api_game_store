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
        
    def get_all_plataforma(self):
        query = f'''
        SELECT *
        FROM plataforma;
'''
        
        cursor = self.open_cursor()
        cursor.execute(query)
        plataformas = cursor.fetchall()

        cursor.close()
        self.db.close()

        return plataformas

    def get_plataforma_by_nome(self, nome):
        query = f'''
        SELECT *
        FROM plataforma
        WHERE nome = '{nome}'
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        plataforma = cursor.fetchone()

        cursor.close()
        self.db.close()

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
        
        cursor = self.open_cursor()
        cursor.execute(query)
        
        plataforma = cursor.fetchone()

        cursor.close()
        self.db.close()

        return plataforma
    
    def update_plataforma(self, request, id):

        nome = request.form['nome']

        plataforma = self.get_plataforma_by_id(id)

        if plataforma:
            print('entrou plataforma update')
            query = f'''
            UPDATE plataforma
            SET nome = '{nome}';
'''
            cursor = self.open_cursor()
            cursor.execute(query)
            self.db.commit()

            cursor.close()
            self.db.close()

            return True
        else:
            return False
        
    def delete_plataforma(self, id):

        plataforma = self.get_plataforma_by_id(id)

        if plataforma:
            query = f'''
            UPDATE plataforma
            SET ativo = 0
'''
            
            cursor = self.open_cursor()
            cursor.execute(query)
            self.db.commit()

            cursor.close()
            self.db.close()

            return True
        else:
            return False
        