import mysql.connector;
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.database_access import database_access

class fornecedor_DAO:

    def __init__(self):
        self.database_access_dao = database_access()

    def fornecedor(self, request):
        nome = request.form["nome"]
        cnpj = request.form["cnpj"]
        telefone = request.form['telefone']
        email = request.form["email"]

        existe = self.get_fornecedor_by_nome(nome)

        if not existe:
            try:
                query = f'''
                INSERT
                INTO fornecedor (nome, cnpj, telefone, email)
                VALUES
                ('{nome}','{cnpj}','{telefone}','{email}');
        '''
                self.database_access_dao.execute_query(query)

                return True
            except:
                return False
        else:
            return False
    
    #READ BY ID
    def get_fornecedor_by_id(self, id_fornecedor):

        query = f'''
        SELECT *
        FROM fornecedor
        WHERE id_fornecedor = '{id_fornecedor}';
        '''

        fornecedor = self.database_access_dao.fetch(query)

        if fornecedor:
            return fornecedor
        else:
            return None
    
    #READ BY cnpj
    def get_fornecedor_by_nome(self, nome):
        query = f'''
        select * 
        from fornecedor
        where nome = '{nome}';
'''

        fornecedor = self.database_access_dao.fetch(query)

        if fornecedor:
            return fornecedor
        else:
            return None
    
    #READ BY probuto
    def get_fornecedor_by_probuto(self, fk_id_probuto):
        query = f'''
        "SELECT *
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
        novo_telefone = request.form['telefone']
        novo_email = request.form["email"]
    
        fornecedor_atualizar = self.get_fornecedor_by_id(id_fornecedor)[0]

        fornecedor_atualizado = {
            'nome': novo_nome if (novo_nome != '') else fornecedor_atualizar[1],
            'cnpj': novo_cnpj if (novo_cnpj != '') else fornecedor_atualizar[2],
            'telefone': novo_telefone if (novo_telefone != '') else fornecedor_atualizar[3],
            'email': novo_email if (novo_email != '') else fornecedor_atualizar[4]
        }

        try:

            query = f'''
            UPDATE fornecedor
            SET nome = '{fornecedor_atualizado['nome']}', 
            cnpj = '{fornecedor_atualizado['cnpj']}', 
            telefone = '{fornecedor_atualizado['telefone']}', 
            email = '{fornecedor_atualizado['email']}'
            WHERE id_fornecedor = '{id_fornecedor}'
    '''
            self.database_access_dao.execute_query(query)

            return True
        except:
            return False

    #DELETE
    def fornecedor_desativar(self, id_fornecedor):

        fornecedor = self.get_fornecedor_by_id(id_fornecedor)[0]

        #fornecedor EXISTE?
        if not fornecedor:
            return False
        else:
            query = f'''UPDATE fornecedor SET ativo = 0 WHERE id_fornecedor = '{id_fornecedor}';'''
            self.database_access_dao.execute_query(query)

            return True