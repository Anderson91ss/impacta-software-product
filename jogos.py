from flask import Flask , render_template, request, redirect, url_for, flash, session
import sqlite3 as sql


app=Flask(__name__)


#-----------------------------------------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template ("login.html")

def registrar_usuario_db(username, password):
    con = sql.connect('registro_jogo.db')
    cur = con.cursor()
    cur.execute('INSERT INTO usuarios_jogo(username,password) values (?,?)', (username, password))
    con.commit()
    con.close()


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        registrar_usuario_db(username, password)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')
    

def verificar_usuario(username, password):
    con = sql.connect('registro_jogo.db')
    cur = con.cursor()
    cur.execute('Select username,password FROM usuarios_jogo WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False




@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(verificar_usuario(username, password))
        if verificar_usuario(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))



@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash("Usuario ou Senha Incorreto","warning")
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


#------------------------------------------------------------------------------------

@app.route("/games")
def games():
    con = sql.connect ('registro_jogo.db')
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("select * from registro_jogo")
    data = cur.fetchall()
    return render_template ("games.html", datas=data)

@app.route("/add_game", methods=["POST", "GET"])
def add_game():
    if request.method=="POST":
        nome_jogo = request.form["nome_jogo"]
        lancamento = request.form["lancamento"]
        plataforma = request.form["plataforma"]
        genero = request.form["genero"]
        desenvolvedora = request.form["desenvolvedora"]
        con = sql.connect ('registro_jogo.db')
        cur = con.cursor()
        cur.execute("insert into registro_jogo(NOME_JOGO,LANCAMENTO,PLATAFORMA,GENERO,DESENVOLVEDORA) values (?, ?, ?, ?, ?)",(nome_jogo, lancamento, plataforma, genero, desenvolvedora))
        con.commit()
        flash("Jogo cadastrado", "success")
        return redirect(url_for("games"))
    return render_template("add_game.html")

@app.route("/edit_game/<string:id>", methods=["POST","GET"])
def edit_game(id):
    if request.method=="POST":
        nome_jogo = request.form["nome_jogo"]
        lancamento = request.form["lancamento"]
        plataforma = request.form["plataforma"]
        genero = request.form["genero"]
        desenvolvedora = request.form["desenvolvedora"] 
        con = sql.connect ('registro_jogo.db')
        cur = con.cursor()
        cur.execute("update registro_jogo set NOME_JOGO=?,LANCAMENTO=?,PLATAFORMA=?,GENERO=?,DESENVOLVEDORA=? where id=?", (nome_jogo, lancamento, plataforma, genero, desenvolvedora, id))
        con.commit()
        flash("Jogo atualizado", "success")
        return redirect(url_for("games"))
    con = sql.connect ('registro_jogo.db')
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("select * from registro_jogo where ID=?", (id))
    data=cur.fetchone()
    return render_template("edit_game.html", datas=data)

@app.route("/delete_game/<string:id>", methods=["GET"])
def delete_game(id):
    con = sql.connect ('registro_jogo.db')
    cur = con.cursor()
    cur.execute("delete from registro_jogo where ID=?", (id))
    con.commit()
    flash("Jogo deletado", "warning")
    return redirect(url_for("games"))

if __name__=='__main__':
    app.secret_key="admin123"
    app.run(debug=True)