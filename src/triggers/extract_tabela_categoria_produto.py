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

    # Dica de segurança: removi a senha do log para não expor credenciais em produção
    logging.info(f"Servidor: {sql_server}, banco: {sql_database}, usuário: {sql_user}")
   
    try:
        # A string de conexão é a mesma para origem e destino neste caso
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

        # --- Conexão de Origem ---
        with pyodbc.connect(conn_str) as conn_source:
            cursor_source = conn_source.cursor()
            cursor_source.execute("SELECT * FROM erp.categoria_produto")
            rows = cursor_source.fetchall()
            columns = [description[0] for description in cursor_source.description]

        if not rows:
            logging.warning('Nenhum registro encontrado na tabela categoria_produto')
            return

        logging.info(f'Extração bem-sucedida: {len(rows)} registros encontrados')

        # --- Conexão de Destino ---
        with pyodbc.connect(conn_str) as conn_dest:
            cursor_dest = conn_dest.cursor()

            cursor_dest.execute("DELETE FROM itsm.categoria_produto")
            logging.info('Tabela de destino limpa')

            placeholders = ','.join(['?' for _ in columns])
            
          
            insert_query = f"INSERT INTO itsm.categoria_produto ({','.join(columns)}) VALUES ({placeholders})"

     
            cursor_dest.execute("SET IDENTITY_INSERT itsm.categoria_produto ON")
            
      
            cursor_dest.executemany(insert_query, rows)
            
       
            cursor_dest.execute("SET IDENTITY_INSERT itsm.categoria_produto OFF")
            
            conn_dest.commit()

        logging.info(f'Carregamento bem-sucedido: {len(rows)} registros inseridos')

    except pyodbc.Error as e:
        logging.error(f"Erro SQL: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        raise