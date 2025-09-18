import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials

# ========== CONFIG STREAMLIT ==========
st.set_page_config(page_title="Quiz SOU+", layout="centered")
st.title("🎮 Descubra seu perfil SOU+ BigBang Rio")
st.markdown("""
**SOU+ é a Energia Que Move Cada Um de Nós**


Todos nós temos algo especial que nos move: uma forma única de pensar, agir ou se conectar.
Cada cor dá visibilidade às diferentes forças que compõem cada pessoa.


O SOU+ é a nossa forma de mapear essas forças, de um jeito leve, e integrado a toda experiência do Big Bang deste ano.
**E aí? Pronto(a) para descobrir o seu perfil SOU+?**
""")

nome = st.text_input("Digite seu nome")

# ========== CONFIG GOOGLE SHEETS ==========
SHEET_ID = "1xgQBzO8BY86iys5AIE85wxqlW7Ug7ThfYAR3dPTNcEw"
SHEET_NAME = "Respostas SOU+ BBB25"  # ajuste se o nome da aba for diferente

scope = ["https://www.googleapis.com/auth/spreadsheets", 
         "https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_file(
    "credenciais.json", scopes=scope
)
gc = gspread.authorize(credentials)
sh = gc.open_by_key("1xgQBzO8BY86iys5AIE85wxqlW7Ug7ThfYAR3dPTNcEw")
worksheet = sh.worksheet("Respostas SOU+ BBB25")

# Lista de perguntas e alternativas associadas aos perfis
perguntas_opcoes = [
    # Bloco 1 – Como você pensa
    ("Quando aparece um desafio novo, você:", [("Analisa e planeja a solução", "Geek"), ("Testa na prática e ajusta no caminho", "Aventura"), ("Pede ajuda ou troca ideias", "Conexão"), ("Busca uma forma criativa e diferente de resolver", "Arte")]),
    ("Qual dessas matérias da escola mais te atraía?", [("Matemática ou ciências exatas", "Geek"), ("Educação física", "Aventura"), ("História ou sociologia", "Conexão"), ("Artes ou literatura", "Arte")]),
    ("Para tomar uma decisão, você prefere:", [("Dados e lógica", "Geek"), ("Intuição e impulso", "Aventura"), ("Conversar e alinhar com pessoas", "Conexão"), ("Imaginar cenários criativos", "Arte")]),
    ("Diante de uma tarefa difícil, você:", [("Divide em etapas lógicas", "Geek"), ("Vai tentando até dar certo", "Aventura"), ("Busca parceria para compartilhar", "Conexão"), ("Reinventa o jeito de fazer", "Arte")]),
    ("Seu maior talento está em:", [("Resolver problemas", "Geek"), ("Superar desafios físicos", "Aventura"), ("Criar laços fortes com pessoas", "Conexão"), ("Ter ideias originais", "Arte")]),

    # Bloco 2 – Como você age
    ("Se fosse jogar um game, você escolheria:", [("De estratégia/puzzle", "Geek"), ("De corrida/ação", "Aventura"), ("Multiplayer cooperativo", "Conexão"), ("Criativo/sandbox", "Arte")]),
    ("Num imprevisto, você costuma:", [("Calcular opções antes de agir", "Geek"), ("Agir rápido e corrigir depois", "Aventura"), ("Procurar apoio das pessoas", "Conexão"), ("Improvisar com criatividade", "Arte")]),
    ("Quando tem tempo livre, você prefere:", [("Ler ou estudar algo novo", "Geek"), ("Praticar um esporte", "Aventura"), ("Sair com amigos/família", "Conexão"), ("Ir a um show, cinema ou oficina criativa", "Arte")]),
    ("Seu hobby ideal é:", [("Montar quebra-cabeças, xadrez ou programação", "Geek"), ("Surf, corrida ou trekking", "Aventura"), ("Jantar com amigos, jogos de grupo", "Conexão"), ("Pintura, música ou dança", "Arte")]),
    ("Se tivesse que montar uma barraca de camping, você:", [("Leria o manual e organizaria", "Geek"), ("Montaria tentando na prática", "Aventura"), ("Chamaria amigos para montar juntos", "Conexão"), ("Improvisaria com o que tivesse", "Arte")]),

    # Bloco 3 – Seu estilo social
    ("Em uma roda de conversa, você costuma ser:", [("O que faz perguntas inteligentes", "Geek"), ("O que conta histórias de aventuras", "Aventura"), ("O que escuta e conecta as pessoas", "Conexão"), ("O que faz piadas e anima", "Arte")]),
    ("O que mais te dá energia em um evento como o Big Bang?", [("Os desafios que exigem raciocínio", "Geek"), ("As atividades esportivas", "Aventura"), ("Estar junto do time", "Conexão"), ("As expressões culturais e artísticas", "Arte")]),
    ("Em um sorteio de atividade, você adoraria pegar:", [("Um quiz de lógica", "Geek"), ("Uma corrida ou prova física", "Aventura"), ("Um jogo de colaboração", "Conexão"), ("Uma competição de dança", "Arte")]),
    ("O que mais te deixa satisfeito ao final de uma atividade?", [("Ter resolvido de forma inteligente", "Geek"), ("Ter dado o máximo de energia", "Aventura"), ("Ter unido o grupo", "Conexão"), ("Ter criado algo memorável", "Arte")]),
    ("Quando conhece alguém novo, você:", [("Faz perguntas técnicas ou curiosas", "Geek"), ("Propõe uma atividade ou esporte", "Aventura"), ("Procura algo em comum", "Conexão"), ("Usa humor ou criatividade", "Arte")]),

    # Bloco 4 – Estilo de vida e preferências
    ("Viagem dos sonhos:", [("Conhecer museus ou centros tecnológicos", "Geek"), ("Explorar trilhas e natureza", "Aventura"), ("Um mochilão com amigos", "Conexão"), ("Festival de música e cultura", "Arte")]),
    ("Se fosse escolher um objeto para levar para o Big Bang:", [("Um livro ou gadget", "Geek"), ("Um tênis esportivo", "Aventura"), ("Um baralho/jogo de grupo", "Conexão"), ("Um instrumento musical", "Arte")]),
    ("Sua refeição favorita é:", [("Algo saudável e prático", "Geek"), ("Churrasco, lanche ou energético", "Aventura"), ("Um prato compartilhado com amigos", "Conexão"), ("Uma comida exótica e colorida", "Arte")]),
    ("Um lugar no Rio que mais combina com você:", [("Museu do Amanhã", "Geek"), ("Pedra da Gávea", "Aventura"), ("Lapa", "Conexão"), ("Sambódromo", "Arte")]),
    ("Estilo musical que te move:", [("Eletrônica ou clássica", "Geek"), ("Rock, reggae ou esportivo/vibrante", "Aventura"), ("MPB, samba de roda", "Conexão"), ("Samba-enredo, funk, axé", "Arte")]),

    # Bloco 5 – Inspirações e sonhos
    ("Um superpoder que você gostaria de ter:", [("Inteligência ilimitada", "Geek"), ("Superforça/velocidade", "Aventura"), ("Ler emoções das pessoas", "Conexão"), ("Criar realidades", "Arte")]),
    ("Se tivesse que escolher um símbolo para você:", [("Um cérebro", "Geek"), ("Um raio", "Aventura"), ("Um coração", "Conexão"), ("Uma estrela", "Arte")]),
    ("O que mais te motiva num projeto:", [("Resolver algo complexo", "Geek"), ("Sentir adrenalina e ação", "Aventura"), ("Ver o grupo junto", "Conexão"), ("Criar algo original", "Arte")]),
    ("Uma qualidade que mais reconhecem em você:", [("Inteligência", "Geek"), ("Energia", "Aventura"), ("Empatia", "Conexão"), ("Criatividade", "Arte")]),
    ("Um elogio que você adora ouvir:", [("“Você é muito estratégico”", "Geek"), ("“Você tem muita disposição”", "Aventura"), ("“Você inspira confiança”", "Conexão"), ("“Você é muito criativo”", "Arte")]),

    # Bloco 6 – Situações práticas
    ("Em uma corrida de equipe, você seria:", [("O que organiza a estratégia", "Geek"), ("O que corre mais rápido", "Aventura"), ("O que ajuda o mais lento", "Conexão"), ("O que faz torcida animada", "Arte")]),
    ("Numa gincana de perguntas, você:", [("Assume a liderança para responder", "Geek"), ("Arrisca mesmo sem certeza", "Aventura"), ("Incentiva quem está inseguro", "Conexão"), ("Dá respostas criativas e engraçadas", "Arte")]),
    ("Se uma atividade for cancelada de última hora, você:", [("Pensa em outra solução", "Geek"), ("Puxa outra atividade esportiva", "Aventura"), ("Propõe um jogo em grupo", "Conexão"), ("Cria uma dinâmica diferente", "Arte")]),
    ("Ao ouvir uma música contagiante, você:", [("Analisa a letra/ritmo", "Geek"), ("Começa a se mexer", "Aventura"), ("Chama alguém para dançar junto", "Conexão"), ("Inventa passos criativos", "Arte")]),
    ("O que você mais gostaria de deixar marcado no Big Bang 2025?", [("Uma solução inteligente num desafio", "Geek"), ("Uma vitória esportiva", "Aventura"), ("Uma amizade verdadeira", "Conexão"), ("Uma apresentação memorável", "Arte")])
]

respostas = []
pontuacoes = {"Geek": 0, "Aventura": 0, "Conexão": 0, "Arte": 0}

for i, (pergunta, opcoes) in enumerate(perguntas_opcoes):
    labels = [texto for texto, _ in opcoes]
    escolha = st.radio(pergunta, labels, key=f"pergunta_{i}")
    for label, tipo in opcoes:
        if escolha == label:
            pontuacoes[tipo] += 1

if st.button("Ver meu perfil"):
    perfil_principal = max(pontuacoes, key=pontuacoes.get)
    total = sum(pontuacoes.values())
    emoji = {"Geek": "💙", "Aventura": "💚", "Conexão": "🩷", "Arte": "💛"}[perfil_principal]

    st.subheader(f"Seu perfil principal é: SOU+ {perfil_principal} {emoji}")
    st.write("Distribuição:")
    for tipo, valor in pontuacoes.items():
        percentual = round((valor / total) * 100)
        st.write(f"- {tipo}: {percentual}%")

     # ========== SALVAR NO GOOGLE SHEETS ==========
    if nome:
        nova_linha = [
            nome,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            pontuacoes["Geek"],
            pontuacoes["Aventura"],
            pontuacoes["Conexão"],
            pontuacoes["Arte"],
            perfil_principal
        ]
        worksheet.append_row(nova_linha)
        st.success("✅ Resposta salva no Google Sheets!")

