
from uu import Error
from DAO.prod_plat_DAO import prod_plat_DAO
from DAO.database_access import database_access
from DAO.fornecedor_DAO import fornecedor_DAO
from DAO.forn_prod_DAO import forn_prod_DAO;


class produto_DAO:

    

    def __init__(self):
        self.database_access_dao = database_access()
        self.prod_plat_dao = prod_plat_DAO()
        self.fornecedor_dao = fornecedor_DAO()
        self.forn_prod_dao = forn_prod_DAO()

    # CREATE
    def cadastrar(self, request):
        nome = request.form['nome']
        preco = request.form['preco']
        plataforma = request.form['plataforma']
        categoria = request.form['categoria']
        fornecedor = request.form['fornecedor']

        try:
            args = [nome, preco, plataforma, categoria, fornecedor]
            self.database_access_dao.call_procedure('create_plataforma', args)
            return True
        except Error as err:
            print(err)
            return False

    # READ (ID)
    def get_produto_by_id(self, id):
        query = f'''
        select p.id_produto, p.nome, p.preco, c.id_categoria as categoria, plat.id_plataforma as plataforma, f.id_fornecedor, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        INNER JOIN forn_prod as fp ON fp.fk_id_produto = p.id_produto
        INNER JOIN fornecedor as f ON fp.fk_id_fornecedor = f.id_fornecedor
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
        select p.id_produto, p.nome, p.preco, c.id_categoria as categoria, plat.id_plataforma as plataforma, f.id_fornecedor, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        INNER JOIN forn_prod as fp ON fp.fk_id_produto = p.id_produto
        INNER JOIN fornecedor as f ON fp.fk_id_fornecedor = f.id_fornecedor
        where p.nome = '{nome}';
'''
        
        user = self.database_access_dao.fetch(query)
        print('user: '+ str(user))

        if user:
            return user
        else:
            return None

    # READ (PLATAFORMA)
    def produto_plataforma(self, plataforma):

        plataforma = plataforma.upper()

        query = f'''
        select p.id_produto, p.nome, p.preco, c.id_categoria as categoria, plat.id_plataforma as plataforma, f.id_fornecedor, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        INNER JOIN forn_prod as fp ON fp.fk_id_produto = p.id_produto
        INNER JOIN fornecedor as f ON fp.fk_id_fornecedor = f.id_fornecedor
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
        select p.id_produto, p.nome, p.preco, c.id_categoria as categoria, plat.id_plataforma as plataforma, f.id_fornecedor, p.ativo
        from produto as p
        INNER JOIN categoria as c ON p.fk_id_categoria = c.id_categoria
        INNER JOIN prod_plat as pd ON pd.fk_id_produto = p.id_produto
        INNER JOIN plataforma as plat ON plat.id_plataforma = pd.fk_id_plataforma
        INNER JOIN forn_prod as fp ON fp.fk_id_produto = p.id_produto
        INNER JOIN fornecedor as f ON fp.fk_id_fornecedor = f.id_fornecedor
        where c.nome = '{categoria}';
'''
        
        produtos = self.database_access_dao.fetch(query)

        if produtos:
            return produtos
        else:
            return None

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
            'fornecedor': params['fornecedor'] if (params['fornecedor'] != '') else produto_atualizar[5]
        }

        args = [
            id,
            produto_atualizado['nome'],
            produto_atualizado['preco'],
            produto_atualizado['plataforma'],
            produto_atualizado['categoria'],
            produto_atualizado['fornecedor']
        ]

        try:
            self.database_access_dao.call_procedure('update_produto', args)
            return True
        except Error as err:
            print(err)
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
