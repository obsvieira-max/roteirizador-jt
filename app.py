import streamlit as st
import pandas as pd
import requests
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor

# Configuração da página
st.set_page_config(page_title="Roteirizador J&T - SILVIO", page_icon="🚚", layout="wide")

# --- CONEXÃO COM PLANILHA (Detecta se está no PC ou na Nuvem) ---
try:
    if "gcp_service_account" in st.secrets:
        # Modo Nuvem (Streamlit Cloud)
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, 
                ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    else:
        # Modo Local (Seu PC)
        creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', 
                ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    
    client = gspread.authorize(creds)
    sheet = client.open('Base_CEPs_Silvio').sheet1
except Exception as e:
    st.error(f"Erro ao conectar na planilha: {e}")

def buscar_cep_inteligente(cep):
    try:
        cell = sheet.find(cep)
        if cell:
            row = sheet.row_values(cell.row)
            return {"cep": row[0], "logradouro": row[1], "bairro": row[2], "localidade": row[3], "uf": row[4]}
    except: pass
    
    try:
        resp = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=3)
        res = resp.json()
        if 'erro' not in res:
            nova_linha = [cep, res.get('logradouro'), res.get('bairro'), res.get('localidade'), res.get('uf')]
            sheet.append_row(nova_linha)
            return res
    except: pass
    return None

# --- INTERFACE ---
st.title("🚚 Roteirizador J&T Express - Desenvolvido por SILVIO")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Pesquisa Avulsa", "🔍 Consulta por Faixa"])

with tab1:
    ceps_input = st.text_area("Insira os CEPs (um por linha):", height=150)
    if st.button("🚀 Processar"):
        resultados = []
        for c in ceps_input.split('\n'):
            cep = c.strip().replace("-", "").replace(".", "")
            if len(cep) == 8:
                res = buscar_cep_inteligente(cep)
                if res:
                    resultados.append({"CEP": cep, "Rua": res.get('logradouro'), "Bairro": res.get('bairro'), "Cidade": res.get('localidade')})
        if resultados:
            st.table(pd.DataFrame(resultados))

with tab2:
    intervalo_input = st.text_input("Insira o intervalo (Ex: 74000000 74000999):")
    if st.button("🔍 Consultar Faixa"):
        try:
            inicio, fim = intervalo_input.split()
            i, f = int(inicio), int(fim)
            ceps_lista = [str(num).zfill(8) for num in range(i, f + 1)]
            with st.spinner("Consultando e salvando na planilha..."):
                with ThreadPoolExecutor(max_workers=5) as executor:
                    executor.map(buscar_cep_inteligente, ceps_lista)
            st.success("Consulta finalizada!")
        except: st.error("Formato inválido. Use: 74000000 74000999")