from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario, Post, Comentario

with app.app_context():
    database.create_all()