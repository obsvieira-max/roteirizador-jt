import streamlit as st
import gspread

# --- CONFIGURAÇÃO DA PLANILHA ---
# Substitua pelo link real da sua planilha no Google Sheets
URL_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

def conectar_planilha():
    # Carrega as credenciais que configuramos no Secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
    # Abre a planilha pelo link
    sh = gc.open_by_url(URL_PLANILHA)
    return sh.sheet1

# --- INTERFACE ---
st.title("🚚 Roteirizador J&T Express - SILVIO")

try:
    aba = conectar_planilha()
    st.success("Conectado à planilha com sucesso!")
    
    # Campo para entrada de dados
    ceps_input = st.text_area("Insira os CEPs (um por linha):")
    
    if st.button("Processar"):
        if ceps_input:
            st.write("Processando os dados...")
            # Aqui entrará a lógica do seu roteirizador
            st.write(f"Você inseriu os seguintes CEPs: {ceps_input.splitlines()}")
        else:
            st.warning("Por favor, insira pelo menos um CEP.")

except Exception as e:
    st.error(f"Erro ao conectar na planilha: {e}")
