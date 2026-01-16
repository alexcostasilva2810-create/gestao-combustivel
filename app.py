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
    .quadro-seguro { color: #00FF00 !important; background: rgba(0, 0, 0, 0.8) !important; padding: 10px; border-radius: 8px; border: 2px solid #00FF00; font-weight: bold; text-align: center; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

if 'pagina' not in st.session_state: st.session_state.pagina = "abastecimento"
if 'form_id' not in st.session_state: st.session_state.form_id = 0

def reset_lancamento():
    st.session_state.form_id += 1
    st.session_state.t_rodando = False
    st.session_state.tempo_final_str = "00:00:00"

# #-------------------------------------------------------------------------#
#                             MENU DE NAVEGAÇÃO
# #-------------------------------------------------------------------------#
st.markdown("### 📋 MENU DE NAVEGAÇÃO")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    if st.button("🏠 TELA INICIAL", use_container_width=True): st.session_state.pagina = "inicio"
with col_m2:
    if st.button("📂 MENU PRINCIPAL", use_container_width=True): st.session_state.pagina = "menu"
with col_m3:
    if st.button("⛽ NOVO ABASTECIMENTO", use_container_width=True):
        st.session_state.pagina = "abastecimento"
        reset_lancamento()

st.markdown("---")

if st.session_state.pagina == "abastecimento":
    st.markdown('<h1 style="color:white; text-align:center; font-size: 40px;">ZION</h1>', unsafe_allow_html=True)
    st.markdown('<div class="banner-interno-verde">ACOMPANHAMENTO DE ABASTECIMENTO</div>', unsafe_allow_html=True)

    CAPACIDADES = {"ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700, "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000, "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792, "TIMBORANA": 19792, "JATOBA": 84000}
    navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()), key=f"n_{st.session_state.form_id}")
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

    if transbordou:
        st.error(f"🚨 BLOQUEIO: {total_geral:,} lts excede o limite!")
    else:
        st.markdown(f'<div class="quadro-seguro">✅ VOLUME SEGURO: {total_geral:,} lts</div>', unsafe_allow_html=True)

    # CRONÔMETRO
    if 't_rodando' not in st.session_state: st.session_state.t_rodando = False
    classe_piscante = "piscando" if st.session_state.t_rodando else ""

    col_timer, col_fotos = st.columns([1, 2])
    with col_timer:
        if st.session_state.t_rodando:
            st.session_state.tempo_final_str = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - st.session_state.t_inicio)))
        st.markdown(f'<div style="background:white; color:red; font-size:24px; text-align:center; border:2px solid blue;">{st.session_state.tempo_final_str}</div>', unsafe_allow_html=True)
        bt1, bt2 = st.columns(2)
        if bt1.button("▶️ INICIAR"): st.session_state.t_inicio = time.time(); st.session_state.t_rodando = True; st.rerun()
        if bt2.button("🛑 PARAR"): st.session_state.t_rodando = False; st.rerun()

    # ÁREA DE FOTOS E ASSINATURA (QUE PISCÃO)
    st.markdown(f'<div class="{classe_piscante}">', unsafe_allow_html=True)
    with col_fotos:
        f1, f2 = st.columns(2)
        with f1: foto_a = st.camera_input("FOTO ANTES (A)", key=f"fa_{st.session_state.form_id}")
        with f2: foto_d = st.camera_input("FOTO DEPOIS (D)", key=f"fd_{st.session_state.form_id}")

    st.markdown("ASSINATURA DIGITAL")
    canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#FFFFFF", height=120, key=f"c_{st.session_state.form_id}")
    st.markdown('</div>', unsafe_allow_html=True) # Fim da área piscante

    # BOTÃO DE GERAR PDF (FORA DA ÁREA PISCANTE, SEMPRE VISÍVEL NO FINAL)
    if not transbordou:
        if st.button("GERAR COMUNICADO FINAL", use_container_width=True, type="primary"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, "ZION - Comunicado de Abastecimento", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", "", 12)
            
            # Texto detalhado restaurado
            texto = (f"Comunico que o empurrador {navio} está apto a receber o consumo de {qtd_pedida:,} lts, "
                     f"visto que possui um saldo de {saldo_bb:,} lts (BB) e {saldo_be:,} lts (BE), "
                     f"somados ao saldo remanescente de {remanescente:,} lts.\n\n"
                     f"Portanto, o saldo total após o abastecimento será de {total_geral:,} lts.\n"
                     f"Ressaltamos que a capacidade total do empurrador é de {CAPACIDADES[navio]:,} lts.\n\n"
                     f"Informo que o empurrador levou {st.session_state.tempo_final_str} para abastecer.")
            pdf.multi_cell(0, 8, texto)
            
            if foto_a and foto_d:
                pdf.image(Image.open(foto_a), x=10, y=100, w=90)
                pdf.image(Image.open(foto_d), x=110, y=100, w=90)
            if canvas_result.image_data is not None:
                img_sig = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                buf = io.BytesIO(); img_sig.save(buf, format="PNG")
                pdf.image(buf, x=70, y=200, w=60)
                pdf.text(70, 245, f"Assinado digitalmente em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
            
            st.download_button("📥 BAIXAR COMUNICADO FINAL", data=bytes(pdf.output(dest='S')), file_name=f"Zion_{navio}.pdf", use_container_width=True)
