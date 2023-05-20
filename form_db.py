import sqlite3 as sql

con = sql.connect('registro_jogo.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS registro_jogo')
cur.execute('DROP TABLE IF EXISTS usuarios_jogo')

registro_jogo_sql = '''
CREATE TABLE registro_jogo (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME_JOGO TEXT,
    LANCAMENTO TEXT,
    PLATAFORMA TEXT,
    GENERO TEXT,
    DESENVOLVEDORA TEXT
)
'''

usuarios_jogo_sql = '''
CREATE TABLE usuarios_jogo (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
'''

cur.execute(registro_jogo_sql)
cur.execute(usuarios_jogo_sql)
con.commit()
con.close()