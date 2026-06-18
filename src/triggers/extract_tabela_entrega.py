import logging
import azure.functions as func
import os
import pyodbc

bp = func.Blueprint()

# Nota: O seu schedule atual ("0 * * * * *") vai rodar a cada 1 minuto. 
# Se quiser que rode uma vez por dia às 6h da manhã, mude para: "0 0 6 * * *"
@bp.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def extract_entrega(myTimer: func.TimerRequest) -> None:

    # --- Variáveis da Origem ---
    sql_server_source = os.getenv("SQL_SERVER_SOURCE")
    sql_database_source = os.getenv("SQL_DATABASE_SOURCE")
    sql_user_source = os.getenv("SQL_USER_SOURCE")
    sql_password_source = os.getenv("SQL_PASSWORD_SOURCE")

    # --- Variáveis do Destino ---
    sql_server_dest = os.getenv("SQL_SERVER_DESTINO")
    sql_database_dest = os.getenv("SQL_DATABASE_DESTINO")
    sql_user_dest = os.getenv("SQL_USER_DESTINO")
    sql_password_dest = os.getenv("SQL_PASSWORD_DESTINO")

    logging.info(f"Iniciando integração de Entregas. Lendo de: {sql_database_source} | Gravando em: {sql_database_dest}")

    # --- String de Conexão: ORIGEM ---
    conn_str_source = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server_source};"
        f"DATABASE={sql_database_source};"
        f"UID={sql_user_source};"
        f"PWD={sql_password_source};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )

    # --- String de Conexão: DESTINO ---
    conn_str_dest = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={sql_server_dest};"
        f"DATABASE={sql_database_dest};"
        f"UID={sql_user_dest};"
        f"PWD={sql_password_dest};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
   
    try:
        # --- 1. EXTRAÇÃO (Conecta na ORIGEM) ---
        with pyodbc.connect(conn_str_source) as conn_source:
            cursor_source = conn_source.cursor()
            
            # Busca todas as entregas da origem
            query_select = "SELECT * FROM erp.entrega"
            cursor_source.execute(query_select)
            rows = cursor_source.fetchall()

            if not rows:
                logging.warning("Nenhum registro encontrado na origem (erp.entrega).")
                return

            columns = [column[0] for column in cursor_source.description]
            logging.info(f"Extração de entregas bem-sucedida: {len(rows)} registros encontrados.")

        # --- 2. LIMPEZA E CARREGAMENTO (Conecta no DESTINO) ---
        with pyodbc.connect(conn_str_dest) as conn_dest:
            cursor_dest = conn_dest.cursor()

            # Nome da tabela correspondente no banco de destino
            table_name = "dbo.entrega"

            cursor_dest.execute(f"DELETE FROM {table_name}")
            logging.info(f"Tabela de destino ({table_name}) limpa.")

            placeholders = ",".join(["?" for _ in columns])
            insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

            # Habilita a inserção manual de IDs
            cursor_dest.execute(f"SET IDENTITY_INSERT {table_name} ON")
            
            # Executa a inserção em lote de todas as linhas de entregas
            cursor_dest.executemany(insert_query, rows)
            
            # Desabilita a inserção manual do ID
            cursor_dest.execute(f"SET IDENTITY_INSERT {table_name} OFF")

            # Efetiva as transações no banco de destino
            conn_dest.commit()

            logging.info(f"Carga finalizada: {len(rows)} entregas inseridas com sucesso no destino.")          

    except pyodbc.Error as e:
        logging.error(f"Erro de SQL no processamento de entregas: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Erro inesperado no processo de entregas: {str(e)}")
        raise