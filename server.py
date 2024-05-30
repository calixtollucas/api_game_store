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
<<<<<<< HEAD
from produto_DAO import produto_DAO
=======
from DAO.categoria_DAO import categoria_DAO;
>>>>>>> 55fa2d13ceae7cc3f518bf56760669c2195a2429

app = Flask(__name__)

cliente_dao = cliente_DAO()
plataforma_dao = plataforma_DAO()
<<<<<<< HEAD
produto_dao = produto_DAO()
=======
categoria_dao = categoria_DAO()
>>>>>>> 55fa2d13ceae7cc3f518bf56760669c2195a2429

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
    
#REAG ALL
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


if __name__ == '__main__':
    app.run(debug=True)
