import tkinter as tk
from tkinter import messagebox, simpledialog
from database import criar_tabelas
from aluno import incluir_aluno, listar_alunos, alterar_aluno, excluir_aluno
from disciplina import incluir_disciplina, listar_disciplinas, alterar_disciplina, excluir_disciplina
from nota import incluir_nota, listar_notas, alterar_nota, excluir_nota
from utils import exportar_json

criar_tabelas()

def center(win, w, h):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - w // 2
    y = (win.winfo_screenheight() // 2) - h // 2
    win.geometry(f"{w}x{h}+{x}+{y}")
    win.resizable(False, False)

BG = "#121212"
FG = "#e6e6e6"
BTN = "#263238"
ACC = "#1976d2"
ENTRY = "#2a2a2a"
FONT = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 16, "bold")

janela = tk.Tk()
janela.title("Sistema de Cadastro Escolar")
center(janela, 520, 420)
janela.configure(bg=BG)

tk.Label(janela, text="Sistema de Cadastro Escolar", font=FONT_TITLE, bg=BG, fg=ACC).pack(pady=16)

def estilo_btn(win, text, command):
    return tk.Button(win, text=text, command=command, font=FONT, width=30, bg=BTN, fg=FG, activebackground=ACC, bd=0)

def tela_aluno():
    win = tk.Toplevel(janela)
    win.title("Cadastrar Alunos")
    center(win, 480, 300)
    win.configure(bg=BG)

    tk.Label(win, text="Matrícula:", bg=BG, fg=FG).grid(row=0, column=0, sticky="e", padx=8, pady=6)
    e_matricula = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=30)
    e_matricula.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(win, text="Nome:", bg=BG, fg=FG).grid(row=1, column=0, sticky="e", padx=8, pady=6)
    e_nome = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=30)
    e_nome.grid(row=1, column=1, padx=8, pady=6)

    tk.Label(win, text="Data de Nascimento:", bg=BG, fg=FG).grid(row=2, column=0, sticky="e", padx=8, pady=6)
    e_dt = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=30)
    e_dt.grid(row=2, column=1, padx=8, pady=6)

    def incluir_cmd():
        m = e_matricula.get().strip()
        n = e_nome.get().strip()
        d = e_dt.get().strip()
        if not m or not n:
            messagebox.showwarning("Atenção", "Matrícula e nome são obrigatórios.", parent=win)
            return
        try:
            incluir_aluno(m, n, d)
            messagebox.showinfo("Sucesso", "Aluno cadastrado!", parent=win)
            e_matricula.delete(0, tk.END); e_nome.delete(0, tk.END); e_dt.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar aluno:\n{e}\n\nSe o erro for 'database is locked', feche o SQLite Viewer antes.", parent=win)

    def listar_cmd():
        try:
            dados = listar_alunos()
            txt = "\n".join([f"{a[0]} - {a[1]} ({a[2]})" for a in dados]) if dados else "Nenhum aluno cadastrado."
            messagebox.showinfo("Lista de Alunos", txt, parent=win)
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=win)

    def alterar_cmd():
        matricula = simpledialog.askstring("Alterar", "Matrícula do aluno a alterar:", parent=win)
        if not matricula:
            return
        novo_nome = simpledialog.askstring("Novo nome", "Nome:", parent=win)
        nova_dt = simpledialog.askstring("Nova data de nascimento", "Data:", parent=win)
        try:
            alterar_aluno(matricula, novo_nome or "", nova_dt or "")
            messagebox.showinfo("Sucesso", "Aluno alterado.", parent=win)
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=win)

    def excluir_cmd():
        matricula = simpledialog.askstring("Excluir", "Matrícula do aluno a excluir:", parent=win)
        if not matricula:
            return
        if messagebox.askyesno("Confirmação", f"Confirma exclusão do aluno {matricula}?", parent=win):
            try:
                excluir_aluno(matricula)
                messagebox.showinfo("Sucesso", "Aluno excluído.", parent=win)
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=win)

    tk.Button(win, text="Incluir", command=incluir_cmd, bg=ACC, fg="white", bd=0, width=14).grid(row=4, column=0, pady=10)
    tk.Button(win, text="Listar", command=listar_cmd, bg=BTN, fg=FG, bd=0, width=14).grid(row=4, column=1, pady=10)
    tk.Button(win, text="Alterar", command=alterar_cmd, bg=BTN, fg=FG, bd=0, width=14).grid(row=5, column=0, pady=6)
    tk.Button(win, text="Excluir", command=excluir_cmd, bg="#b71c1c", fg="white", bd=0, width=14).grid(row=5, column=1, pady=6)

def tela_disciplina():
    win = tk.Toplevel(janela)
    win.title("Cadastrar Disciplinas")
    center(win, 520, 340)
    win.configure(bg=BG)

    labels = ["Nome:", "Turno:", "Sala:", "Professor:"]
    entries = []
    for i, lab in enumerate(labels):
        tk.Label(win, text=lab, bg=BG, fg=FG).grid(row=i, column=0, sticky="e", padx=8, pady=6)
        e = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=34)
        e.grid(row=i, column=1, padx=8, pady=6)
        entries.append(e)

    def incluir_cmd():
        vals = [e.get().strip() for e in entries]
        if not vals[0]:
            messagebox.showwarning("Atenção", "Nome é obrigatório.", parent=win)
            return
        try:
            incluir_disciplina(*vals)
            messagebox.showinfo("Sucesso", "Disciplina cadastrada.", parent=win)
            for e in entries: e.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"{e}", parent=win)

    def listar_cmd():
        try:
            dados = listar_disciplinas()
            txt = "\n".join([f"{d[0]} - {d[1]} ({d[2]}, {d[3]}, {d[4]})" for d in dados]) if dados else "Nenhuma disciplina cadastrada."
            messagebox.showinfo("Lista de Disciplinas", txt, parent=win)
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=win)

    def alterar_cmd():
        disciplina_id = simpledialog.askinteger("Alterar", "ID da disciplina:", parent=win)
        if disciplina_id is None:
            return
        novo_nome = simpledialog.askstring("Novo nome", "Nome:", parent=win)
        novo_turno = simpledialog.askstring("Novo turno", "Turno:", parent=win)
        nova_sala = simpledialog.askstring("Nova sala", "Sala:", parent=win)
        novo_prof = simpledialog.askstring("Novo professor", "Professor:", parent=win)
        try:
            alterar_disciplina(disciplina_id, novo_nome or "", novo_turno or "", nova_sala or "", novo_prof or "")
            messagebox.showinfo("Sucesso", "Disciplina alterada.", parent=win)
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=win)

    def excluir_cmd():
        disciplina_id = simpledialog.askinteger("Excluir", "ID da disciplina:", parent=win)
        if disciplina_id is None:
            return
        if messagebox.askyesno("Confirmar", f"Confirma exclusão da disciplina {disciplina_id}?", parent=win):
            try:
                excluir_disciplina(disciplina_id)
                messagebox.showinfo("Sucesso", "Disciplina excluída.", parent=win)
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=win)

    tk.Button(win, text="Incluir", command=incluir_cmd, bg=ACC, fg="white", bd=0, width=14).grid(row=5, column=0, pady=10)
    tk.Button(win, text="Listar", command=listar_cmd, bg=BTN, fg=FG, bd=0, width=14).grid(row=5, column=1, pady=10)
    tk.Button(win, text="Alterar", command=alterar_cmd, bg=BTN, fg=FG, bd=0, width=14).grid(row=6, column=0, pady=6)
    tk.Button(win, text="Excluir", command=excluir_cmd, bg="#b71c1c", fg="white", bd=0, width=14).grid(row=6, column=1, pady=6)

def tela_nota():
    win = tk.Toplevel(janela)
    win.title("Cadastrar Notas")
    center(win, 520, 320)
    win.configure(bg=BG)

    tk.Label(win, text="Matrícula do Aluno:", bg=BG, fg=FG).grid(row=0, column=0, sticky="e", padx=8, pady=6)
    e_mat = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=30)
    e_mat.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(win, text="ID da Disciplina:", bg=BG, fg=FG).grid(row=1, column=0, sticky="e", padx=8, pady=6)
    e_disc = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=30)
    e_disc.grid(row=1, column=1, padx=8, pady=6)

    tk.Label(win, text="Nota:", bg=BG, fg=FG).grid(row=2, column=0, sticky="e", padx=8, pady=6)
    e_val = tk.Entry(win, bg=ENTRY, fg=FG, insertbackground=FG, width=30)
    e_val.grid(row=2, column=1, padx=8, pady=6)

    def incluir_cmd():
        m = e_mat.get().strip()
        d = e_disc.get().strip()
        v = e_val.get().strip()
        if not (m and d and v):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=win)
            return
   
        try:
            disc_id = int(d)
        except ValueError:
            messagebox.showerror("Erro", "ID da disciplina deve ser um número inteiro.", parent=win)
            return
        try:
            valor_float = float(v.replace(',', '.'))  
        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número (ex: 7.5).", parent=win)
            return
        try:
            incluir_nota(m, disc_id, valor_float)
            messagebox.showinfo("Sucesso", "Nota cadastrada!", parent=win)
            e_mat.delete(0, tk.END); e_disc.delete(0, tk.END); e_val.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar nota:\n{e}\n\nSe for 'database is locked', feche o SQLite Viewer antes.", parent=win)

    def listar_cmd():
        try:
            dados = listar_notas()
            if not dados:
                messagebox.showinfo("Lista de Notas", "Nenhuma nota cadastrada.", parent=win)
                return
            txt = "\n".join([f"{n[0]} - {n[1]} / {n[2]}: {n[3]}" for n in dados])
            messagebox.showinfo("Lista de Notas", txt, parent=win)
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=win)

    def alterar_cmd():
        nota_id = simpledialog.askinteger("Alterar", "ID da nota:", parent=win)
        if nota_id is None:
            return
        novo = simpledialog.askstring("Novo valor", "Nova nota:", parent=win)
        if novo is None:
            return
        try:
            novo_float = float(str(novo).replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.", parent=win)
            return
        try:
            alterar_nota(nota_id, novo_float)
            messagebox.showinfo("Sucesso", "Nota alterada.", parent=win)
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=win)

    def excluir_cmd():
        nota_id = simpledialog.askinteger("Excluir", "ID da nota:", parent=win)
        if nota_id is None:
            return
        if messagebox.askyesno("Confirmar", f"Confirma exclusão da nota {nota_id}?", parent=win):
            try:
                excluir_nota(nota_id)
                messagebox.showinfo("Sucesso", "Nota excluída.", parent=win)
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=win)

    tk.Button(win, text="Incluir", command=incluir_cmd, bg=ACC, fg="white", bd=0, width=14).grid(row=3, column=0, pady=10)
    tk.Button(win, text="Listar", command=listar_cmd, bg=BTN, fg=FG, bd=0, width=14).grid(row=3, column=1, pady=10)
    tk.Button(win, text="Alterar", command=alterar_cmd, bg=BTN, fg=FG, bd=0, width=14).grid(row=4, column=0, pady=6)
    tk.Button(win, text="Excluir", command=excluir_cmd, bg="#b71c1c", fg="white", bd=0, width=14).grid(row=4, column=1, pady=6)

estilo_btn(janela, "Cadastrar Alunos", tela_aluno).pack(pady=6)
estilo_btn(janela, "Cadastrar Disciplinas", tela_disciplina).pack(pady=6)
estilo_btn(janela, "Cadastrar Notas", tela_nota).pack(pady=6)
estilo_btn(janela, "Exportar JSON", exportar_json).pack(pady=6)
estilo_btn(janela, "Sair", janela.quit).pack(pady=6)

janela.mainloop()
