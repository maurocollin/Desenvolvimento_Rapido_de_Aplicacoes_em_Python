from .database import connect_db

def insert_aluno(nome, matricula, notas):
    media = sum(notas) / len(notas)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO alunos (nome, matricula, nota1, nota2, nota3, nota4, media)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, matricula, *notas, media))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()
    return False

def select_all_alunos():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alunos')
        alunos = cursor.fetchall()
        conn.close()
        return alunos
    return []

def select_alunos_por_termo(termo):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM alunos WHERE nome LIKE ? OR matricula LIKE ?"
        cursor.execute(query, (f"%{termo}%", f"%{termo}%"))
        alunos = cursor.fetchall()
        conn.close()
        return alunos
    return []

def update_aluno(id_aluno, nome, matricula, notas):
    media = sum(notas) / len(notas)
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE alunos 
            SET nome = ?, matricula = ?, nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?, media = ?
            WHERE id = ?
        ''', (nome, matricula, *notas, media, id_aluno))
        conn.commit()
        conn.close()
        return True
    return False

def delete_aluno(id_aluno):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM alunos WHERE id = ?', (id_aluno,))
        conn.commit()
        conn.close()
        return True
    return False