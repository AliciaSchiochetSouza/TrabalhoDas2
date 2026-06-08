import logging
import azure.functions as func
import os
import pyodbc
from datetime import datetime

bp = func.Blueprint()


@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False, name="extract_entrega") 
def extract_entrega(myTimer: func.TimerRequest) -> None:

    # Log de início com timestamp
    inicio = datetime.now()
    logging.info(f"[pyodbc] Iniciando extração de dados - Horário: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info(f"""[pyodbc] servidor: {sql_server}, banco: {sql_database}, usuário: {sql_user}""")

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
            
            query = "select top 5 * from erpentrega"

            # Executa a consulta SQL
            cursor.execute(query)

            # Busca todos os resultados da consulta
            rows = cursor.fetchall()

            logging.info(f"[pyodbc] Dados extraídos com sucesso: {len(rows)} linhas retornadas")
            logging.info(f"[pyodbc] Dados: {rows}")

        # Log de finalização com timestamp
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        logging.info(f"[pyodbc] Finalização da extração - Horário: {fim.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"[pyodbc] Tempo total de execução: {duracao:.2f} segundos")
           

    except Exception as e:
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        logging.error(f"[pyodbc] Erro ao ler extract.tabela_entrega: {str(e)}")
        logging.error(f"[pyodbc] Tempo até erro: {duracao:.2f} segundos")
        raise