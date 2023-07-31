from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Chave secreta para sessão

# Configuração do banco de dados
db = mysql.connector.connect(
    host='localhost',
    database='bd_pessoa',
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

# Rota da página inicial (login)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        matricula = request.form['matricula']

        # Verificar se a matrícula existe no banco de dados
        cursor.execute("SELECT * FROM pessoa WHERE matricula = %s", (matricula,))
        pessoa = cursor.fetchone()

        if pessoa:
            # Se a matrícula existe, autenticar o usuário e redirecionar para a página de opções
            user = User(matricula)
            login_user(user)
            return redirect('/opcao')
        else:
            # Se a matrícula não existe, exibir alert em JavaScript e redirecionar para a página inicial
            return render_template('index.html', invalid_matricula=True)

    return render_template('index.html')

# Rota da página de opções
@app.route('/opcao')
@login_required
def opcao():
    matricula = current_user.id
    # Buscar nome da pessoa no banco de dados
    cursor.execute("SELECT nome FROM pessoa WHERE matricula = %s", (matricula,))
    nome = cursor.fetchone()[0]
    return render_template('opcao.html', nome=nome)

# Rota da página de dados
@app.route('/dados', methods=['GET', 'POST'])
@login_required
def dados():
    matricula = current_user.id
    # Buscar nome da pessoa no banco de dados
    cursor.execute("SELECT nome FROM pessoa WHERE matricula = %s", (matricula,))
    nome = cursor.fetchone()[0]

    # Exibir dados existentes
    cursor.execute("SELECT * FROM pessoa")
    dados = cursor.fetchall()

    if request.method == 'POST':
        # Inserir novos dados no banco de dados
        nome = request.form['nome']
        cargo = request.form['cargo']
        matricula = request.form['matricula']
        cursor.execute("INSERT INTO pessoa (matricula, nome, cargo) VALUES (%s, %s, %s)", (matricula, nome, cargo))
        db.commit()
        return redirect(url_for('dados'))

    return render_template('dados.html', nome=nome, dados=dados)

# Rota de logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
