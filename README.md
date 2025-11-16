# Sistema de Cadastro Escolar

Projeto desenvolvido em Python utilizando **Tkinter** para interface gráfica e **SQLite** como banco de dados local.  
O sistema realiza o **cadastro de alunos, disciplinas e notas**, seguindo o modelo de dados definido pelo professor, incluindo **exportação dos dados para arquivo JSON**.

---

## 📌 Funcionalidades

| Módulo          | Ações Disponíveis |
|-----------------|------------------|
| **Alunos**      | Cadastrar, Listar, Alterar, Excluir |
| **Disciplinas** | Cadastrar, Listar, Alterar, Excluir |
| **Notas**       | Cadastrar, Listar, Alterar, Excluir |
| **Exportação**  | Gera arquivo `dados.json` com todos os registros |

---

## 🗂 Estrutura do Banco de Dados (SQLite)

O sistema cria automaticamente o banco `cadastro_escolar.db` na primeira execução, contendo:

