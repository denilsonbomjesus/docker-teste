import os
import psycopg2
from psycopg2 import Error

# função para obter as variáveis de ambiente
def get_db_config():
    return {
        "dbname": os.getenv("POSTGRES_DB", "mydatabase"),
        "user": os.getenv("POSTGRES_USER", "myuser"),
        "password": os.getenv("POSTGRES_PASSWORD", "mypassword"),
        "host": os.getenv("POSTGRES_HOST", "db"), # 'db' é o nome do serviço Postgres no docker-compose
        "port": os.getenv("POSTGRES_PORT", "5432")
    }

# função para conectar ao banco de dados
def connect_db():
    config = get_db_config()
    conn = None
    try:
        print(f"Tentando conectar ao PostgreSQL em {config['host']}:{config['port']}...")
        conn = psycopg2.connect(**config)
        print("Conexão com o PostgreSQL realizado com sucesso!")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None
    
# função para criar tabela
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Tabela 'messages' criada ou já existente.")
    except Error as e:
        print(f"Erro ao criar a tabela: {e}")

# função para inserir dados
def insert_message(conn, message):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (content) VALUES (%s);", (message,))
        conn.commit()
        print(f"Mensagem '{message}' inserida com sucesso!")
    except Error as e:
        print(f"Erro ao inserir a mensagem: {e}")

# função para ler os dados
def read_messages(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, created_at FROM messages;")
        messages = cursor.fetchall()
        if messages:
            print("\nMensagens no banco de dados:")
            for msg in messages:
                print(f"ID: '{msg[0]}', Conteúdo: '{msg[1]}', Criado em: '{msg[2]}'")
        else:
            print("\nNenhuma mensagem encontrada no banco de dados.")
    except Error as e:
        print(f"Erro ao ler mensagens: {e}")

if __name__ == "__main__":
    conn = None
    try:
        conn = connect_db()
        if conn:
            create_table(conn)

            # inserir algumas mensagens de teste
            insert_message(conn, "Hello World, Docker com PostgreSQL")
            insert_message(conn, "Configurando Docker, com WSL 2 e Ubuntu")

            # ler todas as mensagens
            read_messages(conn)

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o PostgreSQL fechada.")