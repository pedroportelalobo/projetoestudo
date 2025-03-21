from comunidadeimpressionadora import database, login_manager
from comunidadeimpressionadora.decorators import admin_required
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True, cascade='all, delete-orphan')
    cursos = database.Column(database.String, nullable=False, default='Não Informado')
    is_admin = database.Column(database.Boolean, default=False)

    def contar_posts(selfs):
        return len(selfs.posts)

    def excluir_perfil(self):
        for post in self.posts:
            database.session.delete(post)
        database.session.delete(self)
        database.session.commit()

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    comentarios = database.relationship('Comentario', back_populates='post', lazy=True, cascade="all, delete-orphan")


class Comentario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    corpo = database.Column(database.String(500), nullable=False)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)
    post_id = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False)
    post = database.relationship('Post', back_populates='comentarios')
    username = database.Column(database.String(100), nullable=False)
