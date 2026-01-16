import streamlit as st
from datetime import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
import time
from PIL import Image
import io

# #-------------------------------------------------------------------------#
#                             CONFIGURAÇÕES VISUAIS
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION - SISTEMA DE GESTÃO", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1524522173746-f628baad3644?q=80&w=2000&auto=format&fit=crop");
        background-size: cover; background-position: center; background-attachment: fixed;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75); z-index: -1;
    }
    label, .stMarkdown p { 
        font-size: 16px !important; color: #FFFFFF !important;  
        font-weight: bold !important; text-shadow: 1px 1px 3px #000;
    }
    .alerta-capacidade {
        color: #FFFF00 !important; font-size: 14px !important; font-weight: 800 !important;
        background: rgba(0, 0, 0, 0.6); padding: 8px 12px; border-radius: 5px;
        margin-bottom: 10px; display: inline-block; border: 1px solid #FFFF00;
    }
    .quadro-seguro {
        color: #00FF00 !important; background: rgba(0, 0, 0, 0.8) !important;
        padding: 10px; border-radius: 8px; border: 2px solid #00FF00;
        font-weight: bold; text-align: center; font-size: 16px;
    }
    .alerta-transbordo-flutuante {
        background-color: #FFFF00 !important; color: #FF0000 !important; 
        padding: 15px; border-radius: 10px; border: 4px solid #FF0000;
        font-weight: 900; text-align: center; font-size: 18px;
        margin-bottom: 15px; box-shadow: 0px 10px 30px rgba(255, 0, 0, 0.7);
    }
    .banner-interno-verde {
        color: #28a745; text-align: center; font-weight: 900; font-size: 24px;
        margin-bottom: 20px; background: rgba(255, 255, 255, 0.95); padding: 12px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# #-------------------------------------------------------------------------#
#               LÓGICA DE NAVEGAÇÃO E LIMPEZA
# #-------------------------------------------------------------------------#

if 'pagina' not in st.session_state: st.session_state.pagina = "abastecimento"
if 'form_id' not in st.session_state: st.session_state.form_id = 0

def reset_lancamento():
    st.session_state.form_id += 1
    st.session_state.t_rodando = False
    st.session_state.t_inicio = 0
    st.session_state.tempo_final_str = "00:00:00"

# #-------------------------------------------------------------------------#
#                             TELA DE ABASTECIMENTO
# #-------------------------------------------------------------------------#

if st.session_state.pagina == "abastecimento":
    st.markdown('<h1 style="color:white; text-align:center; font-size: 40px; margin-bottom: 5px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)

    CAPACIDADES = {
        "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
        "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
        "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
        "TIMBORANA": 19792, "JATOBA": 84000
    }

    navio_selecionado = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()), key=f"navio_{st.session_state.form_id}")
    st.markdown(f'<div class="alerta-capacidade">Capacidade do Tanque: {CAPACIDADES[navio_selecionado]:,} lts</div>', unsafe_allow_html=True)

    # DADOS DE ENTRADA
    col_a, col_b = st.columns(2)
    with col_a:
        data_abast = st.date_input("DATA", format="DD/MM/YYYY", key=f"dt_{st.session_state.form_id}")
        saldo_bb = st.number_input("SALDO BB (LTS)", min_value=0, key=f"bb_{st.session_state.form_id}")
        saldo_be = st.number_input("SALDO BE (LTS)", min_value=0, key=f"be_{st.session_state.form_id}")
    with col_b:
        qtd_pedida = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0, key=f"qp_{st.session_state.form_id}")
        remanescente = st.number_input("REMANESCENTE (LTS)", min_value=0, key=f"rm_{st.session_state.form_id}")

    # CÁLCULO DE SEGURANÇA (SOMA QUÁDRUPLA)
    total_geral = saldo_bb + saldo_be + remanescente + qtd_pedida
    limite = CAPACIDADES[navio_selecionado]
    transbordou = total_geral > limite

    # STATUS DE VOLUME
    if transbordou:
        st.markdown(f'<div style="color:red; background:white; padding:10px; border:2px solid red; font-weight:bold; text-align:center; border-radius:8px;">⚠️ VOLUME ATUAL: {total_geral:,} lts (EXCEDE O LIMITE!)</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="quadro-seguro">✅ VOLUME SEGURO: {total_geral:,} lts</div>', unsafe_allow_html=True)

    st.markdown("---")

    # CONTROLE DE TEMPO E FOTOS LADO A LADO
    col_esq, col_dir = st.columns(2)
    
    with col_esq:
        st.markdown("<p style='text-align:center;'>CRONÔMETRO</p>", unsafe_allow_html=True)
        if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
        if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"
        
        # Display do Timer
        if st.session_state.t_rodando:
            segundos = int(time.time() - st.session_state.t_inicio)
            st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
        
        st.markdown(f'<div style="background:white; color:red; font-size:28px; text-align:center; border-radius:10px; border:2px solid blue; padding:5px;">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns(2)
        if btn_c1.button("▶️ INICIAR", use_container_width=True):
            st.session_state.t_inicio = time.time(); st.session_state.t_rodando = True
        if btn_c2.button("🛑 PARAR", use_container_width=True):
            st.session_state.t_rodando = False

    with col_dir:
        # CAPTURADORES DE IMAGEM LADO A LADO [Solicitado pelo usuário]
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            # camera_input abre a câmera diretamente no mobile
            foto_antes = st.camera_input("FOTO ANTES (A)", key=f"fa_{st.session_state.form_id}")
        with f_col2:
            foto_depois = st.camera_input("FOTO DEPOIS (D)", key=f"fd_{st.session_state.form_id}")

    st.markdown("---")
    st.markdown("<p>ASSINATURA DIGITAL</p>", unsafe_allow_html=True)
    canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=120, key=f"canvas_{st.session_state.form_id}")

    # --- BLOQUEIO E BOTÃO FINAL ---
    if transbordou:
        st.markdown(f"""
            <div class="alerta-transbordo-flutuante">
                🚨 BLOQUEIO DE SEGURANÇA 🚨<br>
                A soma ({total_geral:,} lts) ultrapassa o limite!<br>
                <b>IMPEDIR O TRANSBORDO PARA LIBERAR IMPRESSÃO</b>
            </div>
        """, unsafe_allow_html=True)
        st.button("GERAR COMUNICADO FINAL (BLOQUEADO)", use_container_width=True, disabled=True)
    else:
        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            st.success("Gerando documento... Verifique o download abaixo.")
            # (Aqui entra a lógica do FPDF conforme histórico anterior)

st.markdown("---")
if st.button("📂 LIMPAR TUDO / NOVO LANÇAMENTO", use_container_width=True):
    reset_lancamento()
    st.rerun()
