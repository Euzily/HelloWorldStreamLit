import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
from io import StringIO
from PIL import Image
import pdfplumber
import os
import pandas as pd
from itertools import islice
import nltk
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import Counter


def processar_texto(texto):
  # Remoção de caracteres especiais
  texto = re.sub(r'[^\w\s]', '', texto)
  palavras = texto.lower().split()
  
  # Contagem de frequência das palavras
  freq_palavras = Counter(palavras)
  palavras_frequentes_ordenadas = freq_palavras.most_common(num_palavras)    
  palavras_top = [palavra[0] for palavra in palavras_frequentes_ordenadas[0:29]]
  palavras_freq = [palavra[1] for palavra in palavras_frequentes_ordenadas[0:29]]
  fig=go.Figure(go.Bar(x=palavras_top, y=palavras_freq, text=palavras_freq, textposition='outside'))  
  fig.update_layout(autosize=False, width=1000, height=500, title_text='Palavras mais frequentes')
  fig.update_xaxes(tickangle = -45)
  #fig.show()   
  # Nuvem de palavras
  nuvem_palavras = WordCloud(width=800, height=400, background_color ='white').generate(texto)
  return fig, nuvem_palavras

def remocao_stopwords(texto):
  regex_token = '\w+'
  tokens = re.findall(regex_token, texto)
  tokens_limpos = []
  for item in tokens:
    if (item not in stopwords) and (len(item) > 2):
      tokens_limpos.append(item)

  palavras_frequentes_ordenadas = Counter(tokens_limpos).most_common(num_palavras)
  words_tokens = [palavra[0] for palavra in palavras_frequentes_ordenadas[:29]]
  freq_tokens = [palavra[1] for palavra in palavras_frequentes_ordenadas[:29]]
  fig_stopwords = go.Figure(go.Bar(x=words_tokens, y=freq_tokens, text=freq_tokens, textposition='outside'))
  fig_stopwords.update_layout(autosize=False, width=1000, height=500, title_text='Palavras mais utilizadas sem as Stopwords')
  fig_stopwords.update_xaxes(tickangle=-45)

  nuvem_palavras_stopwords = WordCloud(width=800, height=400, background_color='white').generate(' '.join(tokens_limpos))
  return fig_stopwords, nuvem_palavras_stopwords


def texto_url(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  paragraphs = soup.find_all('p')
  texto = ' '.join([p.get_text() for p in paragraphs])
  return texto
  
def texto_pdf(pdf):
  pdf = pdfplumber.open(pdf)
  page = pdf.pages[0]
  page.page_number
  todas_paginas = ''
  page = pdf.pages[0]
  for page in pdf.pages:
    todas_paginas = todas_paginas + page.extract_text()
    todas_paginas = todas_paginas + ' '
  return todas_paginas

foto = Image.open('teste_imagem.png')
st.image(foto, caption='', use_column_width=True)

st.title("Análise de Textos")
st.subheader("Descubra a frequência das palavras mais usadas no texto!")
st.write("Este notebook tem o intuito de realizar uma análise descritiva básica de textos importados pelo usuário nos formatos: PDF, um link de página ou um texto direto.")
st.write("Se quiser aprender mais sobre a análise descritiva, [clique aqui!](https://cinnecta.com/conteudos/analise-descritiva/#:~:text=A%20an%C3%A1lise%20descritiva%20utiliza%20gr%C3%A1ficos,p%C3%BAblico%20de%20forma%20mais%20precisa.)")

st.write("---")

st.subheader('Escolha da quantia de Palavras')
qtd_palavras = st.selectbox("Quantas palavras você gostaria de analisar a frequência no texto?", ["10", "15", "20", "30"])
num_palavras = int(qtd_palavras)

st.write("---")
st.header('Stopwords')
st.write('Para uma análise mais otimizada da frequência de palavras do texto devemos tomar cuidado com as Stopwords, palavras que podem ser suprimidas (ocultadas ou omitidas) sem comprometer o sentido.')
st.write('Algumas Stopwords do Português: ')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')
st.write(stopwords)
 
  
st.write("---")
st.header('Entrada do Texto')
st.write("Selecione a forma que gostaria de inserir seu texto a ser analisado: ")
resposta = st.radio("Em que formato gostaria de inserir o texto?", ('Arquivo PDF','URL de uma página','Texto direto'))

if resposta == 'Arquivo PDF':
  arquivo_usuario = st.file_uploader("Selecione um arquivo PDF", type="pdf")
  if arquivo_usuario is not None:
    resposta_stopword = st.radio("Deseja realizar a análise sem Stopwords?", ('Sim', 'Não'))
    if resposta_stopword == 'Sim':
      texto_pdf = texto_pdf(arquivo_usuario)
      st.write("Texto extraído do PDF:")
      st.write(texto_pdf)
      top_palavras, nuvem_palavras = remocao_stopwords(texto_pdf)
      st.subheader("Palavras mais frequentes:")
      st.write(top_palavras)
      st.subheader("Nuvem de Palavras:")
      st.image(nuvem_palavras.to_array())
      
    elif resposta_stopword == 'Não':
      texto_pdf = texto_pdf(arquivo_usuario)
      st.write("Texto extraído do PDF:")
      st.write(texto_pdf)
      top_palavras, nuvem_palavras = processar_texto(texto_pdf)
      st.subheader("Palavras mais frequentes:")
      st.write(top_palavras)
      st.subheader("Nuvem de Palavras:")
      st.image(nuvem_palavras.to_array())

elif resposta == 'URL de uma página':
  arquivo_usuario = st.text_input("Digite o link da página:")
  if arquivo_usuario:
    resposta_stopword = st.radio("Deseja realizar a análise sem Stopwords?", ('Sim', 'Não'))
    if resposta_stopword == 'Sim':
      texto_url = texto_url(arquivo_usuario)
      st.write("Texto extraído da página:")
      st.write(texto_url)
      top_palavras, nuvem_palavras = remocao_stopwords(texto_url)
      st.subheader("Palavras mais frequentes:")
      st.write(top_palavras)
      st.subheader("Nuvem de Palavras:")
      st.image(nuvem_palavras.to_array())
      
    elif resposta_stopword == 'Não':
      texto_url = texto_url(arquivo_usuario)
      st.write("Texto extraído da página:")
      st.write(texto_url)
      top_palavras, nuvem_palavras = processar_texto(texto_url)
      st.subheader("Palavras mais frequentes:")
      st.write(top_palavras)
      st.subheader("Nuvem de Palavras:")
      st.image(nuvem_palavras.to_array())

elif resposta == 'Texto direto':
  arquivo_usuario = st.text_area("Cole o texto aqui:")
  if arquivo_usuario:
    resposta_stopword = st.radio("Deseja realizar a análise sem Stopwords?", ('Sim', 'Não'))
    if resposta_stopword == 'Sim':
      top_palavras, nuvem_palavras = remocao_stopwords(arquivo_usuario)
      st.subheader("Palavras mais frequentes:")
      st.write(top_palavras)
      st.subheader("Nuvem de Palavras:")
      st.image(nuvem_palavras.to_array())
      
    elif resposta_stopword == 'Não':
      top_palavras, nuvem_palavras = processar_texto(arquivo_usuario)
      st.subheader("Palavras mais frequentes:")
      st.write(top_palavras)
      st.subheader("Nuvem de Palavras:")
      st.image(nuvem_palavras.to_array())
