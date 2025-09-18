import streamlit as st
import random
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import datetime
import plotly.express as px

st.set_page_config(page_title="Quiz SOU+ Big Bang", layout="centered")
st.title("🎮 Descubra seu perfil SOU+ Big Bang Rio")
st.markdown("""
**SOU+ é a Energia Que Move Cada Um de Nós**

Todos nós temos algo especial que nos move: uma forma única de pensar, agir ou se conectar.  
Cada cor dá visibilidade às diferentes forças que compõem cada pessoa.  

O SOU+ é a nossa forma de mapear essas forças, de um jeito leve, e integrado a toda experiência do Big Bang deste ano.  
**E aí? Pronto(a) para descobrir o seu perfil SOU+?**
""")

# Entrada de nome
nome = st.text_input("Digite seu nome igual ao que está no People Force")


quiz_perguntas = [

    ("Quando aparece um desafio novo, você:", [
        ("Busca uma forma criativa e diferente de resolver", "Arte"),
        ("Pede ajuda ou troca ideias", "Conexão"),
        ("Testa na prática e ajusta no caminho", "Aventura"),
        ("Analisa e planeja a solução", "Geek")
    ]),

    ("Qual dessas matérias da escola mais te atraía?", [
        ("História ou sociologia", "Conexão"),
        ("Educação física", "Aventura"),
        ("Artes ou literatura", "Arte"),
        ("Matemática ou ciências exatas", "Geek")
    ]),

    ("Para tomar uma decisão, você prefere:", [
        ("Imaginar cenários criativos", "Arte"),
        ("Conversar e alinhar com pessoas", "Conexão"),
        ("Intuição e impulso", "Aventura"),
        ("Dados e lógica", "Geek")
    ]),

    ("Diante de uma tarefa difícil, você:", [
        ("Reinventa o jeito de fazer", "Arte"),
        ("Busca parceria para compartilhar", "Conexão"),
        ("Vai tentando até dar certo", "Aventura"),
        ("Divide em etapas lógicas", "Geek")
    ]),

    ("Seu maior talento está em:", [
        ("Criar laços fortes com pessoas", "Conexão"),
        ("Superar desafios físicos", "Aventura"),
        ("Ter ideias originais", "Arte"),
        ("Resolver problemas", "Geek")
    ]),

    ("Se fosse jogar um game, você escolheria:", [
        ("Criativo/sandbox", "Arte"),
        ("De corrida/ação", "Aventura"),
        ("Multiplayer cooperativo", "Conexão"),
        ("De estratégia/puzzle", "Geek")
    ]),

    ("Num imprevisto, você costuma:", [
        ("Improvisar com criatividade", "Arte"),
        ("Calcular opções antes de agir", "Geek"),
        ("Agir rápido e corrigir depois", "Aventura"),
        ("Procurar apoio das pessoas", "Conexão")
    ]),

    ("Quando tem tempo livre, você prefere:", [
        ("Ir a um show, cinema ou oficina criativa", "Arte"),
        ("Sair com amigos/família", "Conexão"),
        ("Praticar um esporte", "Aventura"),
        ("Ler ou estudar algo novo", "Geek")
    ]),

    ("Seu hobby ideal é:", [
        ("Pintura, música ou dança", "Arte"),
        ("Surf, corrida ou trekking", "Aventura"),
        ("Montar quebra-cabeças, xadrez ou programação", "Geek"),
        ("Jantar com amigos, jogos de grupo", "Conexão")
    ]),

    ("Se tivesse que montar uma barraca de camping, você:", [
        ("Chamaria amigos para montar juntos", "Conexão"),
        ("Improvisaria com o que tivesse", "Arte"),
        ("Leria o manual e organizaria", "Geek"),
        ("Montaria tentando na prática", "Aventura")
    ]),

    ("Em uma roda de conversa, você costuma ser:", [
        ("O que faz piadas e anima", "Arte"),
        ("O que conta histórias de aventuras", "Aventura"),
        ("O que escuta e conecta as pessoas", "Conexão"),
        ("O que faz perguntas inteligentes", "Geek")
    ]),

    ("O que mais te dá energia em um evento como o Big Bang?", [
        ("Estar junto do time", "Conexão"),
        ("As expressões culturais e artísticas", "Arte"),
        ("Os desafios que exigem raciocínio", "Geek"),
        ("As atividades esportivas", "Aventura")
    ]),

    ("Em um sorteio de atividade, você adoraria pegar:", [
        ("Um jogo de colaboração", "Conexão"),
        ("Uma corrida ou prova física", "Aventura"),
        ("Uma competição de dança", "Arte"),
        ("Um quiz de lógica", "Geek")
    ]),

    ("O que mais te deixa satisfeito ao final de uma atividade?", [
        ("Ter criado algo memorável", "Arte"),
        ("Ter dado o máximo de energia", "Aventura"),
        ("Ter resolvido de forma inteligente", "Geek"),
        ("Ter unido o grupo", "Conexão")
    ]),

    ("Quando conhece alguém novo, você:", [
        ("Faz perguntas técnicas ou curiosas", "Geek"),
        ("Propõe uma atividade ou esporte", "Aventura"),
        ("Usa humor ou criatividade", "Arte"),
        ("Procura algo em comum", "Conexão")
    ]),

    ("Viagem dos sonhos:", [
        ("Festival de música e cultura", "Arte"),
        ("Um mochilão com amigos", "Conexão"),
        ("Explorar trilhas e natureza", "Aventura"),
        ("Conhecer museus ou centros tecnológicos", "Geek")
    ]),

    ("Se fosse escolher um objeto para levar para o Big Bang:", [
        ("Um instrumento musical", "Arte"),
        ("Um livro ou gadget", "Geek"),
        ("Um baralho/jogo de grupo", "Conexão"),
        ("Um tênis esportivo", "Aventura")
    ]),

    ("Sua refeição favorita é:", [
        ("Churrasco, lanche ou energético", "Aventura"),
        ("Uma comida exótica e colorida", "Arte"),
        ("Um prato compartilhado com amigos", "Conexão"),
        ("Algo saudável e prático", "Geek")
    ]),

    ("Um lugar no Rio que mais combina com você:", [
        ("Lapa", "Conexão"),
        ("Museu do Amanhã", "Geek"),
        ("Sambódromo", "Arte"),
        ("Pedra da Gávea", "Aventura")
    ]),

    ("Estilo musical que te move:", [
        ("MPB, samba de roda", "Conexão"),
        ("Rock, reggae ou esportivo/vibrante", "Aventura"),
        ("Eletrônica ou clássica", "Geek"),
        ("Samba-enredo, funk, axé", "Arte")
    ]),

    ("Um superpoder que você gostaria de ter:", [
        ("Criar realidades", "Arte"),
        ("Ler emoções das pessoas", "Conexão"),
        ("Inteligência ilimitada", "Geek"),
        ("Superforça/velocidade", "Aventura")
    ]),

    ("Se tivesse que escolher um símbolo para você:", [
        ("Um cérebro", "Geek"),
        ("Uma estrela", "Arte"),
        ("Um coração", "Conexão"),
        ("Um raio", "Aventura")
    ]),

    ("O que mais te motiva num projeto:", [
        ("Criar algo original", "Arte"),
        ("Ver o grupo junto", "Conexão"),
        ("Resolver algo complexo", "Geek"),
        ("Sentir adrenalina e ação", "Aventura")
    ]),

    ("Uma qualidade que mais reconhecem em você:", [
        ("Inteligência", "Geek"),
        ("Criatividade", "Arte"),
        ("Energia", "Aventura"),
        ("Empatia", "Conexão")
    ]),

    ("Um elogio que você adora ouvir:", [
        ("Você é muito criativo", "Arte"),
        ("Você inspira confiança", "Conexão"),
        ("Você é muito estratégico", "Geek"),
        ("Você tem muita disposição", "Aventura")
    ]),

    ("Em uma corrida de equipe, você seria:", [
        ("O que corre mais rápido", "Aventura"),
        ("O que ajuda o mais lento", "Conexão"),
        ("O que organiza a estratégia", "Geek"),
        ("O que faz torcida animada", "Arte")
    ]),

    ("Numa gincana de perguntas, você:", [
        ("Incentiva quem está inseguro", "Conexão"),
        ("Dá respostas criativas e engraçadas", "Arte"),
        ("Assume a liderança para responder", "Geek"),
        ("Arrisca mesmo sem certeza", "Aventura")
    ]),

    ("Se uma atividade for cancelada de última hora, você:", [
        ("Propõe um jogo em grupo", "Conexão"),
        ("Cria uma dinâmica diferente", "Arte"),
        ("Puxa outra atividade esportiva", "Aventura"),
        ("Pensa em outra solução", "Geek")
    ]),

    ("Ao ouvir uma música contagiante, você:", [
        ("Inventa passos criativos", "Arte"),
        ("Analisa a letra/ritmo", "Geek"),
        ("Chama alguém para dançar junto", "Conexão"),
        ("Começa a se mexer", "Aventura")
    ]),

    ("O que você mais gostaria de deixar marcado no Big Bang 2025?", [
        ("Uma amizade verdadeira", "Conexão"),
        ("Uma vitória esportiva", "Aventura"),
        ("Uma apresentação memorável", "Arte"),
        ("Uma solução inteligente num desafio", "Geek")
    ])
]


# Pontuação
pontuacoes = {"Geek": 0, "Aventura": 0, "Conexão": 0, "Arte": 0}
respostas = []

st.markdown("---")
st.markdown("## Responda às perguntas:")

for i, (pergunta, opcoes) in enumerate(quiz_perguntas):
    random.shuffle(opcoes)
    escolha = st.radio(pergunta, [alt for alt, _ in opcoes], key=f"pergunta_{i}")
    for alt, perfil in opcoes:
        if alt == escolha:
            pontuacoes[perfil] += 1
            respostas.append((pergunta, alt, perfil))

# Desempate se necessário
max_score = max(pontuacoes.values())
principais = [p for p, v in pontuacoes.items() if v == max_score]

if len(principais) > 1:
    st.warning("Houve um empate! Responda a pergunta extra para desempate:")
    opcao_desempate = st.radio(
        "Qual dessas frases mais representa você agora?",
        [
            "Prefiro resolver com lógica e planejamento",
            "Prefiro ação e movimento",
            "Prefiro estar junto das pessoas",
            "Prefiro me expressar de forma criativa"
        ],
        key="desempate"
    )
    if "lógica" in opcao_desempate:
        pontuacoes["Geek"] += 1
    elif "movimento" in opcao_desempate:
        pontuacoes["Aventura"] += 1
    elif "pessoas" in opcao_desempate:
        pontuacoes["Conexão"] += 1
    elif "criativa" in opcao_desempate:
        pontuacoes["Arte"] += 1

# Botão para exibir o resultado
if st.button("Ver meu perfil") and nome:
    total = sum(pontuacoes.values())
    porcentagens = {p: round((v / total) * 100, 1) for p, v in pontuacoes.items()}
    perfil_principal = max(pontuacoes, key=pontuacoes.get)

    descricoes = {
        "Geek": "💙 Sua cor é o Azul\n\nO cérebro do time. Analítico, curioso, resolve problemas e domina o conhecimento.",
        "Aventura": "💚 Sua cor é o Verde\n\nO desbravador. Ama movimento, desafios físicos e ambientes inesperados.",
        "Conexão": "🩷 Sua cor é o Rosa\n\nA base do time. Une pessoas, cuida do grupo e garante colaboração.",
        "Arte": "💛 Sua cor é o Amarelo\n\nA alma criativa. Expressivo, contagia com energia, empolgação e dá ritmo às experiências."
    }

    st.subheader(f"Seu perfil principal é: SOU+ {perfil_principal}")
    st.markdown(descricoes[perfil_principal])

    # Gráfico de barras
    st.markdown("### Distribuição dos seus perfis:")
    df = pd.DataFrame.from_dict(pontuacoes, orient='index', columns=['Pontos'])
    df.reset_index(inplace=True)
    df.columns = ['Perfil', 'Pontos']
    df['%'] = df['Pontos'] / total * 100
    fig = px.bar(df, x='Perfil', y='%', color='Perfil', text='%', height=400)
    st.plotly_chart(fig)

    # Salvar no Google Sheets
    try:
        secrets = st.secrets["gcp_service_account"]
        creds = service_account.Credentials.from_service_account_info(secrets)
        cliente = gspread.authorize(creds)
        planilha = cliente.open("Respostas SOU+ BBB25")
        aba = planilha.worksheet("Respostas SOU+")
        aba.append_row([
            nome,
            str(datetime.datetime.now()),
            perfil_principal,
            porcentagens["Geek"],
            porcentagens["Aventura"],
            porcentagens["Conexão"],
            porcentagens["Arte"]
        ])
        st.success("Resultado salvo com sucesso no Google Sheets!")
    except Exception as e:
        st.error(f"Erro ao salvar na planilha: {e}")

elif nome == "":
    st.info("Por favor, preencha seu nome para ver o resultado.")
