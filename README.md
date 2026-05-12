# Sistema de Registro de Notas de Alunos

Projeto desenvolvido para a disciplina de **Desenvolvimento Rápido de Aplicações em Python**.

## 🛠️ Tecnologias Utilizadas
* Python 3
* SQLite
* Tkinter

## 📊 SQLite vs PostgreSQL (Análise Técnica)
Conforme solicitado no enunciado, optou-se pelo uso do SQLite em substituição ao PostgreSQL.

### Ganhos:
* **Portabilidade:** O banco de dados é um arquivo único, facilitando a execução sem dependências externas.
* **Simplicidade:** Ideal para sistemas de pequeno porte, sem necessidade de servidor dedicado.

### Perdas:
* **Escalabilidade:** Limitações em acessos simultâneos de escrita.
* **Tipagem:** Menor rigor na validação de tipos de dados comparado ao PostgreSQL.

## 🚀 Como executar
1. Certifique-se de ter o Python 3 instalado.
2. Execute o comando: `python main.py`.