from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    cpfcnpj = db.Column(db.String(20), unique=True, nullable=True)
    tipo = db.Column(db.String(20), nullable=True)  # 'F' for individual, 'J' for legal entity
    numero = db.Column(db.String(10), nullable=True)
    verificado = db.Column(db.String(10), default=False)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    photo_path = db.Column(db.String(200), nullable=True)
    fornecedor = db.Column(db.Boolean(50), nullable=True)
    empresa = db.Column(db.String(50), nullable=True)
    cotacoes = db.relationship('cotacao', backref='user', lazy=True)
    produtos = db.relationship('produto', backref='user', lazy=True)
    lances = db.relationship('lances', backref='user', lazy=True)
    participacoes = db.relationship('participacao', backref='user', lazy=True)
    notificacoes = db.relationship('notificacao', backref='user', lazy=True)
    logs = db.relationship('logs', backref='user', lazy=True)


class cotacao(db.Model):
    __tablename__ = 'cotacao'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    dataFinal = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_estimado = db.Column(db.Float, nullable=False)
    filePath = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.String(50), nullable=True)
    categorias = db.Column(db.String(150), nullable=True)

    status = db.Column(db.String(50), nullable=True)  # 'Aberto', 'Fechado', 'Cancelado'
    lances = db.relationship('lances', backref='cotacao', lazy=True)
    participacoes = db.relationship('participacao', backref='cotacao', lazy=True)


class lances(db.Model):
    __tablename__ = 'lances'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cotacao_id = db.Column(db.Integer, db.ForeignKey('cotacao.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    nome = db.Column(db.String(50), nullable=True)
    data = db.Column(db.DateTime, nullable=False)
    proposta = db.Column(db.String(200), nullable=True)



class participacao(db.Model):
    __tablename__ = 'participacao'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cotacao_id = db.Column(db.Integer, db.ForeignKey('cotacao.id'), nullable=False)
    nome = db.Column(db.String(50), nullable=True)
    data = db.Column(db.DateTime, nullable=False)


class produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(1024), nullable=False)
    data = db.Column(db.Date, nullable=False)
    filePath = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(50), nullable=True)  # 'Aberto', 'Fechado', 'Cancelado'

    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data': self.data.isoformat() if self.data else None,
            'filePath': self.filePath,
            'status': self.status,
            # adicione outros campos conforme necessário
        }
    
class notificacao(db.Model):
    __tablename__ = 'notificacao'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mensagem = db.Column(db.String(200), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    lido = db.Column(db.Boolean, default=False)

class comentarios(db.Model):
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cotacao_id = db.Column(db.Integer, db.ForeignKey('cotacao.id'), nullable=False)
    comentario = db.Column(db.String(200), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    # 1-5 rating
    data = db.Column(db.DateTime, nullable=False)

class logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.String(500), nullable=True)



def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def registrar_log(user_id, action, details=None):
    novo_log = logs(
        user_id=user_id,
        action=action,
        timestamp=datetime.now(),
        details=details
    )
    db.session.add(novo_log)
    db.session.commit()