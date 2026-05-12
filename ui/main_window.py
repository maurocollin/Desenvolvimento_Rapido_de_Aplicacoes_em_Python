import tkinter as tk
from tkinter import messagebox, ttk
from core.repository import (
    insert_aluno, select_all_alunos, select_alunos_por_termo, 
    update_aluno, delete_aluno
)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Notas")
        self.root.geometry("800x600")

        # --- Frame de Entrada de Dados ---
        self.frame_inputs = tk.LabelFrame(self.root, text="Dados do Aluno", padx=10, pady=10)
        self.frame_inputs.pack(fill="x", padx=10, pady=10)

        tk.Label(self.frame_inputs, text="Nome:").grid(row=0, column=0, sticky="w")
        self.ent_nome = tk.Entry(self.frame_inputs, width=40)
        self.ent_nome.grid(row=0, column=1, columnspan=3, pady=2)

        tk.Label(self.frame_inputs, text="Matrícula:").grid(row=1, column=0, sticky="w")
        self.ent_matricula = tk.Entry(self.frame_inputs, width=20)
        self.ent_matricula.grid(row=1, column=1, pady=2, sticky="w")

        # Notas
        self.ent_notas = []
        for i in range(4):
            tk.Label(self.frame_inputs, text=f"Nota {i+1}:").grid(row=2, column=i*2, sticky="w")
            ent = tk.Entry(self.frame_inputs, width=8)
            ent.grid(row=2, column=i*2 + 1, padx=5, pady=2)
            self.ent_notas.append(ent)

        # Botões de Ação
        self.btn_salvar = tk.Button(self.frame_inputs, text="Salvar Novo", command=self.salvar_aluno, bg="green", fg="white")
        self.btn_salvar.grid(row=3, column=0, pady=10)

        self.btn_atualizar = tk.Button(self.frame_inputs, text="Atualizar Selecionado", command=self.atualizar_dados)
        self.btn_atualizar.grid(row=3, column=1, pady=10)

        self.btn_limpar = tk.Button(self.frame_inputs, text="Limpar Campos", command=self.limpar_campos)
        self.btn_limpar.grid(row=3, column=2, pady=10)

        # --- Frame de Busca ---
        self.frame_busca = tk.Frame(self.root)
        self.frame_busca.pack(fill="x", padx=10, pady=5)

        tk.Label(self.frame_busca, text="Buscar:").pack(side="left")
        self.ent_busca = tk.Entry(self.frame_busca, width=30)
        self.ent_busca.pack(side="left", padx=5)
        
        tk.Button(self.frame_busca, text="Pesquisar", command=self.pesquisar_alunos).pack(side="left", padx=2)
        tk.Button(self.frame_busca, text="Ver Todos", command=self.atualizar_tabela).pack(side="left", padx=2)

        # --- Tabela (Treeview) ---
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Matrícula", "N1", "N2", "N3", "N4", "Média"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)

        self.tree.bind("<<TreeviewSelect>>", self.carregar_nos_campos)

        self.btn_excluir = tk.Button(self.root, text="Excluir Aluno Selecionado", command=self.excluir_dados, bg="red", fg="white")
        self.btn_excluir.pack(pady=5)

        self.atualizar_tabela()

    def validar_notas(self, notas):
        for n in notas:
            if not (0 <= n <= 10):
                return False
        return True

    def salvar_aluno(self):
        try:
            nome = self.ent_nome.get()
            mat = self.ent_matricula.get()
            notas = [float(e.get()) for e in self.ent_notas]

            if not nome or not mat:
                raise ValueError("Nome e Matrícula são obrigatórios.")
            
            if not self.validar_notas(notas):
                messagebox.showerror("Erro", "As notas devem estar entre 0 e 10.")
                return

            if insert_aluno(nome, mat, notas):
                messagebox.showinfo("Sucesso", "Aluno cadastrado!")
                self.limpar_campos()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar (Matrícula duplicada?)")
        except ValueError as e:
            messagebox.showerror("Erro", f"Dados inválidos: {e}")

    def pesquisar_alunos(self):
        termo = self.ent_busca.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for aluno in select_alunos_por_termo(termo):
            self.tree.insert("", "end", values=aluno)

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for aluno in select_all_alunos():
            self.tree.insert("", "end", values=aluno)

    def carregar_nos_campos(self, event):
        selecionado = self.tree.selection()
        if selecionado:
            aluno = self.tree.item(selecionado)['values']
            self.ent_nome.delete(0, tk.END)
            self.ent_nome.insert(0, aluno[1])
            self.ent_matricula.delete(0, tk.END)
            self.ent_matricula.insert(0, aluno[2])
            for i in range(4):
                self.ent_notas[i].delete(0, tk.END)
                self.ent_notas[i].insert(0, aluno[i+3])

    def atualizar_dados(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno na tabela.")
            return
        
        try:
            id_aluno = self.tree.item(selecionado)['values'][0]
            nome = self.ent_nome.get()
            mat = self.ent_matricula.get()
            notas = [float(e.get()) for e in self.ent_notas]

            if not self.validar_notas(notas):
                messagebox.showerror("Erro", "As notas devem estar entre 0 e 10.")
                return

            if update_aluno(id_aluno, nome, mat, notas):
                messagebox.showinfo("Sucesso", "Dados atualizados!")
                self.atualizar_tabela()
        except ValueError:
            messagebox.showerror("Erro", "Notas inválidas.")

    def excluir_dados(self):
        selecionado = self.tree.selection()
        if not selecionado:
            return
        
        id_aluno = self.tree.item(selecionado)['values'][0]
        if messagebox.askyesno("Confirmar", "Deseja excluir este aluno?"):
            if delete_aluno(id_aluno):
                self.atualizar_tabela()
                self.limpar_campos()

    def limpar_campos(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_matricula.delete(0, tk.END)
        for e in self.ent_notas:
            e.delete(0, tk.END)