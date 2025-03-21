from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user
from markupsafe import Markup

class FormCriarConta(FlaskForm):
    username = StringField('Nome do Usuário:', validators=[DataRequired(), Length(4, 12)])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha:', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastra-se com outro e-mail ou faça login para continuar')

    def validate_username(self, username):
        loginuser = Usuario.query.filter_by(username=username.data).first()
        if loginuser:
            raise ValidationError('Usuário já cadastrado. Cadastra-se com outro username')

class FormLogin(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class FormResetar(FlaskForm):
    email = StringField('Insira o E-mail para Recuperação:', validators=[DataRequired()])
    botao_submit_resetar = SubmitField('Recuperar Senha')
    botao_retornar_login = SubmitField('Retornar ao login')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do Usuário:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil:', validators=[FileAllowed(['jpg', 'png'])])

    curso_excell = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')

    botao_submit_editar_perfil = SubmitField('Confirmar')
    botao_excluir_perfil = SubmitField('Excluir Perfil')

def validate_email(self, email):
    if current_user.email != email.data:
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Já existe um Usuário com esse E-mail. Cadastre outro E-mail!')

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')
    botao_submit_editarpos = SubmitField('Atualizar Post')

class FormComentarPost(FlaskForm):
    corpo = TextAreaField('Comentar:', render_kw={"style": "font-weight: bold;"}, validators=[DataRequired()])
    botao_submit_comentarpost = SubmitField('Comentar')

    def __init__(self, *args, **kwargs):
        super(FormComentarPost, self).__init__(*args, **kwargs)
        self.corpo.label = Markup('<strong>Comentar:</strong>')