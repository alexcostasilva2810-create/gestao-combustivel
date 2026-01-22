import streamlit as st
from datetime import datetime, timezone, timedelta
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
import time
from PIL import Image
import io
import numpy as np
# Inicialização do estado da sessão
if "dados_nf_validos" not in st.session_state:
    st.session_state.dados_nf_validos = None

# #-------------------------------------------------------------------------#
#                          ERP ZION - LÓGICA CENTRAL
# #-------------------------------------------------------------------------#
def salvar_os_automatica():
    """
    Consolida dados do Abastecimento (Bloco 6) e NF (Bloco 5)
    e gera uma Ordem de Serviço (O.S.) automática.
    """
    # Puxa os dados exatos salvos na memória (Session State)
    abast = st.session_state.get('dados_abastecimento', {})
    nf_dados = st.session_state.get('dados_nf_validos', {})
    chave_pura = st.session_state.get('chave_limpa', '')

    # Verifica se há algo para salvar
    if abast or nf_dados:
        if 'historico_os' not in st.session_state:
            st.session_state.historico_os = []

        # Gerador de O.S. 0001 em diante
        proxima_os = f"{len(st.session_state.historico_os) + 1:04d}"
        
        # Mapeamento fiel aos campos das suas telas
        novo_registro = {
            "ID_OS": proxima_os,
            "USUARIO": st.session_state.get('usuario_logado', 'Admin'),
            "EMPURRADOR": abast.get('empurrador', 'N/A'),
            "DATA": abast.get('data', ''),
            "QTD PEDIDA": abast.get('qtd_pedida', 0),
            "SALDO BB": abast.get('saldo_bb', 0),
            "SALDO BE": abast.get('saldo_be', 0),
            "REMANESCENTE": abast.get('remanescente', 0),
            "NUMERO NF": nf_dados.get('NÚMERO DA NOTA FISCAL', 'N/A'),
            "UF": nf_dados.get('UF', 'N/A'),
            "CHAVE ACESSO": chave_pura
        }

        # Evita duplicar a mesma O.S. se o usuário clicar várias vezes no PDF
        if not any(d.get('CHAVE ACESSO') == chave_pura and d.get('NUMERO NF') == novo_registro['NUMERO NF'] for d in st.session_state.historico_os):
            st.session_state.historico_os.insert(0, novo_registro)
            # DICA: Quando configurarmos o Notion, a chamada da API entrará aqui.


# #-------------------------------------------------------------------------#
#                                CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#
st.set_page_config(page_title="ZION - SISTEMA DE GESTÃO", layout="centered")

st.markdown("""
    <style>
    @keyframes blinking { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .piscando { animation: blinking 1s infinite; }
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    label, .stMarkdown p { font-size: 16px !important; color: #FFFFFF !important; font-weight: bold !important; text-shadow: 1px 1px 3px #000; }
    .banner-interno-verde { color: #28a745; text-align: center; font-weight: 900; font-size: 24px; margin-bottom: 20px; background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px; }
    
    /* MENSAGENS DE LOGIN PEDIDAS */
    .msg-sucesso { color: #008000 !important; background-color: #FFFFFF !important; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #008000; margin-top: 10px; }
    .msg-erro { color: #FF0000 !important; background-color: #000000 !important; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px !important; font-weight: bold !important; border: 3px solid #FF0000; margin-top: 10px; }
    
    /* USUÁRIO NO TOPO DIREITO */
    .user-header { position: fixed; top: 10px; right: 10px; color: #00FF00; font-weight: bold; background: rgba(0,0,0,0.6); padding: 5px 15px; border-radius: 20px; border: 1px solid #00FF00; z-index: 1000; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO ÍCONE E APP (PWA) ---
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="/static/manifest.json">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <link rel="apple-touch-icon" href="/static/icone ZION.png">
        <title>ZION</title>
    </head>
    """,
    unsafe_allow_html=True
)

# #-------------------------------------------------------------------------#
#                LÓGICA DE NAVEGAÇÃO E ESTADO (MEMÓRIA) (BLOCO 1)
# #-------------------------------------------------------------------------#
if 'pagina' not in st.session_state: st.session_state.pagina = "inicio"
if 'usuario_logado' not in st.session_state: st.session_state.usuario_logado = None
if 'navio_atual' not in st.session_state: st.session_state.navio_atual = "ANGELO"
if 'form_id' not in st.session_state: st.session_state.form_id = 0
if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"

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

def reset_lancamento():
    st.session_state.form_id += 1
    st.session_state.t_rodando = False
    st.session_state.tempo_final_str = "00:00:00"

# EXIBE USUÁRIO LOGADO SE EXISTIR
if st.session_state.usuario_logado:
    st.markdown(f'<div class="user-header">👤 {st.session_state.usuario_logado}</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 1: LOGO ZION E BOTÃO INICIAR (BLOCO 2)
# #-------------------------------------------------------------------------#

if st.session_state.pagina == "inicio":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<h1 style="color:white; text-align:center; font-size: 100px; font-weight: 900;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:white; font-size: 20px; letter-spacing: 5px;">SISTEMA DE GESTÃO NAVAL</p>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 INICIAR SESSÃO", use_container_width=True):
        st.session_state.pagina = "login"

        st.rerun()

# #-------------------------------------------------------------------------#
#            TELA 2: LOGIN COM CAMPOS E ALERTAS (BLOCO 3)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "login":
    st.markdown('<h1 style="color:white; text-align:center; font-size: 60px; font-weight: 900;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACESSO AO SISTEMA</div>', unsafe_allow_html=True)
    
    empurrador_login = st.selectbox("EMPURRADOR", options=list(LOGINS_VALIDOS.keys()))
    user_input = st.text_input("USUÁRIO")
    pw_input = st.text_input("SENHA", type="password")
    
    if st.button("ENTRAR", use_container_width=True, type="primary"):
        credenciais = LOGINS_VALIDOS.get(empurrador_login)
        if user_input == credenciais["user"] and pw_input == credenciais["pass"]:
            st.markdown(f'<div class="msg-sucesso">👍 SEJA BEM VINDO <b>{user_input}</b> ao Sistema Zion !</div>', unsafe_allow_html=True)
            st.session_state.usuario_logado = user_input
            st.session_state.navio_atual = empurrador_login
            time.sleep(2)
            st.session_state.pagina = "menu_central"
            st.rerun()
        else:
            st.markdown('<div class="msg-erro">👎 SUAS CREDENCIAS ESTÃO INCONSISTENTE ENTRE EM CONTATO PELO ZAP 91-9-9349-7079 E DIGA QUE NÃO ESTA CONSEGUINDO ACESSA O SITEMA .</div>', unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#            TELA 3: MENU CENTRAL (OS 4 BOTÕES) (BLOCO 4)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "menu_central":
    st.markdown('<h1 style="color:white; text-align:center;">MENU PRINCIPAL</h1>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 TELA INICIAL (SAIR)", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.session_state.usuario_logado = None
            st.rerun()
        if st.button("⛽ ACOMPANHAMENTO ABASTECIMENTO", use_container_width=True):
            st.session_state.pagina = "abastecimento"
            st.rerun()
    with c2:
        if st.button("📄 DADOS DA NOTA FISCAL", use_container_width=True):
            st.session_state.pagina = "nota_fiscal"
            st.rerun()
        if st.button("📊 TABELA DE CONSUMO RECEBIDA", use_container_width=True):
            st.session_state.pagina = "tabela_consumo"
            st.rerun()

# #-------------------------------------------------------------------------#
#             TELA DE ABASTECIMENTO INTEGRADA (RODAPÉ RESTAURADO)
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "abastecimento":
    # --- BOTÕES DE NAVEGAÇÃO E RESET TOTAL ---
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ MENU CENTRAL", use_container_width=True):
            st.session_state.pagina = "menu_central"
            st.rerun()
    with col_nav2:
        if st.button("➕ NOVO LANÇAMENTO", use_container_width=True):
            st.session_state.navio_atual = "ANGELO"
            st.session_state.t_rodando = False
            st.session_state.t_inicio = 0
            st.session_state.tempo_final_str = "00:00:00"
            st.session_state.dados_nf_validos = {}
            st.session_state.chave_limpa = ""
            st.session_state.dados_abastecimento = {}
            st.session_state.form_id += 1 
            st.rerun()

    st.markdown('<h1 style="color:white; text-align:center; font-size: 40px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)

    CAPACIDADES = {
        "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
        "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
        "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
        "TIMBORANA": 19792, "JATOBA": 84000, "CEDRO": 22000, "MOGNO": 25000,
        "FREIJO": 18000, "SUCUPIRA": 30000
    }
    
    navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()), 
                         index=list(CAPACIDADES.keys()).index(st.session_state.navio_atual), 
                         key=f"n_{st.session_state.form_id}")
    
    st.markdown(f'<div style="color: #FFFF00; font-weight: bold;">Capacidade do Tanque: {CAPACIDADES[navio]:,} lts</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        data_abast = st.date_input("DATA", format="DD/MM/YYYY", key=f"d_{st.session_state.form_id}")
        saldo_bb = st.number_input("SALDO BB (LTS)", min_value=0, key=f"bb_{st.session_state.form_id}")
        saldo_be = st.number_input("SALDO BE (LTS)", min_value=0, key=f"be_{st.session_state.form_id}")
    with col_b:
        qtd_pedida = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0, key=f"qp_{st.session_state.form_id}")
        remanescente = st.number_input("REMANESCENTE (LTS)", min_value=0, key=f"rm_{st.session_state.form_id}")

    total_geral = saldo_bb + saldo_be + remanescente + qtd_pedida
    transbordou = total_geral > CAPACIDADES[navio]
    valor_formatado = f"{total_geral:,}".replace(",", ".")

    if transbordou:
        st.markdown(f'''<div style="color: #FFFFFF; background-color: #FF0000; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px; font-weight: 900; border: 3px solid white; margin-bottom: 20px;">
            🚨 BLOQUEIO: {valor_formatado} Lts excede o limite!</div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div style="color: #FFFFFF; background-color: #28a745; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px; font-weight: 900; border: 3px solid white; margin-bottom: 20px;">
            ✅ VOLUME SEGURO: {valor_formatado} Lts Capacidade permitida!</div>''', unsafe_allow_html=True)

    col_timer, col_fotos_upload = st.columns([1, 2])
    with col_timer:
        if st.session_state.t_rodando:
            st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - st.session_state.t_inicio)))
        st.markdown(f'<div style="background:white; color:red; font-size:24px; text-align:center; border:2px solid blue; padding:5px;">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        bt1, bt2 = st.columns(2)
        if bt1.button("▶️ INICIAR", use_container_width=True, key=f"start_{st.session_state.form_id}"):
            st.session_state.t_inicio = time.time(); st.session_state.t_rodando = True; st.rerun()
        if bt2.button("🛑 PARAR", use_container_width=True, key=f"stop_{st.session_state.form_id}"):
            st.session_state.t_rodando = False; st.rerun()

    with col_fotos_upload:
        foto_a = st.file_uploader("CARREGAR FOTO ANTES (A)", type=['jpg', 'png', 'jpeg'], key=f"up_a_{st.session_state.form_id}")
        foto_d = st.file_uploader("CARREGAR FOTO DEPOIS (D)", type=['jpg', 'png', 'jpeg'], key=f"up_d_{st.session_state.form_id}")

    st.markdown("---")
    st.markdown('<div style="background-color: #004d40; color: white; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold;">VERIFICAÇÃO DE NOTA FISCAL (NF-e)</div>', unsafe_allow_html=True)
    chave_acesso = st.text_input("DIGITE OU COLE A CHAVE DE ACESSO", max_chars=54, key=f"nf_input_{st.session_state.form_id}")
    chave_limpa = "".join(filter(str.isdigit, chave_acesso))
    
   # --- INÍCIO DO BLOCO DE VERIFICAÇÃO NF COM LEITOR ---
from streamlit_camera_barcode_reader import camera_barcode_reader

# 1. Abre a câmera para leitura automática do código de barras
barcode = camera_barcode_reader()

if barcode:
    # Se a câmera detectar o código, salva no estado da sessão
    st.session_state.chave_acesso = barcode.replace(" ", "")
    st.success("Código capturado com sucesso!")

# 2. Campo de entrada (Recebe o valor da câmera ou manual)
chave_input = st.text_input(
    "DIGITE OU COLE A CHAVE DE ACESSO", 
    value=st.session_state.get('chave_acesso', ""),
    max_chars=44
)

# 3. Limpa a chave (remove espaços) para a lógica das linhas abaixo
chave_limpa = "".join(filter(str.isdigit, chave_input))

# 4. Botão de Verificação (Mantendo sua lógica original de processamento)
if st.button("🔍 VERIFICAÇÃO NF", use_container_width=True):
    if len(chave_limpa) == 44:
        comp_br = f"{chave_limpa[4:6]}/{chave_limpa[2:4]}"
        
        # O bloco que você marcou na linha 279
        st.session_state.dados_nf_validos = {
            "UF": "AMAZONAS - AM", 
            "COMPETÊNCIA": comp_br, 
            "CNPJ": chave_limpa[6:20],
            "MOD": chave_limpa[20:22], 
            "SÉRIE": chave_limpa[22:25], 
            "NÚMERO": chave_limpa[25:34],
            "CHAVE": chave_limpa
        }
        st.success("Nota Fiscal validada!")
    else:
        st.error("A chave de acesso deve conter exatamente 44 dígitos.")
    if st.session_state.get('dados_nf_validos'):
        for campo, valor in st.session_state.dados_nf_validos.items():
            st.markdown(f'<div style="background-color: #f1f3f4; padding: 8px; margin: 5px 0; border-radius: 5px; border-left: 5px solid #2e7d32; color: black; font-weight: bold;">{campo}: {valor}</div>', unsafe_allow_html=True)

    st.markdown("ASSINATURA DIGITAL :")
    canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=120, key=f"sig_{st.session_state.form_id}")

    if not transbordou:
        if st.button("SALVAR E GERAR O ARQUIVO EM PDF", use_container_width=True, type="primary"):
            st.session_state.dados_abastecimento = {
                'empurrador': navio, 'data': data_abast.strftime("%d/%m/%Y"),
                'qtd_pedida': qtd_pedida, 'saldo_bb': saldo_bb, 'saldo_be': saldo_be, 'remanescente': remanescente,
                'nf_numero': st.session_state.dados_nf_validos.get("NÚMERO", "N/A")
            }
            salvar_os_automatica()

            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", "B", 22); pdf.set_text_color(0, 51, 204)
            pdf.cell(0, 15, "ZION INTEGRADO", ln=True, align="C")
            pdf.set_font("Arial", "B", 14); pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Comunicado de Abastecimento", ln=True, align="C")
            pdf.ln(5)
            
            pdf.set_font("Arial", "", 12)
            corpo = (f"Comunico que o empurrador {navio} recebeu o consumo de {qtd_pedida:,} lts, "
                     f"visto que possuia um saldo de {saldo_bb:,} lts (BB) e {saldo_be:,} lts (BE), "
                     f"somados ao saldo remanescente de {remanescente:,} lts.\n\n"
                     f"Portanto, o saldo total após o abastecimento é de {total_geral:,} lts.\n"
                     f"Ressaltamos que a capacidade total do empurrador é de {CAPACIDADES[navio]:,} lts.\n\n"
                     f"Informo que o empurrador levou {st.session_state.tempo_final_str} para abastecer.")
            pdf.multi_cell(0, 8, corpo)
            
            y_f = pdf.get_y() + 5
            if foto_a: pdf.image(Image.open(foto_a), x=15, y=y_f, w=80)
            if foto_d: pdf.image(Image.open(foto_d), x=110, y=y_f, w=80)
            
            pdf.set_y(y_f + 55)
            pdf.set_fill_color(240, 240, 240); pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 8, "DADOS DA NOTA FISCAL (NF-e)", ln=True, fill=True, border=1, align="C")
            pdf.set_font("Arial", "", 9)
            if st.session_state.dados_nf_validos:
                nf = st.session_state.dados_nf_validos
                pdf.cell(45, 6, " NUMERO DA NF:", border=1); pdf.cell(50, 6, f" {nf['NÚMERO']}", border=1)
                pdf.cell(45, 6, " CNPJ:", border=1); pdf.cell(50, 6, f" {nf['CNPJ']}", border=1, ln=True)
                pdf.cell(45, 6, " SERIE:", border=1); pdf.cell(50, 6, f" {nf['SÉRIE']}", border=1)
                pdf.cell(45, 6, " COMPETENCIA:", border=1); pdf.cell(50, 6, f" {nf['COMPETÊNCIA']}", border=1, ln=True)
                pdf.cell(45, 6, " CHAVE DE ACESSO:", border=1); pdf.cell(145, 6, f" {nf['CHAVE']}", border=1, ln=True)

            if canvas_result.image_data is not None:
                img_sig = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO(); img_sig.save(buf, format="PNG")
                pdf.image(buf, x=75, y=pdf.get_y()+2, w=55)
            
            pdf.ln(18)
            pdf.line(40, pdf.get_y(), 170, pdf.get_y())
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 5, f"{st.session_state.usuario_logado}", ln=True, align="C")
            
            fuso_br = timezone(timedelta(hours=-3))
            agora_br = datetime.now(fuso_br).strftime("%d/%m/%Y às %H:%M:%S")
            pdf.set_font("Arial", "I", 8)
            pdf.cell(0, 5, f"Assinado digitalmente em: {agora_br}", ln=True, align="C")
            pdf.cell(0, 5, f"Localização: Belém, Pará - Brasil", ln=True, align="C")
            
            st.download_button("📥 BAIXAR RELATÓRIO FINAL", data=bytes(pdf.output(dest='S')), file_name=f"Zion_Final_{navio}.pdf", use_container_width=True)

        st.markdown(f'''<div style="color: #008000; background-color: #FFFFFF; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px; font-weight: 900; border: 3px solid #008000; margin-top: 20px;">
            ⚠️ Após gerar o PDF favor enviar o arquivo para o CIOP.</div>''', unsafe_allow_html=True)
# #-------------------------------------------------------------------------#
#             TABELA DE CONSUMO (BLOCO 7) - CORREÇÃO DE EXIBIÇÃO
# #-------------------------------------------------------------------------#
elif st.session_state.pagina == "tabela_consumo":
    if st.button("⬅️ VOLTAR AO MENU CENTRAL", use_container_width=True):
        st.session_state.pagina = "menu_central"
        st.rerun()

    st.markdown('<h1 style="color:white; text-align:center;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div style="background-color: #2e7d32; color: white; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold;">TABELA DE CONSUMO (O.S.)</div>', unsafe_allow_html=True)

    # Inicializa o histórico se não existir
    if 'historico_os' not in st.session_state: 
        st.session_state.historico_os = []

    # --- BOTÃO DE SALVAR ---
    if st.button("💾 SALVAR LANÇAMENTO E GERAR O.S.", use_container_width=True, type="primary"):
        abast = st.session_state.get('dados_abastecimento', {})
        nf_dados = st.session_state.get('dados_nf_validos', {})
        
        if abast and nf_dados:
            proxima_os = f"{len(st.session_state.historico_os) + 1:04d}"
            
            # Dados exatos das suas telas
            registro_os = {
                "ID_OS": proxima_os,
                "USUARIO": st.session_state.get('usuario_logado', 'Admin'),
                "EMPURRADOR": abast.get('empurrador', 'N/A'),
                "DATA": abast.get('data', ''),
                "QTD PEDIDA": abast.get('qtd_pedida', 0),
                "SALDO BB": abast.get('saldo_bb', 0),
                "SALDO BE": abast.get('saldo_be', 0),
                "REMANESCENTE": abast.get('remanescente', 0),
                "NUMERO NF": nf_dados.get('NÚMERO DA NOTA FISCAL', 'N/A'),
                "UF": nf_dados.get('UF', 'N/A'),
                "CHAVE ACESSO": st.session_state.get('chave_limpa', '')
            }
            st.session_state.historico_os.insert(0, registro_os)
            st.success(f"✅ O.S. {proxima_os} Gerada!")
        else:
            st.error("⚠️ Erro: Você precisa preencher os Blocos 5 e 6 antes de salvar!")

    # --- EXIBIÇÃO DA TABELA (FORA DO IF PARA APARECER SEMPRE) ---
    st.write("---")
    st.markdown("### 📋 Registros de Consumo")
    
    if st.session_state.historico_os:
        # Se tem dados, mostra a tabela preenchida
        st.dataframe(st.session_state.historico_os, use_container_width=True)
    else:
        # Se está vazia, cria uma tabela de exemplo apenas com os cabeçalhos corretos
        import pandas as pd
        colunas = ["ID_OS", "USUARIO", "EMPURRADOR", "DATA", "QTD PEDIDA", "SALDO BB", "SALDO BE", "REMANESCENTE", "NUMERO NF", "UF", "CHAVE ACESSO"]
        df_vazio = pd.DataFrame(columns=colunas)
        st.dataframe(df_vazio, use_container_width=True)
        st.info("A tabela está vazia. Realize um lançamento para gerar a primeira O.S.")
