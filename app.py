import os
import time
from datetime import datetime, timedelta
from nicegui import ui, app
import pandas as pd
from fpdf import FPDF
import base64

# --- CONFIGURAÇÕES DE ESTILO E ESTADO ---
# Simulando o session_state do Streamlit
if 'dados' not in app.storage.user:
    app.storage.user['dados'] = {
        'pagina': 'inicio',
        'usuario': None,
        'navio': 'ANGELO',
        'historico_os': [],
        'nf_validada': {},
        'chave_limpa': '',
        't_inicio': 0,
        't_rodando': False,
        'tempo_str': '00:00:00'
    }

LOGINS_VALIDOS = {
    "ANGELO": {"user": "ALEX", "pass": "2463"},
    "ANGICO": {"user": "MANOEL BARATA", "pass": "12345"},
    "AROEIRA": {"user": "aroeira_zion", "pass": "zion03"},
    # ... adicione os outros conforme seu original
}

CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000, "CEDRO": 22000, "MOGNO": 25000,
    "FREIJO": 18000, "SUCUPIRA": 30000
}

# CSS Customizado (Fundo escuro e estilo Zion)
ui.query('body').style('background-color: #0d1117; color: white; font-family: sans-serif;')
ui.add_head_html('''
    <style>
        .zion-card { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border: 1px solid #30363d; }
        .banner-verde { background-color: #28a745; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    </style>
''')

# --- LÓGICA DE NAVEGAÇÃO ---
def ir_para(pagina):
    app.storage.user['dados']['pagina'] = pagina
    layout_principal.refresh()

# --- COMPONENTES DE TELA ---

@ui.refreshable
def layout_principal():
    dados = app.storage.user['dados']
    
    # Cabeçalho de Usuário
    if dados['usuario']:
        with ui.row().classes('w-full justify-end p-2'):
            ui.label(f"👤 {dados['usuario']} | {dados['navio']}").classes('text-green-400 font-bold border p-2 rounded-full')

    # TELA 1: INÍCIO
    if dados['pagina'] == 'inicio':
        with ui.column().classes('w-full items-center justify-center mt-20'):
            ui.label('ZION').style('font-size: 100px; font-weight: 900; line-height: 1;')
            ui.label('SISTEMA DE GESTÃO NAVAL').classes('tracking-widest text-lg mb-10')
            ui.button('🚀 INICIAR SESSÃO', on_click=lambda: ir_para('login')).classes('w-64 h-16 text-lg').props('color=primary')

    # TELA 2: LOGIN
    elif dados['pagina'] == 'login':
        with ui.column().classes('w-full max-w-md mx-auto items-center mt-10'):
            ui.label('ZION').classes('text-6xl font-black mb-4')
            ui.label('ACESSO AO SISTEMA').classes('banner-verde w-full mb-6')
            
            navio_sel = ui.select(list(LOGINS_VALIDOS.keys()), label='EMPURRADOR').classes('w-full bg-white rounded p-1')
            user_in = ui.input('USUÁRIO').classes('w-full bg-white rounded p-1')
            pass_in = ui.input('SENHA', password=True).classes('w-full bg-white rounded p-1')
            
            async def validar_login():
                cred = LOGINS_VALIDOS.get(navio_sel.value)
                if cred and user_in.value == cred['user'] and pass_in.value == cred['pass']:
                    ui.notify(f'Bem vindo {user_in.value}!', type='positive')
                    dados['usuario'] = user_in.value
                    dados['navio'] = navio_sel.value
                    ir_para('menu')
                else:
                    ui.notify('Credenciais Inválidas!', type='negative')

            ui.button('ENTRAR', on_click=validar_login).classes('w-full h-12 mt-4').props('color=primary')

    # TELA 3: MENU CENTRAL
    elif dados['pagina'] == 'menu':
        with ui.column().classes('w-full max-w-2xl mx-auto mt-10 items-center'):
            ui.label('MENU PRINCIPAL').classes('text-3xl mb-10')
            with ui.grid(columns=2).classes('w-full gap-4'):
                ui.button('🏠 TELA INICIAL (SAIR)', on_click=lambda: ir_para('inicio')).classes('h-20').props('outline color=white')
                ui.button('⛽ ABASTECIMENTO', on_click=lambda: ir_para('abastecimento')).classes('h-20').props('color=blue-9')
                ui.button('📄 NOTA FISCAL', on_click=lambda: ir_para('nf')).classes('h-20').props('color=blue-9')
                ui.button('📊 TABELA CONSUMO', on_click=lambda: ir_para('tabela')).classes('h-20').props('color=green-8')

    # TELA 4: ABASTECIMENTO
    elif dados['pagina'] == 'abastecimento':
        ui.button('⬅️ VOLTAR', on_click=lambda: ir_para('menu')).props('flat color=white')
        with ui.column().classes('w-full max-w-lg mx-auto zion-card'):
            ui.label('ACOMPANHAMENTO DE ABASTECIMENTO').classes('banner-verde w-full mb-4')
            
            cap = CAPACIDADES[dados['navio']]
            ui.label(f'Capacidade: {cap:,} lts').classes('text-yellow-400 font-bold')
            
            s_bb = ui.number('SALDO BB', value=0).classes('w-full bg-white rounded p-1')
            s_be = ui.number('SALDO BE', value=0).classes('w-full bg-white rounded p-1')
            q_ped = ui.number('QTD PEDIDA', value=0).classes('w-full bg-white rounded p-1')
            rem = ui.number('REMANESCENTE', value=0).classes('w-full bg-white rounded p-1')
            
            res_label = ui.label().classes('w-full p-4 rounded text-center font-black mt-4')
            
            def calcular():
                total = s_bb.value + s_be.value + q_ped.value + rem.value
                if total > cap:
                    res_label.text = f"🚨 BLOQUEIO: {total:,.0f} Lts excede o limite!"
                    res_label.style('background-color: red;')
                else:
                    res_label.text = f"✅ VOLUME SEGURO: {total:,.0f} Lts"
                    res_label.style('background-color: green;')

            ui.button('CALCULAR VOLUME', on_click=calcular).classes('w-full')
            
            # Cronômetro Simples
            with ui.row().classes('w-full justify-center items-center border p-2 mt-4'):
                timer_display = ui.label('00:00:00').classes('text-2xl text-red-500 font-mono')
                ui.button(icon='play_arrow', on_click=lambda: ui.notify('Iniciado')).props('round color=green')
                ui.button(icon='stop', on_click=lambda: ui.notify('Parado')).props('round color=red')

    # TELA 5: NOTA FISCAL
    elif dados['pagina'] == 'nf':
        ui.button('⬅️ VOLTAR', on_click=lambda: ir_para('menu')).props('flat color=white')
        with ui.column().classes('w-full max-w-lg mx-auto zion-card'):
            ui.label('VERIFICAÇÃO DE NOTA FISCAL').classes('banner-verde w-full mb-4')
            chave = ui.input('CHAVE DE ACESSO (44 DÍGITOS)').classes('w-full bg-white rounded p-1')
            
            def validar_nf():
                limpa = "".join(filter(str.isdigit, chave.value))
                if len(limpa) == 44:
                    dados['nf_validada'] = {"NF": limpa[25:34], "UF": "AMAZONAS", "CNPJ": limpa[6:20]}
                    ui.notify('Nota Validada!', type='positive')
                    layout_principal.refresh()
                else:
                    ui.notify('Chave Inválida', type='negative')

            ui.button('🔍 VERIFICAR', on_click=validar_nf).classes('w-full')
            
            if dados['nf_validada']:
                with ui.column().classes('w-full mt-4 p-2 bg-gray-800 rounded border-l-4 border-green-500'):
                    for k, v in dados['nf_validada'].items():
                        ui.label(f"{k}: {v}").classes('text-white font-bold')

# --- INICIALIZAÇÃO ---
with ui.column().classes('w-full'):
    layout_principal()

# O storage_secret é essencial para o app.storage funcionar no Render
ui.run(
    host='0.0.0.0', 
    port=int(os.environ.get("PORT", 8080)), 
    storage_secret='ZION_SECRET_2026',
    title="ZION Gestão Naval"
)
