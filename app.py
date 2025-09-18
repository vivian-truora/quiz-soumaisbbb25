import streamlit as st
import random
import datetime
import gspread
from google.oauth2 import service_account
import pandas as pd


# Configuração da página
st.set_page_config(page_title="Quiz SOU+ Big Bang Rio", layout="centered")
st.title("🎮 Descubra seu perfil SOU+ Big Bang Rio")


st.markdown("""
**SOU+ é a Energia Que Move Cada Um de Nós**
Todos nós temos algo especial que nos move: uma forma única de pensar, agir ou se conectar.
Cada cor dá visibilidade às diferentes forças que compõem cada pessoa.


O SOU+ é a nossa forma de mapear essas forças, de um jeito leve, e integrado a toda experiência do Big Bang deste ano.
**E aí? Pronto(a) para descobrir o seu perfil SOU+?**
""")


# Nome do participante
nome = st.text_input("Digite seu nome completo")


# Perguntas
quiz_perguntas = [
("Quando aparece um desafio novo, você:", [
("Busca uma forma criativa e diferente de resolver", "Arte"),
("Pede ajuda ou troca ideias", "Conexão"),
("Testa na prática e ajusta no caminho", "Aventura"),
("Analisa e planeja a solução", "Geek")]),


("Qual dessas matérias da escola mais te atraía?", [
("História ou sociologia", "Conexão"),
("Educação física", "Aventura"),
("Artes ou literatura", "Arte"),
("Matemática ou ciências exatas", "Geek")]),


("Para tomar uma decisão, você prefere:", [
("Imaginar cenários criativos", "Arte"),
("Conversar e alinhar com pessoas", "Conexão"),
("Intuição e impulso", "Aventura"),
("Dados e lógica", "Geek")]),


("Diante de uma tarefa difícil, você:", [
("Reinventa o jeito de fazer", "Arte"),
("Busca parceria para compartilhar", "Conexão"),
("Vai tentando até dar certo", "Aventura"),
("Divide em etapas lógicas", "Geek")]),


("Seu maior talento está em:", [
("Criar laços fortes com pessoas", "Conexão"),
("Superar desafios físicos", "Aventura"),
("Ter ideias originais", "Arte"),
("Resolver problemas", "Geek")]),


("Se fosse jogar um game, você escolheria:", [
("Criativo/sandbox", "Arte"),
("De corrida/ação", "Aventura"),
("Multiplayer cooperativo", "Conexão"),
("De estratégia/puzzle", "Geek")]),


("Num imprevisto, você costuma:", [
("Improvisar com criatividade", "Arte"),
("Calcular opções antes de agir", "Geek"),
("Agir rápido e corrigir depois", "Aventura"),
("Procurar apoio das pessoas", "Conexão")]),


("Quando tem tempo livre, você prefere:", [
("Ir a um show, cinema ou oficina criativa", "Arte"),
("Sair com amigos/família", "Conexão"),
("Praticar um esporte", "Aventura"),
("Ler ou estudar algo novo", "Geek")]),


("Seu hobby ideal é:", [
("Pintura, música ou dança", "Arte"),
("Surf, corrida ou trekking", "Aventura"),
("Montar quebra-cabeças, xadrez ou programação", "Geek"),
("Jantar com amigos, jogos de grupo", "Conexão")]),


("Se tivesse que montar uma barraca de camping, você:", [
("Chamaria amigos para montar juntos", "Conexão"),
("Improvisaria com o que tivesse", "Arte"),
("Leria o manual e organizaria", "Geek"),
("Montaria tentando na prática", "Aventura")]),


("Em uma roda de conversa, você costuma ser:", [
]
pontuacoes = {"Geek": 0, "Aventura": 0, "Conexão": 0, "Arte": 0}
respostas = []

for idx, (pergunta, alternativas) in enumerate(quiz_perguntas):
    random.shuffle(alternativas)
    resposta = st.radio(pergunta, [a[0] for a in alternativas], key=f"pergunta_{idx}")
    perfil = next(p for txt, p in alternativas if txt == resposta)
    pontuacoes[perfil] += 1
    respostas.append((pergunta, resposta))

# Verifica empate
max_score = max(pontuacoes.values())
empatados = [p for p, v in pontuacoes.items() if v == max_score]

if len(empatados) > 1:
    st.markdown("### ❓ Houve um empate! Responda a pergunta de desempate:")
    desempate = st.radio("Com qual dessas atitudes você mais se identifica:", [
        ("Reinventa o jeito de fazer", "Arte"),
        ("Busca parceria para compartilhar", "Conexão"),
        ("Vai tentando até dar certo", "Aventura"),
        ("Divide em etapas lógicas", "Geek")
    ], key="desempate")
    pontuacoes[[p for txt, p in [("Reinventa o jeito de fazer", "Arte"), ("Busca parceria para compartilhar", "Conexão"), ("Vai tentando até dar certo", "Aventura"), ("Divide em etapas lógicas", "Geek")] if txt == desempate][0]] += 1

# Resultado final
if st.button("Ver meu perfil"):
    total = sum(pontuacoes.values())
    porcentagens = {p: round((v/total)*100) for p,v in pontuacoes.items()}
    perfil_principal = max(pontuacoes, key=pontuacoes.get)

    descricoes = {
        "Geek": "✨ **SOU+ Geek**  \n💙 Sua cor é o Azul  \nO cérebro do time. Analítico, curioso, resolve problemas e domina o conhecimento.",
        "Aventura": "✨ **SOU+ Aventura**  \n 💚 Sua cor é o Verde  \nO desbravador. Ama movimento, desafios físicos e ambientes inesperados.",
        "Conexão": "✨ **SOU+ Conexão**  \n 🩷 Sua cor é o Rosa  \nA base do time. Une pessoas, cuida do grupo e garante colaboração.",
        "Arte": "✨ **SOU+ Criativo**  \n 💛 Sua cor é o Amarelo  \nA alma criativa. Expressivo, contagia com energia, empolgação e dá ritmo às experiências."
    }

    st.markdown(descricoes[perfil_principal])

    st.markdown("### Seus percentuais:")
    for p in ["Geek", "Aventura", "Conexão", "Arte"]:
        st.write(f"{p}: {porcentagens[p]}%")

    # Salvar no Google Sheets via Streamlit Secrets
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
