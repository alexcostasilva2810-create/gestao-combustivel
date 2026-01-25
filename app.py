import os
import time
from nicegui import ui, app

#---------------------------------------------------------#
#      BLOCO 1 - CONFIGURAÇÕES DE SEGURANÇA E BOOT
#---------------------------------------------------------#
# O storage_secret permite que o app lembre quem está logado
ui.run_with(app, storage_secret='ZION_SISTEMA_V3_2026')

#---------------------------------------------------------#
#      BLOCO 2 - BANCO DE DADOS DE ACESSO (LOGINS)
#---------------------------------------------------------#
LOGINS_VALIDOS = {
    "ANGICO": {"user": "MANOEL BARATA", "pass": "12345"},
    "ANGELO": {"user": "ALEX", "pass": "2463"},
    "SUCUPIRA": {"user": "sucupira_zion", "pass": "zion17"},
    "AROEIRA": {"user": "aroeira_zion", "pass": "zion03"},
    "BRENO": {"user": "breno_zion", "pass": "zion04"}
}

#---------------------------------------------------------#
#      BLOCO 3 - FUNÇÕES DE NAVEGAÇÃO E LÓGICA
#---------------------------------------------------------#
def ir_para(pagina_destino):
    """Troca de página e atualiza o visual"""
    app.storage.user['dados']['pagina'] = pagina_destino
    layout_principal.refresh()

def realizar_login(navio, usuario, senha):
    """Valida as credenciais do usuário"""
    credenciais = LOGINS_VALIDOS.get(navio)
    if credenciais and usuario == credenciais['user'] and senha == credenciais['pass']:
        app.storage.user['dados'].update({'usuario': usuario, 'navio': navio})
        ir_para('menu')
    else: 
        ui.notify('Dados Incorretos ou Usuário Inválido', type='negative')

#---------------------------------------------------------#
#      BLOCO 4 - INTERFACE VISUAL (LAYOUT)
#---------------------------------------------------------#
@ui.refreshable
def layout_principal():
    # Inicializa os dados se o usuário acabou de entrar
    if 'dados' not in app.storage.user:
        app.storage.user['dados'] = {'pagina': 'inicio', 'usuario': None, 'navio': None}
    
    d = app.storage.user['dados']
    
    # Estilo padrão do fundo (Zion Dark Theme)
    ui.query('body').style('background-color: #0d1117; color: white; font-family: sans-serif;')
    
    # --- TELA INICIAL ---
    if d['pagina'] == 'inicio':
        with ui.column().classes('w-full items-center mt-20'):
            ui.label('ZION NAVAL').style('font-size: 60px; font-weight: 900; color: #3b82f6;')
            ui.label('SISTEMA DE GESTÃO DE FROTA').classes('text-gray-400 mb-8')
            ui.button('INICIAR OPERAÇÃO', on_click=lambda: ir_para('login')).classes('w-64 h-16 bg-blue-600 hover:bg-blue-700')

    # --- TELA DE LOGIN ---
    elif d['pagina'] == 'login':
        with ui.column().classes('w-full max-w-md mx-auto p-6 bg-slate-900 rounded-lg mt-10 shadow-xl'):
            ui.label('ACESSO AO NAVIO').classes('text-2xl mb-4 text-center font-bold')
            
            sel_navio = ui.select(list(LOGINS_VALIDOS.keys()), label='SELECIONE O NAVIO').classes('w-full bg-white rounded p-1')
            val_user = ui.input('NOME DE USUÁRIO').classes('w-full bg-white rounded p-1 mt-2')
            val_pass = ui.input('SENHA', password=True).classes('w-full bg-white rounded p-1 mt-2')
            
            ui.button('ENTRAR', on_click=lambda: realizar_login(sel_navio.value, val_user.value, val_pass.value)).classes('w-full mt-6 bg-green-700 h-12')
            ui.button('VOLTAR', on_click=lambda: ir_para('inicio')).props('flat').classes('w-full text-gray-400 mt-2')

    # --- MENU PRINCIPAL (APÓS LOGIN) ---
    elif d['pagina'] == 'menu':
        with ui.column().classes('w-full items-center mt-10 p-4'):
            ui.label(f"NAVIO: {d['navio']}").classes('text-green-400 text-2xl font-bold')
            ui.label(f"OPERADOR: {d['usuario']}").classes('text-gray-400 mb-6')
            
            # Bloco de Câmera (Igual ao AppSheet)
            with ui.card().classes('w-full max-w-lg bg-slate-800 p-6 border border-blue-900 shadow-2xl'):
                ui.label('📷 REGISTRO DE CAMPO').classes('text-white font-bold text-lg mb-4 text-center')
                ui.upload(on_upload=lambda e: ui.notify(f'Foto {e.name} enviada com sucesso!'),
                          label='CAPTURAR FOTO AGORA', 
                          auto_upload=True).props('capture="camera"').classes('w-full')
                ui.label('Toque acima para abrir a câmera direto').classes('text-xs text-gray-500 text-center mt-2')

            ui.button('SAIR DO SISTEMA', on_click=lambda: ir_para('inicio')).classes('mt-12 bg-red-900 w-64')

#---------------------------------------------------------#
#      BLOCO 5 - INICIALIZAÇÃO DO SERVIDOR (MAIN)
#---------------------------------------------------------#
@ui.page('/')
def main():
    layout_principal()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host='0.0.0.0', 
        port=int(os.environ.get("PORT", 8080)), 
        title="ZION Naval - Gestão",
        reload=False
    )
