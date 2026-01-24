import os
import pandas as pd
from datetime import datetime
from nicegui import ui, app

# 1. CONFIGURAÇÃO DE SEGURANÇA (Obrigatório para o Render)
# Isso deve vir antes de qualquer lógica de interface
app.add_static_files('/static', 'static')

# Inicialização do banco de dados na sessão do usuário
@app.get('/')
def check_storage():
    if 'db_comb' not in app.storage.user:
        app.storage.user['db_comb'] = []

# --- DADOS INICIAIS ---
empurradores_lista = ["ANGELO", "ANGICO", "AROEIRA", "BRENO", "CANJERANA", "CUMARU", "IPE", "SAMAUMA", "JACARANDA", "LUIZ FELIPE", "QUARUBA", "TIMBORANA", "JATOBA"]

# --- INTERFACE E ESTILO ---
ui.query('body').classes('bg-slate-50')

# Menu Lateral
with ui.left_drawer().classes('bg-blue-900 text-white') as side_menu:
    ui.label('🚢 GESTÃO ZION').classes('text-xl font-bold mb-4')
    menu = ui.radio(['Abastecimento', 'Cálculo de Memória'], value='Abastecimento').classes('text-white')

# --- BLOCO 1: ABASTECIMENTO ---
@ui.refreshable
def aba_abastecimento():
    ui.label('⛽ Controle de Abastecimento').classes('text-h4 text-blue-900')
    
    db = app.storage.user.get('db_comb', [])
    if not db:
        ui.info("Nenhum dado encontrado. Faça o lançamento no Cálculo de Memória.")
        return

    # Tabela de Dados
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': 'DATA', 'field': 'Data', 'width': 100},
            {'headerName': 'EMPURRADOR', 'field': 'Empurrador', 'width': 150},
            {'headerName': 'LOCAL', 'field': 'Local', 'width': 200},
            {'headerName': 'DATA ENTREGA', 'field': 'Data_Entrega', 'editable': True},
            {'headerName': 'CICLO', 'field': 'Ciclo', 'editable': True},
        ],
        'rowData': db,
    }).classes('w-full h-80')

    async def salvar_tabela():
        dados_atualizados = await grid.get_client_data()
        app.storage.user['db_comb'] = dados_atualizados
        ui.notify('Dados atualizados com sucesso!', type='positive')

    ui.button('💾 Salvar Alterações', on_click=salvar_tabela).props('color=primary')

# --- BLOCO 2: CÁLCULO DE MEMÓRIA ---
def aba_calculo():
    ui.label('📝 Cálculo de Memória').classes('text-h4 text-blue-900')
    
    with ui.card().classes('w-full q-pa-md shadow-2'):
        with ui.row().classes('w-full items-center'):
            emp = ui.select(empurradores_lista, label='Empurrador').classes('w-1/3')
            data_v = ui.date(value=datetime.now().strftime('%Y-%m-%d')).classes('w-1/3')
            trecho = ui.input('Trecho (Ex: MANAUS X BELEM)').classes('w-1/3')

        ui.separator().classes('my-4')

        with ui.row().classes('w-full'):
            with ui.column().classes('w-1/2 p-2'):
                ui.label('📍 IDA').classes('font-bold text-blue-700')
                h_ida = ui.number('Horas Ida', value=0)
                q_ida = ui.number('Queima Ida', value=0)
            
            with ui.column().classes('w-1/2 p-2'):
                ui.label('📍 VOLTA').classes('font-bold text-blue-700')
                h_volta = ui.number('Horas Volta', value=0)
                q_volta = ui.number('Queima Volta', value=0)

        def finalizar():
            nova_viagem = {
                'Empurrador': emp.value,
                'Data': data_v.value,
                'Local': trecho.value,
                'Plano_H_Ida': h_ida.value,
                'Queima_Ida': q_ida.value,
                'Plano_H_Volta': h_volta.value,
                'Queima_Volta': q_volta.value,
                'Data_Entrega': '',
                'Ciclo': ''
            }
            app.storage.user['db_comb'].append(nova_viagem)
            ui.notify('Viagem salva com sucesso!', type='positive')
            aba_abastecimento.refresh()

        ui.button('💾 FINALIZAR E ENVIAR PARA ABASTECIMENTO', on_click=finalizar).classes('w-full mt-4 bg-green-700 text-white')

# --- RENDERIZAÇÃO PRINCIPAL ---
@ui.refreshable
def carregar_conteudo():
    if menu.value == 'Abastecimento':
        aba_abastecimento()
    else:
        aba_calculo()

menu.on_change(carregar_conteudo.refresh)

with ui.column().classes('w-full max-w-5xl mx-auto q-pa-lg'):
    carregar_conteudo()

# --- MOTOR DO RENDER (CUIDADO AQUI) ---
# Pega a porta automática do Render
porta = int(os.environ.get("PORT", 8080))

ui.run(
    host='0.0.0.0', 
    port=porta, 
    storage_secret='ZION_NAVAL_SECRET_KEY_2026', # A SENHA ESTÁ AQUI
    title="ZION Gestão Naval"
)
