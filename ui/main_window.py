import tkinter as tk
from tkinter import ttk, messagebox
from core.repository import (
    insert_aluno, select_all_alunos, select_alunos_por_criterio, 
    update_aluno, delete_aluno
)

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Notas - Estácio")
        self.root.geometry("850x650")
        
        # --- Configuração do Modo Escuro (Dark Mode) e Estilo ---
        self.set_dark_theme()
        
        # Variável de controle de seleção
        self.id_selecionado = None
        
        # --- UI: FORMULÁRIO DE CADASTRO E EDIÇÃO (Responsivo) ---
        # Usamos LabelFrame padrão do tkinter mas com cores personalizadas
        self.frame_form = tk.LabelFrame(
            self.root, 
            text=" Cadastro e Edição ", 
            padx=15, 
            pady=15, 
            bg=self.dark_frame_bg, 
            fg=self.dark_text
        )
        self.frame_form.pack(fill="x", padx=20, pady=(15, 10))

        # Configuração das colunas da grelha para serem ajustáveis/responsivas
        # Atribuímos 'weight=1' para todas as colunas que devem expandir
        cols_for_weight = [1, 2, 3, 5, 6, 7]
        for col in cols_for_weight:
            self.frame_form.columnconfigure(col, weight=1)
        
        self.frame_form.columnconfigure(0, weight=0) # Nome label
        self.frame_form.columnconfigure(4, weight=0) # Matrícula label
        
        # Linha 0: Nome e Matrícula (Expandem proporcionalmente)
        tk.Label(self.frame_form, text="Nome:", bg=self.dark_frame_bg, fg=self.dark_text, anchor="center").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.ent_nome = tk.Entry(self.frame_form, bg=self.dark_entry_bg, fg=self.dark_text, insertbackground=self.dark_text)
        self.ent_nome.grid(row=0, column=1, columnspan=3, sticky="we", padx=5, pady=5)

        tk.Label(self.frame_form, text="Matrícula:", bg=self.dark_frame_bg, fg=self.dark_text, anchor="center").grid(row=0, column=4, sticky="ew", padx=5, pady=5)
        self.ent_matricula = tk.Entry(self.frame_form, bg=self.dark_entry_bg, fg=self.dark_text, insertbackground=self.dark_text)
        self.ent_matricula.grid(row=0, column=5, columnspan=2, sticky="we", padx=5, pady=5)

        # Linha 1: Notas (Divididas uniformemente)
        self.notas_entries = []
        for i in range(4):
            # Configuração das colunas de notas para serem uniformes
            self.frame_form.columnconfigure(i*2+1, uniform="notas_col", weight=1)
            
            tk.Label(self.frame_form, text=f"Nota {i+1}:", bg=self.dark_frame_bg, fg=self.dark_text, anchor="center").grid(row=1, column=i*2, sticky="ew", padx=5, pady=10)
            ent = tk.Entry(self.frame_form, bg=self.dark_entry_bg, fg=self.dark_text, insertbackground=self.dark_text, width=8)
            ent.grid(row=1, column=i*2+1, sticky="w", padx=5, pady=10)
            self.notas_entries.append(ent)

        # Linha 2: Botões CRUD (Centralizados e Dinâmicos)
        self.frame_btn_acoes = tk.Frame(self.frame_form, bg=self.dark_frame_bg)
        self.frame_btn_acoes.grid(row=2, column=0, columnspan=8, pady=(15, 0))

        tk.Button(self.frame_btn_acoes, text="Cadastrar", command=self.salvar_aluno, 
                  bg=self.dark_btn_green_bg, fg=self.dark_text_white, width=15).pack(side="left", padx=5)
        tk.Button(self.frame_btn_acoes, text="Atualizar Selecionado", command=self.atualizar_dados, 
                  bg=self.dark_btn_bg, fg=self.dark_text, width=20).pack(side="left", padx=5)
        tk.Button(self.frame_btn_acoes, text="Limpar Campos", command=self.limpar_campos, 
                  bg=self.dark_btn_bg, fg=self.dark_text, width=15).pack(side="left", padx=5)

        # --- UI: ÁREA DE BUSCA (Modo Escuro) ---
        self.frame_busca = tk.LabelFrame(
            self.root, 
            text=" Busca (ID, Nome ou Matrícula) ", 
            padx=15, 
            pady=10, 
            bg=self.dark_frame_bg, 
            fg=self.dark_text
        )
        self.frame_busca.pack(fill="x", padx=20, pady=10)

        self.ent_busca = tk.Entry(self.frame_busca, bg=self.dark_entry_bg, fg=self.dark_text, insertbackground=self.dark_text, width=40)
        self.ent_busca.pack(side="left", padx=(0, 10))
        
        tk.Button(self.frame_busca, text="Pesquisar", command=self.pesquisar_alunos, 
                  bg=self.dark_btn_blue_bg, fg=self.dark_text_white, width=12).pack(side="left", padx=5)
        tk.Button(self.frame_busca, text="Ver Todos", command=self.atualizar_tabela, 
                  bg=self.dark_btn_bg, fg=self.dark_text, width=12).pack(side="left", padx=5)

        # --- UI: LISTAGEM (Treeview) COM ESTILO DARK ---
        # Definimos o estilo específico para a Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Matrícula", "N1", "N2", "N3", "N4", "Média"), show="headings", style="Dark.Treeview")
        
        colunas_config = [
            ("ID", 40), ("Nome", 200), ("Matrícula", 100), 
            ("N1", 60), ("N2", 60), ("N3", 60), ("N4", 60), ("Média", 80)
        ]
        
        for col, width in colunas_config:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.carregar_selecao)

        # --- UI: BOTÃO EXCLUIR AJUSTADO (Apenas tamanho do texto, centralizado no rodapé) ---
        # Usamos um frame para centralizar o botão de exclusão
        self.frame_rodape = tk.Frame(self.root, bg=self.dark_bg)
        self.frame_rodape.pack(fill="x", padx=20, pady=(5, 15))
        
        # Botão sem fill="x" para manter apenas o tamanho do texto
        self.btn_excluir = tk.Button(self.frame_rodape, text="Excluir Registro Selecionado", 
                                     command=self.excluir_dados, bg=self.dark_btn_red_bg, 
                                     fg=self.dark_text_white, font=("Arial", 9, "bold"), pady=5)
        self.btn_excluir.pack() # Pack padrão centraliza

        self.atualizar_tabela()

    # --- LÓGICA DE INTERFACE ---
    
    def set_dark_theme(self):
        """Define as cores e estilos do tema escuro."""
        # Paleta de Cores Modo Escuro
        self.dark_bg = "#1e1e1e"            # Fundo principal
        self.dark_frame_bg = "#2d2d2d"      # Fundo dos frames
        self.dark_entry_bg = "#3c3c3c"      # Fundo dos campos de entrada
        self.dark_text = "#ffffff"          # Texto padrão
        self.dark_text_white = "#ffffff"    # Texto branco para botões coloridos
        self.dark_btn_bg = "#3c3c3c"        # Fundo dos botões padrão
        self.dark_btn_green_bg = "#28a745"  # Fundo botão Cadastrar (Verde)
        self.dark_btn_blue_bg = "#007bff"   # Fundo botão Pesquisar (Azul)
        self.dark_btn_red_bg = "#dc3545"    # Fundo botão Excluir (Vermelho)
        self.dark_selected_bg = "#0056b3"   # Fundo da linha selecionada na Treeview
        
        self.root.configure(bg=self.dark_bg)
        
        # Estilo para os widgets ttk (Treeview)
        style = ttk.Style()
        style.theme_use("clam") # 'clam' permite maior personalização de cores
        
        # Estilo para a Treeview
        style.configure("Dark.Treeview", 
                        background=self.dark_frame_bg, 
                        foreground=self.dark_text, 
                        fieldbackground=self.dark_frame_bg, 
                        rowheight=25, 
                        borderwidth=0, 
                        font=("Arial", 9))
        
        # Estilo para os cabeçalhos da Treeview
        style.configure("Dark.Treeview.Heading", 
                        background=self.dark_bg, 
                        foreground=self.dark_text, 
                        borderwidth=1, 
                        font=("Arial", 9, "bold"))
        style.map("Dark.Treeview.Heading", 
                  background=[('pressed', '#0a0a0a'), ('active', '#3c3c3c')])

        # Estilo para a linha selecionada na Treeview
        style.map("Dark.Treeview", 
                  background=[('selected', self.dark_selected_bg)])

    def limpar_campos(self):
        """Limpa todos os campos de entrada e a seleção."""
        self.ent_nome.delete(0, tk.END)
        self.ent_matricula.delete(0, tk.END)
        for ent in self.notas_entries:
            ent.delete(0, tk.END)
        self.ent_busca.delete(0, tk.END)
        self.id_selecionado = None

    def atualizar_tabela(self):
        """Atualiza a Treeview com todos os registros do repositório."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for aluno in select_all_alunos():
            self.tree.insert("", "end", values=aluno)

    def pesquisar_alunos(self):
        """Busca alunos no repositório com base no termo digitado."""
        termo = self.ent_busca.get().strip()
        
        # Lógica de Busca Aprimorada: Se campo vazio, mostra todos
        if not termo:
            self.atualizar_tabela()
            return

        resultados = select_alunos_por_criterio(termo)
        
        # Limpa a tabela antes de processar o resultado
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tratamento de Erro: Se nada for encontrado, exibe mensagem
        if not resultados:
            messagebox.showwarning("Aviso de Busca", "Nome, ID ou matrícula inexistente.")
            self.atualizar_tabela() # Recarrega a lista completa
            return

        # Se encontrou, popula a tabela
        for aluno in resultados:
            self.tree.insert("", "end", values=aluno)

    def salvar_aluno(self):
        """Cadastra um novo aluno no repositório."""
        try:
            nome = self.ent_nome.get().strip()
            mat = self.ent_matricula.get().strip()
            
            # Validação: Campos obrigatórios
            if not nome or not mat:
                raise ValueError("Preencha todos os campos obrigatórios (Nome e Matrícula).")

            notas = [float(ent.get()) for ent in self.notas_entries]
            
            if insert_aluno(nome, mat, *notas):
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                self.limpar_campos()
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", "Falha ao cadastrar. Verifique se a matrícula já existe.")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", f"Entrada inválida: {e}")

    def carregar_selecao(self, event):
        """Carrega os dados da linha selecionada na Treeview para o formulário."""
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
        """Atualiza o registro do aluno selecionado no repositório."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno na lista para editar.")
            return
        
        try:
            nome = self.ent_nome.get().strip()
            mat = self.ent_matricula.get().strip()
            notas = [float(ent.get()) for ent in self.notas_entries]
            
            if not nome or not mat:
                raise ValueError("Preencha todos os campos obrigatórios.")

            if update_aluno(self.id_selecionado, nome, mat, *notas):
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                self.atualizar_tabela()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar registro.")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", f"Entrada inválida: {e}")

    def excluir_dados(self):
        """Remove o aluno selecionado do repositório após confirmação."""
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno na lista para excluir.")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja remover este registro permanentemente?"):
            if delete_aluno(self.id_selecionado):
                messagebox.showinfo("Sucesso", "Registro removido com sucesso!")
                self.atualizar_tabela()
                self.limpar_campos()
            else:
                messagebox.showerror("Erro", "Falha ao remover registro.")