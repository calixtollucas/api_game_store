import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)

class cliente_DAO:

    def __init__(self):
        pass

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

"""
- CRUD PEDIDO
- Create
- Read(id, endereco, cliente)
- update
- delete
"""

class pedido_DAO:
    def pedido(self, request):
        endereco = request.form["endereco"]
        fk_id_cliente = request.form["fk_id_cliente"]
        fk_id_probuto = request.form["fk_id_probuto"]


        query = f'''
        INSERT 
        INTO 
        cliente (endereco, fk_id_cliente, fk_id_probuto) 
        VALUES ("{endereco}", "{fk_id_cliente}", "{fk_id_probuto}")
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()

        cursor.close()
        self.db.close()
    
    #READ BY ID
    def get_pedido_by_id(self, id_pedido):

        query = f'''
        "SELECT id_pedido, endereco, fk_id_cliente, fk_id_probuto, ativo 
        FROM pedido 
        WHERE id_pedido = {id_pedido}",
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()

        cursor.close()
        self.db.close()
    
    #READ BY ENDERECO
    def get_pedido_by_cliente_nome(self, endereco):
        query = f'''
        "SELECT id_pedido, endereco, fk_id_cliente, fk_id_probuto, ativo 
        FROM pedido 
        WHERE endereco {endereco}"
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close()
    
    #READ BY CLIENTE
    def get_pedido_by_cliente_email(self, fk_id_cliente):
        query = f'''
        "SELECT id_pedido, endereco, fk_id_cliente, fk_id_probuto, ativo 
        FROM pedido 
        WHERE fk_id_cliente {fk_id_cliente}"
        '''
    
        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close()

    #UPDATE 
    def cliente_atualizar(self, id_pedido, request):
        novo_endereco = request.form ["endereco"]
        novo_cliente = request.form["fk_id_cliente"]
        novo_probuto = request.form ["fk_id_probuto"]
        novo_ativo = request.form ["ativo"]
    
        user = self.get_pedido_by_id(id_pedido)

        query = f'''
        "UPDATE pedido 
        SET fk_id_cliente = "{novo_cliente}", endereco = "{novo_endereco}", fk_id_probuto = "{novo_probuto}", 
        WHERE id_pedido = {id_pedido}
        '''
    
        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close() 

        return True

    #DELETE
    def cliente_desativar(self, id_pedido):
        pedido = self.get_pedido_by_id(id_pedido)
        cursor = self.open_cursor()

        #CLIENTE EXISTE?
        if not pedido:
            return False
        else:
            cursor.execute(f'''UPDATE pedido SET ativo = 0 WHERE id_pedido = {id_pedido}''')
            self.db.commit()

        cursor.close()
        self.db.close()

        return True