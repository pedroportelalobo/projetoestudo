from comunidadeimpressionadora import app, database, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormComentarPost, FormResetar
from comunidadeimpressionadora.models import Usuario, Post,  Comentario
from comunidadeimpressionadora.decorators import admin_required
import secrets
import os
from PIL import Image

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts = posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}',  'alert-success')
            redirects_safe = ['/', '/contato', '/usuarios', '/perfil','/perfil/editar', '/login', '/post/criar', 'par_next', '/resetar_senha']
            par_next = request.args.get('next')
            if par_next and (par_next in redirects_safe or par_next.startswith('/post/') and par_next.count('/') == 2):
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario)
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        redirects_safe = ['/', '/contato', '/usuarios', '/perfil', '/login', '/post/criar', 'par_next']
        par_next = request.args.get('next')
        if par_next and par_next in redirects_safe:
            return redirect(par_next)
        else:
            return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/resetar_senha', methods=['GET', 'POST'])
def resetar():
    form = FormResetar()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario:
                flash('E-mail de recuperação enviado! (Em construção)', 'success')
            else:
                flash('E-mail não encontrado!', 'danger')
        else:
            flash('Por favor, preencha todos os campos corretamente.', 'danger')

    return render_template('esquecersenha.html', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito Com Sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name and campo.data:
            lista_cursos.append(campo.label.text)
    if not lista_cursos:
        return 'Não Informado'

    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))

    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        for curso in current_user.cursos.split(';'):
            for campo in form:
                if curso in campo.label.text:
                    campo.data = True
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/perfil/editar/excluir-perfil', methods=['GET', 'POST'])
@login_required
def excluir_perfil():
    if request.method == 'POST':
        current_user.excluir_perfil()
        flash('Seu perfil e posts foram excluídos com sucesso.', 'alert-danger')
        return redirect(url_for('home'))

    return render_template('confirmar_exclusao.html')

@app.route('/usuario/<int:usuario_id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        Post.query.filter_by(id_usuario=usuario.id).delete()
        database.session.commit()
        database.session.delete(usuario)
        database.session.commit()
        flash('Usuário excluído com sucesso.', 'alert-success')
    else:
        flash('Usuário não encontrado.', 'alert-danger')
    return redirect(url_for('usuarios'))

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    form_comentarpost = FormComentarPost()
    return render_template('post.html', post=post, form=form, form_comentarpost=form_comentarpost)


@app.route('/post/<int:post_id>/comentar', methods=['POST'])
@login_required
def comentar(post_id):
    post = Post.query.get_or_404(post_id)
    form_comentarpost = FormComentarPost()

    if form_comentarpost.validate_on_submit():
        comentario_texto = form_comentarpost.corpo.data

        if comentario_texto:
            novo_comentario = Comentario(corpo=comentario_texto, post=post, username=current_user.username)
            database.session.add(novo_comentario)
            database.session.commit()

    return redirect(url_for('exibir_post', post_id=post.id))

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required

def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor or current_user.is_admin:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect((url_for('home')))

    else:
        abort(403)


