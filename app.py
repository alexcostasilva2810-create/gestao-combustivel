from nicegui import ui, app
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io

# --- Lógica de Dados ---
dados = {
    'empurrador': '',
    'operacao': '',
    'chave_nfe': '',
    'tabela': [
        {"Nº TANQUE": "1", "PRODUTO": "DIESEL", "REMAN": 0, "CARGA": 0},
        {"Nº TANQUE": "2", "PRODUTO": "DIESEL", "REMAN": 0, "CARGA": 0}
    ]
}

# --- Funções de Ação ---
def processar_leitura(e):
    codigo = e.args
    input_chave.value = codigo
    ui.notify(f'Código da NF-e capturado!', type='positive')

def gerar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "ZION - GESTÃO NAVAL", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(190, 10, f"Empurrador: {input_empurrador.value}", ln=True)
    pdf.cell(190, 10, f"Chave NF-e: {input_chave.value}", ln=True)
    
    # Salva em memória para download
    output = pdf.output(dest='S').encode('latin-1')
    ui.download(output, f"Checklist_{input_empurrador.value}.pdf")

# --- Interface ---
ui.query('body').classes('bg-blue-50')

with ui.column().classes('w-full items-center q-pa-md max-w-2xl mx-auto'):
    # Cabeçalho
    ui.label('ZION - GESTÃO NAVAL').classes('text-h4 text-blue-900 font-bold text-center')
    ui.label('CHECK LIST DE ABASTECIMENTO').classes('text-h6 text-grey-7')

    # Bloco Identificação e Câmera
    with ui.card().classes('w-full q-pa-md'):
        ui.label('Identificação').classes('text-bold border-b w-full')
        input_empurrador = ui.input('Empurrador / Comandante').classes('w-full')
        
        # O Leitor de QR Code / Barra
        ui.label('Scanner de Nota Fiscal').classes('mt-4 text-sm text-grey-6')
        # Container do vídeo da câmera
       ui.html('<div id="reader" style="width:100%; min-height: 250px; border: 1px solid #ccc; border-radius: 8px"></div>', sanitize=False)
        
        with ui.row().classes('w-full justify-center mt-2'):
            ui.button('ATIVAR SCANNER', on_click=lambda: ui.run_javascript('startScan()'))\
                .props('icon=qr_code_scanner color=primary')
        
        input_chave = ui.input('Chave de Acesso (44 dígitos)').classes('w-full mt-4').bind_value(dados, 'chave_nfe')

    # Tabela de Volumes (Usando AgGrid para ser similar ao data_editor)
    ui.label('Volumes (Tanques)').classes('text-bold mt-4')
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': 'Tanque', 'field': 'Nº TANQUE', 'editable': True},
            {'headerName': 'Produto', 'field': 'PRODUTO', 'editable': True},
            {'headerName': 'Carga', 'field': 'CARGA', 'editable': True},
        ],
        'rowData': dados['tabela'],
    }).classes('w-full h-40')

    # Botão Finalizar
    ui.button('FINALIZAR E GERAR PDF', on_click=gerar_pdf).classes('w-full h-12 mt-6').props('color=green text-white')

# --- Scripts de Scanner (Html5-QRCode) ---
ui.add_head_html('<script src="https://unpkg.com/html5-qrcode"></script>')
ui.on('barcode_detected', processar_leitura)

ui.add_body_html('''
<script>
    let html5QrCode;
    function startScan() {
        html5QrCode = new Html5Qrcode("reader");
        const config = { fps: 10, qrbox: { width: 280, height: 150 } };
        
        html5QrCode.start(
            { facingMode: "environment" }, 
            config,
            (decodedText) => {
                emitEvent('barcode_detected', decodedText);
                html5QrCode.stop();
            }
        ).catch(err => alert("Erro na câmera: " + err));
    }
</script>
''')

ui.run(port=8080, title="ZION Gestão")
