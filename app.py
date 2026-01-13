# ==========================================
# BLOCO 1: CONFIGURAÇÃO E SEGURANÇA
# ==========================================
import streamlit as st
import requests
from datetime import date

# Configuração da Interface (Define o ícone e título no navegador do celular)
st.set_page_config(
    page_title="Zion Combustível", 
    page_icon="⛽", 
    layout="centered"
)

# Puxando as chaves de segurança configuradas nos Secrets
try:
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
    DATABASE_ID = st.secrets["DATABASE_ID"]
except KeyError:
    st.error("⚠️ Erro: As chaves NOTION_TOKEN ou DATABASE_ID não foram encontradas nos Secrets.")
    st.stop()

# ==========================================
# BLOCO 2: FUNÇÃO DE COMUNICAÇÃO COM O NOTION
# ==========================================
def enviar_ao_notion(dados):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Payload montado conforme as colunas da sua imagem
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

# ==========================================
# BLOCO 3: INTERFACE VISUAL (FORMULÁRIO)
# ==========================================
st.title("⛽ Recebimento Zion")
st.write("Preencha os dados do abastecimento abaixo:")

with st.form("form_combustivel", clear_on_submit=True):
    # Campos de Identificação
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

    # Campos de Medição
    col3, col4 = st.columns(2)
    with col3:
        tanque_bb = st.number_input("TANQUE BB", step=0.01)
        antes = st.number_input("NÍVEL ANTES", step=0.01)
    with col4:
        tanque_be = st.number_input("TANQUE BE", step=0.01)
        depois = st.number_input("NÍVEL DEPOIS", step=0.01)

    # Botão de Envio
    enviar = st.form_submit_button("CONCLUIR E SALVAR")

    if enviar:
        if not empurrador:
            st.warning("O campo EMPURRADOR é obrigatório.")
        else:
            dados_finais = {
                "empurrador": empurrador, "pedido": pedido, "n_nf": n_nf,
                "qtos_lts": qtos_lts, "chave_nf": chave_nf, "realizado": str(realizado),
                "fornecedor": fornecedor, "cnpj": cnpj, "tanque_bb": tanque_bb,
                "tanque_be": tanque_be, "antes": antes, "depois": depois
            }
            
            with st.spinner('Enviando para o Notion...'):
                res = enviar_ao_notion(dados_finais)
                
            if res.status_code == 200:
                st.balloons()
                st.success("✅ Sucesso! Dados registrados na tabela Zion.")
            else:
                st.error(f"❌ Erro na integração: {res.text}")
