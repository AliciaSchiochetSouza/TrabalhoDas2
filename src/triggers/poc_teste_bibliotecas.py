import logging
import time
import azure.functions as func
import os
import pyodbc
from sqlalchemy import URL, create_engine, text


bp = func.Blueprint()

@bp.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False,
            use_monitor=False) 
def poc_teste_cliente(timer: func.TimerRequest) -> None:
    sql_server = os.getenv("SQL_SERVER_SOURCE")
    database = os.getenv("SQL_DATABASE_SOURCE")
    user = os.getenv("SQL_USER_SOURCE")
    password = os.getenv("SQL_PASSWORD_SOURCE")
    
    logging.info(f"Iniciando | Servidor {sql_server}, banco: {database}, usuário: {user}, senha: {password}")
    
    # Configura a string de conexão para o banco de dados SQL Server
    conn_str = URL.create(
        "mssql+pyodbc",
        host=sql_server,
        database=database,
        username=user,
        password=password,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "no",
            "Connection Timeout": "30"
        }
    )
    
    engine = create_engine(conn_str)
    
    try:
        # ===== MEDIÇÃO COM SQLALCHEMY =====
        logging.info("Iniciando medição com SQLAlchemy...")
        
        inicio_sqlalchemy = time.perf_counter()
        with engine.connect() as conn:
            query = text("select * from erp.entrega")
            result = conn.execute(query)
            rows_sqlalchemy = [dict(row) for row in result.mappings()]
            
            for row in rows_sqlalchemy:
                logging.info(f"Entrega extraído (SQLAlchemy): {row}")
        
        fim_sqlalchemy = time.perf_counter()
        duracao_sqlalchemy = (fim_sqlalchemy - inicio_sqlalchemy) * 1000
        logging.info(f"SQLAlchemy - Tempo de execução: {duracao_sqlalchemy:.2f} ms")
        
        # ===== MEDIÇÃO COM PYODBC =====
        logging.info("Iniciando medição com pyODBC...")
        
        conn_str_pyodbc = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={sql_server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
        )
        
        inicio_pyodbc = time.perf_counter()
        with pyodbc.connect(conn_str_pyodbc) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from erp.entrega")
            rows_pyodbc = cursor.fetchall()
            
            for row in rows_pyodbc:
                logging.info(f"Entrega extraído (pyODBC): {row}")
        
        fim_pyodbc = time.perf_counter()
        duracao_pyodbc = (fim_pyodbc - inicio_pyodbc) * 1000
        logging.info(f"pyODBC - Tempo de execução: {duracao_pyodbc:.2f} ms")
        
        # ===== COMPARAÇÃO =====
        logging.info(f"SQLAlchemy: {duracao_sqlalchemy:.2f} ms | pyODBC: {duracao_pyodbc:.2f} ms | Diferença: {abs(duracao_sqlalchemy - duracao_pyodbc):.2f} ms")

    except Exception as e:
        logging.error(f"Erro ao ler erp.entrega: {str(e)}")
        raise