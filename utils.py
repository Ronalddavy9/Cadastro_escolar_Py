import json
from aluno import listar_alunos
from disciplina import listar_disciplinas
from nota import listar_notas

def exportar_json():
    dados = {
        "alunos": [{"matricula": a[0], "nome": a[1], "dt_nascimento": a[2]} for a in listar_alunos()],
        "disciplinas": [{"id": d[0], "nome": d[1], "turno": d[2], "sala": d[3], "professor": d[4]} for d in listar_disciplinas()],
        "notas": [{"id": n[0], "aluno": n[1], "disciplina": n[2], "valor": n[3]} for n in listar_notas()]
    }
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print("Dados exportados para dados.json com sucesso!")
