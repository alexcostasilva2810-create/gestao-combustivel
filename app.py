import streamlit as st
import base64
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="ZION - Governança", page_icon="🔐", layout="centered")

def carregar_imagem_base64(caminho):
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_base64 = carregar_imagem_base64("ZION.jpg")
fundo_base64 = carregar_imagem_base64("plataforma.jpg")

# --- 2. ESTILO VISUAL ---
fundo_estilo = f"""
    background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
    url("data:image/jpg;base64,{fundo_base64}");
    background-size: cover; background-position: center; background-attachment: fixed;
""" if fundo_base64 else "background-color: #1E1E1E;"

st.markdown(f"""
    <style>
    .stApp {{ {fundo_estilo} }}
    .container-central {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .titulo-zion {{ color: white !important; font-size: 35px !important; font-weight: bold; text-shadow: 2px 2px 4px #000; }}
    .subtitulo-zion {{ color: #ddd !important; font-size: 18px !important; margin-bottom: 20px; }}
    .stButton {{ display: flex; justify-content: center; }}
    .stButton>button {{ width: 100%; max-width: 300px; height: 3.5em; background-color: #007bff; color: white; font-weight: bold; border-radius: 12px; }}
    input {{ background-color: white !important; color: black !important; border-radius: 8px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BLOCO DE GOVERNANÇA (13 VAGAS) ---
def validar_acesso(usuario, senha):
    # Dicionário preparado para 13 usuários (Chave: Usuário / Valor: Senha)
    # Para ativar, basta mudar o nome 'user1' e a senha 'senha1'
    usuarios_autorizados = {
        "admin": "zion123",    # Usuário mestre
        "user2": "senha2",     # Vaga 02
        "user3": "senha3",     # Vaga 03
        "user4": "senha4",     # Vaga 04
        "user5": "senha5",     # Vaga 05
        "user6": "senha6",     # Vaga 06
        "user7": "senha7",     # Vaga 07
        "user8": "senha8",     # Vaga 08
        "user9": "senha9",     # Vaga 09
        "user10": "senha10",   # Vaga 10
        "user11": "senha11",   # Vaga 11
        "user12": "senha12",   # Vaga 12
        "user13": "senha13",   # Vaga 13
    }
    
    if usuario in usuarios_autorizados and usuarios_autorizados[usuario] == senha:
        st.session_state.autenticado = True
        st.session_state.usuario_logado = usuario
        st.success(f"Acesso Validado! Bem-vindo, {usuario}")
        time.sleep(1)
        st.rerun()
    else:
        st.error("Usuário ou Senha incorretos!")

# --- 4. FLUXO DE TELAS ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# TELA DE LOGIN
if not st.session_state.autenticado:
    st.markdown('<div class="container-central">', unsafe_allow_html=True)
    if logo_base64:
        st.markdown(f'<img src="data:image/jpg;base64,{logo_base64}" width="200" style="border-radius:20px;">', unsafe_allow_html=True)
    st.markdown('<p class="titulo-zion">GOVERNANÇA DE ACESSO</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user_input = st.text_input("Usuário")
        pass_input = st.text_input("Senha", type="password")
        if st.button("INICIAR"):
            validar_acesso(user_input, pass_input)
    st.markdown('</div>', unsafe_allow_html=True)

# TELA PRINCIPAL (PÓS-LOGIN)
else:
    if 'tela' not in st.session_state: st.session_state.tela = 'inicio'

    if st.session_state.tela == 'inicio':
        st.markdown('<div class="container-central">', unsafe_allow_html=True)
        if logo_base64:
            st.markdown(f'<img src="data:image/jpg;base64,{logo_base64}" width="220" style="border-radius:20px;">', unsafe_allow_html=True)
        
        # MENSAGEM SOLICITADA
        st.markdown('<p class="titulo-zion">Bem vindo ao Zion !!</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:white;">Usuário: {st.session_state.usuario_logado}</p>', unsafe_allow_html=True)
        
        # Botão centralizado no quadrado marcado anteriormente
        if st.button("ABRIR FORMULÁRIO"):
            st.session_state.tela = 'form'
            st.rerun()
        
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.tela == 'form':
        st.markdown('<h2 style="color:white; text-align:center;">📝 Novo Registro</h2>', unsafe_allow_html=True)
        with st.form("registro"):
            emp = st.text_input("EMPURRADOR")
            ped = st.text_input("Nº PEDIDO")
            if st.form_submit_button("SALVAR"):
                st.success("✅ Dados Salvos!")
                st.session_state.tela = 'inicio'
                st.rerun()
