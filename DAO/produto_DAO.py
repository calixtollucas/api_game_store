

from uu import Error
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import (errorcode, connection, MySQLConnection)
from DAO.prod_plat_DAO import prod_plat_DAO
from DAO.database_access import database_access


class produto_DAO:

    prod_plat_dao = prod_plat_DAO()

    def __init__(self):
        self.database_access_dao = database_access()

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
        select p.id_produto, p.nome, p.preco, c.nome as categoria, plat.nome as plataforma, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        where p.id_produto = '{id}';
    '''

        user = self.database_access_dao.fetch(query)[0]


        if user and (user[4]!=0):
            return user
        else:
            return None

    # READ (NOME)

    def get_produto_by_nome(self, nome):

        query = f'''
        select p.id_produto, p.nome, p.preco, c.nome as categoria, plat.nome as plataforma, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        where p.nome = '{nome}';
'''
        
        user = self.database_access_dao.fetch(query)

        if user:
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
            return user
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
    def atualizar_produto(self, request):

        nome = request.form['nome']
        preco = request.form['preco']
        plataforma = request.form['plataforma']
        categoria = request.form['categoria']

        try:
            query = f""" 
            UPDATE produto
            SET nome = '{nome}', preco = '{preco}', plataforma = '{plataforma}',categoria = '{categoria}'
            """

            self.database_access_dao.execute_query(query)

            return True
        except:
            return False

    # DELETE (desativar)
    def desativar_cliente(self, id):
        # PRODUTO ESTÁ CADASTRADO?
        produto = self.get_produto_by_id(id)

        cursor = self.open_cursor()

        # PRODUTO ESTÁ CADASTRADO?
        if not produto:
            return False
        else:
            # DO CONTRÁRIO:
            cursor.execute(
                f'''UPDATE produto SET ativo = 0 WHERE id_produto = {id}''')
            self.db.commit()

        cursor.close()
        self.db.close()
