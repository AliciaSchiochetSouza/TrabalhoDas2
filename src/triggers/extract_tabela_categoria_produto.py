import logging
import azure.functions as func
import os
import pyodbc

bp = func.Blueprint()


@bp.timer_trigger(
    schedule="0 0 6 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def extract_categoria_produtos(myTimer: func.TimerRequest) -> None:

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")

    sql_server_destino = os.getenv("SQL_SERVER_DESTINO")
    sql_database_destino = os.getenv("SQL_DATABASE_DESTINO")
    sql_user_destino = os.getenv("SQL_USER_DESTINO")
    sql_password_destino = os.getenv("SQL_PASSWORD_DESTINO")

    rows = []
    columns = []

    try:
        # ---------- EXTRAÇÃO ----------
        conn_str_source = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={sql_server};"
            f"DATABASE={sql_database};"
            f"UID={sql_user};"
            f"PWD={sql_password};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )

        with pyodbc.connect(conn_str_source) as conn_source:
            cursor_source = conn_source.cursor()

            query = "SELECT * FROM erp.categoria_produto"

            cursor_source.execute(query)

            rows = cursor_source.fetchall()

            # Obtém os nomes das colunas
            columns = [col[0] for col in cursor_source.description]

            logging.info(f"Colunas encontradas: {columns}")
            logging.info(f"Quantidade de registros extraídos: {len(rows)}")

        # ---------- DESTINO ----------
        conn_str_destino = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={sql_server_destino};"
            f"DATABASE={sql_database_destino};"
            f"UID={sql_user_destino};"
            f"PWD={sql_password_destino};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )

        with pyodbc.connect(conn_str_destino) as conn_destino:
            cursor_destino = conn_destino.cursor()

            # Exemplo de INSERT dinâmico usando as colunas extraídas
            if rows:

                colunas_sql = ", ".join(columns)
                placeholders = ", ".join(["?"] * len(columns))

                insert_query = f"""
                    INSERT INTO dbo.categoria_produto ({colunas_sql})
                    VALUES ({placeholders})
                """

                cursor_destino.executemany(insert_query, rows)
                conn_destino.commit()

                logging.info(
                    f"{len(rows)} registros inseridos em dbo.categoria_produto."
                )

    except Exception as e:
        logging.error(
            f"Erro ao processar extract.tabela_categoria_produto: {str(e)}"
        )
        raise