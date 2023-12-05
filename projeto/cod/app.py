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
    password='labinfo'
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

# Rota da página inicial (login)
@app.route('/', methods=['GET', 'POST'])
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

# Rota de logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
