import streamlit as st
from datetime import datetime
from fpdf import FPDF
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import time

# #-------------------------------------------------------------------------#
#                             BLOCO 1: CONFIGURAÇÕES
# #-------------------------------------------------------------------------#

st.set_page_config(page_title="ZION TECNOLOGIA", layout="centered")

# CSS com Plano de Fundo Naval e Acessibilidade (Fonte 14pt)
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1516939884455-1445c8652f83?q=80&w=1974&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Camada escura suave para dar contraste aos campos */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(255, 255, 255, 0.85); /* Transparência suave branca */
        z-index: -1;
    }

    .box-branco { 
        background-color: rgba(255, 255, 255, 0.95); 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #ddd;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Acessibilidade: Fontes em tamanho 14pt (aprox 19px) */
    label, .stSelectbox, .stNumberInput, .stDateInput, p, .stButton { 
        font-size: 19px !important; 
        color: #004a99 !important; 
        font-weight: bold !important;
    }
    
    input { font-size: 19px !important; }

    .banner-interno-verde {
        color: #28a745;
        text-align: center;
        font-weight: 900;
        font-size: 26px;
        padding: 10px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    
    .timer-display { 
        font-size: 36px; 
        font-weight: bold; 
        color: #d32f2f; 
        text-align: center; 
        padding: 15px; 
        background: #fdfdfd; 
        border-radius: 10px; 
        border: 3px solid #007bff; 
    }
    </style>
    """, unsafe_allow_html=True)

# Capacidades mantidas conforme o original
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

if 'passo' not in st.session_state: st.session_state.passo = 'INICIAL'
if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
if 't_inicio' not in st.session_state: st.session_state.t_inicio = 0
if 'tempo_final_str' not in st.session_state: st.session_state.tempo_final_str = "00:00:00"

# #-------------------------------------------------------------------------#
#                             BLOCO 2: TELA INICIAL
# #-------------------------------------------------------------------------#

if st.session_state.passo == 'INICIAL':
    st.markdown('<h1 style="color:#007bff; text-align:center; font-size: 45px;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    if st.button("INICIAR NOVO REGISTRO", use_container_width=True, type="primary"):
        st.session_state.passo = 'INPUT'
        st.rerun()

# #-------------------------------------------------------------------------#
#                             BLOCO 3: INPUT DE DADOS
# #-------------------------------------------------------------------------#

elif st.session_state.passo == 'INPUT':
    st.markdown('<h1 style="color:#007bff; text-align:center; margin-bottom:5px;">ZION</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-branco">', unsafe_allow_html=True)
        
        # Banner verde DENTRO da caixa branca
        st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)
        
        navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
        limite = CAPACIDADES[navio]
        st.info(f"Capacidade do Tanque: {limite:,} lts")
        
        col1, col2 = st.columns(2)
        with col1:
            dt_input = st.date_input("DATA", format="DD/MM/YYYY")
            s_bb = st.number_input("SALDO BB (LTS)", min_value=0)
            s_be = st.number_input("SALDO BE (LTS)", min_value=0)
            s_rem = st.number_input("REMANESCENTE (LTS)", min_value=0)
            
        with col2:
            pedido = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            
            st.markdown("<label>CONTROLE DE TEMPO</label>", unsafe_allow_html=True)
            placeholder_tempo = st.empty()
            
            c_t1, c_t2 = st.columns(2)
            if c_t1.button("▶️ INICIAR", use_container_width=True):
                st.session_state.t_inicio = time.time()
                st.session_state.t_rodando = True
            
            if c_t2.button("🛑 PARAR", use_container_width=True):
                st.session_state.t_rodando = False
            
            if st.session_state.t_rodando:
                segundos = int(time.time() - st.session_state.t_inicio)
                st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(segundos))
                placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
                time.sleep(0.1)
                st.rerun()
            else:
                placeholder_tempo.markdown(f'<div class="timer-display">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)

        st.markdown("---")
        # Assinatura com rótulo simplificado
        st.markdown("<label>ASSINATURA DIGITAL</label>", unsafe_allow_html=True)
        canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#f8f9fa", height=150, key="canvas_v_final_acessivel")

        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            if canvas_result.image_data is not None:
                st.session_state.assinatura = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                st.session_state.dados_pdf = {
                    "navio": navio, "pedido": pedido, "s_bb": s_bb, "s_be": s_be, 
                    "s_rem": s_rem, "total": s_bb+s_be+s_rem+pedido, "limite": limite,
                    "tempo": st.session_state.tempo_final_str,
                    "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
                }
                st.session_state.passo = 'RELATORIO'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
