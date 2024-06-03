"""
- CRUD CLIENTE
- Create(cadastro e login)
- Read(id, nome, email)
- update
- delete
"""

from flask import Flask, jsonify, request;
from DAO.cliente_DAO import cliente_DAO as cliente_DAO;
from DAO.plataforma_DAO import plataforma_DAO;
from DAO.produto_DAO import produto_DAO
from DAO.categoria_DAO import categoria_DAO;
from DAO.pedido_DAO import pedido_DAO;
from DAO.fornecedor_DAO import fornecedor_DAO;

app = Flask(__name__)

cliente_dao = cliente_DAO() # TESTADO
plataforma_dao = plataforma_DAO() # TESTADO
produto_dao = produto_DAO()
categoria_dao = categoria_DAO()
fornecedor_dao = fornecedor_DAO()
pedido_dao = pedido_DAO()

#CREATE (CADASTRO)
@app.route('/cadastrar', methods = ['POST'])
def cadastrar():
    
    cliente_dao.cadastrar(request)

    return jsonify({'message': "Cliente cadastrado com sucesso!"}),201


#CREATE (LOGIN)
@app.route('/login', methods = ['POST'])
def login():
    
    user = cliente_dao.check_login(request)

    if user:
        return jsonify({"Message": "logado com sucesso"}), 200
    else:
        return jsonify({"Message": "Este usuário não existe"}), 404

    
    

#READ BY ID
@app.route('/cliente/id/<int:id>', methods = ['GET'])
def clientes_id(id):

    user = cliente_dao.get_client_by_id(id)
    
    if user:
        return jsonify({
            'id': id,
            'nome': user[0],
            'email': user[1],
            'telefone': user[2],
            'ativo': user[3]
        }), 200
    else:
        return jsonify({'message': 'Cliente não encontrado via ID'}), 404
    
#READ BY NAME
@app.route('/cliente/nome/<string:nome>', methods = ['GET'])
def cliente_nome(nome):

    user = cliente_dao.get_cliente_by_nome(nome)
    
    if user and (user[5]!=0):
        return jsonify({
            'nome': nome,
            'id': user[0],
            'email': user[1],
            'telefone': user[2],
            'ativo': user[3]
        }), 200
    
    else: 
        return jsonify({'message': 'Cliente não encontrado via nome'}), 404
    
#READ BY EMAIL
@app.route('/cliente/email/<string:email>', methods = ['GET'])
def cliente_email(email):

    user = cliente_dao.get_cliente_by_email(email)

    if user[5] == 0:
        return jsonify({"Mensagem": "Este usuário não existe"})
    
    if user:
        return jsonify({
            'email': email,
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'senha': user[3],
            'telefone': user[4],
            'ativo': user[5],
        })
    else:
        return jsonify({'message': 'Cliente não encontrado via email'})

#UPDATE 
@app.route('/cliente/atualizar/<int:id>', methods = ['PUT'])
def cliente_atualizar(id):
    
    if cliente_dao.atualizar_cliente(id, request):
        return jsonify({'message': 'Cliente atualizado com sucesso'})
    else:
        return jsonify({'message': 'O cliente não foi atualizado, verifique se o id é o correto'}), 200

#DELETE
@app.route('/cliente/alterar_ativo/<int:id>', methods = ['DELETE'])
def cliente_desativar(id):
   
    if cliente_dao.desativar_cliente(id):
        return jsonify({'message': 'Campo "ativo" alterado com sucesso'}), 200 
    else:
        return jsonify({'message': 'O cliente não existe, não pode ser desativado'})
    

#CRUD PLATAFORMA
#CREATE PLATAFORMA
@app.route('/plataforma', methods = ['POST'])
def create_plataforma():
    
    if plataforma_dao.create_plataforma(request):
        return jsonify({
            'message': 'Plataforma criada com sucesso'
        })
    else:
        return jsonify({
            'message': 'plataforma não foi criada'
        })
    
#READ ALL
@app.route('/plataforma', methods=['GET'])
def get_all_plataforma():
    plataformas = plataforma_dao.get_all_plataforma()

    if plataformas:

        retorno = []

        for plataforma in plataformas:
            retorno.append({
                'id': plataforma[0],
                'nome': plataforma[1],
                'ativo': plataforma[2]
            })

        return jsonify(retorno)
    else:
        jsonify({
            "message": "Não foi possível acessar os dados ou a tabela está vazia"
        })

#READ PLATAFORMA BY ID
@app.route('/plataforma/id/<int:id>', methods = ['GET'])
def get_plataforma_by_id(id):

    plataforma = plataforma_dao.get_plataforma_by_id(id)
    
    if plataforma and (plataforma[2]!=0):
        return jsonify({
            'id': plataforma[0],
            'nome': plataforma[1],
            'ativo': plataforma[2]
        })
    else:
        return jsonify({
            'Message': 'Esta plataforma não existe'
        })

#UPDATE PLATAFORMA
@app.route('/plataforma/<int:id>', methods=['PUT'])
def update_plataforma(id):

    updated = plataforma_dao.update_plataforma(request, id)

    if updated:
        return jsonify({
            'message': 'Plataforma Atualizada com sucesso'
        }), 200
    else:
        return jsonify({
            'message': 'A plataforma especificada não existe ou ocorreu algum erro na requisição'
        }), 200

#DELETE PLATAFORMA
@app.route('/plataforma/<int:id>', methods = ['DELETE'])
def delete_plataforma(id):
    
    deleted = plataforma_dao.delete_plataforma(id)

    if deleted:
        return jsonify({
            'message': 'deletado com sucesso'
        })
    else:
        return jsonify({
            'message': 'A plataforma não existe ou ocorreu algum erro'
        })

# CRUD CATEGORIA
# CREATE de Categoria
@app.route('/categoria', methods=['POST'])
def create_categoria():
    if categoria_dao.create_categoria(request):
        return jsonify({'message': "Categoria criada com sucesso!"}), 201
    else:
        return jsonify({'message': "Erro ao criar a categoria"}), 400

# READ Categoria pelo ID
@app.route('/categoria/id/<int:id>', methods=['GET'])
def get_categoria_by_id(id):
    categoria = categoria_dao.get_categoria_by_id(id)
    if categoria:
        return jsonify({
            'id': categoria[0],
            'nome': categoria[1],
            'ativo': categoria[2]
        }), 200
    else:
        return jsonify({'message': 'Categoria não encontrada via ID'}), 404

# READ Categoria pelo Nome
@app.route('/categoria/nome/<string:nome>', methods=['GET'])
def get_categoria_by_nome(nome):
    categoria = categoria_dao.get_categoria_by_nome(nome)
    if categoria:
        return jsonify({
            'id': categoria[0],
            'nome': categoria[1],
            'ativo': categoria[2]
        }), 200
    else:
        return jsonify({'message': 'Categoria não encontrada via nome'}), 404

# UPDATE Categoria
@app.route('/categoria/<int:id>', methods=['PUT'])
def update_categoria(id):
    if categoria_dao.update_categoria(id, request):
        return jsonify({'message': 'Categoria atualizada com sucesso'}), 200
    else:
        return jsonify({'message': 'Erro ao atualizar a categoria'}), 400

# DELETE Categoria
@app.route('/categoria/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    if categoria_dao.delete_categoria(id):
        return jsonify({'message': 'Categoria deletada com sucesso'}), 200
    else:
        return jsonify({'message': 'Erro ao deletar a categoria'}), 400

#CRUD PRODUTO
#CREATE PRODUTO
@app.route('/produto', methods=['POST'])
def create_produto():

    produto_criado = produto_dao.cadastrar(request)

    if produto_criado:
        return jsonify({
            'message': 'Produto Criado com Sucesso'
        })
    else:
        return jsonify({
            'message': 'não foi possível criar seu produto'
        })

@app.route('/produto/id/<int:id>', methods=['GET'])
def get_produto_id(id):
    produto = produto_dao.get_produto_by_id(id)
    print(produto)

    if produto and (produto[0]!=0):
        return jsonify({
            'id': produto[0],
            'nome': produto[1],
            'preco': produto[2],
            'categoria': produto[3],
            'plataforma': produto[4],
            'fornecedor': produto[5],
            'ativo': produto[6]
        })
    else:
        return jsonify({
            'message': 'O produto não existe'
        })

@app.route('/produto/nome/<string:nome>', methods=['GET'])
def get_produto_nome(nome):

    produtos = produto_dao.get_produto_by_nome(nome)

    result = []

    if produtos is None:
        result = {
            'message': 'produto nao encontrado'
        }
    else:
        for prod in produtos:

            if prod and prod[6]!=0:
                result.append({
                    'id': prod[0],
                    'nome': prod[1],
                    'preco': prod[2],
                    'categoria': prod[3],
                    'plataforma': prod[4],
                    'fornecedor': prod[5],
                    'ativo': prod[6]
                })
        
    return jsonify(result)

@app.route('/produto/plataforma/<string:plataforma>', methods = ['GET'])
def get_produto_by_plataforma(plataforma):
    produtos = produto_dao.produto_plataforma(plataforma)
    result = []

    if produtos is None:
        result = {
            'message': 'Produto nao encontrado via Plataforma'
        }
    else:
        for produto in produtos:

            if produto and produto[6]!=0:
                result.append({
                    'id': produto[0],
                    'nome': produto[1],
                    'preco': produto[2],
                    'categoria': produto[3],
                    'plataforma': produto[4],
                    'fornecedor': produto[5],
                    'ativo': produto[6]
                })
    
    return jsonify(result)

@app.route('/produto/categoria/<string:categoria>')
def get_produto_by_categoria(categoria):
    produtos = produto_dao.produto_categoria(categoria)
    result = []

    if produtos is not None:
        for produto in produtos:
            if produto and produto[6]!= 0:
                result.append({
                    'id': produto[0],
                    'nome': produto[1],
                    'preco': produto[2],
                    'plataforma': produto[3],
                    'categoria': produto[4],
                    'fornecedor': produto[5],
                    'ativo': produto[6]
                    })
    else:
        result.append({
            'message': 'produto nao encontrado via Categoria'
        })
    
    return jsonify(result)

#UPDATE PRODUTO
@app.route('/produto/<int:id>', methods = ['PUT'])
def update_produto(id):
    
    params = {
        'nome': request.form['nome'],
        'preco': request.form['preco'],
        'plataforma':request.form['plataforma'],
        'categoria': request.form['categoria'],
        'fornecedor': request.form['fornecedor']
    }

    atualizado = produto_dao.atualizar_produto(params, id)

    return jsonify({'message': 'atualizado!'})

#DELETE PRODUTO
@app.route('/produto/<int:id>', methods = ['DELETE'])
def delete_produto(id):
    deletado = produto_dao.desativar_produto(id)

    if deletado:
        return jsonify({
            'message': 'produto deletado com sucesso'
        })
    else:
        return jsonify({
            'message': 'não foi possível deletar o produto'
        })

#CRUD FORNECEDOR
#CREATE
@app.route('/fornecedor', methods=['POST'])
def create_fornecedor():

    criado = fornecedor_dao.fornecedor(request)

    if criado:
        return jsonify({
            'message': 'fornecedor criado com sucesso'
        })
    else:
        return jsonify({
            'message': 'Não foi possível criar o fornecedor'
        })

#GET FORNECEDOR ID
@app.route('/fornecedor/id/<int:id>')
def get_fornecedor_id(id):
    fornecedor = fornecedor_dao.get_fornecedor_by_id(id)[0]

    if fornecedor and fornecedor[5]!= 0:
        return jsonify({
            'id': fornecedor[0],
            'nome': fornecedor[1],
            'cnpj': fornecedor[2],
            'telefone': fornecedor[3],
            'email': fornecedor[4],
            'ativo': fornecedor[5]
        })
    else:
        return jsonify({
            'message': 'Fornecedor não encontrado via ID'
        })
    
#GET FORNECEDOR NOME
@app.route('/fornecedor/nome/<string:nome>', methods=['GET'])
def get_fornecedor_nome(nome):
    fornecedor = fornecedor_dao.get_fornecedor_by_nome(nome)[0]

    if fornecedor and fornecedor[5]!=0:
        return jsonify({
            'id': fornecedor[0],
            'nome': fornecedor[1],
            'cnpj': fornecedor[2],
            'telefone': fornecedor[3],
            'email': fornecedor[4],
            'ativo': fornecedor[5]
        })
    else:
        return jsonify({
            'message': 'Fornecedor não encontrado via ID'
        })
#UPDATE FORNECEDOR
@app.route('/fornecedor/<int:id>', methods = ['PUT'])
def update_fornecedor(id):
    updated = fornecedor_dao.fornecedor_atualizar(id, request)

    if updated:
        return jsonify({
            'message': 'Atualizado'
        })
    else:
        return jsonify({
            'message': 'Não foi possível atualizar'
        })

#DELETE FORNECEDOR
@app.route('/fornecedor/<int:id>', methods = ['DELETE'])
def delete_fornecedor(id):
    deletado = fornecedor_dao.fornecedor_desativar(id)

    if deletado:
        return jsonify({
            'message': 'Deletado'
        })
    else:
        return jsonify({
            'message': 'Não foi possível deletar'
        })

#CRUD PEDIDO
#CREATE PEDIDO
@app.route('/pedido', methods=['POST'])
def create_pedido():
  
    params = {
        'endereco': request.form["endereco"],
        'id_cliente': request.form["id_cliente"],
        'id_produto': request.form["id_produto"]
    }

    pedido_criado = pedido_dao.pedido(params)

    print(pedido_criado)
    if pedido_criado:
        return jsonify({
            'message': 'pedido criado com sucesso'
        })
    else:
        return jsonify({
            'message': 'não foi possível criar o pedido'
        })
    
#GET PEDIDO BY CLIENTE
@app.route('/pedido/cliente_id/<int:id>', methods=['GET'])
def get_pedido_by_id_cliente(id):

    pedido = pedido_dao.get_pedido_by_id_cliente(id)

    if pedido:
        return jsonify(pedido)
    else:
        return jsonify({
            'message': 'pedido não encontrado'
        })
    
#GET PEDIDO BY ENDERECO
@app.route('/pedido/endereco/<string:endereco>', methods = ['GET'])
def get_pedido_by_endereco(endereco):

    pedido = pedido_dao.get_pedido_by_endereco(endereco)

    if pedido:
        return jsonify(pedido)
    else:
        return jsonify({
            'message': 'pedido nao encontrado'
        })

#UPDATE PEDIDO
@app.route('/pedido/<int:id>', methods = ['PUT'])
def update_pedido(id):

    params = {
        'endereco': request.form['endereco'],
        'id_cliente': request.form['id_cliente'],
        'id_produto': request.form['id_produto']
    }

    atualizado = pedido_dao.pedido_atualizar(id, params)

    if atualizado:
        return jsonify({
            'message': 'pedido atualizado com sucesso'
        })
    else:
        return jsonify({
            'message': 'nao foi possivel atualizar o pedido especificado'
        })
#GET PEDIDO ID_CLIENTE
if __name__ == '__main__':
    app.run(debug=True)
