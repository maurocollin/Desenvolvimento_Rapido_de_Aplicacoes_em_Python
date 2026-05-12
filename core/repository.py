from core.database import connect_db

def calcular_media(n1, n2, n3, n4):
    """Calcula a média aritmética simples de 4 notas."""
    return (n1 + n2 + n3 + n4) / 4

def insert_aluno(nome, matricula, n1, n2, n3, n4):
    """Cadastra um novo aluno com o cálculo da média."""
    media = calcular_media(n1, n2, n3, n4)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO alunos (nome, matricula, nota1, nota2, nota3, nota4, media)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, matricula, n1, n2, n3, n4, media))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir aluno: {e}")
            return False
        finally:
            conn.close()

def select_all_alunos():
    """Retorna todos os registros da tabela alunos."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        alunos = cursor.fetchall()
        conn.close()
        return alunos
    return []

def update_aluno(aluno_id, nome, matricula, n1, n2, n3, n4):
    """Atualiza os dados de um aluno e recalcula a média."""
    media = calcular_media(n1, n2, n3, n4)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE alunos 
                SET nome = ?, matricula = ?, nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?, media = ?
                WHERE id = ?
            """, (nome, matricula, n1, n2, n3, n4, media, aluno_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar aluno: {e}")
            return False
        finally:
            conn.close()

def delete_aluno(aluno_id):
    """Remove um registro de aluno pelo ID."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar aluno: {e}")
            return False
        finally:
            conn.close()