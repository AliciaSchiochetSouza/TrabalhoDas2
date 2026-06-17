import logging
import azure.functions as func
import os
import pyodbc

bp = func.Blueprint()

@bp.timer_trigger(schedule="0 0 6 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_categoria_produtos(myTimer: func.TimerRequest) -> None:

    sql_server = os.getenv("SQL_SERVER_SOURCE")
    sql_database = os.getenv("SQL_DATABASE_SOURCE")
    sql_user = os.getenv("SQL_USER_SOURCE")
    sql_password = os.getenv("SQL_PASSWORD_SOURCE")

    # Dica de segurança: Senha removida do log
    logging.info(f"Iniciando processo. Servidor: {sql_server}, Banco: {sql_database}, Usuário: {sql_user}")

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
            cursor = conn.cursor()
            
            # --- 1. EXTRAÇÃO (Origem) ---
            query_select = "SELECT * FROM erp.categoria_produto"
            cursor.execute(query_select)
            rows = cursor.fetchall()

            if not rows:
                logging.warning("Nenhum registro encontrado na origem (erp.categoria_produto).")
                return

            # Pega dinamicamente o nome das colunas retornado pelo SELECT
            columns = [column[0] for column in cursor.description]
            logging.info(f"Extração bem-sucedida: {len(rows)} registros encontrados.")

            # --- 2. LIMPEZA (Destino) ---
            cursor.execute("DELETE FROM itsm.categoria_produto")
            logging.info("Tabela de destino (itsm.categoria_produto) limpa.")

            # --- 3. CARREGAMENTO (Destino) ---
            placeholders = ",".join(["?" for _ in columns])
            insert_query = f"INSERT INTO itsm.categoria_produto ({','.join(columns)}) VALUES ({placeholders})"

            # Habilita a inserção manual do ID
            cursor.execute("SET IDENTITY_INSERT itsm.categoria_produto ON")
            
            # Executa o insert para todas as linhas
            cursor.executemany(insert_query, rows)
            
            # Desabilita a inserção manual do ID
            cursor.execute("SET IDENTITY_INSERT itsm.categoria_produto OFF")

            # Efetiva as transações no banco de dados
            conn.commit()

            logging.info(f"Carga finalizada: {len(rows)} registros inseridos no destino.")          

    except pyodbc.Error as e:
        logging.error(f"Erro de SQL no processamento da tabela_categoria_produto: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        raise