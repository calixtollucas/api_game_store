from winreg import REG_RESOURCE_LIST
from DAO.database_access import database_access

class pedido_DAO:

    def __init__(self):
        self.database_access_dao = database_access()

    def pedido(self, params):
        
        try:
            query = f'''
            INSERT 
            INTO 
            pedido (endereco, fk_id_cliente, fk_id_produto) 
            VALUES ("{params['endereco']}", "{params['id_cliente']}", "{params['id_produto']}");
            '''

            self.database_access_dao.execute_query(query)

            return True
        except:
            return False
    #READ BY ID
    def get_pedido_by_id(self, id_pedido):

        query = f'''
        SELECT * 
        FROM pedido 
        WHERE id_pedido = '{id_pedido}';
        '''

        pedido = self.database_access_dao.fetch(query)[0]

        if pedido:
            return pedido
        else:
            return False
    
    #READ BY ENDERECO
    def get_pedido_by_endereco(self, endereco):
        query = f'''
        SELECT * 
        FROM pedido 
        WHERE endereco = '{endereco}';
        '''

        pedidos = self.database_access_dao.fetch(query)

        if pedidos:
            result = []
            for pedido in pedidos:
                if pedido[3]!= 0:
                    result.append({
                        'id_pedido': pedido[0],
                        'endereco': pedido[1],
                        'id_cliente': pedido[2],
                        'id_produto': pedido[4],
                        'ativo': pedido[3],
                    })
            return result
        else:
            return None
    
    #READ BY CLIENTE
    def get_pedido_by_id_cliente(self, fk_id_cliente):
        query = f'''
        SELECT *
        FROM pedido 
        WHERE fk_id_cliente = {fk_id_cliente};
        '''
    
        pedidos = self.database_access_dao.fetch(query)

        if pedidos:
            result = []

            for pedido in pedidos:
                if pedido[3] != 0:
                    result.append({
                        'id_pedido': pedido[0],
                        'endereco': pedido[1],
                        'id_cliente': pedido[2],
                        'id_produto': pedido[4],
                        'ativo': pedido[3],
                    })
            return result
        else:
            return None


    #UPDATE 
    def pedido_atualizar(self, id_pedido, params):
        
        #encontra o pedido que quer atualizar
        pedido_atualizar = self.get_pedido_by_id(id_pedido)

        if not pedido_atualizar:
            return False
        else:
            produto_atualizado = {
                'endereco': params['endereco'] if (params['endereco'] != '') else pedido_atualizar[1],
                'id_cliente': params['id_cliente'] if (params['id_cliente'] != '') else pedido_atualizar[2],
                'id_produto': params['id_produto'] if (params['id_produto'] != '') else pedido_atualizar[4],
            }

            query = f'''
            UPDATE pedido 
            SET fk_id_cliente = "{produto_atualizado['id_cliente']}", 
            endereco = "{produto_atualizado["endereco"]}", 
            fk_id_produto = "{produto_atualizado['id_produto']}"
            WHERE id_pedido = {id_pedido};
            '''
        
            self.database_access_dao.execute_query(query)

            return True

    #DELETE
    def pedido_desativar(self, id_pedido):

        pedido = self.get_pedido_by_id(id_pedido)

        #pedido EXISTE?
        if not pedido:
            return False
        else:
            query = f'''UPDATE pedido SET ativo = 0 WHERE id_pedido = {id_pedido}'''
            self.database_access_dao.execute_query(query)

        return True