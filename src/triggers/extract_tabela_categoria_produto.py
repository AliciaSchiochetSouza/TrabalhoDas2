import logging
import azure.functions as func
import os
import pyodbc

bp = func.Blueprint()


@bp.timer_trigger(schedule="0 0 6 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_categoria_produtos(myTimer: func.TimerRequest) -> None:

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")
    
    sql_server_destino = os.getenv("SQA_SERVER_DESTINO")
    sql_database_destino = os.getenv("SQL_DATABASE_DESTINO")
    sql_user_destino = os.getenv("SQL_USER_DESTINO")
    sql_password_destino = os.getenv("SQL_PASSWORD_DESTINO")

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

            query = "SELECT * FROM item.chamado"

            cursor_source.execute(query)

            rows = cursor_source.fetchall()

            columns = [description[0] for description in cursor_source.description]
            
        # Configura a string de conexão para o banco de dados SQL Server
        conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={sql_server_destino};"
            f"DATABASE={sql_database_destino};"
            f"UID={sql_user_destino};"
            f"PWD={sql_password_destino};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        try:
            # Estabelece a conexão com o banco de dados usando pyodbc
            with pyodbc.connect(conn_str) as conn:
                # Cria um cursor para executar a consulta   
                cursor = conn.cursor()
                
                query = "select top 5 * from erp.categoria_produto"

                # Executa a consulta SQL
                cursor.execute(query)

                # Busca todos os resultados da consulta
                rows = cursor.fetchall()

                logging.info(rows)           

        except Exception as e:
            logging.error(f"Erro ao ler extract.tabela_categoria_produto: {str(e)}")
            raise
    except Exception as e:
        logging.error(f"Erro ao ler extract.tabela_categoria_produto: {str(e)}")
        raise
    