import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Quiz SOU+", layout="centered")

st.title("🎮 Descubra seu perfil SOU+ BigBang Rio")
st.write("Responda as perguntas e descubra qual força te move!")

nome = st.text_input("Digite seu nome")

# Listas com perguntas e alternativas (sem os rótulos dos perfis)
perguntas = [
    # Bloco 1 – Como você pensa
    "Quando aparece um desafio novo, você:",
    "Qual dessas matérias da escola mais te atraía?",
    "Para tomar uma decisão, você prefere:",
    "Diante de uma tarefa difícil, você:",
    "Seu maior talento está em:",

    # Bloco 2 – Como você age
    "Se fosse jogar um game, você escolheria:",
    "Num imprevisto, você costuma:",
    "Quando tem tempo livre, você prefere:",
    "Seu hobby ideal é:",
    "Se tivesse que montar uma barraca de camping, você:",

    # Bloco 3 – Seu estilo social
    "Em uma roda de conversa, você costuma ser:",
    "O que mais te dá energia em um evento como o Big Bang?",
    "Em um sorteio de atividade, você adoraria pegar:",
    "O que mais te deixa satisfeito ao final de uma atividade?",
    "Quando conhece alguém novo, você:",

    # Bloco 4 – Estilo de vida e preferências
    "Viagem dos sonhos:",
    "Se fosse escolher um objeto para levar para o Big Bang:",
    "Sua refeição favorita é:",
    "Um lugar no Rio que mais combina com você:",
    "Estilo musical que te move:",

    # Bloco 5 – Inspirações e sonhos
    "Um superpoder que você gostaria de ter:",
    "Se tivesse que escolher um símbolo para você:",
    "O que mais te motiva num projeto:",
    "Uma qualidade que mais reconhecem em você:",
    "Um elogio que você adora ouvir:",

    # Bloco 6 – Situações práticas
    "Em uma corrida de equipe, você seria:",
    "Numa gincana de perguntas, você:",
    "Se uma atividade for cancelada de última hora, você:",
    "Ao ouvir uma música contagiante, você:",
    "O que você mais gostaria de deixar marcado no Big Bang 2025?",
]

opcoes = [
    ["Analisa e planeja a solução", "Testa na prática e ajusta no caminho", "Pede ajuda ou troca ideias", "Busca uma forma criativa e diferente de resolver"],
    ["Matemática ou ciências exatas", "Educação física", "História ou sociologia", "Artes ou literatura"],
    ["Dados e lógica", "Intuição e impulso", "Conversar e alinhar com pessoas", "Imaginar cenários criativos"],
    ["Divide em etapas lógicas", "Vai tentando até dar certo", "Busca parceria para compartilhar", "Reinventa o jeito de fazer"],
    ["Resolver problemas", "Superar desafios físicos", "Criar laços fortes com pessoas", "Ter ideias originais"],

    ["De estratégia/puzzle", "De corrida/ação", "Multiplayer cooperativo", "Criativo/sandbox"],
    ["Calcular opções antes de agir", "Agir rápido e corrigir depois", "Procurar apoio das pessoas", "Improvisar com criatividade"],
    ["Ler ou estudar algo novo", "Praticar um esporte", "Sair com amigos/família", "Ir a um show, cinema ou oficina criativa"],
    ["Montar quebra-cabeças, xadrez ou programação", "Surf, corrida ou trekking", "Jantar com amigos, jogos de grupo", "Pintura, música ou dança"],
    ["Leria o manual e organizaria", "Montaria tentando na prática", "Chamaria amigos para montar juntos", "Improvisaria com o que tivesse"],

    ["O que faz perguntas inteligentes", "O que conta histórias de aventuras", "O que escuta e conecta as pessoas", "O que faz piadas e anima"],
    ["Os desafios que exigem raciocínio", "As atividades esportivas", "Estar junto do time", "As expressões culturais e artísticas"],
    ["Um quiz de lógica", "Uma corrida ou prova física", "Um jogo de colaboração", "Uma competição de dança"],
    ["Ter resolvido de forma inteligente", "Ter dado o máximo de energia", "Ter unido o grupo", "Ter criado algo memorável"],
    ["Faz perguntas técnicas ou curiosas", "Propõe uma atividade ou esporte", "Procura algo em comum", "Usa humor ou criatividade"],

    ["Conhecer museus ou centros tecnológicos", "Explorar trilhas e natureza", "Um mochilão com amigos", "Festival de música e cultura"],
    ["Um livro ou gadget", "Um tênis esportivo", "Um baralho/jogo de grupo", "Um instrumento musical"],
    ["Algo saudável e prático", "Churrasco, lanche ou energético", "Um prato compartilhado com amigos", "Uma comida exótica e colorida"],
    ["Museu do Amanhã", "Pedra da Gávea", "Lapa", "Sambódromo"],
    ["Eletrônica ou clássica", "Rock, reggae ou esportivo/vibrante", "MPB, samba de roda", "Samba-enredo, funk, axé"],

    ["Inteligência ilimitada", "Superforça/velocidade", "Ler emoções das pessoas", "Criar realidades"],
    ["Um cérebro", "Um raio", "Um coração", "Uma estrela"],
    ["Resolver algo complexo", "Sentir adrenalina e ação", "Ver o grupo junto", "Criar algo original"],
    ["Inteligência", "Energia", "Empatia", "Criatividade"],
    ["Você é muito estratégico", "Você tem muita disposição", "Você inspira confiança", "Você é muito criativo"],

    ["O que organiza a estratégia", "O que corre mais rápido", "O que ajuda o mais lento", "O que faz torcida animada"],
    ["Assume a liderança para responder", "Arrisca mesmo sem certeza", "Incentiva quem está inseguro", "Dá respostas criativas e engraçadas"],
    ["Pensa em outra solução", "Puxa outra atividade esportiva", "Propõe um jogo em grupo", "Cria uma dinâmica diferente"],
    ["Analisa a letra/ritmo", "Começa a se mexer", "Chama alguém para dançar junto", "Inventa passos criativos"],
    ["Uma solução inteligente num desafio", "Uma vitória esportiva", "Uma amizade verdadeira", "Uma apresentação memorável"],
]

respostas = []
tipos = ["Geek", "Aventura", "Conexão", "Arte"]
pontuacoes = {tipo: 0 for tipo in tipos}

for i, pergunta in enumerate(perguntas):
    resposta = st.radio(pergunta, opcoes[i], index=None, key=f"pergunta_{i}")
    respostas.append(resposta)

if st.button("Ver meu perfil"):
    for r in respostas:
        if r in opcoes[perguntas.index(pergunta)]:
            idx = opcoes[perguntas.index(pergunta)].index(r)
            tipo = tipos[idx]  # 0 = Geek, 1 = Aventura, 2 = Conexão, 3 = Arte
            pontuacoes[tipo] += 1

    perfil = max(pontuacoes, key=pontuacoes.get)
    emoji = {"Geek": "💙", "Aventura": "💚", "Conexão": "🩵", "Arte": "💛"}[perfil]

    st.subheader(f"Seu perfil é: SOU+ {perfil} {emoji}")

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
