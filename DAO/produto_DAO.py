
from uu import Error
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.prod_plat_DAO import prod_plat_DAO
from DAO.database_access import database_access
from DAO.categoria_DAO import categoria_DAO


class produto_DAO:

    

    def __init__(self):
        self.database_access_dao = database_access()
        self.prod_plat_dao = prod_plat_DAO()

    # CREATE
    def cadastrar(self, request):
        nome = request.form['nome']
        preco = request.form['preco']
        plataforma = request.form['plataforma']
        categoria = request.form['categoria']

        query = f'''
        INSERT 
        INTO produto (nome, preco, fk_id_categoria) 
        VALUES ('{nome}', '{preco}','{categoria}')
        '''
        try:
            
            self.database_access_dao.execute_query(query)

            id_produto = self.get_produto_by_nome(nome)[0]

            self.prod_plat_dao.create_prod_plat(id_produto, plataforma)

            return True
        except Error as err:
            print(err)
            return False

    # READ (ID)
    def get_produto_by_id(self, id):
        query = f'''
        select p.id_produto, p.nome, p.preco, c.id_categoria as categoria, plat.id_plataforma as plataforma, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        where p.id_produto = '{id}';
    '''

        user = self.database_access_dao.fetch(query)[0]


        if user and (user[5]!=0):
            return user
        else:
            return None

    # READ (NOME)

    def get_produto_by_nome(self, nome):

        query = f'''
        select p.id_produto, p.nome, p.preco, c.id_categoria as categoria, plat.id_plataforma as plataforma, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        where p.nome = '{nome}';
'''
        
        user = self.database_access_dao.fetch(query)[0]

        if user and user[5]!= 0:
            return user
        else:
            return None

    # READ (PLATAFORMA)
    def produto_plataforma(self, plataforma):

        plataforma = plataforma.upper()

        query = f'''
        select p.id_produto, p.nome, p.preco, c.nome as categoria, plat.nome as plataforma, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        where plat.nome = '{plataforma}';
'''
        
        user = self.database_access_dao.fetch(query)

        if user:
            result = []
            for u in user:
                if u[5]!= 0:
                    result.append(u)
            return result
        else:
            return None

    # READ (CATEGORIA)
    def produto_categoria(self, categoria):

        query = f'''
        select p.id_produto, p.nome, p.preco, c.nome as categoria, plat.nome as plataforma, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        where c.nome = '{categoria}';
'''
        
        produtos = self.database_access_dao.fetch(query)
        result = []

        if produtos:
            return produtos
        else:
            return None

    # READ (TIPO) !!!PENDENTE!!!

    # UPDATE
    def atualizar_produto(self, params, id):

        #pesquisar o produto a ser atualizado
        produto_atualizar = self.get_produto_by_id(id)

        #adicionar novos valores num outro dict onde os campos serão os novos caso os mesmos não forem vazios
        #e caso estiverem, terão os mesmos valores dos campos do produto pesquisado
        produto_atualizado = {
            'nome': params['nome'] if (params['nome'] != '') else produto_atualizar[1],
            'preco': params['preco'] if (params['preco'] != '') else produto_atualizar[2],
            'categoria': params['categoria'] if (params['categoria'] != '') else produto_atualizar[3],
            'plataforma': params['plataforma'] if (params['plataforma'] != '') else produto_atualizar[4],
        }

        # alterar o produto, juntamente com as tabelas prod_plat e forn_prod
        query = f'''
        UPDATE produto
        SET nome = '{produto_atualizado['nome']}', preco = '{produto_atualizado['preco']}', fk_id_categoria = '{produto_atualizado['categoria']}'
        WHERE id_produto = '{id}'
'''
        
        self.database_access_dao.execute_query(query)

        #atualizar prod_plat
        prod_plat = self.prod_plat_dao.get_prod_plat(id, produto_atualizar[4])[0]
        
        if self.prod_plat_dao.update_prod_plat(produto_atualizado['plataforma'], prod_plat[0]):
            return True
        else:
            return False

        

    # DELETE (desativar)
    def desativar_produto(self, id):
        # PRODUTO ESTÁ CADASTRADO?
        produto = self.get_produto_by_id(id)

        # PRODUTO ESTÁ CADASTRADO?
        if not produto:
            return False
        else:
            query = f'''UPDATE produto SET ativo = 0 WHERE id_produto = {id}'''
            # DO CONTRÁRIO:
            self.database_access_dao.execute_query(query)

            return True
