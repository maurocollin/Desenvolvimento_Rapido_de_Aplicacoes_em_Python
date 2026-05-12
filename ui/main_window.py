import tkinter as tk
from tkinter import ttk, messagebox
from core.repository import (
    insert_aluno, select_all_alunos, select_alunos_por_termo, 
    update_aluno, delete_aluno
)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Notas - Estácio")
        self.root.geometry("850x650")
        self.root.configure(padx=20, pady=20)

        # Variável para controle de seleção
        self.id_selecionado = None
        
        # --- UI: FORMULÁRIO DE DADOS ---
        frame_form = tk.LabelFrame(self.root, text=" Cadastro e Edição de Alunos ", padx=15, pady=15)
        frame_form.pack(fill="x", pady=(0, 10))

        # Configuração das colunas para alinhamento uniforme
        for i in range(8):
            frame_form.columnconfigure(i, weight=1)

        # Linha 0: Nome e Matrícula
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_nome = tk.Entry(frame_form)
        self.ent_nome.grid(row=0, column=1, columnspan=4, sticky="we", padx=5, pady=5)

        tk.Label(frame_form, text="Matrícula:").grid(row=0, column=5, sticky="e", padx=5, pady=5)
        self.ent_matricula = tk.Entry(frame_form)
        self.ent_matricula.grid(row=0, column=6, columnspan=2, sticky="we", padx=5, pady=5)

        # Linha 1: Notas (Distribuídas uniformemente)
        self.ent_notas = []
        for i in range(4):
            tk.Label(frame_form, text=f"Nota {i+1}:").grid(row=1, column=i*2, sticky="e", padx=5, pady=5)
            ent = tk.Entry(frame_form, width=8)
            ent.grid(row=1, column=i*2+1, sticky="w", padx=5, pady=5)
            self.ent_notas.append(ent)

        # Linha 2: Botões de Ação Principal
        frame_acoes = tk.Frame(frame_form)
        frame_acoes.grid(row=2, column=0, columnspan=8, pady=(15, 0))

        tk.Button(frame_acoes, text="Salvar Novo", command=self.salvar_aluno, 
                  bg="#28a745", fg="white", width=15, relief="flat").pack(side="left", padx=5)
        
        tk.Button(frame_acoes, text="Atualizar Selecionado", command=self.atualizar_dados, 
                  width=18).pack(side="left", padx=5)
        
        tk.Button(frame_acoes, text="Limpar Campos", command=self.limpar_campos, 
                  width=15).pack(side="left", padx=5)

        # --- UI: ÁREA DE BUSCA ---
        frame_busca = tk.LabelFrame(self.root, text=" Filtros e Busca ", padx=15, pady=10)
        frame_busca.pack(fill="x", pady=10)

        tk.Label(frame_busca, text="Buscar (Nome/Matrícula):").pack(side="left", padx=(0, 10))
        self.ent_busca = tk.Entry(frame_busca, width=40)
        self.ent_busca.pack(side="left", padx=5)
        
        tk.Button(frame_busca, text="Pesquisar", command=self.pesquisar_alunos, 
                  bg="#007bff", fg="white", width=12).pack(side="left", padx=5)
        
        tk.Button(frame_busca, text="Ver Todos", command=self.atualizar_tabela, 
                  width=12).pack(side="left", padx=5)

        # --- UI: LISTAGEM (TREEVIEW) ---
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Matrícula", "N1", "N2", "N3", "N4", "Média"), show="headings")
        
        # Definir cabeçalhos e larguras
        colunas_config = [
            ("ID", 40), ("Nome", 200), ("Matrícula", 100), 
            ("N1", 60), ("N2", 60), ("N3", 60), ("N4", 60), ("Média", 80)
        ]
        
        for col, width in colunas_config:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.carregar_nos_campos)

        # Botão de Exclusão (Sempre visível no rodapé)
        self.btn_excluir = tk.Button(self.root, text="Excluir Aluno Selecionado", command=self.excluir_dados, 
                                     bg="#dc3545", fg="white", font=("Arial", 9, "bold"), pady=5)
        self.btn_excluir.pack(fill="x")

        self.atualizar_tabela()

    # --- LÓGICA DE INTERFACE ---
    
    def validar_notas(self, notas):
        for n in notas:
            if not (0 <= n <= 10):
                return False
        return True

    def salvar_aluno(self):
        try:
            nome = self.ent_nome.get().strip()
            mat = self.ent_matricula.get().strip()
            if not nome or not mat:
                raise ValueError("Nome e Matrícula são obrigatórios.")

            notas = [float(e.get()) for e in self.ent_notas]
            if not self.validar_notas(notas):
                messagebox.showerror("Erro", "As notas devem estar entre 0 e 10.")
                return

            if insert_aluno(nome, mat, notas):
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                self.limpar_campos()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar. Verifique se a matrícula já existe.")
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def pesquisar_alunos(self):
        termo = self.ent_busca.get().strip()
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
            self.id_selecionado = aluno[0]
            self.ent_nome.delete(0, tk.END)
            self.ent_nome.insert(0, aluno[1])
            self.ent_matricula.delete(0, tk.END)
            self.ent_matricula.insert(0, aluno[2])
            for i in range(4):
                self.ent_notas[i].delete(0, tk.END)
                self.ent_notas[i].insert(0, aluno[i+3])

    def atualizar_dados(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno na tabela para editar.")
            return
        
        try:
            nome = self.ent_nome.get().strip()
            mat = self.ent_matricula.get().strip()
            notas = [float(e.get()) for e in self.ent_notas]

            if not self.validar_notas(notas):
                messagebox.showerror("Erro", "As notas devem estar entre 0 e 10.")
                return

            if update_aluno(self.id_selecionado, nome, mat, notas):
                messagebox.showinfo("Sucesso", "Dados atualizados!")
                self.atualizar_tabela()
        except ValueError:
            messagebox.showerror("Erro", "Verifique se as notas são números válidos.")

    def excluir_dados(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir.")
            return
        
        id_aluno = self.tree.item(selecionado)['values'][0]
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este aluno permanentemente?"):
            if delete_aluno(id_aluno):
                self.atualizar_tabela()
                self.limpar_campos()

    def limpar_campos(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_matricula.delete(0, tk.END)
        for e in self.ent_notas:
            e.delete(0, tk.END)
        self.id_selecionado = None
        self.ent_busca.delete(0, tk.END)