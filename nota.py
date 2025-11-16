from database import conectar

def incluir_nota(matricula, disciplina_id, valor):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO nota (matricula, disciplina_id, valor) VALUES (?, ?, ?)",
                (matricula, int(disciplina_id), float(valor)))
    con.commit()
    con.close()

def listar_notas():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT n.id, a.nome, d.nome, n.valor
        FROM nota n
        JOIN aluno a ON a.matricula = n.matricula
        JOIN disciplina d ON d.id = n.disciplina_id
        ORDER BY n.id
    """)
    dados = cur.fetchall()
    con.close()
    return dados

def alterar_nota(id, valor):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE nota SET valor=? WHERE id=?", (float(valor), id))
    con.commit()
    con.close()

def excluir_nota(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM nota WHERE id=?", (id,))
    con.commit()
    con.close()
