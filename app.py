from flask import Flask , render_template, request, redirect, url_for, flash
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
@app.route("/index")

def index():
    con = sql.connect ('registro_jogo.db')
    con.row_factory=sql.Row
    cur = con.cursor()
    cur.execute("select * from registro_jogo")
    data = cur.fetchall()
    return render_template ("index.html", datas=data)

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
        return redirect(url_for("index"))
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
        return redirect(url_for("index"))
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
    return redirect(url_for("index"))

if __name__=='__main__':
    app.secret_key="admin123"
    app.run(debug=True)
