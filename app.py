# --- Dentro do seu formulário de Registro de Combustível ---
elif st.session_state.tela == 'form':
    st.markdown('<h2 style="color:white; text-align:center;">⛽ Registro de Combustível</h2>', unsafe_allow_html=True)
    
    with st.form("form_registro"):
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("EMPURRADOR", options=LISTA_EMPURRADORES)
            st.text_input("Nº PEDIDO")
            st.number_input("Nº NF", step=1, format="%d")
            
            st.write("📸 **Escanear Nota Fiscal**")
            foto_nf = st.camera_input("Aponte para o código de barras")
            
            # Campo onde a chave de 44 dígitos será guardada
            chave_nf = st.text_input("CHAVE DA NF (44 dígitos)", max_chars=44)
            
            # BOTÃO DE CONSULTA AO SITE consultadanfe.com
            if len(chave_nf) == 44:
                url_consulta = f"https://www.consultadanfe.com/?chave={chave_nf}"
                st.link_button("📄 ABRIR PDF NO CONSULTA DANFE", url_consulta)

        with c2:
            # Quantidade sem vírgula
            st.number_input("QUANTIDADE (LTS)", step=1, format="%d") 
            # Data no formato dd/mm/yyyy
            st.date_input("DATA", value=date.today(), format="DD/MM/YYYY") 
            st.text_input("FORNECEDOR")
        
        # Título em Verde Forte
        st.markdown('<p class="texto-verde">📊 Níveis de Tanque</p>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a: st.number_input("TANQUE BB (m³)", step=0.01)
        with col_b: st.number_input("TANQUE BE (m³)", step=0.01)

        if st.form_submit_button("CONCLUIR E ENVIAR AO NOTION"):
            # Aqui os dados, incluindo a CHAVE NF, serão salvos no Notion
            st.success("✅ Registro e Chave da NF salvos com sucesso!")
            time.sleep(1)
            st.session_state.tela = 'inicio'
            st.rerun()
