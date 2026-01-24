import os
import time
from datetime import datetime
from nicegui import ui, app

# --- BANCO DE DADOS COMPLETO ---
LOGINS_VALIDOS = {
    "ANGELO": {"user": "ALEX", "pass": "2463"},
    "ANGICO": {"user": "MANOEL BARATA", "pass": "12345"},
    "AROEIRA": {"user": "aroeira_zion", "pass": "zion03"},
    "BRENO": {"user": "breno_zion", "pass": "zion04"},
    "CANJERANA": {"user": "canjerana_zion", "pass": "zion05"},
    "CUMARU": {"user": "cumaru_zion", "pass": "zion06"},
    "IPE": {"user": "ipe_zion", "pass": "zion07"},
    "SAMAUMA": {"user": "samauma_zion", "pass": "zion08"},
    "JACARANDA": {"user": "jacaranda_zion", "pass": "zion09"},
    "LUIZ FELIPE": {"user": "luizf_zion", "pass": "zion10"},
    "QUARUBA": {"user": "quaruba_zion", "pass": "zion11"},
    "TIMBORANA": {"user": "timborana_zion", "pass": "zion12"},
    "JATOBA": {"user": "jatoba_zion", "pass": "zion13"},
    "CEDRO": {"user": "cedro_zion", "pass": "zion14"},
    "MOGNO": {"user": "mogno_zion", "pass": "zion15"},
    "FREIJO": {"user": "freijo_zion", "pass": "zion16"},
    "SUCUPIRA": {"user": "sucupira_zion", "pass": "zion17"}
}

CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000, "CEDRO": 22000, "MOGNO": 25000,
    "FREIJO": 18000, "SUCUPIRA": 30000
}

# --- INICIALIZAÇÃO DE ESTADO ---
if 'dados' not in app.storage.user:
    app.storage.user['dados'] = {
        'pagina': 'inicio',
        'usuario': None,
        'navio': 'ANGELO',
        'historico_os': [],
        'nf_validada': {},
        't_inicio': 0,
        't_rodando': False,
        'tempo_str': '00:00:00'
    }

# --- ESTILIZAÇÃO ---
ui.query('body').style('background-color: #0d1117; color: white;')
ui.add_head_html('''
    <style>
        .zion-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border: 1px solid #30363d; }
        .banner-verde { background-color: #28a745; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    </style>
''')

# --- FUNÇÕES DE APOIO ---
def ir_para(pagina):
    app.storage.user['dados']['pagina'] = pagina
    layout_principal.refresh()

def atualizar_cronometro():
    d = app.storage.user['dados']
    if d['t_rodando']:
        segundos = int(time.time() - d['t_inicio'])
        d['tempo_str'] = time.strftime('%H:%M:%S', time.gmtime(segundos))

# --- TELAS ---
@ui.refreshable
def layout_principal():
    dados = app.storage.user['dados']
    
    # Timer que roda a cada 1 segundo para o cronômetro
    ui.timer(1.0, atualizar_cronometro)

    # TELA 1: INÍCIO
    if dados['pagina'] == 'inicio':
        with ui.column().classes('w-full items-center justify-center mt-20'):
            ui.label('ZION').style('font-size: 80px; font-weight: 900;')
            ui.label('SISTEMA DE GESTÃO NAVAL').classes('mb-10')
            ui.button('🚀 INICIAR SESSÃO', on_click=lambda: ir_para('login')).classes('w-64 h-16')

    # TELA 2: LOGIN
    elif dados['pagina'] == 'login':
        with ui.column().classes('w-full max-w-md mx-auto items-center mt-10'):
            ui.label('ACESSO AO SISTEMA').classes('banner-verde w-full mb-6')
            navio_sel = ui.select(list(LOGINS_VALIDOS.keys()), label='EMPURRADOR').classes('w-full bg-white rounded p-1')
            user_in = ui.input('USUÁRIO').classes('w-full bg-white rounded p-1')
            pass_in = ui.input('SENHA', password=True).classes('w-full bg-white rounded p-1')

            def validar():
                cred = LOGINS_VALIDOS.get(navio_sel.value)
                if cred and user_in.value == cred['user'] and pass_in.value == cred['pass']:
                    dados.update({'usuario': user_in.value, 'navio': navio_sel.value})
                    ir_para('menu')
                else:
                    ui.notify('Dados Incorretos!', type='negative')

            ui.button('ENTRAR', on_click=validar).classes('w-full mt-4 bg-blue-600')

    # TELA 3: MENU
    elif dados['pagina'] == 'menu':
        with ui.column().classes('w-full items-center mt-10'):
            ui.label(f"👤 {dados['usuario']} | {dados['navio']}").classes('text-green-400 mb-10')
            with ui.grid(columns=2).classes('w-full max-w-xl gap-4'):
                ui.button('⛽ ABASTECIMENTO', on_click=lambda: ir_para('abastecimento')).classes('h-20 bg-blue-900')
                ui.button('📄 NOTA FISCAL', on_click=lambda: ir_para('nf')).classes('h-20 bg-blue-900')
                ui.button('📊 TABELA', on_click=lambda: ir_para('tabela')).classes('h-20 bg-green-900')
                ui.button('🏠 SAIR', on_click=lambda: (dados.update({'usuario': None}), ir_para('inicio'))).classes('h-20')

    # TELA 4: ABASTECIMENTO
    elif dados['pagina'] == 'abastecimento':
        ui.button('⬅️ VOLTAR', on_click=lambda: ir_para('menu')).props('flat color=white')
        with ui.column().classes('w-full max-w-lg mx-auto zion-card'):
            cap = CAPACIDADES[dados['navio']]
            ui.label(f'Capacidade: {cap:,} lts').classes('text-yellow-400 font-bold')
            
            s_bb = ui.number('SALDO BB', value=0).classes('w-full bg-white p-1')
            s_be = ui.number('SALDO BE', value=0).classes('w-full bg-white p-1')
            q_ped = ui.number('QTD PEDIDA', value=0).classes('w-full bg-white p-1')
            rem = ui.number('REMANESCENTE', value=0).classes('w-full bg-white p-1')
            
            res_label = ui.label().classes('w-full p-4 rounded text-center mt-4')

            def calcular():
                total = (s_bb.value or 0) + (s_be.value or 0) + (q_ped.value or 0) + (rem.value or 0)
                if total > cap:
                    res_label.text = f"🚨 BLOQUEIO: {total:,.0f} Lts excede o limite!"
                    res_label.style('background-color: red;')
                else:
                    res_label.text = f"✅ VOLUME SEGURO: {total:,.0f} Lts"
                    res_label.style('background-color: green;')

            ui.button('VERIFICAR VOLUME', on_click=calcular).classes('w-full bg-blue-600')

            # CRONÔMETRO FUNCIONAL
            with ui.row().classes('w-full justify-center items-center mt-4 border p-2'):
                ui.label().bind_text_from(dados, 'tempo_str').classes('text-2xl text-red-500 font-mono')
                ui.button(icon='play_arrow', on_click=lambda: (dados.update({'t_inicio': time.time(), 't_rodando': True}))).props('round color=green')
                ui.button(icon='stop', on_click=lambda: (dados.update({'t_rodando': False}))).props('round color=red')

    # TELA 6: TABELA DE CONSUMO (O.S.)
    elif dados['pagina'] == 'tabela':
        ui.button('⬅️ VOLTAR', on_click=lambda: ir_para('menu')).props('flat color=white')
        ui.label('REGISTROS DE CONSUMO (O.S.)').classes('text-2xl mb-4')
        
        # Cria a tabela com os dados do histórico
        colunas = [
            {'name': 'ID', 'label': 'ID', 'field': 'ID'},
            {'name': 'NAVIO', 'label': 'NAVIO', 'field': 'NAVIO'},
            {'name': 'DATA', 'label': 'DATA', 'field': 'DATA'},
        ]
        ui.table(columns=colunas, rows=dados['historico_os']).classes('w-full bg-white text-black')

# --- EXECUÇÃO ---
with ui.column().classes('w-full'):
    layout_principal()

ui.run(
    host='0.0.0.0', 
    port=int(os.environ.get("PORT", 8080)), 
    storage_secret='ZION_SISTEMA_2026_FINAL', # Resolvido o erro do Render
    title="ZION Gestão"
)
