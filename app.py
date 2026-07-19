import streamlit as st
import gspread

# --- CONFIGURAÇÃO ---
# URL da sua planilha
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1YtwnZoiHf1bWgqj574zuOKqc5HybPkfJbxTxO5o1iCk/edit"

def conectar_planilha():
    # Carrega credenciais do Secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
    # Abre a planilha pelo link
    sh = gc.open_by_url(URL_PLANILHA)
    return sh.sheet1

# --- INTERFACE ---
st.set_page_config(page_title="Roteirizador J&T", layout="wide")
st.title("🚚 Roteirizador J&T Express - SILVIO")

try:
    aba = conectar_planilha()
    st.success("Conectado à planilha com sucesso!")
    
    # Exemplo simples de uso: ler a primeira linha como cabeçalho
    # dados = aba.get_all_values()
    # st.write(f"Planilha carregada com {len(dados)} linhas.")
    
    ceps_input = st.text_area("Insira os CEPs (um por linha):")
    
    if st.button("Processar"):
        if ceps_input:
            st.info("Processando...")
            # Aqui você adiciona a lógica de busca na planilha
        else:
            st.warning("Por favor, insira os CEPs.")

except Exception as e:
    st.error(f"Erro ao conectar: {e}")
    st.write("Verifique se o e-mail 'silvio-robot...' é editor na planilha.")
