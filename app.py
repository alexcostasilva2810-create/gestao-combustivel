import streamlit as st
import requests
from datetime import date

# Configuração da Página para Ícone no Celular
st.set_page_config(page_title="Gestão Zion", page_icon="⛽")

# Chaves de Conexão (Pegaremos no passo 3)
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
DATABASE_ID = st.secrets["DATABASE_ID"]

def enviar_notion(dados):
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
            "QTOS LTS": {"number": dados['lts']},
            "CHAVE DA NF": {"rich_text": [{"text": {"content": dados['chave']}}]},
            "REALIZADO": {"date": {"start": dados['data']}},
            "FORNECEDOR": {"rich_text": [{"text": {"content": dados['fornecedor']}}]},
            "CNPJ": {"rich_text": [{"text": {"content": dados['cnpj']}}]},
            "TANQUE BB": {"number": dados['t_bb']},
            "TANQUE BE": {"number": dados['t_be']},
            "ANTES": {"number": dados['antes']},
            "DEPOIS": {"number": dados['depois']}
        }
    }
    return requests.post(url, headers=headers, json=payload)

st.title("⛽ Registro de Abastecimento")

with st.form("form_abastecimento"):
    empurrador = st.text_input("EMPURRADOR")
    col1, col2 = st.columns(2)
    with col1:
        pedido = st.text_input("PEDIDO")
        n_nf = st.number_input("Nº NF", step=1)
        lts = st.number_input("QTOS LTS", step=0.01)
    with col2:
        chave = st.text_input("CHAVE DA NF")
        data_f = st.date_input("REALIZADO", date.today())
        fornecedor = st.text_input("FORNECEDOR")
    
    cnpj = st.text_input("CNPJ")
    
    col3, col4 = st.columns(2)
    with col3:
        t_bb = st.number_input("TANQUE BB", step=0.01)
        antes = st.number_input("ANTES", step=0.01)
    with col4:
        t_be = st.number_input("TANQUE BE", step=0.01)
        depois = st.number_input("DEPOIS", step=0.01)

    if st.form_submit_button("SALVAR NO NOTION"):
        dados = {
            "empurrador": empurrador, "pedido": pedido, "n_nf": n_nf,
            "lts": lts, "chave": chave, "data": str(data_f),
            "fornecedor": fornecedor, "cnpj": cnpj, "t_bb": t_bb,
            "t_be": t_be, "antes": antes, "depois": depois
        }
        res = enviar_notion(dados)
        if res.status_code == 200:
            st.success("Enviado com sucesso!")
        else:
            st.error(f"Erro: {res.text}")
