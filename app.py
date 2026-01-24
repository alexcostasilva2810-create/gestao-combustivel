from nicegui import ui, app
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÕES E ESTADO ---
# Simulando o st.session_state com um dicionário global ou app.storage
if 'db_comb' not in app.storage.user:
    app.storage.user['db_comb'] = []

empurradores_lista = ["ANGELO", "ANGICO", "AROEIRA", "BRENO", "CANJERANA", "CUMARU", "IPE", "SAMAUMA", "JACARANDA", "LUIZ FELIPE", "QUARUBA", "TIMBORANA", "JATOBA"]

# --- FUNÇÕES DE APOIO ---
def salvar_memoria(dados_form):
    app.storage.user['db_comb'].append(dados_form)
    ui.notify('Salvo com sucesso no padrão BR!', type='positive')
    aba_abastecimento.refresh() # Atualiza a tabela automaticamente

# --- INTERFACE: BLOCO 1 - ABASTECIMENTO ---
@ui.refreshable
def aba_abastecimento():
    ui.label('⛽ Controle de Abastecimento').classes('text-h4')
    ui.label("Os campos 'Data Entrega', 'Local Abast.' e 'Ciclo' são editáveis direto na tabela.").classes('text-caption')
    
    db = app.storage.user.get('db_comb', [])
    
    if not db:
        ui.info("Aguardando lançamentos no Cálculo de Memória...")
        return

    # Processamento dos dados para a Grid
    rows = []
    for i, row in enumerate(db):
        trecho = str(row.get('Local', '')).upper()
        origem, destino = (trecho.split('X', 1) + [""])[:2] if 'X' in trecho else (trecho, "")
        
        h_total = row.get('Plano_H_Ida', 0) + row.get('Plano_H_Volta', 0)
        lh_rpm = (row['Plano_H_Ida'] * row['Queima_Ida'] + row['Plano_H_Volta'] * row['Queima_Volta']) / h_total if h_total > 0 else row.get('Queima_Ida', 0)

        rows.append({
            'id_ref': i,
            'ID': 1001 + i,
            'DATA': row.get('Data'),
            'EMPURRADOR': row.get('Empurrador'),
            'ORIGEM': origem.strip(),
            'DESTINO': destino.strip(),
            'DATA_ENTREGA': row.get('Data_Entrega', ''),
            'LOCAL_ABAST': row.get('Local_Abast', ''),
            'CICLO': row.get('Ciclo', ''),
            'L_H_RPM': round(lh_rpm, 2),
            'ODM_FIM': round(row.get('ODM_Fim_Final', 0), 2)
        })

    # Tabela Editável (AgGrid)
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': 'ID', 'field': 'ID', 'width': 80},
            {'headerName': 'EMPURRADOR', 'field': 'EMPURRADOR'},
            {'headerName': 'DATA ENTREGA', 'field': 'DATA_ENTREGA', 'editable': True},
            {'headerName': 'LOCAL ABAST.', 'field': 'LOCAL_ABAST', 'editable': True},
            {'headerName': 'CICLO', 'field': 'CICLO', 'editable': True},
            {'headerName': 'L/H RPM', 'field': 'L_H_RPM'},
            {'headerName': 'ODM FIM', 'field': 'ODM_FIM'},
        ],
        'rowData': rows,
    }).classes('w-full h-80')

    async def gravar():
        # No NiceGUI, pegamos os dados editados da grid
        updated_rows = await grid.get_client_data()
        for r in updated_rows:
            idx = r['id_ref']
            app.storage.user['db_comb'][idx]['Data_Entrega'] = r['DATA_ENTREGA']
            app.storage.user['db_comb'][idx]['Local_Abast'] = r['LOCAL_ABAST']
            app.storage.user['db_comb'][idx]['Ciclo'] = r['CICLO']
        ui.notify('Alterações gravadas com sucesso!')

    ui.button('💾 Gravar Alterações', on_click=gravar).props('color=primary')

# --- INTERFACE: BLOCO 2 - CÁLCULO DE MEMÓRIA ---
def aba_calculo():
    ui.label('📝 Cálculo de Memória (Ida e Volta)').classes('text-h4')
    
    with ui.row().classes('w-full'):
        emp = ui.select(empurradores_lista, label='EMPURRADOR').classes('w-1/4')
        data_v = ui.date(value=datetime.now().strftime('%Y-%m-%d')).classes('w-1/4')
        trecho = ui.input('TRECHO (Ex: MANAUS X BELEM)').classes('w-1/3')

    ui.separator()

    def coluna_entrada(label):
        with ui.column().classes('w-full p-4 border rounded'):
            ui.label(f'📍 {label}').classes('text-bold text-lg')
            s_odm = ui.number('SALDO ODM', value=0)
            o_comp = ui.number('ODM COMPRA', value=0)
            t_hor = ui.number('PLANO HORAS', value=0)
            queima = ui.number('QUEIMA L/H', value=0)
            h_mca = ui.number('HORAS MCA', value=0)
            return {'s_odm': s_odm, 'o_comp': o_comp, 't_hor': t_hor, 'queima': queima, 'h_mca': h_mca}

    with ui.row().classes('w-full'):
        res_i = coluna_entrada('IDA')
        res_v = coluna_entrada('VOLTA')

    def finalizar():
        # Lógica de cálculo simplificada para o exemplo
        nova_linha = {
            "Empurrador": emp.value,
            "Data": data_v.value,
            "Local": trecho.value,
            "Plano_H_Ida": res_i['t_hor'].value,
            "Queima_Ida": res_i['queima'].value,
            "Plano_H_Volta": res_v['t_hor'].value,
            "Queima_Volta": res_v['queima'].value,
            "ODM_Fim_Final": 0 # Adicione sua fórmula aqui
        }
        salvar_memoria(nova_linha)

    ui.button('💾 FINALIZAR E SALVAR', on_click=finalizar).classes('w-full h-12').props('color=green')

# --- MENU LATERAL E NAVEGAÇÃO ---
with ui.left_drawer().classes('bg-blue-50') as side_menu:
    ui.label('🚢 Menu de Gestão').classes('text-xl mb-4')
    nav = ui.radio(['Abastecimento', 'Cálculo de Memória', 'Rancho', 'Dashboard'], value='Abastecimento')

# Área Principal Dinâmica
@ui.refreshable
def container_principal():
    if nav.value == 'Abastecimento':
        aba_abastecimento()
    elif nav.value == 'Cálculo de Memória':
        aba_calculo()
    else:
        ui.label(f'Página {nav.value} em construção...')

# Re-renderiza a tela quando o rádio do menu lateral muda
nav.on_change(container_principal.refresh)

# Inicializa o container
with ui.column().classes('w-full'):
    container_principal()

# --- EXECUÇÃO ---
# storage_secret é necessário para usar app.storage.user (como session_state)
ui.run(host='0.0.0.0', port=8080, storage_secret='ZION_SENHA_SEGURA_123')
