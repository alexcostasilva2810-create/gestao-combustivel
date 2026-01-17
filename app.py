import streamlit as st
from datetime import datetime, timezone, timedelta
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
import time
from PIL import Image
import io
import numpy as np


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
    "ANGICO": {"user": "angico_zion", "pass": "zion02"},
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

# Bloco 5 - Nota Fiscal (Versão Compatível com Render Free)
st.markdown('<h1 style="color:white; text-align:center;">ZION</h1>', unsafe_allow_html=True)
st.markdown('<div class="banner-interno-verde">DADOS DA NOTA FISCAL</div>', unsafe_allow_html=True)

st.markdown('### 📷 TIRAR FOTO DO QR CODE')
# Isso abre a câmera do celular de forma nativa e segura
foto_qr = st.camera_input("Aponte para o QR Code da NF")

if foto_qr:
    st.success("Foto registrada com sucesso!")
    st.info("O sistema armazenará a imagem para conferência.")

st.markdown("---")
# Campo para o tripulante confirmar a chave
chave_nf = st.text_input("CONFIRME A CHAVE DE ACESSO (44 DÍGITOS)", max_chars=44)

# #-------------------------------------------------------------------------#
#                           TELA DE ABASTECIMENTO (BLOCO 6)
# #-------------------------------------------------------------------------#
if st.session_state.pagina == "abastecimento":
    # --- ADIÇÃO DOS BOTÕES DE NAVEGAÇÃO ---
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ MENU CENTRAL", use_container_width=True):
            st.session_state.pagina = "menu_central"
            st.rerun()
    with col_nav2:
        if st.button("➕ NOVO ABASTECIMENTO", use_container_width=True):
            reset_lancamento()
            st.rerun()
    # ---------------------------------------

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

    # CRONÔMETRO
    classe_piscante = "piscando" if st.session_state.t_rodando else ""
    col_timer, col_fotos_upload = st.columns([1, 2])
    with col_timer:
        if st.session_state.t_rodando:
            st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - st.session_state.t_inicio)))
        st.markdown(f'<div style="background:white; color:red; font-size:24px; text-align:center; border:2px solid blue; padding:5px;">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        bt1, bt2 = st.columns(2)
        if bt1.button("▶️ INICIAR", use_container_width=True):
            st.session_state.t_inicio = time.time(); st.session_state.t_rodando = True; st.rerun()
        if bt2.button("🛑 PARAR", use_container_width=True):
            st.session_state.t_rodando = False; st.rerun()

    with col_fotos_upload:
        foto_a = st.file_uploader("CARREGAR FOTO ANTES (A)", type=['jpg', 'png', 'jpeg'], key=f"up_a_{st.session_state.form_id}")
        foto_d = st.file_uploader("CARREGAR FOTO DEPOIS (D)", type=['jpg', 'png', 'jpeg'], key=f"up_d_{st.session_state.form_id}")

    st.markdown("ASSINATURA DIGITAL :")
    canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=150, key=f"sig_{st.session_state.form_id}")

    st.markdown("---")
    
    if not transbordou:
        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", "B", 22)
            pdf.set_text_color(0, 51, 204)
            pdf.cell(0, 15, "ZION", ln=True, align="C")
            pdf.set_font("Arial", "B", 14)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, "Comunicado de Abastecimento", ln=True, align="C")
            pdf.ln(10)
            
            pdf.set_font("Arial", "", 12)
            corpo = (f"Comunico que o empurrador {navio} está apto a receber o consumo de {qtd_pedida:,} lts, "
                     f"visto que possui um saldo de {saldo_bb:,} lts (BB) e {saldo_be:,} lts (BE), "
                     f"somados ao saldo remanescente de {remanescente:,} lts.\n\n"
                     f"Portanto, o saldo total após o abastecimento será de {total_geral:,} lts.\n"
                     f"Ressaltamos que a capacidade total do empurrador é de {CAPACIDADES[navio]:,} lts.\n\n"
                     f"Informo que o empurrador levou {st.session_state.tempo_final_str} para abastecer.\n\n"
                     f"Segue abaixo as fotos do antes e depois do abastecimento:")
            pdf.multi_cell(0, 8, corpo)
            pdf.ln(5)
            
            y_fotos = pdf.get_y()
            if foto_a:
                pdf.image(Image.open(foto_a), x=15, y=y_fotos, w=85)
            if foto_d:
                pdf.image(Image.open(foto_d), x=110, y=y_fotos, w=85)
            
            if canvas_result.image_data is not None:
                img_sig = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO(); img_sig.save(buf, format="PNG")
                pdf.image(buf, x=75, y=218, w=60) 
            
            pdf.set_y(245)
            pdf.line(30, 245, 180, 245) 
            
            fuso_br = timezone(timedelta(hours=-3))
            agora_br = datetime.now(fuso_br).strftime("%d/%m/%Y às %H:%M:%S")
            geo_info = "Belém, Pará - Brasil"
            
            pdf.set_font("Arial", "I", 9)
            pdf.cell(0, 10, f"Assinado digitalmente em: {agora_br}", ln=True, align="C")
            pdf.cell(0, 5, f"Localização: {geo_info}", ln=True, align="C")
            
            st.download_button("📥 BAIXAR RELATÓRIO PDF", data=bytes(pdf.output(dest='S')), file_name=f"Zion_{navio}.pdf", use_container_width=True)

        st.markdown(f'''<div style="color: #008000; background-color: #FFFFFF; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px; font-weight: 900; border: 3px solid #008000; margin-top: 20px;">
            ⚠️ Após gerar o PDF favor enviar o arquivo para o CIOP.</div>''', unsafe_allow_html=True)
