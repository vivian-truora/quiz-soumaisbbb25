import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Quiz SOU+", layout="centered")

# Novo texto de introdução
st.title("SOU+ é a Energia Que Move Cada Um de Nós")
st.write("""
Todos nós temos algo especial que nos move: uma forma única de pensar, agir ou se conectar.\n
Cada cor dá visibilidade às diferentes forças que compõem cada pessoa.\n
O SOU+ é a nossa forma de mapear essas forças, de um jeito leve, e integrado a toda experiência do Big Bang deste ano.\n
E aí? Prontos para descobrir o seu perfil SOU+?\n
Quem é você no game?
""")

nome = st.text_input("Digite seu nome")

# Dicionário de alternativas para perfis (exemplo com 3 perguntas)
tipo_por_resposta = {
    # Pergunta 1
    "Analisa e planeja a solução": "Geek",
    "Testa na prática e ajusta no caminho": "Aventura",
    "Pede ajuda ou troca ideias": "Conexão",
    "Busca uma forma criativa e diferente de resolver": "Arte",

    # Pergunta 2
    "Matemática ou ciências exatas": "Geek",
    "Educação física": "Aventura",
    "História ou sociologia": "Conexão",
    "Artes ou literatura": "Arte",

    # Pergunta 3
    "Dados e lógica": "Geek",
    "Intuição e impulso": "Aventura",
    "Conversar e alinhar com pessoas": "Conexão",
    "Imaginar cenários criativos": "Arte",
}

# Lista de perguntas (exemplo)
perguntas = [
    ("Quando aparece um desafio novo, você:", [
        "Analisa e planeja a solução",
        "Testa na prática e ajusta no caminho",
        "Pede ajuda ou troca ideias",
        "Busca uma forma criativa e diferente de resolver"
    ]),
    ("Qual dessas matérias da escola mais te atraía?", [
        "Matemática ou ciências exatas",
        "Educação física",
        "História ou sociologia",
        "Artes ou literatura"
    ]),
    ("Para tomar uma decisão, você prefere:", [
        "Dados e lógica",
        "Intuição e impulso",
        "Conversar e alinhar com pessoas",
        "Imaginar cenários criativos"
    ])
]

pontuacoes = {"Geek": 0, "Aventura": 0, "Conexão": 0, "Arte": 0}

for i, (pergunta, alternativas) in enumerate(perguntas):
    resposta = st.radio(pergunta, alternativas, key=f"pergunta_{i}")
    tipo = tipo_por_resposta[resposta]
    pontuacoes[tipo] += 1

if st.button("Ver meu perfil"):
    perfil_principal = max(pontuacoes, key=pontuacoes.get)
    total = sum(pontuacoes.values())

    descricao = {
        "Geek": "💙 Sua cor é o Azul\n\nO cérebro do time. Analítico, curioso, resolve problemas e domina o conhecimento.",
        "Aventura": "💚 Sua cor é o Verde\n\nO desbravador. Ama movimento, desafios físicos e ambientes inesperados.",
        "Conexão": "🖧 Sua cor é o Rosa\n\nA base do time. Une pessoas, cuida do grupo e garante colaboração.",
        "Arte": "💛 Amarelo\n\nA alma criativa. Expressivo, contagia com energia, empolgação e dá ritmo às experiências."
    }

    emoji = {"Geek": "💙", "Aventura": "💚", "Conexão": "🖧", "Arte": "💛"}[perfil_principal]

    st.subheader(f"SOU+ {perfil_principal} {emoji}")
    st.write(descricao[perfil_principal])
    st.write("Distribuição:")

    for tipo, valor in pontuacoes.items():
        percentual = round((valor / total) * 100)
        st.write(f"- {tipo}: {percentual}%")

    if nome:
        data = pd.DataFrame([{ "nome": nome, "data": datetime.datetime.now(), **pontuacoes }])
        try:
            existentes = pd.read_csv("respostas.csv")
            data = pd.concat([existentes, data], ignore_index=True)
        except:
            pass
        data.to_csv("respostas.csv", index=False)
