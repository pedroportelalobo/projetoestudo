from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv
import sqlalchemy

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para continuar'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)
if not inspector.has_table("usuario"):
    with app.app_contex():
        database.drop_all()
        database.create_all()
        print("Base de dados Criada")
else:
    print("Base de dados inexistente")


from comunidadeimpressionadora import routes
