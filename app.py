import streamlit as st
import requests
import base64
import json
from datetime import datetime

# ── Configurações do GitHub ──────────────────────────────────────────────────
GITHUB_TOKEN  = st.secrets["github"]["token"]
GITHUB_REPO   = st.secrets["github"]["repo"]
GITHUB_FILE   = st.secrets["github"]["file"]
GITHUB_BRANCH = st.secrets["github"]["branch"]

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

COLUNAS = [
    "timestamp","email","nome_psicologo","crp","cpf","data_relatorio",
    "fundamentacao_teorica","unidade_escolar","unidade_regional","grupo",
    "inicio_atuacao","acolhimentos_por_visita","visitas_semestre",
    "q1_apoio_pedagogico","q2_acoes_preventivas","q3_regras_conflitos",
    "q4_intimidacao_violencia","q5_familias_comunidade","q6_espacos_fisicos",
    "q7_colaboracao_equipe","q8_processos_coletivos","q9_acolhimento_psicologo",
    "q10_relevancia_trabalho","q11_encaminhamentos_rede","q12_acoes_rede",
    "q13_colaboracao_regional",
    "reflexoes_efeitos","desafios","ponto_apoio","pontos_semestre",
    "boa_pratica","sugestao","numero_estudantes","etapas_ensino",
    "realidade_geografica","fatores_risco","fatores_protecao",
    "descricao_fenomenos","questoes_importantes","relacoes_estabelecer",
    "rede_protetiva","objetivos_semestre","impactos_esperados",
    "possibilidades_acoes","titulos_acoes","publico_alvo",
    "materiais_necessarios","descricao_acoes","metodologia","encaminhamento"
]

def ler_csv_github():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}?ref={GITHUB_BRANCH}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 404:
        return None, None
    r.raise_for_status()
    dados = r.json()
    conteudo = base64.b64decode(dados["content"]).decode("utf-8")
    return conteudo, dados["sha"]

def escapar(valor):
    return str(valor).replace('"', '""').replace('\n', ' ').replace('\r', '')

def salvar_csv_github(novo_conteudo, sha=None):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"
    payload = {
        "message": "Nova resposta - Mapeamento e Autoavaliação",
        "content": base64.b64encode(novo_conteudo.encode("utf-8")).decode("utf-8"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    r.raise_for_status()

def adicionar_resposta(dados):
    conteudo, sha = ler_csv_github()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if conteudo is None:
        novo = ",".join(COLUNAS) + "\n"
    else:
        novo = conteudo

    linha = f'"{timestamp}"'
    for campo in COLUNAS[1:]:
        linha += f',"{escapar(dados.get(campo, ""))}"'
    linha += "\n"

    novo += linha
    salvar_csv_github(novo, sha)

# ── Interface ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mapeamento e Autoavaliação", page_icon="📋", layout="wide")

st.title("📋 Mapeamento e Autoavaliação")
st.markdown("**Psicólogos Escolares — SEE-SP**")
st.divider()

with st.form("formulario_completo"):

    # SEÇÃO 1 - IDENTIFICAÇÃO
    st.subheader("1. Identificação")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("E-mail *")
        nome_psicologo = st.text_input("Nome do Psicólogo *")
        crp = st.text_input("CRP *")
        cpf = st.text_input("CPF *")
    with col2:
        data_relatorio = st.text_input("Data do Relatório *", placeholder="DD/MM/AAAA")
        fundamentacao_teorica = st.text_area("Fundamentação Teórica *", height=100)
        unidade_escolar = st.text_input("Unidade Escolar *", placeholder="Ex: E.E. NOME DA ESCOLA")
        unidade_regional = st.selectbox("Unidade Regional de Ensino *", [
            "", "D.E.REG. NORTE 1", "D.E.REG. NORTE 2", "D.E.REG. LESTE 1", "D.E.REG. LESTE 2",
            "D.E.REG. LESTE 3", "D.E.REG. LESTE 4", "D.E.REG. LESTE 5", "D.E.REG. SUL 1",
            "D.E.REG. SUL 2", "D.E.REG. SUL 3", "D.E.REG. CENTRO-OESTE", "D.E.REG. GUARULHOS NORTE",
            "D.E.REG. GUARULHOS SUL", "D.E.REG. MAUA", "D.E.REG. OSASCO", "D.E.REG. JUNDIAI",
            "D.E.REG. BRAGANCA PAULISTA", "D.E.REG. OURINHOS", "D.E.REG. ADAMANTINA",
            "D.E.REG. MARILIA", "D.E.REG. SAO JOSE DO RIO PRETO", "D.E.REG. MOGI DAS CRUZES"
        ])

    col3, col4 = st.columns(2)
    with col3:
        grupo = st.selectbox("Grupo *", ["", "Grupo 01", "Grupo 02", "Grupo 03", "Grupo 04"])
        inicio_atuacao = st.text_input("Início do Período de Atuação na UE *", placeholder="Número de dias ou data")
    with col4:
        acolhimentos_por_visita = st.selectbox("Em média, quantos acolhimentos por visita? *", [
            "", "1", "2", "3", "4", "5 ou mais"
        ])
        visitas_semestre = st.selectbox("Quantidade de visitas no semestre *", [
            "", "1 a 3 visitas", "3 a 6 visitas", "6 a 10 visitas", "Mais de 10 visitas"
        ])

    st.divider()

    # SEÇÃO 2 - AUTOAVALIAÇÃO (0-10)
    st.subheader("2. Autoavaliação (0 = nunca / 10 = sempre)")
    st.markdown("Avalie cada item de **0 a 10**:")

    col_a, col_b = st.columns(2)
    with col_a:
        q1 = st.slider("Realizei ações voltadas ao apoio pedagógico e às necessidades de aprendizagem dos estudantes", 0, 10, 5)
        q2 = st.slider("Com que frequência realizei ações preventivas ou de mediação relacionadas às relações sociais?", 0, 10, 5)
        q3 = st.slider("O quanto participei das discussões sobre regras, sanções e intervenções nos conflitos?", 0, 10, 5)
        q4 = st.slider("Com que frequência identifiquei, atuei e acompanhei casos de intimidação/violência?", 0, 10, 5)
        q5 = st.slider("O quanto estive envolvido em ações relacionadas à participação das famílias e comunidade?", 0, 10, 5)
        q6 = st.slider("Com que frequência promovi reflexões sobre os espaços físicos e seu impacto no bem-estar?", 0, 10, 5)
        q7 = st.slider("Como avalio minha atuação colaborativa com professores, gestores e equipe escolar?", 0, 10, 5)
    with col_b:
        q8  = st.slider("Com que frequência participei de processos coletivos (reuniões, ATPC, planejamentos)?", 0, 10, 5)
        q9  = st.slider("O psicólogo escolar é acolhido dentro da escola?", 0, 10, 5)
        q10 = st.slider("O trabalho do psicólogo é percebido como relevante para a escola e comunidade?", 0, 10, 5)
        q11 = st.slider("A escola encaminha as situações necessárias à rede protetiva?", 0, 10, 5)
        q12 = st.slider("A escola realiza ações compartilhadas com a rede protetiva?", 0, 10, 5)
        q13 = st.slider("Como avalio minha atuação colaborativa com a unidade regional (PEC, Supervisor)?", 0, 10, 5)

    st.divider()

    # SEÇÃO 3 - REFLEXÕES
    st.subheader("3. Reflexões sobre a Atuação")
    reflexoes_efeitos = st.text_area("As reflexões e efeitos das minhas ações nessa escola foram: *", height=120)
    desafios = st.text_area("Os desafios que encontro nessa escola são: *", height=120)
    ponto_apoio = st.text_area("Um ponto de apoio que ajudaria minha prática seria: *", height=100)
    pontos_semestre = st.text_area("Pontos importantes para serem trabalhados nesse semestre: *", height=120)
    boa_pratica = st.text_area("Uma boa prática que realizei em parceria com a escola: *", height=120)
    sugestao = st.text_area("Alguma sugestão? (opcional)", height=80)

    st.divider()

    # SEÇÃO 4 - MAPEAMENTO DA ESCOLA
    st.subheader("4. Mapeamento da Escola")
    col5, col6 = st.columns(2)
    with col5:
        numero_estudantes = st.text_input("Número de Estudantes *")
        etapas_ensino = st.multiselect("Etapas de Ensino *", [
            "ANOS INICIAIS", "ANOS FINAIS", "ENSINO MÉDIO", "EJA", "EJA TEC"
        ])
    with col6:
        realidade_geografica = st.text_area("Qual a realidade geográfica dessa escola? *", height=100)

    fatores_risco = st.text_area("Fatores de risco identificados na unidade escolar *", height=120)
    fatores_protecao = st.text_area("Fatores de proteção identificados na unidade escolar *", height=120)
    descricao_fenomenos = st.text_area("Descrição, análise e qualificação dos fenômenos observados *", height=150)

    st.divider()

    # SEÇÃO 5 - PLANEJAMENTO
    st.subheader("5. Planejamento de Atuação")
    questoes_importantes = st.text_area("Questões importantes para atuação nessa escola *", height=120)
    relacoes_estabelecer = st.text_area("Relações dentro da escola que precisam ser estabelecidas *", height=100)
    rede_protetiva = st.text_area("Equipamentos da rede protetiva / parceiros no território *", height=100)
    objetivos_semestre = st.text_area("Objetivos para atuação no semestre (até 3 objetivos) *", height=120)
    impactos_esperados = st.text_area("Impactos esperados com os objetivos *", height=120)

    st.divider()

    # SEÇÃO 6 - AÇÕES
    st.subheader("6. Ações")
    possibilidades_acoes = st.multiselect("Possibilidades de Ações *", [
        "Apoio ao processo de ensino-aprendizagem",
        "Relações e Convivência escolar",
        "Desenvolvimento e formação",
        "Avaliação e encaminhamento"
    ])
    titulos_acoes = st.text_area("Títulos das Ações (numere cada ação) *", height=100)
    publico_alvo = st.text_area("Público-alvo (numere de acordo com a ação) *", height=100)
    materiais_necessarios = st.text_area("Materiais necessários (numere para cada ação) *", height=100)
    descricao_acoes = st.text_area("Descrição das Ações (numere para cada ação) *", height=150)
    metodologia = st.text_area("Qual metodologia sustenta cada ação? (numere para cada ação) *", height=150)

    st.divider()

    # TERMO
    st.subheader("7. Encaminhamento")
    encaminhamento = st.checkbox("Li e estou ciente desses encaminhamentos. *")

    st.divider()
    enviar = st.form_submit_button("📤 Enviar Formulário", use_container_width=True)

if enviar:
    erros = []
    if not email: erros.append("E-mail")
    if not nome_psicologo: erros.append("Nome do Psicólogo")
    if not crp: erros.append("CRP")
    if not cpf: erros.append("CPF")
    if not data_relatorio: erros.append("Data do Relatório")
    if not unidade_escolar: erros.append("Unidade Escolar")
    if not unidade_regional: erros.append("Unidade Regional")
    if not grupo: erros.append("Grupo")
    if not encaminhamento: erros.append("Confirmação de encaminhamento")

    if erros:
        st.error(f"Por favor, preencha os campos obrigatórios: {', '.join(erros)}")
    else:
        dados = {
            "email": email,
            "nome_psicologo": nome_psicologo,
            "crp": crp,
            "cpf": cpf,
            "data_relatorio": data_relatorio,
            "fundamentacao_teorica": fundamentacao_teorica,
            "unidade_escolar": unidade_escolar,
            "unidade_regional": unidade_regional,
            "grupo": grupo,
            "inicio_atuacao": inicio_atuacao,
            "acolhimentos_por_visita": acolhimentos_por_visita,
            "visitas_semestre": visitas_semestre,
            "q1_apoio_pedagogico": q1,
            "q2_acoes_preventivas": q2,
            "q3_regras_conflitos": q3,
            "q4_intimidacao_violencia": q4,
            "q5_familias_comunidade": q5,
            "q6_espacos_fisicos": q6,
            "q7_colaboracao_equipe": q7,
            "q8_processos_coletivos": q8,
            "q9_acolhimento_psicologo": q9,
            "q10_relevancia_trabalho": q10,
            "q11_encaminhamentos_rede": q11,
            "q12_acoes_rede": q12,
            "q13_colaboracao_regional": q13,
            "reflexoes_efeitos": reflexoes_efeitos,
            "desafios": desafios,
            "ponto_apoio": ponto_apoio,
            "pontos_semestre": pontos_semestre,
            "boa_pratica": boa_pratica,
            "sugestao": sugestao,
            "numero_estudantes": numero_estudantes,
            "etapas_ensino": ", ".join(etapas_ensino),
            "realidade_geografica": realidade_geografica,
            "fatores_risco": fatores_risco,
            "fatores_protecao": fatores_protecao,
            "descricao_fenomenos": descricao_fenomenos,
            "questoes_importantes": questoes_importantes,
            "relacoes_estabelecer": relacoes_estabelecer,
            "rede_protetiva": rede_protetiva,
            "objetivos_semestre": objetivos_semestre,
            "impactos_esperados": impactos_esperados,
            "possibilidades_acoes": ", ".join(possibilidades_acoes),
            "titulos_acoes": titulos_acoes,
            "publico_alvo": publico_alvo,
            "materiais_necessarios": materiais_necessarios,
            "descricao_acoes": descricao_acoes,
            "metodologia": metodologia,
            "encaminhamento": "Li e estou ciente desses encaminhamentos."
        }
        try:
            adicionar_resposta(dados)
            st.success(f"✅ Formulário enviado com sucesso! Obrigado, {nome_psicologo}!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
