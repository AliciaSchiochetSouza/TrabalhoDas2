from sqlalchemy import create_engine, text
from benchmark_config import BENCHMARK_ROUNDS, SQLITE_QUERY, DEFAULT_SQLITE_DB
from benchmark_utils import benchmark_query, print_result, save_result


def get_connection_url():
    db_path = str(DEFAULT_SQLITE_DB)
    return f"sqlite:///{db_path}"


def run_query():
    engine = create_engine(get_connection_url())
    with engine.connect() as connection:
        result = connection.execute(text(SQLITE_QUERY))
        return result.fetchall()


def main():
    result = benchmark_query(run_query, rounds=BENCHMARK_ROUNDS)
    print_result("SQLAlchemy (SQLite)", result)
    save_result("sqlalchemy_sqlite", result)


if __name__ == "__main__":
    main()
