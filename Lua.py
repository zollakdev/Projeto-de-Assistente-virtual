import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk

nltk.download('punkt')

audio = sr.Recognizer()
maquina = pyttsx3.init()


def executa_comando():
    try:
        with sr.Microphone() as source:
            print('Ouvindo..')
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'lua' in comando:
                comando = comando.replace('lua', '')
                maquina.say(comando)
                maquina.runAndWait()

    except:
        print('Microfone não está ok')

    return comando


def comando_voz_usuario():
    while True:
        comando = executa_comando()
        if 'parar' in comando:
            break
        if 'horas' in comando:
            hora = datetime.datetime.now().strftime('%H:%M')
            maquina.say('Agora são ' + hora)
            maquina.runAndWait()
            break
        elif 'pesquisar' in comando:
            maquina.say("O que você gostaria de pesquisar?")
            maquina.runAndWait()
            with sr.Microphone() as source:
                print('Ouvindo..')
                voz = audio.listen(source)
                query = audio.recognize_google(voz, language='pt-BR')
                query = query.lower()
            maquina.say("Pesquisando: " + query)
            maquina.runAndWait()
            resultado_wikipedia = wikipedia_search(query)
            resultado_bbc = bbc_search(query)
            if resultado_wikipedia:
                maquina.say("Resumo da Wikipedia:")
                maquina.runAndWait()
                resumo = sumarizar_texto(resultado_wikipedia)
                maquina.say(resumo)
                maquina.runAndWait()
            elif resultado_bbc:
                maquina.say("Resultado da BBC:")
                maquina.runAndWait()
                maquina.say(resultado_bbc)
                maquina.runAndWait()
            else:
                maquina.say("Nenhum resultado encontrado.")
                maquina.runAndWait()
            break
        elif 'toque' in comando:
            musica = comando.replace('toque por', '')
            resultado = pywhatkit.playonyt(musica)
            maquina.say('Tocando música')
            maquina.runAndWait()
            break
        elif 'como você está' in comando:
            maquina.say('Estou bem, obrigado por perguntar. E você?')
            maquina.runAndWait()
            break
        elif 'o que é' in comando:
            maquina.say(wikipedia.summary(comando, 2))
            maquina.runAndWait()
            break
        elif 'o que você sabe sobre' in comando:
            maquina.say(wikipedia.summary(comando, 2))
            maquina.runAndWait()
            break
        elif 'bbc' in comando:
            maquina.say('A BBC é uma empresa de mídia britânica que opera televisão, rádio e serviços online. Foi fundada em 1922 e é uma das maiores empresas de mídia do mundo. A BBC é financiada por uma taxa de licença que é paga por todos os lares com um aparelho de televisão no Reino Unido. A BBC é conhecida por sua programação de alta qualidade e seus altos padrões de jornalismo. A BBC também é uma importante fonte de notícias e informações para o mundo todo.')
            maquina.runAndWait()
        elif 'mais nada' in comando or 'nada obrigado' in comando:
            maquina.say("Eu que agradeço, até a próxima")
            maquina.runAndWait()
            break
        else:
            maquina.say('Não entendi seu comando. Por favor, tente novamente.')
            maquina.runAndWait()

    maquina.say("Fico feliz em ajudar. O que mais posso fazer por você?")
    maquina.runAndWait()


def wikipedia_search(query):
    try:
        wikipedia.set_lang('pt')
        search_results = wikipedia.search(query)
        if search_results:
            page = wikipedia.page(search_results[0])
            return page.content
    except:
        return None


def bbc_search(query):
    try:
        url = 'https://www.bbc.co.uk/search?q=' + query
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_elements = soup.find_all('article')
        if article_elements:
            article = article_elements[0]
            title = article.find('h1').text
            link = article.find('a')['href']
            return f"{title}: {link}"
    except:
        return None


def sumarizar_texto(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer('portuguese'))
    summarizer = LexRankSummarizer()
    resumo = summarizer(parser.document, sentences_count=2)
    return ' '.join(str(sentence) for sentence in resumo)


while True:
    comando_voz_usuario()
    maquina.stop()
