import tkinter as tk
from tkinter import ttk, messagebox
from core.repository import insert_aluno, select_all_alunos, update_aluno, delete_aluno

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Notas - Estácio")
        self.root.geometry("800x600")

        # Variáveis de controle
        self.id_selecionado = None
        
        # --- UI: Formulário ---
        frame_form = tk.LabelFrame(self.root, text="Dados do Aluno", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.ent_nome = tk.Entry(frame_form, width=30)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Matrícula:").grid(row=0, column=2, sticky="w")
        self.ent_matricula = tk.Entry(frame_form, width=15)
        self.ent_matricula.grid(row=0, column=3, padx=5, pady=2)

        # Notas
        self.notas_entries = []
        for i in range(4):
            tk.Label(frame_form, text=f"Nota {i+1}:").grid(row=1, column=i*2, sticky="w")
            ent = tk.Entry(frame_form, width=5)
            ent.grid(row=1, column=i*2+1, padx=5, pady=2)
            self.notas_entries.append(ent)

        # --- UI: Botões CRUD ---
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Cadastrar", command=self.salvar_aluno, bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Atualizar", command=self.atualizar_dados).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Excluir", command=self.excluir_dados, bg="red", fg="white").pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpar Campos", command=self.limpar_campos).pack(side="left", padx=5)

        # --- UI: Listagem (Treeview) ---
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Matrícula", "N1", "N2", "N3", "N4", "Média"), show="headings")
        colunas = [("ID", 30), ("Nome", 150), ("Matrícula", 100), ("N1", 50), ("N2", 50), ("N3", 50), ("N4", 50), ("Média", 70)]
        
        for col, width in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.carregar_selecao)

        self.atualizar_tabela()

    # --- Lógica da Interface ---
    def limpar_campos(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_matricula.delete(0, tk.END)
        for ent in self.notas_entries:
            ent.delete(0, tk.END)
        self.id_selecionado = None

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for aluno in select_all_alunos():
            self.tree.insert("", "end", values=aluno)

    def salvar_aluno(self):
        try:
            notas = [float(ent.get()) for ent in self.notas_entries]
            if insert_aluno(self.ent_nome.get(), self.ent_matricula.get(), *notas):
                messagebox.showinfo("Sucesso", "Aluno cadastrado!")
                self.limpar_campos()
                self.atualizar_tabela()
        except ValueError:
            messagebox.showerror("Erro", "Insira notas válidas (0-10).")

    def carregar_selecao(self, event):
        item = self.tree.selection()
        if item:
            aluno = self.tree.item(item, "values")
            self.id_selecionado = aluno[0]
            self.ent_nome.delete(0, tk.END)
            self.ent_nome.insert(0, aluno[1])
            self.ent_matricula.delete(0, tk.END)
            self.ent_matricula.insert(0, aluno[2])
            for i in range(4):
                self.notas_entries[i].delete(0, tk.END)
                self.notas_entries[i].insert(0, aluno[3+i])

    def atualizar_dados(self):
        if not self.id_selecionado:
            return messagebox.showwarning("Aviso", "Selecione um aluno na lista.")
        try:
            notas = [float(ent.get()) for ent in self.notas_entries]
            if update_aluno(self.id_selecionado, self.ent_nome.get(), self.ent_matricula.get(), *notas):
                messagebox.showinfo("Sucesso", "Dados atualizados!")
                self.atualizar_tabela()
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos.")

    def excluir_dados(self):
        if not self.id_selecionado:
            return messagebox.showwarning("Aviso", "Selecione um aluno na lista.")
        if messagebox.askyesno("Confirmar", "Deseja excluir este registro?"):
            if delete_aluno(self.id_selecionado):
                self.atualizar_tabela()
                self.limpar_campos()