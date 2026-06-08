import logging
import azure.functions as func
import os
import sqlite3
from datetime import datetime

bp = func.Blueprint()


@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def extract_entrega(myTimer: func.TimerRequest) -> None:

    # Log de início com timestamp
    inicio = datetime.now()
    logging.info(f"[sqlite3] Iniciando extração de dados - Horário: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")

    # Obtém o caminho do banco de dados sqlite3 (pode estar em uma variável de ambiente ou usar um padrão)
    db_path = os.getenv("SQLITE_DB_PATH", "data/database.db")
    
    logging.info(f"[sqlite3] Caminho do banco de dados: {db_path}")

    try:
        # Estabelece a conexão com o banco de dados SQLite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query adaptada para SQLite3 (sem 'top', usa LIMIT)
        query = "SELECT * FROM erpentrega LIMIT 5"

        # Executa a consulta SQL
        cursor.execute(query)

        # Busca todos os resultados da consulta
        rows = cursor.fetchall()

        # Obtém os nomes das colunas
        column_names = [description[0] for description in cursor.description]
        
        logging.info(f"[sqlite3] Dados extraídos com sucesso: {len(rows)} linhas retornadas")
        logging.info(f"[sqlite3] Colunas: {column_names}")
        logging.info(f"[sqlite3] Dados: {rows}")

        # Fecha a conexão
        conn.close()

        # Log de finalização com timestamp
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        logging.info(f"[sqlite3] Finalização da extração - Horário: {fim.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"[sqlite3] Tempo total de execução: {duracao:.2f} segundos")
           

    except Exception as e:
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        logging.error(f"[sqlite3] Erro ao ler extract.tabela_entrega: {str(e)}")
        logging.error(f"[sqlite3] Tempo até erro: {duracao:.2f} segundos")
        raise