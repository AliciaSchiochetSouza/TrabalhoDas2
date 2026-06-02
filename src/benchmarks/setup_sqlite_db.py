import sqlite3
from pathlib import Path

# Criar diretorio data se nao existir
data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

db_path = data_dir / "benchmark.db"

# Conectar e criar tabela
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Criar tabela de teste
cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria_produto (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        descricao TEXT,
        preco REAL,
        estoque INTEGER
    )
""")

# Inserir dados de teste (1000 registros)
cursor.executemany(
    "INSERT INTO categoria_produto (nome, descricao, preco, estoque) VALUES (?, ?, ?, ?)",
    [
        (f"Produto {i}", f"Descricao do produto {i}", 10.50 + i * 0.1, 100 + i)
        for i in range(1000)
    ],
)

conn.commit()
conn.close()

print(f"Banco de dados SQLite criado em: {db_path}")
print(f"Dados de teste inseridos: 1000 registros")
