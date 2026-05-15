# Sistema de Registro de Notas de Alunos - GRUPO 4

Este projeto foi desenvolvido como parte da **Atividade Verificadora de Aprendizagem** para a disciplina de **Desenvolvimento Rápido de Aplicações em Python**. O sistema permite a gestão completa (CRUD) de alunos e suas respectivas notas.

# Identificação
* **Aluno:** Mauro Henrique Collin Ferreira 
* **Matrícula:** 202403689601
* **Curso:** Análise e Desenvolvimento de Sistemas (ADS) 
* **Professor:** Ralfh V Ansuattigui

## 🛠️ Tecnologias e Requisitos
* **Linguagem:** Python 3.10 ou superior
* **Base de Dados:** SQLite 3 (`schema.sql`)
* **Interface Gráfica:** Tkinter (Customizado em Dark Mode)

## Análise Técnica: SQLite vs PostgreSQL
Conforme os requisitos da atividade, optou-se pela utilização do **SQLite** por ser embutido, portátil e mais leve.

### Ganhos:
* **Portabilidade:** A base de dados é um ficheiro único (`sistema_notas.db`), permitindo a execução imediata sem a necessidade de configurar um servidor externo como o PostgreSQL.
* **Agilidade no Desenvolvimento:** Ideal para prototipagem rápida e aplicações de pequeno porte.

### Perdas:
* **Escalabilidade:** O SQLite não suporta múltiplos acessos simultâneos de escrita tão eficientemente quanto o PostgreSQL.
* **Segurança:** Ausência de um sistema robusto de gestão de utilizadores e permissões a nível de motor de base de dados.

## 🚀 Como Preparar e Rodar o Sistema

### 1. Pré-requisitos
Antes de começar, você precisará instalar as ferramentas básicas:

* **Python:** Baixe em: [python.org/downloads/windows](https://www.python.org/downloads/windows/)
  - **IMPORTANTE:** Na tela inicial de instalação, marque a opção **"Add Python to PATH"**.
* **Git:** Baixe em: [git-scm.com/install/windows](https://git-scm.com/install/windows)

### 2. Clonar o Repositório
Abra o **CMD** ou terminal da sua IDE e execute:
```bash
git clone https://github.com/maurocollin/desenvolvimento_rapido_de_aplicacoes_em_python.git
cd desenvolvimento_rapido_de_aplicacoes_em_python

# Cria o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual (Windows)
.venv\Scripts\activate

# Instala dependências
pip install -r requirements.txt

# Executar o ponto de entrada do sistema
python main.py
