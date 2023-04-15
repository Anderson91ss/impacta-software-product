import sqlite3 as sql

con = sql.connect ('registro_jogo.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS registro_jogo')

sql = '''CREATE TABLE "registro_jogo" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME_JOGO"      TEXT,
    "LANCAMENTO"     TEXT,
    "PLATAFORMA"     TEXT,
    "GENERO"         TEXT,
    "DESENVOLVEDORA" TEXT
    )'''

cur.execute(sql)
con.commit()
con.close()
