from pathlib import Path

BENCHMARK_ROUNDS = 5
RESULTS_DIR = Path(__file__).parent / "results"
SQL_SERVER_QUERY = "SELECT TOP 1000 * FROM erp.categoria_produto"
POSTGRES_QUERY = "SELECT * FROM erp.categoria_produto LIMIT 1000"
SQLITE_QUERY = "SELECT * FROM categoria_produto LIMIT 1000"
DEFAULT_SQLITE_DB = Path(__file__).parent.parent / "data" / "benchmark.db"
