# Comunidade de Estudo

**Um projeto feito para demonstração de estudo pessoal e integração de Python com Flask.**

## Descrição

Projeto criado e testado localmente usando PyCharm (Python 3.12). 

## Instruções de Execução

1. Execute o arquivo `main.py`.
2. O arquivo `requirements.txt` contém todas as dependências utilizadas no decorrer do desenvolvimento.

## Banco de Dados

Para conceder privilégios de administrador:
1. Abra a pasta `instance` e acesse `comunidade.db` com um programa de manuseio de banco de dados (exemplo: DB Browser for SQLite).
2. Vá até a tabela `usuario`, clique com o botão direito e selecione "navegar tabela".
3. Na coluna `is_admin`, altere o valor de `0` para `1` e aplique as alterações.

## Funcionalidades

- Cadastro de e-mail e username (nome de usuário)
- Senhas encriptadas
- Posts (editar/excluir/adicionar comentários)
- Perfil de usuário com foto de avatar
- Marcação de "cursos"

## Objetivo
O objetivo principal deste projeto é demonstrar as habilidades adquiridas no curso Hashtag Treinamentos, aplicando técnicas de desenvolvimento e evidenciando minha vontade de aprender e me desenvolver continuamente. As seguintes técnicas foram incluídas:

- Ativação de permissões administrativas
- Opção de comentários em posts
- Área organizada para recuperação de senha
- Opção do usuário para excluir sua conta e todos os posts associados
