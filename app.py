import streamlit as st
from supabase import create_client
from datetime import datetime

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Avaliação de Desempenho — Programa Psicólogos nas Escolas",
    page_icon="🏫",
    layout="centered",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fonte e base */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Cabeçalho principal */
    .header-block {
        background: linear-gradient(135deg, #1a3a5c 0%, #2563a8 100%);
        color: white;
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .header-block h1 {
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        color: white;
    }
    .header-block p {
        font-size: 0.9rem;
        opacity: 0.85;
        margin: 0;
        color: white;
    }

    /* Bloco de seção */
    .secao-titulo {
        background: #f0f4fb;
        border-left: 4px solid #2563a8;
        padding: 0.7rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        font-size: 1rem;
        color: #1a3a5c;
    }

    /* Comportamento observável */
    .comportamento {
        background: #f8f9fb;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #374151;
    }

    /* Aviso */
    .aviso {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #9a3412;
        margin: 0.5rem 0 1.5rem 0;
    }

    /* Rodapé */
    .rodape {
        text-align: center;
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ── Conexão Supabase ─────────────────────────────────────────────────────────
@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)

supabase = init_supabase()

# ── Constantes ───────────────────────────────────────────────────────────────
URES = [
    "Selecione a URE",
    "URE 01 - Capital",
    "URE 02 - Santo André",
    "URE 03 - Mauá",
    "URE 04 - São Bernardo do Campo",
    "URE 05 - Diadema",
    "URE 06 - Ribeirão Pires",
    "URE 07 - Guarulhos Norte",
    "URE 08 - Guarulhos Sul",
    "URE 09 - Mogi das Cruzes",
    "URE 10 - Suzano",
    "URE 11 - Itaquaquecetuba",
    "URE 12 - Franco da Rocha",
    "URE 13 - Osasco",
    "URE 14 - Carapicuíba",
    "URE 15 - Taboão da Serra",
    "URE 16 - Cotia",
    "URE 17 - Itapevi",
    "URE 18 - Barueri",
    "URE 19 - Santana de Parnaíba",
    "URE 20 - Jandira",
    "URE 21 - Itapecerica da Serra",
    "URE 22 - Embu das Artes",
    "URE 23 - São Lourenço da Serra",
    "URE 24 - Campinas Leste",
    "URE 25 - Campinas Oeste",
    "URE 26 - Campinas Norte",
    "URE 27 - Campinas Sul",
    "URE 28 - Americana",
    "URE 29 - Sumaré",
    "URE 30 - Hortolândia",
    "URE 31 - Indaiatuba",
    "URE 32 - Jundiaí",
    "URE 33 - Atibaia",
    "URE 34 - Bragança Paulista",
    "URE 35 - Piracicaba",
    "URE 36 - Limeira",
    "URE 37 - Rio Claro",
    "URE 38 - São Carlos",
    "URE 39 - Araraquara",
    "URE 40 - Ribeirão Preto Norte",
    "URE 41 - Ribeirão Preto Sul",
    "URE 42 - Franca",
    "URE 43 - Barretos",
    "URE 44 - Sertãozinho",
    "URE 45 - Jaboticabal",
    "URE 46 - São José do Rio Preto",
    "URE 47 - Catanduva",
    "URE 48 - Votuporanga",
    "URE 49 - Fernandópolis",
    "URE 50 - Araçatuba",
    "URE 51 - Birigui",
    "URE 52 - Lins",
    "URE 53 - Marília",
    "URE 54 - Tupã",
    "URE 55 - Presidente Prudente",
    "URE 56 - Adamantina",
    "URE 57 - Ourinhos",
    "URE 58 - Assis",
    "URE 59 - Avaré",
    "URE 60 - Itapetininga",
    "URE 61 - Sorocaba Norte",
    "URE 62 - Sorocaba Sul",
    "URE 63 - Botucatu",
    "URE 64 - Bauru",
    "URE 65 - Jaú",
    "URE 66 - São José dos Campos",
    "URE 67 - Jacareí",
    "URE 68 - Taubaté",
    "URE 69 - Pindamonhangaba",
    "URE 70 - Guaratinguetá",
    "URE 71 - Lorena",
    "URE 72 - Cruzeiro",
    "URE 73 - Caraguatatuba",
    "URE 74 - Ubatuba",
    "URE 75 - São Sebastião",
    "URE 76 - Santos",
    "URE 77 - Cubatão",
    "URE 78 - São Vicente",
    "URE 79 - Praia Grande",
    "URE 80 - Itanhaém",
    "URE 81 - Registro",
    "URE 82 - Itapeva",
    "URE 83 - Itararé",
    "URE 84 - Sorocaba Leste",
    "URE 85 - Votorantim",
    "URE 86 - Pilar do Sul",
    "URE 87 - São Roque",
    "URE 88 - Itatiba",
    "URE 89 - Valinhos",
    "URE 90 - Paulínia",
    "URE 91 - Pedreira",
]

PERIODOS = [
    "Selecione o período",
    "2025 — 1º Semestre",
    "2025 — 2º Semestre",
    "2026 — 1º Semestre",
    "2026 — 2º Semestre",
]

ESCALA = {
    "1 — Raramente observado": 1,
    "2 — Observado ocasionalmente, de forma inconsistente": 2,
    "3 — Observado adequadamente na maioria das situações": 3,
    "4 — Observado de forma consistente e contribui positivamente": 4,
    "5 — Observado como referência, fortalece continuamente a equipe": 5,
}

COMPETENCIAS = {
    "escuta": {
        "titulo": "Competência 1 — Escuta",
        "definicao": "Capacidade de compreender contextos, acolher diferentes perspectivas, estabelecer diálogo qualificado e considerar informações relevantes antes da definição de encaminhamentos.",
        "itens": [
            ("escuta_1", "1.1 Comunicação e disponibilidade para escuta",
             "O Líder comunica orientações de forma clara e demonstra disponibilidade para ouvir dúvidas, necessidades, sugestões e diferentes perspectivas relacionadas ao trabalho."),
            ("escuta_2", "1.2 Escuta e mediação",
             "O Líder escuta as diferentes partes envolvidas e atua na mediação de desafios, divergências e conflitos com equilíbrio, respeito e imparcialidade."),
            ("escuta_3", "1.3 Acolhimento e construção de relações colaborativas",
             "O Líder acolhe demandas e desafios apresentados pelos diferentes atores e contribui para a construção de relações de trabalho seguras, respeitosas e colaborativas."),
        ],
    },
    "praxis": {
        "titulo": "Competência 2 — Práxis",
        "definicao": "Capacidade de articular conhecimento, informações e experiência prática para planejar a atuação, tomar decisões qualificadas e refletir sobre as necessidades e desafios do território.",
        "itens": [
            ("praxis_1", "2.1 Planejamento e organização",
             "O Líder organiza o trabalho com clareza, estabelece prioridades, estrutura rotinas e acompanha a execução das ações de acordo com as necessidades do território."),
            ("praxis_2", "2.2 Uso de informações para a tomada de decisão",
             "O Líder utiliza registros, dados, relatos e outras informações disponíveis para compreender situações, orientar decisões e qualificar o planejamento das ações."),
            ("praxis_3", "2.3 Qualificação da atuação",
             "O Líder orienta e acompanha a atuação da equipe de forma coerente com as diretrizes do Programa, favorecendo intervenções contextualizadas, preventivas, coletivas e institucionalmente qualificadas."),
        ],
    },
    "multiplicacao": {
        "titulo": "Competência 3 — Multiplicação",
        "definicao": "Capacidade de compartilhar conhecimentos, promover aprendizagem, desenvolver pessoas e equipes e ampliar a autonomia dos atores envolvidos no trabalho.",
        "itens": [
            ("multiplicacao_1", "3.1 Desenvolvimento e feedback",
             "O Líder oferece orientações, acompanhamento e feedbacks que contribuem para o desenvolvimento profissional e o aprimoramento da atuação da equipe."),
            ("multiplicacao_2", "3.2 Aprendizagem e troca de conhecimentos",
             "O Líder promove ou viabiliza espaços de estudo, reflexão, análise de situações e troca de experiências que favorecem a aprendizagem coletiva."),
            ("multiplicacao_3", "3.3 Articulação e fortalecimento da autonomia",
             "O Líder articula-se com diferentes atores e espaços institucionais para fortalecer a atuação integrada e ampliar a autonomia das equipes e dos profissionais no território."),
        ],
    },
    "etica": {
        "titulo": "Competência 4 — Ética",
        "definicao": "Capacidade de atuar com responsabilidade, coerência, transparência, respeito às pessoas e às responsabilidades profissionais, preservando os limites de atuação e os princípios que orientam o Programa.",
        "itens": [
            ("etica_1", "4.1 Coerência e responsabilidade profissional",
             "O Líder atua de forma coerente com os princípios, diretrizes e responsabilidades institucionais do Programa, demonstrando respeito e responsabilidade em suas decisões e relações profissionais."),
            ("etica_2", "4.2 Respeito às responsabilidades e à autonomia profissional",
             "O Líder respeita as responsabilidades, os limites de atuação e a autonomia técnica dos diferentes profissionais, considerando suas atribuições e conhecimentos específicos."),
            ("etica_3", "4.3 Transparência e equidade",
             "O Líder conduz relações, decisões e pactuações com transparência, respeito e equidade, buscando assegurar tratamento justo e clareza nos acordos estabelecidos."),
        ],
    },
}

# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-block">
    <h1>🏫 Avaliação de Desempenho e Competências</h1>
    <p>Programa Psicólogos nas Escolas — Bloco de Competências do Líder Regional</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
Esta avaliação tem caráter **formativo e confidencial**. Responda considerando comportamentos 
efetivamente observados durante o período de referência, com base em situações concretas.
""")

# ── SEÇÃO 1: Identificação ───────────────────────────────────────────────────
st.markdown('<div class="secao-titulo">Identificação do Participante</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    ure = st.selectbox(
        "URE *",
        URES,
        index=0,
        placeholder="Digite para buscar sua URE...",
    )
with col2:
    perfil = st.selectbox("Perfil do respondente *", ["Selecione", "Psicólogo", "PEC", "Gestor do Programa"])

email = st.text_input("E-mail institucional *", placeholder="nome@educacao.sp.gov.br")
nome_lider = st.text_input("Nome do Líder avaliado *", placeholder="Nome completo do Líder Regional")
periodo = st.selectbox("Período de referência *", PERIODOS)

# ── SEÇÃO 2 a 5: Competências ────────────────────────────────────────────────
respostas = {}  # {campo_base: {"nota": int|None, "sem_insumos": bool}}

SEM_INSUMOS_KEY = "Não tenho insumos suficientes para avaliar"

for comp_key, comp in COMPETENCIAS.items():
    st.markdown(f'<div class="secao-titulo">{comp["titulo"]}</div>', unsafe_allow_html=True)
    st.caption(comp["definicao"])

    for campo, subtitulo, comportamento in comp["itens"]:
        st.markdown(f"**{subtitulo}**")
        st.markdown(f'<div class="comportamento">📋 {comportamento}</div>', unsafe_allow_html=True)

        opcoes = [SEM_INSUMOS_KEY] + list(ESCALA.keys())
        escolha = st.radio(
            "Avaliação:",
            opcoes,
            key=f"radio_{campo}",
            index=0,
            label_visibility="collapsed",
            horizontal=False,
        )

        if escolha == SEM_INSUMOS_KEY:
            respostas[campo] = {"nota": None, "sem_insumos": True}
        else:
            respostas[campo] = {"nota": ESCALA[escolha], "sem_insumos": False}

        st.divider()

# ── SEÇÃO 6: Perguntas abertas ───────────────────────────────────────────────
st.markdown('<div class="secao-titulo">Perguntas Abertas</div>', unsafe_allow_html=True)

st.markdown('<div class="aviso">💡 Use as perguntas abaixo para registrar exemplos, situações ou aspectos relevantes que complementem sua avaliação.</div>', unsafe_allow_html=True)

desenvolvimento = st.text_area(
    "Quais são as oportunidades de desenvolvimento do líder?",
    placeholder="Descreva aspectos que poderiam ser aprimorados e como...",
    height=120,
)

destaques = st.text_area(
    "Quais são os pontos de destaque do líder?",
    placeholder="Descreva situações concretas que ilustrem os pontos fortes observados...",
    height=120,
)

# Pergunta exclusiva do Gestor
entregas_gestor = None
if perfil == "Gestor do Programa":
    st.markdown('<div class="secao-titulo">Bloco Exclusivo — Gestor do Programa</div>', unsafe_allow_html=True)
    st.markdown("Esta questão deve ser respondida somente pelo **Gestor do Programa**.")
    entregas_gestor = st.text_area(
        "Quais são os pontos de desenvolvimento e potenciais do líder em relação às entregas?",
        placeholder="Considere prazos, qualidade e consistência das entregas pactuadas...",
        height=120,
    )

# ── Validação e envio ────────────────────────────────────────────────────────
st.markdown("---")

def validar():
    erros = []
    if ure == "Selecione a URE":
        erros.append("Selecione a URE.")
    if perfil == "Selecione":
        erros.append("Selecione o perfil do respondente.")
    if not email or "@" not in email:
        erros.append("Informe um e-mail institucional válido.")
    if not nome_lider.strip():
        erros.append("Informe o nome do Líder avaliado.")
    if periodo == "Selecione o período":
        erros.append("Selecione o período de referência.")
    return erros

if st.button("✅ Enviar avaliação", type="primary", use_container_width=True):
    erros = validar()
    if erros:
        for e in erros:
            st.error(e)
    else:
        # Monta o payload
        payload = {
            "ure": ure,
            "perfil_respondente": perfil.lower().replace(" do programa", "").replace(" ", "_"),
            "email_respondente": email.strip().lower(),
            "nome_lider": nome_lider.strip(),
            "periodo_referencia": periodo,
            # Escuta
            "escuta_1_nota": respostas["escuta_1"]["nota"],
            "escuta_1_sem_insumos": respostas["escuta_1"]["sem_insumos"],
            "escuta_2_nota": respostas["escuta_2"]["nota"],
            "escuta_2_sem_insumos": respostas["escuta_2"]["sem_insumos"],
            "escuta_3_nota": respostas["escuta_3"]["nota"],
            "escuta_3_sem_insumos": respostas["escuta_3"]["sem_insumos"],
            # Práxis
            "praxis_1_nota": respostas["praxis_1"]["nota"],
            "praxis_1_sem_insumos": respostas["praxis_1"]["sem_insumos"],
            "praxis_2_nota": respostas["praxis_2"]["nota"],
            "praxis_2_sem_insumos": respostas["praxis_2"]["sem_insumos"],
            "praxis_3_nota": respostas["praxis_3"]["nota"],
            "praxis_3_sem_insumos": respostas["praxis_3"]["sem_insumos"],
            # Multiplicação
            "multiplicacao_1_nota": respostas["multiplicacao_1"]["nota"],
            "multiplicacao_1_sem_insumos": respostas["multiplicacao_1"]["sem_insumos"],
            "multiplicacao_2_nota": respostas["multiplicacao_2"]["nota"],
            "multiplicacao_2_sem_insumos": respostas["multiplicacao_2"]["sem_insumos"],
            "multiplicacao_3_nota": respostas["multiplicacao_3"]["nota"],
            "multiplicacao_3_sem_insumos": respostas["multiplicacao_3"]["sem_insumos"],
            # Ética
            "etica_1_nota": respostas["etica_1"]["nota"],
            "etica_1_sem_insumos": respostas["etica_1"]["sem_insumos"],
            "etica_2_nota": respostas["etica_2"]["nota"],
            "etica_2_sem_insumos": respostas["etica_2"]["sem_insumos"],
            "etica_3_nota": respostas["etica_3"]["nota"],
            "etica_3_sem_insumos": respostas["etica_3"]["sem_insumos"],
            # Qualitativo
            "qualitativo_destaques": destaques.strip() or None,
            "qualitativo_desenvolvimento": desenvolvimento.strip() or None,
            "qualitativo_entregas_gestor": entregas_gestor.strip() if entregas_gestor else None,
        }

        try:
            supabase.table("avaliacoes_lider").insert(payload).execute()
            st.success("✅ Avaliação enviada com sucesso! Obrigado pela sua participação.")
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao enviar a avaliação. Tente novamente. Detalhes: {e}")

# ── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rodape">
    Programa Psicólogos nas Escolas · Apoio Educação · Secretaria de Estado da Educação de São Paulo<br>
    As respostas são confidenciais e utilizadas exclusivamente para fins de desenvolvimento profissional.
</div>
""", unsafe_allow_html=True)
