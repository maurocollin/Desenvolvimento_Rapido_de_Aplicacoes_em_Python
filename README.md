# Sistema de Registro de Notas de Alunos - Estácio

Este projeto foi desenvolvido como parte da **Atividade Verificadora de Aprendizagem** para a disciplina de **Desenvolvimento Rápido de Aplicações em Python**. O sistema permite a gestão completa (CRUD) de alunos e suas respectivas notas.

# Aluno
* **Aluno:** Mauro Henrique Collin Ferreira 
* **Matrícula:** 202403689601 
* **Curso:** Análise e Desenvolvimento de Sistemas (ADS) 
* **Professor:** Ralfh V Ansuattigui

## Tecnologias e Requisitos
* **Linguagem:** Python 3.10 ou superior
* **Base de Dados:** SQLite 3
* **Interface Gráfica:** Tkinter (Customizado em Dark Mode)

## Análise Técnica: SQLite vs PostgreSQL
Conforme os requisitos da atividade, optou-se pela utilização do **SQLite**.

### Ganhos:
* **Portabilidade:** A base de dados é um ficheiro único (`sistema_notas.db`), permitindo a execução imediata sem a necessidade de configurar um servidor externo como o PostgreSQL.
* **Agilidade no Desenvolvimento:** Ideal para prototipagem rápida e aplicações de pequeno porte.

### Perdas:
* **Escalabilidade:** O SQLite não suporta múltiplos acessos simultâneos de escrita tão eficientemente quanto o PostgreSQL.
* **Segurança:** Ausência de um sistema robusto de gestão de utilizadores e permissões a nível de motor de base de dados.

## 🚀 Instruções de Execução

Siga os passos abaixo para preparar o ambiente e executar o sistema:

### 1. Criar o Ambiente Virtual (.venv)
No terminal, dentro da pasta do projeto, execute:
```bash
python -m venv .venv