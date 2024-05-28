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

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()

        cursor.close()
        self.db.close()

    def check_login(self, request):
        email = request.form['email']
        senha = request.form['senha']

        query = f'''
        SELECT *
        FROM cliente
        WHERE email = '{email}' AND senha = '{senha}'
    '''
        cursor = self.open_cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    
    def get_client_by_id(self, id):
        query = f'''
        SELECT nome, email, telefone, ativo
        FROM cliente
        WHERE id_cliente = {id}
    '''

        cursor = self.open_cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        self.db.close()

        if user:
            return user
        else:
            return None

    def get_cliente_by_nome(self, nome):

        query = f'''
        SELECT *
        FROM cliente
        WHERE nome = '{nome}'
    '''

        cursor = self.open_cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        self.db.close()

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
        
        cursor = self.open_cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        self.db.close()

        print("user: "+str(user))

        if user:
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
        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close() 

        return True
    
    def desativar_cliente(self, id):
        #CLIENTE EXISTE?
        cliente = self.get_client_by_id(id)

        cursor = self.open_cursor()

        #CLIENTE EXISTE?
        if not cliente:
            return False
        else:
            #DO CONTRÁRIO:
            cursor.execute(f'''UPDATE cliente SET ativo = 0 WHERE id_cliente = {id}''')
            self.db.commit()

        cursor.close()
        self.db.close()

        return True