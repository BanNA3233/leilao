from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import configs
import random
import models
from werkzeug.security import check_password_hash, generate_password_hash
import os
from sqlalchemy import func
from models import registrar_log


app = Flask(__name__)
app.secret_key = "12345678"
app.config['SQLALCHEMY_DATABASE_URI'] = configs.uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.init_db(app)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# Filtro personalizado para formatar números de telefone
@app.template_filter('phone_br')
def phone_br(phone):
    if phone and len(phone) == 11:  # Formato: (XX) XXXXX-XXXX
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif phone and len(phone) == 10:  # Formato: (XX) XXXX-XXXX
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return phone  # Retorna o número original se não for válido

@app.route('/')
def index():
    cotacoes = models.cotacao.query.filter(models.cotacao.status == "Aberto").all()
    return render_template('./model/home.html', cotacoes=cotacoes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']

        user = models.User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, senha):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session["user_verificado"] = user.verificado
            registrar_log(user.id, 'Login', f'Usuário {user.name} logou no sistema.')
            if user.phone == None:
                registrar_log(user.id, 'Registro Incompleto', f'Usuário {user.name} redirecionado para completar registro.')
                return render_template('./registro/completarRegistro.html')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos!')
            registrar_log(None, 'Falha de Login', f'Email ou senha incorretos para o email {email}.')
            message = 'Email ou senha incorretos!'
            return render_template('./login/index.html', message=message)
    return render_template('./login/index.html')

@app.route('/logout')
def logout():
    registrar_log(session["id"], 'Logout', 'Usuário deslogou do sistema.')
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_verificado', None)
    
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        senha = request.form['password']

        senha_hash = generate_password_hash(senha)

        isExist = models.User.query.filter_by(email=email).first()
        if isExist:
            flash('Email já cadastrado!')
            message = 'Email já cadastrado!'
            return render_template('./registro/index.html', message=message)
        if not nome or not email or not senha:
            flash('Preencha todos os campos!')
            message = 'Preencha todos os campos!'
            return render_template('./registro/index.html', message=message)
        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres!')
            message = 'A senha deve ter pelo menos 8 caracteres!'
            return render_template('./registro/index.html', message=message)
        if not any(char.isdigit() for char in senha):
            flash('A senha deve conter pelo menos um número!')
            message = 'A senha deve conter pelo menos um número!'
            return render_template('./registro/index.html', message=message)
        if not any(char.isupper() for char in senha):
            flash('A senha deve conter pelo menos uma letra maiúscula!')
            message = 'A senha deve conter pelo menos uma letra maiúscula!'
            return render_template('./registro/index.html', message=message)
        if not any(char.islower() for char in senha):
            flash('A senha deve conter pelo menos uma letra minúscula!')
            message = 'A senha deve conter pelo menos uma letra minúscula!'
            return render_template('./registro/index.html', message=message)
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in senha):
            flash('A senha deve conter pelo menos um caractere especial!')
            message = 'A senha deve conter pelo menos um caractere especial!'
            return render_template('./registro/index.html', message=message)
        if len(nome) < 3:
            flash('O nome deve ter pelo menos 3 caracteres!')
            message = 'O nome deve ter pelo menos 3 caracteres!'
            return render_template('./registro/index.html', message=message)
        else:
            user = models.User(name=nome, email=email, password=senha_hash, photo_path='../../static/img/default.jpg')
            models.db.session.add(user)
            models.db.session.commit()
            registrar_log(user.id, 'Registro', f'Usuário {user.name} registrado com sucesso.')
            return redirect(url_for('login'))
    return render_template('./registro/index.html')

@app.route('/completarRegistro', methods=['POST'])
def completarR():
    tipo = request.form['tipo-E']
    cpfcnpj = request.form['cpf']
    cep = request.form['cep']
    endereco = request.form['endereco']
    numero = request.form['numero']
    bairro = request.form['bairro']
    cidade = request.form['cidade']
    telefone = request.form['telefone']
    estado = request.form['estado']

    user = models.User.query.filter_by(id=session['user_id']).first()

    if tipo == 'F':
        user.empresa = user.name

    user.phone = telefone
    user.tipo = tipo
    user.cpfcnpj = cpfcnpj
    user.zip_code = cep
    user.address = endereco
    user.numero = numero
    user.bairro = bairro
    user.city = cidade
    user.country = 'Brasil'
    user.state = estado
    models.db.session.commit()
    registrar_log(user.id, 'Registro Completo', f'Usuário {user.name} completou o registro.')
    return redirect(url_for('index'))

@app.route('/perfil/<id>', methods=['GET'])
def perfil(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = models.User.query.filter_by(id=id).first()
    if user:
        print(user.verificado)
        return render_template('./perfil/index.html', user=user)
    

@app.route("/cotacoes/<id>", methods=["GET", "POST"])
def cotacoes(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if id == 'lastday':
        cotacoes = models.cotacao.query.filter(models.cotacao.dataFinal == datetime.today().date()).all()
        made = 'a vencer hoje'
        print(datetime.today().date())
        print(cotacoes)
        return render_template('./cotacoes/index.html', cotacoes=cotacoes, made=made)
    else:
        cotacao = models.cotacao.query.filter_by(id=id).first()
        user = models.User.query.filter(models.User.id == session['user_id']).first()
        print(session['user_id'])
        propostas = models.lances.query.filter(models.lances.cotacao_id == id).all()
        return render_template('./produto/leilao.html', cotacao=cotacao, user=user, propostas=propostas)
    
@app.route("/criarCotacao", methods=["POST"])
def criarCotacao():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data = datetime.today()
        dataFinal = request.form['data_fim']
        tipo = request.form['tipo']
        valor = request.form['valor']
        quantidade = request.form['quantidade']
        file = request.files['banner']

        filePath = f"static/uploads/user_{user_id}/{data.strftime('%Y-%m-%d')}"

        os.makedirs(filePath, exist_ok=True)
        file.save(filePath+"/"+str(random.randint(1, 1000))+".jpg")
        cotacoes = models.cotacao(
            user_id=user_id,
            titulo=titulo,
            descricao=descricao,
            data=data,
            dataFinal=dataFinal,
            tipo=tipo,
            valor_estimado=valor,
            quantidade=quantidade,
            filePath=filePath+"/"+str(random.randint(1, 1000))+".jpg",
            status="Aberto" 
        )

        models.db.session.add(cotacoes)
        models.db.session.commit()

        cotacao = models.cotacao.query.filter_by(user_id=user_id).first()
        registrar_log(user_id, 'Cotação Criada', f'Usuário {session["user_name"]} criou uma nova cotação: {titulo}.')
        print(cotacao)
        return redirect(url_for('cotacoes', id=cotacao.id))
    
@app.route('/serFornecedor', methods=['POST','GET'])
def serFornecedor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = models.User.query.filter_by(id=session['user_id']).first()
    if user.fornecedor == "ativo":
        return render_template('./perfil/fornecedor.html', user=user, message="Você já é um fornecedor ativo!")
    else:
        registrar_log(user.id, 'Solicitação de Fornecedor', f'Usuário {user.name} solicitou ser fornecedor.')
        return render_template('./perfil/Vfornecedor.html', user=user)
    
@app.route('/perfil/fornecedor/', methods=['POST', 'GET'])
@app.route('/perfil/fornecedor/<method>', methods=['POST', 'GET'])
def fornecedor(method=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = models.User.query.filter_by(id=session['user_id']).first()
    if method == None:
        registrar_log(user.id, 'Acesso ao Perfil de Fornecedor', f'Usuário {user.name} acessou o perfil de fornecedor.')
        cotacoes = models.participacao.query.filter(models.participacao.user_id == session['user_id']).count()
        print(cotacoes)
        propostas = models.lances.query.filter(models.lances.user_id == session['user_id']).count()
        comentarios = models.notificacao.query.filter(models.notificacao.user_id == session['user_id']).count()
        media_nota = models.comentarios.query.with_entities(func.avg(models.comentarios.nota)).filter(models.comentarios.user_id == session['user_id']).scalar()
        if media_nota is not None:
            media_nota = round(media_nota, 2)
        else:
            media_nota = "Sem avaliações"

        return render_template('./perfil/perfilFornecedor.html', media_nota=media_nota, cotacoes=cotacoes, propostas=propostas,comentarios=comentarios, user=user)
    if method == 'produto':
        produtos = models.produto.query.filter(models.produto.user_id == session['user_id']).all()
        print(produtos)
        return render_template('./perfil/perfilFornecedorProduto.html', produtos=produtos, user=user)
    if method == 'cproduto':
        if request.method == 'POST':
            user_id = session['user_id']
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            data = datetime.today()
            file = request.files['foto_principal']
            aditionals = request.files.getlist('fotos_adicionais')
            

            print(aditionals)
            filePath = f"static/uploads/user_{user_id}/{data.strftime('%Y-%m-%d')}/{str(random.randint(1, 1000))}"

            os.makedirs(filePath, exist_ok=True)
            file.save(filePath+"/"+"principal.jpg")

            a = 0
            for aditional_file in aditionals:
                if aditional_file and aditional_file.filename:  # Verifica se o arquivo foi enviado
                    aditional_file.save(filePath + f"/{a}_adicional.jpg")
                    a += 1
            
            
            produto = models.produto(
                user_id=user_id,
                titulo=titulo,
                descricao=descricao,
                data=data,
                filePath=filePath,
                status="Aberto" 
            )

            models.db.session.add(produto)
            models.db.session.commit()
            registrar_log(user_id, 'Produto Criado', f'Usuário {session["user_name"]} criou um novo produto: {titulo}.')
            return redirect(url_for('fornecedor', method='produto'))
    if method == 'historico':
        return render_template('./perfil/perfilfornecedorhistorico.html', user=user)

@app.route('/api/<method>/', methods=['GET'])
def get_products(method):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if method == 'produto':
        produtos = models.produto.query.filter(models.produto.user_id == session['user_id']).all()
        print(produtos)
        return jsonify(produtos=[produto.serialize() for produto in produtos]), 200


@app.route('/notificacaoCount', methods=['GET'])
def notificacaoCount():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    notificacoes = models.notificacao.query.filter(
        models.notificacao.user_id == session['user_id'],
        models.notificacao.lido == False
    ).count()
    print(notificacoes)
    return jsonify({"notificacoes": notificacoes}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
