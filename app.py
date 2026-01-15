import streamlit as st
import time
from datetime import date

# =========================================================
# BLOCO 1: CONFIGURAÇÕES, ESTILO E BANCO DE DADOS
# =========================================================
st.set_page_config(page_title="ZION TECNOLOGIA", layout="centered")

# Estilos para Mobile e Alertas Coloridos
st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/plataforma.jpg");
        background-size: cover; background-position: center;
    }
    .stApp::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.8); z-index: -1;
    }
    .box-input { background-color: white; padding: 20px; border-radius: 15px; }
    .alerta-erro { 
        background-color: #ff4b4b; color: white; padding: 15px; 
        border-radius: 10px; font-weight: bold; text-align: center; 
    }
    .alerta-sucesso { 
        background-color: #28a745; color: white; padding: 15px; 
        border-radius: 10px; font-weight: bold; text-align: center; 
    }
    label { color: #007bff !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Tabela de Capacidades
CAPACIDADES = {
    "ANGELO": 17000, "ANGICO": 88000, "AROEIRA": 88000, "BRENO": 34700,
    "CANJERANA": 18000, "CUMARU": 64000, "IPE": 29700, "SAMAUMA": 92000,
    "JACARANDA": 19792, "LUIZ FELIPE": 25000, "QUARUBA": 19792,
    "TIMBORANA": 19792, "JATOBA": 84000
}

# Gerenciador de Navegação
if 'passo' not in st.session_state: st.session_state.passo = 'INICIAL'

# =========================================================
# BLOCO 2: TELA INICIAL
# =========================================================
if st.session_state.passo == 'INICIAL':
    st.image("ZION.jpg", width=250) #
    st.markdown('<h1 style="color:white; text-align:center;">ZION TECNOLOGIA</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color:white; text-align:center;">Sistema de Recebimento de Combustível</h3>', unsafe_allow_html=True)
    
    if st.button("INICIAR REGISTRO", use_container_width=True, type="primary"):
        st.session_state.passo = 'INPUT'
        st.rerun()

# =========================================================
# BLOCO 3: TELA DE INPUT (COM LÓGICA DE SOMA E ALERTAS)
# =========================================================
elif st.session_state.passo == 'INPUT':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Dados de Abastecimento</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-input">', unsafe_allow_html=True)
        
        # Seleção de Navio e exibição da capacidade
        navio = st.selectbox("EMPURRADOR", options=list(CAPACIDADES.keys()))
        limite = CAPACIDADES[navio]
        st.info(f"Capacidade Tanque: {limite:,} lts")
        
        col1, col2 = st.columns(2)
        with col1:
            dt = st.date_input("DATA", format="DD/MM/YYYY") #
            s_bb = st.number_input("SALDO BB (LTS)", min_value=0)
            s_rem = st.number_input("REMANESCENTE (LTS)", min_value=0)
        with col2:
            pedido = st.number_input("QUANTIDADE PEDIDA (LTS)", min_value=0)
            s_be = st.number_input("SALDO BE (LTS)", min_value=0)

        # Lógica de Soma: Saldo BB + Saldo BE + Remanescente + Pedido
        total_geral = s_bb + s_be + s_rem + pedido
        
        # Disparo de Alertas Dinâmicos
        if total_geral > 0:
            if total_geral > limite:
                st.markdown(f'''
                    <div class="alerta-erro">
                        ⚠️ ATENÇÃO A SOMA REMANESCENTE MAIS QUANTO FOI PEDIDO ULTRAPASSA A CAPACIDADE DO TANQUE!<br>
                        Calculado: {total_geral:,} lts | PROCURE PCO/SUPRIMENTOS.
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alerta-sucesso">✅ EMPURRADOR HABILITADO PARA RECEBER ODM.</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("CONFERIR REGISTRO", use_container_width=True, type="primary"):
            st.session_state.dados_final = {"navio": navio, "total": total_geral, "limite": limite}
            st.session_state.passo = 'CONFERENCIA'
            st.rerun()
            
        if st.button("Voltar para Início"):
            st.session_state.passo = 'INICIAL'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# BLOCO 4: TELA DE CONFERÊNCIA FINAL
# =========================================================
elif st.session_state.passo == 'CONFERENCIA':
    res = st.session_state.dados_final
    st.markdown('<h2 style="color:white; text-align:center;">🔍 Conferência Pro</h2>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="box-input">', unsafe_allow_html=True)
        st.write(f"**Navio Selecionado:** {res['navio']}")
        st.write(f"**Soma Total:** {res['total']:,} lts")
        st.write(f"**Capacidade do Navio:** {res['limite']:,} lts")
        
        if res['total'] > res['limite']:
            st.error("BLOQUEADO: Volume acima do limite permitido.")
            if st.button("VOLTAR E CORRIGIR", use_container_width=True):
                st.session_state.passo = 'INPUT'
                st.rerun()
        else:
            if st.button("CONFIRMAR E FINALIZAR", use_container_width=True, type="primary"):
                st.balloons()
                time.sleep(2)
                st.session_state.passo = 'INICIAL'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
