from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Chave secreta para sessão

# Configuração do banco de dados
db = mysql.connector.connect(
    host='localhost',
    database='pabd_moveis',
    user='root',
    password='L@binfo212'
)
cursor = db.cursor()

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Classe para representar o usuário
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Função para carregar o usuário pelo ID (matrícula)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rota da página home
@app.route('/')
def home():
    return render_template('home.html')

# Rota da página inicial (login)
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpf = request.form['cpf']

        # Verificar se a matrícula existe no banco de dados
        cursor.execute("SELECT * FROM funcionario WHERE cpf = %s", (cpf,))
        usuario = cursor.fetchone()

        if usuario:
            # Se a matrícula existe, autenticar o usuário e redirecionar para a página de opções
            user = User(cpf)
            login_user(user)
            return redirect('/opcao')
        else:
            # Se a matrícula não existe, exibir alert em JavaScript e redirecionar para a página inicial
            return render_template('index.html', invalid_cpf=True)

    return render_template('index.html')

# Rota da página de opções
@app.route('/opcao')
@login_required
def opcao():
    cpf = current_user.id
    # Buscar nome da pessoa no banco de dados
    cursor.execute("SELECT nome FROM funcionario WHERE cpf = %s", (cpf,))
    nome = cursor.fetchone()[0]



    # Exibir dados existentes dos funcionários
    cursor.execute("SELECT * FROM funcionario")
    dadosf = cursor.fetchall()

    # Exibir dados existentes dos produtos
    cursor.execute("SELECT * FROM produto")
    dadosp = cursor.fetchall()

    return render_template('opcao.html', nome=nome, dadosf=dadosf, dadosp=dadosp)

@app.route('/add_funcionario', methods=['POST'])
@login_required
def add_funcionario():
    if request.method == 'POST':
        # Obter os dados do formulário
        cpf = request.form['cpf']
        nome = request.form['nomeF']
        funcao = request.form['funcao']
        salario = request.form['salario']
        telefone = request.form['telefone']
        email = request.form['email']

        # Inserir os dados no banco de dados
        cursor.execute("INSERT INTO funcionario (cpf, nome, funcao, salario, telefone, email) VALUES (%s, %s, %s, %s, %s, %s)",
                       (cpf, nome, funcao, salario, telefone, email))
        db.commit()  # Confirmar a transação no banco de dados

        # Redirecionar para a página de opções ou para onde desejar após a inserção
        return redirect('/opcao')

    # Em caso de outro tipo de requisição, retornar algo apropriado (pode ser um erro)
    return "Método não permitido"



@app.route('/add_produto', methods=['POST'])
@login_required
def add_produto():
    if request.method == 'POST':
        # Obter os dados do formulário
        codigo = request.form['codigo']
        nome = request.form['nomeP']
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        valor = request.form['valor']
        qntd_estoque = request.form['qntdEstoque']
        cnpj_fornecedor = request.form['cnpjFornecedor']

        # Inserir os dados no banco de dados
        cursor.execute("INSERT INTO produto (codigo, nome, tipo, descricao, valor, qntd_estoque, cnpj_fornecedor) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (codigo, nome, tipo, descricao, valor, qntd_estoque, cnpj_fornecedor))
        db.commit()  # Confirmar a transação no banco de dados

        # Redirecionar para a página de opções ou para onde desejar após a inserção
        return redirect('/opcao')

    # Em caso de outro tipo de requisição, retornar algo apropriado (pode ser um erro)
    return "Método não permitido"



@app.route('/atualizar_funcionario', methods=['POST'])
@login_required
def atualizar_funcionario():
    if request.method == 'POST':
        # Obter os dados do formulário
        cpf = request.form['cpf']
        novo_nome = request.form['novo_nome']
        nova_funcao = request.form['nova_funcao']
        novo_salario = request.form['novo_salario']
        novo_telefone = request.form['novo_telefone']
        novo_email = request.form['novo_email']

        # Atualizar os dados no banco de dados
        cursor.execute("UPDATE funcionario SET nome = %s, funcao = %s, salario = %s, telefone = %s, email = %s WHERE cpf = %s",
                       (novo_nome, nova_funcao, novo_salario, novo_telefone, novo_email, cpf))
        db.commit()  # Confirmar a transação no banco de dados

        # Redirecionar para a página de opções ou para onde desejar após a atualização
        return redirect('/opcao')

    # Em caso de outro tipo de requisição, retornar algo apropriado (pode ser um erro)
    return "Método não permitido"



@app.route('/atualizar_produto', methods=['POST'])
@login_required
def atualizar_produto():
    if request.method == 'POST':
        # Obter os dados do formulário
        codigo = request.form['codigo']
        novo_nome = request.form['novo_nome']
        novo_tipo = request.form['novo_tipo']
        nova_descricao = request.form['nova_descricao']
        novo_valor = request.form['novo_valor']
        nova_qntd_estoque = request.form['nova_qntdEstoque']
        novo_cnpj_fornecedor = request.form['novo_cnpjFornecedor']

        # Atualizar os dados no banco de dados
        cursor.execute("UPDATE produto SET nome = %s, tipo = %s, descricao = %s, valor = %s, qntd_estoque = %s, cnpj_fornecedor = %s WHERE codigo = %s",
                       (novo_nome, novo_tipo, nova_descricao, novo_valor, nova_qntd_estoque, novo_cnpj_fornecedor, codigo))
        db.commit()  # Confirmar a transação no banco de dados

        # Redirecionar para a página de opções ou para onde desejar após a atualização
        return redirect('/opcao')

    # Em caso de outro tipo de requisição, retornar algo apropriado (pode ser um erro)
    return "Método não permitido"


# Rota de logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
