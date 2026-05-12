import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('sistema_notas.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def create_tables():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                nota1 REAL DEFAULT 0,
                nota2 REAL DEFAULT 0,
                nota3 REAL DEFAULT 0,
                nota4 REAL DEFAULT 0,
                media REAL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()