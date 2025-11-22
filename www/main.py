from flask import Flask, render_template, request, flash, redirect, session, jsonify, g
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecycle123'
app.config['DATABASE'] = 'usuarios.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def create_table():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        cpf TEXT NOT NULL,
        endereco TEXT NOT NULL,
        numero TEXT NOT NULL,
        complemento TEXT NOT NULL
    );
''')
    db.commit()

with app.app_context():
    create_table()


@app.route("/")
def principal():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('telaLogin.html')


@app.route("/acesso", methods=['POST'] )
def acesso():
    email = request.form.get('email')
    senha = request.form.get('password')

    db = get_db()
    usuario = db.execute('SELECT * FROM usuario WHERE email = ? AND senha = ?', (email, senha)).fetchone()

    if usuario:
        return redirect('/home')
    else:
        flash('Email e/ou senha invalidos, tente novamente!')
        return redirect('/login')
    
    
@app.route("/cadastro")
def cadastro():
    return render_template('telaCadastro.html')


@app.route("/cadastrando", methods=['POST'])
def cadastrando():
    nome = request.form.get('name')
    email = request.form.get('email')
    senha = request.form.get('password')
    cpf = request.form.get('cpf')
    endereco = request.form.get('address')
    numero = request.form.get('number')
    complemento = request.form.get('complement')

    db = get_db()
    db.execute('''
        INSERT INTO usuario (nome, email, senha, cpf, endereco, numero, complemento) VALUES(?, ?, ?, ?, ?, ?, ?)
''', (nome, email, senha, cpf, endereco, numero, complemento))
    
    db.commit()

    flash('Senha bem vindo, {nome}!!')

    return redirect('/')


@app.route('/home')
def home():
    return render_template('telaPrincipal.html')

@app.route('/store')
def store():
    return render_template('telaLoja.html')

@app.route('/store/Dell')
def dell():
    return render_template('./produtos/prodDell.html')

@app.route('/store/Mouse')
def mouse():
    return render_template('./produtos/prodMouse.html')

@app.route('/store/Phone')
def phone():
    return render_template('./produtos/prodPhone.html')

@app.route('/store/Placa')
def placa():
    return render_template('./produtos/prodPlaca.html')

@app.route('/missions')
def missions():
    return render_template('telaMissoes.html')

@app.route('/news')
def news():
    return render_template('telaNoticia.html')

@app.route('/news/Alok')
def alok():
    return render_template('./artigos/artigoAlok.html')

@app.route('/news/Inclusao')
def inclusao():
    return render_template('./artigos/artigoInclusao.html')

@app.route('/news/Multirao')
def multirao():
    return render_template('./artigos/artigoMultirao.html')

@app.route('/news/Plastico')
def plastico():
    return render_template('./artigos/artigoPlastico.html')

@app.route('/news/Robo')
def robo():
    return render_template('./artigos/artigoRobo.html')

@app.route('/profile')
def profile():
    return render_template('telaPerfil.html')

@app.route('/ecopoints')
def ecopoints():
    return render_template('telaPontos.html')

@app.route('/videos')
def videos():
    return render_template('telaVideos.html')




if __name__ in '__main__':
    app.run(debug=True)