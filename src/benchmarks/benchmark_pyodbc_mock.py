import sqlite3
from benchmark_config import BENCHMARK_ROUNDS, SQLITE_QUERY, DEFAULT_SQLITE_DB
from benchmark_utils import benchmark_query, print_result, save_result


class MockPyodbc:
    """Simula comportamento de pyodbc usando SQLite como base de dados."""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    def connect(self):
        return sqlite3.connect(self.db_path)


def run_query():
    # Simula como pyodbc funcionaria
    db = MockPyodbc(str(DEFAULT_SQLITE_DB))
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(SQLITE_QUERY)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def main():
    result = benchmark_query(run_query, rounds=BENCHMARK_ROUNDS)
    print_result("pyodbc (Mock)", result)
    save_result("pyodbc_mock", result)


if __name__ == "__main__":
    main()
