import streamlit as st
import requests
import json
from datetime import datetime

# ── Configurações do Supabase ────────────────────────────────────────────────
SUPABASE_URL  = st.secrets["supabase"]["url"]
SUPABASE_KEY  = st.secrets["supabase"]["anon_key"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def salvar_supabase(dados):
    url = f"{SUPABASE_URL}/rest/v1/respostas"
    r = requests.post(url, headers=HEADERS, data=json.dumps(dados))
    if r.status_code not in (200, 201):
        raise Exception(f"Erro ao salvar: {r.status_code} - {r.text}")

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .nota-label {
        font-size: 0.9rem;
        color: #444;
        margin-bottom: 6px;
        font-weight: 500;
    }
    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        flex-wrap: wrap;
        gap: 6px;
    }
    div[data-testid="stRadio"] > div > label {
        background-color: #f0f0f0;
        border: 1.5px solid #ccc;
        border-radius: 50px !important;
        padding: 6px 14px !important;
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 600;
        color: #333;
        transition: all 0.2s;
        min-width: 42px;
        text-align: center;
    }
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #e0e8ff;
        border-color: #4a6cf7;
        color: #4a6cf7;
    }
    div[data-testid="stRadio"] label span { display: none; }
</style>
""", unsafe_allow_html=True)

def nota_radio(label, key):
    st.markdown(f'<div class="nota-label">{label}</div>', unsafe_allow_html=True)
    opcoes = [str(i) for i in range(11)]
    valor = st.radio("", opcoes, index=5, key=key, horizontal=True, label_visibility="collapsed")
    return int(valor)

# ── Interface ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mapeamento e Autoavaliação", page_icon="📋", layout="wide")
st.title("📋 Mapeamento e Autoavaliação")
st.markdown("**Psicólogos Escolares — SEE-SP**")
st.divider()

with st.form("formulario_completo"):

    # SEÇÃO 1
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
        inicio_atuacao = st.text_input("Início do Período de Atuação na UE *", placeholder="Ex: 46225")
    with col4:
        acolhimentos_por_visita = st.selectbox("Em média, quantos acolhimentos por visita? *", [
            "", "1", "2", "3", "4", "5 ou mais"
        ])
        visitas_semestre = st.selectbox("Quantidade de visitas no semestre *", [
            "", "1 a 3 visitas", "3 a 6 visitas", "6 a 10 visitas", "Mais de 10 visitas"
        ])

    st.divider()

    # SEÇÃO 2
    st.subheader("2. Autoavaliação")
    st.markdown("Selecione uma nota de **0** (nunca) a **10** (sempre):")

    q1  = nota_radio("Realizei ações voltadas ao apoio pedagógico e às necessidades de aprendizagem dos estudantes", "q1")
    q2  = nota_radio("Com que frequência realizei ações preventivas ou de mediação relacionadas às relações sociais dos estudantes?", "q2")
    q3  = nota_radio("O quanto participei das discussões sobre regras, sanções e intervenções nos conflitos?", "q3")
    q4  = nota_radio("Com que frequência identifiquei, atuei e acompanhei casos de intimidação/violência/casos sensíveis entre estudantes?", "q4")
    q5  = nota_radio("O quanto estive envolvido em ações ou contatos relacionados à participação das famílias e comunidade?", "q5")
    q6  = nota_radio("Com que frequência promovi reflexões sobre os aspectos dos espaços físicos escolares que afetam o bem-estar e a convivência?", "q6")
    q7  = nota_radio("Como avalio minha atuação colaborativa com professores, gestores e equipe escolar?", "q7")
    q8  = nota_radio("Com que frequência participei de processos coletivos (reuniões, planejamentos, ATPC) ligados à gestão escolar?", "q8")
    q9  = nota_radio("O psicólogo escolar é acolhido dentro da escola?", "q9")
    q10 = nota_radio("O trabalho do psicólogo escolar é percebido como algo relevante para a escola e sua comunidade?", "q10")
    q11 = nota_radio("A escola encaminha as situações necessárias à rede protetiva?", "q11")
    q12 = nota_radio("A escola realiza ações compartilhadas com a rede protetiva?", "q12")
    q13 = nota_radio("Como avalio minha atuação colaborativa com a unidade regional de ensino (PEC, Supervisor)?", "q13")

    st.divider()

    # SEÇÃO 3
    st.subheader("3. Reflexões sobre a Atuação")
    reflexoes_efeitos = st.text_area("As reflexões e efeitos das minhas ações nessa escola foram: *", height=120)
    desafios = st.text_area("Os desafios que encontro nessa escola são: *", height=120)
    ponto_apoio = st.text_area("Um ponto de apoio que ajudaria minha prática seria: *", height=100)
    pontos_semestre = st.text_area("Pontos importantes para serem trabalhados nesse semestre nesta escola: *", height=120)
    boa_pratica = st.text_area("Uma boa prática que realizei em parceria com a escola: *", height=120)
    sugestao = st.text_area("Alguma sugestão? (opcional)", height=80)

    st.divider()

    # SEÇÃO 4
    st.subheader("4. Mapeamento da Escola")
    col5, col6 = st.columns(2)
    with col5:
        numero_estudantes = st.text_input("Número de Estudantes *")
        etapas_ensino = st.multiselect("Etapas de Ensino *", [
            "ANOS INICIAIS", "ANOS FINAIS", "ENSINO MÉDIO", "EJA", "EJA TEC"
        ])
    with col6:
        realidade_geografica = st.text_area("Qual a realidade geográfica dessa escola? *", height=100)

    fatores_risco = st.text_area("Quais são os fatores de risco que você identifica nessa unidade escolar? *", height=120)
    fatores_protecao = st.text_area("Quais são os fatores de proteção que você identifica nessa unidade escolar? *", height=120)
    descricao_fenomenos = st.text_area("Descrição, análise e qualificação dos fenômenos observados *", height=150)

    st.divider()

    # SEÇÃO 5
    st.subheader("5. Planejamento de Atuação")
    questoes_importantes = st.text_area("Questões que acredita serem importantes para atuação nessa escola *", height=120)
    relacoes_estabelecer = st.text_area("Relações de dentro da escola que precisam ser estabelecidas *", height=100)
    rede_protetiva = st.text_area("Aponte equipamentos da rede protetiva / parceiros no território da escola *", height=100)
    objetivos_semestre = st.text_area("Objetivos para atuação no semestre (até 3 objetivos) *", height=120)
    impactos_esperados = st.text_area("Impacto esperado com os objetivos *", height=120)

    st.divider()

    # SEÇÃO 6
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

    # SEÇÃO 7
    st.subheader("7. Encaminhamento")
    st.info("Este documento serve como base para o planejamento das ações do semestre, articulação com a rede protetiva e acompanhamento pelo PEC e Supervisor.")
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
            "email": email, "nome_psicologo": nome_psicologo, "crp": crp, "cpf": cpf,
            "data_relatorio": data_relatorio, "fundamentacao_teorica": fundamentacao_teorica,
            "unidade_escolar": unidade_escolar, "unidade_regional": unidade_regional,
            "grupo": grupo, "inicio_atuacao": inicio_atuacao,
            "acolhimentos_por_visita": acolhimentos_por_visita, "visitas_semestre": visitas_semestre,
            "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7,
            "q8": q8, "q9": q9, "q10": q10, "q11": q11, "q12": q12, "q13": q13,
            "reflexoes_efeitos": reflexoes_efeitos, "desafios": desafios,
            "ponto_apoio": ponto_apoio, "pontos_semestre": pontos_semestre,
            "boa_pratica": boa_pratica, "sugestao": sugestao,
            "numero_estudantes": numero_estudantes, "etapas_ensino": ", ".join(etapas_ensino),
            "realidade_geografica": realidade_geografica, "fatores_risco": fatores_risco,
            "fatores_protecao": fatores_protecao, "descricao_fenomenos": descricao_fenomenos,
            "questoes_importantes": questoes_importantes, "relacoes_estabelecer": relacoes_estabelecer,
            "rede_protetiva": rede_protetiva, "objetivos_semestre": objetivos_semestre,
            "impactos_esperados": impactos_esperados,
            "possibilidades_acoes": ", ".join(possibilidades_acoes),
            "titulos_acoes": titulos_acoes, "publico_alvo": publico_alvo,
            "materiais_necessarios": materiais_necessarios, "descricao_acoes": descricao_acoes,
            "metodologia": metodologia,
            "encaminhamento": "Li e estou ciente desses encaminhamentos."
        }
        try:
            salvar_supabase(dados)
            st.success(f"✅ Formulário enviado com sucesso! Obrigado, {nome_psicologo}!")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
