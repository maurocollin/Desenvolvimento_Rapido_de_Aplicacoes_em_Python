import sqlite3
import os

def connect_db():
    try:
        # Cria a conexão com o banco
        return sqlite3.connect('sistema_notas.db')
    except sqlite3.Error as e:
        print(f"Erro ao conectar: {e}")
        return None

def create_tables():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            
            # UTILIDADE REAL: Lendo o script SQL do arquivo externo
            # Usamos o caminho absoluto baseado na localização deste script
            caminho_sql = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
            
            with open(caminho_sql, 'r', encoding='utf-8') as f:
                script_sql = f.read()
            
            # Executa o script completo (pode conter múltiplos comandos)
            cursor.executescript(script_sql)
            
            conn.commit()
            print("Tabelas verificadas/criadas com sucesso a partir do schema.sql")
        except Exception as e:
            print(f"Erro ao inicializar o banco pelo script: {e}")
        finally:
            conn.close()