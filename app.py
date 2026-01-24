import os
import time
from datetime import datetime
from nicegui import ui, app

# =========================================================
# 1. SEGURANÇA IMEDIATA (RESOLVE O ERRO DA LINHA 36/11)
# =========================================================
# Este comando PRECISA vir antes de qualquer 'app.storage'
ui.run_with(app, storage_secret='ZION_SISTEMA_2026_FINAL')

# =========================================================
# 2. CONFIGURAÇÕES DE ACESSO E CAPACIDADES
# =========================================================
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

# Inicialização segura dos dados
if 'dados' not in app.storage.user:
    app.storage.user['dados'] = {
        'pagina': 'inicio',
        'usuario': None,
        'navio': 'ANGELO',
        't_inicio': 0,
        't_rodando': False,
        'tempo_str': '00:00:00'
    }

# =========================================================
# 3. INTERFACE E ESTILO
# =========================================================
ui.query('body').style('background-color: #0d1117; color: white;')

def ir_para(pagina):
    app.storage.user['dados']['pagina'] = pagina
    layout_principal.refresh()

def timer_tick():
    d = app.storage.user['dados']
    if d['t_rodando']:
        seg = int(time.time() - d['t_inicio'])
        d['tempo_str'] = time.strftime('%H:%M:%S', time.gmtime(seg))

@ui.refreshable
def layout_principal():
    dados = app.storage.user['dados']
    ui.timer(1.0, timer_tick)

    if dados['pagina'] == 'inicio':
        with ui.column().classes('w-full items-center mt-20'):
            ui.label('ZION').style('font-size: 80px; font-weight: 900;')
            ui.button('🚀 ENTRAR NO SISTEMA', on_click=lambda: ir_para('login')).classes('w-64 h-16 bg-blue-600')

    elif dados['pagina'] == 'login':
        with ui.column().classes('w-full max-w-md mx-auto items-center mt-10'):
            ui.label('ACESSO RESTRITO').classes('text-2xl mb-6')
            navio = ui.select(list(LOGINS_VALIDOS.keys()), label='SELECIONE O EMPURRADOR').classes('w-full bg-white p-1')
            user_in = ui.input('USUÁRIO').classes('w-full bg-white p-1')
            pass_in = ui.input('SENHA', password=True).classes('w-full bg-white p-1')
            
            def autenticar():
                cred = LOGINS_VALIDOS.get(navio.value)
                if cred and user_in.value == cred['user'] and pass_in.value == cred['pass']:
                    dados.update({'usuario': user_in.value, 'navio': navio.value})
                    ir_para('menu')
                else:
                    ui.notify('Dados incorretos!', type='negative')
            
            ui.button('CONFIRMAR', on_click=autenticar).classes('w-full mt-4 bg-green-700')

    elif dados['pagina'] == 'menu':
        with ui.column().classes('w-full items-center mt-10'):
            ui.label(f"BEM-VINDO: {dados['usuario']}").classes('text-xl')
            ui.label(f"EMPURRADOR: {dados['navio']}").classes('text-green-400')
            ui.button('⛽ ABASTECIMENTO', on_click=lambda: ir_para('abastecimento')).classes('w-64 h-16 bg-blue-900 mt-4')
            ui.button('🏠 SAIR', on_click=lambda: (dados.update({'usuario': None}), ir_para('inicio'))).classes('w-64 mt-4')

    elif dados['pagina'] == 'abastecimento':
        ui.button('⬅️ VOLTAR', on_click=lambda: ir_para('menu')).props('flat color=white')
        with ui.column().classes('w-full max-w-lg mx-auto p-4 border rounded'):
            ui.label(f"CRONÔMETRO:").classes('text-center w-full')
            ui.label().bind_text_from(dados, 'tempo_str').classes('text-4xl text-red-500 font-mono text-center w-full')
            with ui.row().classes('w-full justify-center'):
                ui.button(icon='play_arrow', on_click=lambda: (dados.update({'t_inicio': time.time(), 't_rodando': True}))).props('round color=green')
                ui.button(icon='stop', on_click=lambda: (dados.update({'t_rodando': False}))).props('round color=red')

# =========================================================
# 4. EXECUÇÃO DO SERVIDOR
# =========================================================
layout_principal()

ui.run(
    host='0.0.0.0', 
    port=int(os.environ.get("PORT", 8080)), 
    title="ZION Naval"
)
