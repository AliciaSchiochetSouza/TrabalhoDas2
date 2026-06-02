import logging
import azure.functions as func
import os
import pyodbc

bp = func.Blueprint()


@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_transportadora(myTimer: func.TimerRequest) -> None:

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info(f"""servidor: {sql_server},banco: {sql_database}, usuário: {sql_user}, senha: {sql_password}""")

    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server};"
        f"DATABASE={sql_database};"
        f"UID={sql_user};"
        f"PWD={sql_password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

   
    try:
        # Estabelece a conexão com o banco de dados usando pyodbc
        with pyodbc.connect(conn_str) as conn:
            # Cria um cursor para executar a consulta   
            cursor = conn.cursor()
            
            query = "select top 5 * from erp.transportadora"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()

            logging.info(rows)           

    except Exception as e:
        logging.error(f"Erro ao ler extract.tabela_transportadora: {str(e)}")
        raise

