
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Quiz SOU+", layout="centered")

st.title("🎮 Descubra seu perfil SOU+")
st.write("Responda as perguntas e descubra qual força te move!")

nome = st.text_input("Digite seu nome")

perguntas = [
    "Você prefere resolver problemas com lógica ou criatividade?",
    "Durante uma atividade em grupo, você tende a liderar, ouvir, criar ou agir?",
    "Se você tivesse que escolher um passatempo, seria: resolver enigmas, fazer trilhas, conversar ou dançar?",
    "Você se sente mais energizado após: um desafio mental, um treino, uma boa conversa ou uma apresentação artística?"
]

respostas = []
tipos = ['Geek', 'Aventura', 'Conexão', 'Arte']
pontuacoes = {tipo: 0 for tipo in tipos}

opcoes = [
    ["Lógica", "Criatividade", "Diálogo", "Atividade física"],
    ["Liderar (Geek)", "Ouvir (Conexão)", "Criar (Arte)", "Agir (Aventura)"],
    ["Enigmas (Geek)", "Trilhas (Aventura)", "Conversar (Conexão)", "Dançar (Arte)"],
    ["Desafio mental (Geek)", "Treino (Aventura)", "Boa conversa (Conexão)", "Apresentação artística (Arte)"]
]

for i, pergunta in enumerate(perguntas):
    resposta = st.radio(pergunta, opcoes[i], key=f"pergunta_{i}")
    respostas.append(resposta)

if st.button("Ver meu perfil"):
    for r in respostas:
        if "Geek" in r or "Lógica" in r or "Enigma" in r or "Desafio" in r:
            pontuacoes["Geek"] += 1
        elif "Aventura" in r or "Trilha" in r or "Atividade física" in r or "Treino" in r:
            pontuacoes["Aventura"] += 1
        elif "Conexão" in r or "Conversar" in r or "Ouvir" in r or "Diálogo" in r:
            pontuacoes["Conexão"] += 1
        elif "Arte" in r or "Criatividade" in r or "Dançar" in r or "Apresentação" in r:
            pontuacoes["Arte"] += 1

    perfil = max(pontuacoes, key=pontuacoes.get)
    emoji = {"Geek": "💙", "Aventura": "💚", "Conexão": "🩷", "Arte": "💛"}[perfil]

    st.subheader(f"Seu perfil é: SOU+ {perfil} {emoji}")

    # Salvar resposta
    if nome:
        data = pd.DataFrame([{
            "nome": nome,
            "data": datetime.datetime.now(),
            **pontuacoes
        }])
        try:
            existentes = pd.read_csv("respostas.csv")
            data = pd.concat([existentes, data], ignore_index=True)
        except:
            pass
        data.to_csv("respostas.csv", index=False)
