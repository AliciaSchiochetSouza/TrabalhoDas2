import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger_aula2(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    
from triggers.extract_tabela_categoria_produto import bp as tabela_categoria_produto_bp
app.register_functions(tabela_categoria_produto_bp)

from triggers.extract_tabela_cliente import bp as tabela_cliente_bp
app.register_functions(tabela_cliente_bp)

from triggers.extract_tabela_entrega import bp as tabela_entrega_bp
app.register_functions(tabela_entrega_bp)

from triggers.extract_tabela_estoque_movimentacao import bp as tabela_estoque_movimentacao_bp
app.register_functions(tabela_estoque_movimentacao_bp)

from triggers.extract_tabela_estoque_saldo import bp as tabela_estoque_saldo_bp
app.register_functions(tabela_estoque_saldo_bp)

from triggers.extract_tabela_pedido_item import bp as tabela_pedido_item_bp
app.register_functions(tabela_pedido_item_bp)

from triggers.extract_tabela_pedidos import bp as tabela_pedidos_bp
app.register_functions(tabela_pedidos_bp)

from triggers.extract_tabela_produto import bp as tabela_produto_bp
app.register_functions(tabela_produto_bp)

from triggers.extract_tabela_regiao import bp as tabela_regiao_bp
app.register_functions(tabela_regiao_bp)

from triggers.extract_tabela_representante import bp as tabela_representante_bp
app.register_functions(tabela_representante_bp)

from triggers.extract_tabela_titulo_receber import bp as tabela_titulo_receber_bp
app.register_functions(tabela_titulo_receber_bp)

from triggers.extract_tabela_transportadora import bp as tabela_transportadora_bp
app.register_functions(tabela_transportadora_bp)

from triggers.extract_tabela import bp as tabela_bp
app.register_functions(tabela_bp)




    

    

    

    

    

    

    

    

    

    

    

    