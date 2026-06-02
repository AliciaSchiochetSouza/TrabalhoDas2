import os
import sqlite3
from benchmark_config import BENCHMARK_ROUNDS, SQLITE_QUERY, DEFAULT_SQLITE_DB
from benchmark_utils import benchmark_query, print_result, save_result


def get_sqlite_path():
    path = os.getenv("SQLITE_DB_PATH")
    if path:
        return path
    return str(DEFAULT_SQLITE_DB)


def run_query():
    db_path = get_sqlite_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(SQLITE_QUERY)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def main():
    result = benchmark_query(run_query, rounds=BENCHMARK_ROUNDS)
    print_result("sqlite3", result)
    save_result("sqlite3", result)


if __name__ == "__main__":
    main()
