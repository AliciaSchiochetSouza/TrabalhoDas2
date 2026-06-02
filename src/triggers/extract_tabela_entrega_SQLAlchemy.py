import logging
import azure.functions as func
import os
from datetime import datetime
from sqlalchemy import create_engine, text

bp = func.Blueprint()


@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_entrega(myTimer: func.TimerRequest) -> None:

    # Log de início com timestamp
    inicio = datetime.now()
    logging.info(f"[SQLAlchemy] Iniciando extração de dados - Horário: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")

    logging.info(f"""[SQLAlchemy] servidor: {sql_server}, banco: {sql_database}, usuário: {sql_user}""")

    # Configura a string de conexão para o banco de dados SQL Server usando SQLAlchemy
    # Formato: mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+18+for+SQL+Server
    conn_str = (
        f"mssql+pyodbc://{sql_user}:{sql_password}@{sql_server}/{sql_database}?"
        "driver=ODBC+Driver+18+for+SQL+Server&"
        "Encrypt=yes&"
        "TrustServerCertificate=no&"
        "Connection+Timeout=30"
    )

   
    try:
        # Cria a engine do SQLAlchemy
        engine = create_engine(conn_str, echo=False)
        
        # Estabelece a conexão
        with engine.connect() as connection:
            
            query = "select top 5 * from erpentrega"

            # Executa a consulta SQL
            result = connection.execute(text(query))

            # Busca todos os resultados da consulta
            rows = result.fetchall()

            logging.info(f"[SQLAlchemy] Dados extraídos com sucesso: {len(rows)} linhas retornadas")
            logging.info(f"[SQLAlchemy] Dados: {rows}")

        # Log de finalização com timestamp
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        logging.info(f"[SQLAlchemy] Finalização da extração - Horário: {fim.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"[SQLAlchemy] Tempo total de execução: {duracao:.2f} segundos")
           

    except Exception as e:
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        logging.error(f"[SQLAlchemy] Erro ao ler extract.tabela_entrega: {str(e)}")
        logging.error(f"[SQLAlchemy] Tempo até erro: {duracao:.2f} segundos")
        raise