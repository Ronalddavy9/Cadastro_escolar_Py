from database import conectar

def incluir_disciplina(nome, turno, sala, professor):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO disciplina (nome, turno, sala, professor) VALUES (?, ?, ?, ?)", (nome, turno, sala, professor))
    con.commit()
    con.close()

def listar_disciplinas():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM disciplina")
    dados = cur.fetchall()
    con.close()
    return dados

def alterar_disciplina(id, nome, turno, sala, professor):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE disciplina SET nome=?, turno=?, sala=?, professor=? WHERE id=?", (nome, turno, sala, professor, id))
    con.commit()
    con.close()

def excluir_disciplina(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM disciplina WHERE id=?", (id,))
    con.commit()
    con.close()
