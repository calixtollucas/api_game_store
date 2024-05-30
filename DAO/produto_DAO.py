

from flask import Flask, jsonify, request
from flask_mysqldb import mysql


class produto_DAO:

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

    # CREATE
    def cadastrar():
        nome = request.form['nome']
        preco = request.form['preco']
        plataforma = request.form['plataforma']
        categoria = request.form['categoria']
        ativo = request.form.get('ativo', '1')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            f'''INSERT INTO produto (nome, preco, plataforma, categoria ativo) VALUES ({nome}, {preco},{plataforma}, {categoria} ,{ativo})''')
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': "Produto cadastrado com sucesso!"}), 201

    # READ (ID)
    def get_produto_by_id(self):
        query = f'''
        SELECT nome, preco, plataforma, categoria, ativo
        FROM produto
        WHERE id_produto = {id}
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

    # READ (NOME)

    def produto_nome(self, nome):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT preco, plataforma, categoria, ativo FROM produto WHERE nome = %s", (nome,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                'id': id,
                'nome': user[0],
                'preco': user[1],
                'plataforma': user[2],
                'categoria': user[3],
                'ativo': user[4]
            }), 200
        else:
            return jsonify({'message': 'Produto não encontrado via nome'}), 404

    # READ (PLATAFORMA)
    def produto_plataforma(self, plataforma):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nome, preco, categoria, ativo FROM produto WHERE plataforma = %s", (plataforma,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                'id': id,
                'nome': user[0],
                'preco': user[1],
                'plataforma': user[2],
                'categoria': user[3],
                'ativo': user[4]
            }), 200
        else:
            return jsonify({'message': 'Produto não encontrado via plataforma'}), 404

    # READ (CATEGORIA)
    def produto_categoria(self, categoria):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nome, preco, plataforma, ativo FROM produto WHERE categoria = %s", (categoria,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                'id': id,
                'nome': user[0],
                'preco': user[1],
                'plataforma': user[2],
                'categoria': user[3],
                'ativo': user[4]
            }), 200
        else:
            return jsonify({'message': 'Produto não encontrado via categoria'}), 404

    # READ (TIPO) !!!PENDENTE!!!

    # UPDATE
    def atualizar_produto(self, ID, nome, preco, plataforma, categoria, ativo):
        conn = mysql.connect()
        cursor = conn.cursor()

        query = f""" 
        UPDATE produto
        SET nome = '{nome}', preco = '{preco}', plataforma = '{plataforma}',
        categoria = '{categoria}', '{ativo}'
        """

        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        conn.close()

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
