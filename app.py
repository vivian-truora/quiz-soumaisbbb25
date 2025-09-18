import streamlit as st
import pandas as pd
import datetime
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials

# ------------------ CONFIGURAÇÃO STREAMLIT ------------------
st.set_page_config(page_title="Quiz SOU+ Big Bang", layout="centered")
st.title("🎮 Descubra seu perfil SOU+ Big Bang Rio")

st.markdown("""
**SOU+ é a Energia Que Move Cada Um de Nós**

Todos nós temos algo especial que nos move: uma forma única de pensar, agir ou se conectar.  
Cada cor dá visibilidade às diferentes forças que compõem cada pessoa.  

O SOU+ é a nossa forma de mapear essas forças, de um jeito leve, e integrado a toda experiência do Big Bang deste ano.  
**E aí? Pronto(a) para descobrir o seu perfil SOU+?**
""")

nome = st.text_input("Digite seu nome")

# ------------------ PERGUNTAS ------------------
perguntas = [
    ("Quando aparece um desafio novo, você:", [
        ("Analisa e planeja a solução", "Geek"),
        ("Testa na prática e ajusta no caminho", "Aventura"),
        ("Pede ajuda ou troca ideias", "Conexão"),
        ("Busca uma forma criativa e diferente de resolver", "Arte")]),

    ("Qual dessas matérias da escola mais te atraía?", [
        ("Matemática ou ciências exatas", "Geek"),
        ("Educação física", "Aventura"),
        ("História ou sociologia", "Conexão"),
        ("Artes ou literatura", "Arte")]),

    ("Para tomar uma decisão, você prefere:", [
        ("Dados e lógica", "Geek"),
        ("Intuição e impulso", "Aventura"),
        ("Conversar e alinhar com pessoas", "Conexão"),
        ("Imaginar cenários criativos", "Arte")]),

    ("Diante de uma tarefa difícil, você:", [
        ("Divide em etapas lógicas", "Geek"),
        ("Vai tentando até dar certo", "Aventura"),
        ("Busca parceria para compartilhar", "Conexão"),
        ("Reinventa o jeito de fazer", "Arte")]),

    ("Seu maior talento está em:", [
        ("Resolver problemas", "Geek"),
        ("Superar desafios físicos", "Aventura"),
        ("Criar laços fortes com pessoas", "Conexão"),
        ("Ter ideias originais", "Arte")]),

    ("Se fosse jogar um game, você escolheria:", [
        ("De estratégia/puzzle", "Geek"),
        ("De corrida/ação", "Aventura"),
        ("Multiplayer cooperativo", "Conexão"),
        ("Criativo/sandbox", "Arte")]),

    ("Num imprevisto, você costuma:", [
        ("Calcular opções antes de agir", "Geek"),
        ("Agir rápido e corrigir depois", "Aventura"),
        ("Procurar apoio das pessoas", "Conexão"),
        ("Improvisar com criatividade", "Arte")]),

    ("Quando tem tempo livre, você prefere:", [
        ("Ler ou estudar algo novo", "Geek"),
        ("Praticar um esporte", "Aventura"),
        ("Sair com amigos/família", "Conexão"),
        ("Ir a um show, cinema ou oficina criativa", "Arte")]),

    ("Seu hobby ideal é:", [
        ("Montar quebra-cabeças, xadrez ou programação", "Geek"),
        ("Surf, corrida ou trekking", "Aventura"),
        ("Jantar com amigos, jogos de grupo", "Conexão"),
        ("Pintura, música ou dança", "Arte")]),

    ("Se tivesse que montar uma barraca de camping, você:", [
        ("Leria o manual e organizaria", "Geek"),
        ("Montaria tentando na prática", "Aventura"),
        ("Chamaria amigos para montar juntos", "Conexão"),
        ("Improvisaria com o que tivesse", "Arte")]),

    ("Em uma roda de conversa, você costuma ser:", [
        ("O que faz perguntas inteligentes", "Geek"),
        ("O que conta histórias de aventuras", "Aventura"),
        ("O que escuta e conecta as pessoas", "Conexão"),
        ("O que faz piadas e anima", "Arte")]),

    ("O que mais te dá energia em um evento como o Big Bang?", [
        ("Os desafios que exigem raciocínio", "Geek"),
        ("As atividades esportivas", "Aventura"),
        ("Estar junto do time", "Conexão"),
        ("As expressões culturais e artísticas", "Arte")]),

    ("Em um sorteio de atividade, você adoraria pegar:", [
        ("Um quiz de lógica", "Geek"),
        ("Uma corrida ou prova física", "Aventura"),
        ("Um jogo de colaboração", "Conexão"),
        ("Uma competição de dança", "Arte")]),

    ("O que mais te deixa satisfeito ao final de uma atividade?", [
        ("Ter resolvido de forma inteligente", "Geek"),
        ("Ter dado o máximo de energia", "Aventura"),
        ("Ter unido o grupo", "Conexão"),
        ("Ter criado algo memorável", "Arte")]),

    ("Quando conhece alguém novo, você:", [
        ("Faz perguntas técnicas ou curiosas", "Geek"),
        ("Propõe uma atividade ou esporte", "Aventura"),
        ("Procura algo em comum", "Conexão"),
        ("Usa humor ou criatividade", "Arte")])
]

# Embaralhar alternativas de cada pergunta
for i in range(len(perguntas)):
    random.shuffle(perguntas[i][1])

pontuacoes = {"Geek": 0, "Aventura": 0, "Conexão": 0, "Arte": 0}
respostas = []

# Interface com as perguntas
for idx, (pergunta, opcoes) in enumerate(perguntas):
    alternativa = st.radio(pergunta, [op[0] for op in opcoes], key=f"pergunta_{idx}")
    perfil = [p for txt, p in opcoes if txt == alternativa][0]
    pontuacoes[perfil] += 1
    respostas.append((pergunta, alternativa))

# Verifica empate
total = sum(pontuacoes.values())
max_score = max(pontuacoes.values())
empatados = [p for p, v in pontuacoes.items() if v == max_score]

if len(empatados) > 1:
    st.markdown("### 🤔 Houve um empate!")
    desempate = st.radio("Escolha a alternativa que mais representa você neste momento:", [
        "Prefiro resolver com lógica e planejamento",
        "Prefiro ação e movimento",
        "Prefiro estar junto das pessoas",
        "Prefiro me expressar de forma criativa"
    ], key="desempate")

    if "lógica" in desempate:
        pontuacoes["Geek"] += 1
    elif "ação" in desempate:
        pontuacoes["Aventura"] += 1
    elif "pessoas" in desempate:
        pontuacoes["Conexão"] += 1
    elif "criativa" in desempate:
        pontuacoes["Arte"] += 1

if st.button("Ver meu perfil"):
    total = sum(pontuacoes.values())
    porcentagens = {p: round((v/total)*100) for p,v in pontuacoes.items()}
    perfil_principal = max(pontuacoes, key=pontuacoes.get)

    descricoes = {
        "Geek": "💙 Sua cor é o Azul\n\nO cérebro do time. Analítico, curioso, resolve problemas e domina o conhecimento.",
        "Aventura": "💚 Sua cor é o Verde\n\nO desbravador. Ama movimento, desafios físicos e ambientes inesperados.",
        "Conexão": "🩷 Sua cor é o Rosa\n\nA base do time. Une pessoas, cuida do grupo e garante colaboração.",
        "Arte": "💛 Amarelo\n\nA alma criativa. Expressivo, contagia com energia, empolgação e dá ritmo às experiências."
    }

    st.subheader(f"Seu perfil principal é: SOU+ {perfil_principal}")
    st.markdown(descricoes[perfil_principal])

    st.write("### Seus percentuais")
    st.write(pd.DataFrame([porcentagens]))

    # Google Sheets - salvar dados
    try:
        escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credenciais = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], escopo)
        cliente = gspread.authorize(credenciais)
        planilha = cliente.open("Respostas SOU+ BBB25")
        aba = planilha.sheet1
        aba.append_row([
            nome,
            str(datetime.datetime.now()),
            perfil_principal,
            porcentagens["Geek"], porcentagens["Aventura"], porcentagens["Conexão"], porcentagens["Arte"]
        ])
    except Exception as e:
        st.warning(f"Erro ao salvar na planilha: {e}")
