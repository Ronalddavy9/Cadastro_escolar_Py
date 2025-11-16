import sqlite3

def conectar():
    return sqlite3.connect("cadastro_escolar.db")

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS aluno (
            matricula TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            dt_nascimento TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS disciplina (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turno TEXT,
            sala TEXT,
            professor TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS nota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT,
            disciplina_id INTEGER,
            valor REAL,
            FOREIGN KEY (matricula) REFERENCES aluno(matricula),
            FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)
        )
    ''')

    con.commit()
    con.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso!")
