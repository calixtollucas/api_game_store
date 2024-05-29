import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)

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