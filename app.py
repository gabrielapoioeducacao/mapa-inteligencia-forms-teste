import streamlit as st
import requests
import base64
import json
from datetime import datetime

# ── Configurações do GitHub (via Streamlit Secrets) ──────────────────────────
GITHUB_TOKEN  = st.secrets["github"]["token"]
GITHUB_REPO   = st.secrets["github"]["repo"]        # ex: gabrielapoioeducacao/mapa-inteligencia-formularios-teste
GITHUB_FILE   = st.secrets["github"]["file"]        # ex: dados/respostas.csv
GITHUB_BRANCH = st.secrets["github"]["branch"]      # ex: principal

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# ── Funções GitHub ────────────────────────────────────────────────────────────
def ler_csv_github():
    """Lê o CSV atual do GitHub. Retorna (conteudo_str, sha)."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}?ref={GITHUB_BRANCH}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 404:
        return None, None          # arquivo ainda não existe
    r.raise_for_status()
    dados = r.json()
    conteudo = base64.b64decode(dados["content"]).decode("utf-8")
    return conteudo, dados["sha"]

def salvar_csv_github(novo_conteudo, sha=None):
    """Cria ou atualiza o CSV no GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    payload = {
        "message": "Resposta formulário",
        "content": base64.b64encode(novo_conteudo.encode("utf-8")).decode("utf-8"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha       # obrigatório para atualizar arquivo existente
    r = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    r.raise_for_status()

def adicionar_resposta(nome, email):
    """Adiciona uma linha ao CSV no GitHub."""
    conteudo, sha = ler_csv_github()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if conteudo is None:
        # primeira vez — cria o cabeçalho
        novo = "timestamp,nome,email\n"
    else:
        novo = conteudo

    novo += f'{timestamp},"{nome}","{email}"\n'
    salvar_csv_github(novo, sha)

# ── Interface ─────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Formulário Teste", page_icon="📋")
st.title("📋 Formulário de Teste")
st.write("Preencha os campos abaixo:")

with st.form("formulario"):
    nome  = st.text_input("Nome completo")
    email = st.text_input("E-mail")
    enviar = st.form_submit_button("Enviar")

if enviar:
    if not nome or not email:
        st.warning("Por favor, preencha todos os campos.")
    else:
        try:
            adicionar_resposta(nome, email)
            st.success(f"✅ Resposta registrada com sucesso! Obrigado, {nome}!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
