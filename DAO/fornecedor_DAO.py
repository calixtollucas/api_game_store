import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)

class fornecedor_DAO:

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

    def fornecedor(self, request):
        nome = request.form["nome"]
        cnpj = request.form["cnpj"]
        email = request.form["email"]
        fk_id_produto = request.form["fk_id_produto"]
        ativo = request.form.get('ativo', '1')


        query = f'''
        INSERT 
        INTO 
        cliente (nome, cnpj, email, fk_id_produto) 
        VALUES ("{nome}", "{cnpj}", "{email}", "{fk_id_produto}")
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()

        cursor.close()
        self.db.close()
    
    #READ BY ID
    def get_fornecedor_by_id(self, id_fornecedor):

        query = f'''
        "SELECT id_fornecedor, nome, cnpj, email, fk_id_produto, ativo 
        FROM fornecedor
        WHERE id_fornecedor = {id_fornecedor}",
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()

        cursor.close()
        self.db.close()
    
    #READ BY cnpj
    def get_fornecedor_by_cnpj_nome(self, cnpj):
        query = f'''
        "SELECT id_fornecedor, nome, cnpj, email, fk_id_probuto, ativo 
        FROM fornecedor 
        WHERE cnpj {cnpj}"
        '''

        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close()
    
    #READ BY probuto
    def get_fornecedor_by_probuto_email(self, fk_id_probuto):
        query = f'''
        "SELECT id_fornecedor, nome, cnpj, email, fk_id_probuto, ativo 
        FROM fornecedor 
        WHERE fk_id_probuto {fk_id_probuto}"
        '''
    
        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close()

    #UPDATE 
    def fornecedor_atualizar(self, id_fornecedor, request):
        novo_nome = request.form ["nome"]
        novo_cnpj = request.form["cnpj"]
        novo_email = request.form["email"]
        novo_probuto = request.form ["fk_id_probuto"]
        novo_ativo = request.form ["ativo"]
    
        user = self.get_fornecedor_by_id(id_fornecedor)

        query = f'''
        "UPDATE fornecedor
        SET nome = "{novo_nome}", cnpj = "{novo_cnpj}", email = "{novo_email}", fk_id_probuto = "{novo_probuto}", 
        WHERE id_fornecedor = {id_fornecedor}
        '''
    
        cursor = self.open_cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()
        self.db.close() 

        return True

    #DELETE
    def fornecedor_desativar(self, id_fornecedor):
        pedido = self.get_pedido_by_id(id_fornecedor)
        cursor = self.open_cursor()

        #fornecedor EXISTE?
        if not pedido:
            return False
        else:
            cursor.execute(f'''UPDATE fornecedor SET ativo = 0 WHERE id_fornecedor = {id_fornecedor}''')
            self.db.commit()

        cursor.close()
        self.db.close()

        return True