import streamlit as st
import requests
from datetime import date

# --- BLOCO 1: CONFIGURAÇÃO INICIAL E ESTILO ---
st.set_page_config(
    page_title="ZION Combustível",
    page_icon="⛽",
    layout="centered"
)

# **IMPORTANTE:** Para que as imagens apareçam, você deve ter os seguintes arquivos
# na RAIZ do seu repositório GitHub (gestao-combustivel):
# - 'ZION.JPG' (sua logo)
# - 'plataforma.jpg' (a imagem de fundo da plataforma)

# URL direta para a imagem da plataforma no seu repositório GitHub
FUNDO_IMAGEM_URL = "https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/plataforma.jpg"
LOGO_ZION_URL = "https://raw.githubusercontent.com/alexcostasilva2810-create/gestao-combustivel/main/ZION.JPG"

# Estilo CSS para o fundo, a logo e os elementos
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{FUNDO_IMAGEM_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .css-1jc7ptx, .css-vk32pt {{ /* Ajusta o padding do main content */
        padding-top: 5rem; /* Ajuste conforme necessário */
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 5rem;
    }}
    h1, h2, h3, p, label {{
        color: white !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        text-align: center;
        font-family: 'Arial', sans-serif; /* Fonte para o título */
    }}
    .stButton>button {{
        width: 80%; /* Botão um pouco menor na largura */
        height: 4em; /* Botão mais alto */
        background-color: #007bff; /* Azul Zion */
        color: white;
        font-size: 1.5em; /* Texto maior no botão */
        font-weight: bold;
        border-radius: 15px; /* Bordas mais arredondadas */
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        margin: auto; /* Centraliza o botão */
        display: block; /* Garante que o margin: auto funcione */
    }}
    .stButton>button:hover {{
        background-color: #0056b3; /* Azul mais escuro no hover */
    }}
    .logo-container {{
        text-align: center;
        margin-bottom: 20px;
    }}
    .logo-img {{
        width: 200px; /* Tamanho da logo na tela inicial */
        height: auto;
        border-radius: 10px; /* Pequenas bordas arredondadas na logo */
        filter: drop-shadow(0 0 10px rgba(0,0,0,0.7)); /* Sombra para destacar a logo */
        margin-top: 20px;
        margin-bottom: 20px;
    }}
    /* Estilo para os campos de entrada ficarem visíveis sobre o fundo */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
        border-radius: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- BLOCO 2: INTEGRAÇÃO COM NOTION ---
try:
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
except KeyError:
    st.error("⚠️ Erro: As chaves NOTION_TOKEN ou DATABASE_ID não foram encontradas nos Secrets do Streamlit.")
    st.stop()

def enviar_ao_notion(dados):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "EMPURRADOR": {"title": [{"text": {"content": dados['empurrador']}}]},
            "PEDIDO": {"rich_text": [{"text": {"content": dados['pedido']}}]},
            "Nº NF": {"number": dados['n_nf']},
            "QTOS LTS": {"number": dados['qtos_lts']},
            "CHAVE DA NF": {"rich_text": [{"text": {"content": dados['chave_nf']}}]},
            "REALIZADO": {"date": {"start": dados['realizado']}},
            "FORNECEDOR": {"rich_text": [{"text": {"content": dados['fornecedor']}}]},
            "CNPJ": {"rich_text": [{"text": {"content": dados['cnpj']}}]},
            "TANQUE BB": {"number": dados['tanque_bb']},
            "TANQUE BE": {"number": dados['tanque_be']},
            "ANTES": {"number": dados['antes']},
            "DEPOIS": {"number": dados['depois']}
        }
    }
    return requests.post(url, headers=headers, json=payload)

# --- BLOCO 3: INTERFACE VISUAL (TELA INICIAL E FORMULÁRIO) ---

# Controle de navegação entre as telas
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'inicial'

# --- TELA INICIAL ---
if st.session_state.pagina_atual == 'inicial':
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(LOGO_ZION_URL, caption="ZION Tecnologia", use_column_width=False, output_format="auto", width=250)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1>ZION Combustível</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Sistema de Registro</h3>", unsafe_allow_html=True)
    
    st.write("") # Espaço para o botão não ficar colado
    if st.button("INICIAR"):
        st.session_state.pagina_atual = 'formulario'
        st.experimental_rerun() # Reinicia para mostrar a tela do formulário

# --- TELA DE FORMULÁRIO ---
elif st.session_state.pagina_atual == 'formulario':
    st.title("⛽ Registro de Recebimento")
    st.markdown("Preencha os dados do abastecimento abaixo:")

    with st.form("form_combustivel", clear_on_submit=True):
        st.markdown("<h4>📝 Identificação</h4>", unsafe_allow_html=True)
        empurrador = st.text_input("EMPURRADOR")
        
        col1, col2 = st.columns(2)
        with col1:
            pedido = st.text_input("PEDIDO")
            n_nf = st.number_input("Nº NF", step=1)
            qtos_lts = st.number_input("QTOS LTS", step=0.01)
            
        with col2:
            chave_nf = st.text_input("CHAVE DA NF")
            realizado = st.date_input("DATA REALIZADO", date.today())
            fornecedor = st.text_input("FORNECEDOR")
        
        cnpj = st.text_input("CNPJ")

        st.markdown("<h4>🛢️ Medição de Tanques</h4>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            tanque_bb = st.number_input("TANQUE BB", step=0.01)
            antes = st.number_input("NÍVEL ANTES", step=0.01)
        with col4:
            tanque_be = st.number_input("TANQUE BE", step=0.01)
            depois = st.number_input("NÍVEL DEPOIS", step=0.01)

        enviar = st.form_submit_button("CONCLUIR E SALVAR REGISTRO")

        if enviar:
            if not empurrador:
                st.error("O campo EMPURRADOR é obrigatório para o registro.")
            else:
                dados_finais = {
                    "empurrador": empurrador, "pedido": pedido, "n_nf": n_nf,
                    "qtos_lts": qtos_lts, "chave_nf": chave_nf, "realizado": str(realizado),
                    "fornecedor": fornecedor, "cnpj": cnpj, "tanque_bb": tanque_bb,
                    "tanque_be": tanque_be, "antes": antes, "depois": depois
                }
                
                with st.spinner('Enviando dados para o Notion...'):
                    res = enviar_ao_notion(dados_finais)
                    
                if res.status_code == 200:
                    st.balloons()
                    st.success("✅ Sucesso! Registro salvo na sua tabela Zion.")
                    # Volta para a tela inicial após o envio
                    st.session_state.pagina_atual = 'inicial'
                    st.experimental_rerun()
                else:
                    st.error(f"❌ Erro ao enviar o registro: {res.text}")
