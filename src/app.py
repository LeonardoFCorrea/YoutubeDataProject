from flask import Flask, render_template, request, redirect, url_for
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from transformers import pipeline
import json

app = Flask(__name__)

# Função para extrair o ID do vídeo a partir do link do YouTube
def extract_video_id(url):
    regex_pattern = r'(?:\/|%3D|v=|vi=)([0-9A-Za-z_-]{11})(?:[%#?&]|$)'
    match = re.search(regex_pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Função para calcular o sentimento de um texto usando um modelo de análise de sentimentos
def calculate_sentiment(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)[0]
    sentiment = result['label']
    score = result['score']
    return sentiment, score

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o formulário
@app.route('/analisar', methods=['POST'])
def analisar():
    video_link = request.form['video_link']
    video_link_second = request.form['video_link_second']

    # Extrai o ID do vídeo a partir do link
    video_id = extract_video_id(video_link)
    video_id_second = extract_video_id(video_link_second)

    comments = []
    comments_second = []
    video_name = ''
    video_name_second = ''

    if video_id:
        comments, average_score, positive_percentage, negative_percentage, video_name = process_video(video_id)
    if video_id_second:
        comments_second, average_score_second, positive_percentage_second, negative_percentage_second, video_name_second = process_video(video_id_second)

    return render_template('index.html', comments=comments, average_score=average_score,
                           positive_percentage=positive_percentage, negative_percentage=negative_percentage,
                           video_name=video_name,
                           comments_second=comments_second, average_score_second=average_score_second,
                           positive_percentage_second=positive_percentage_second,
                           negative_percentage_second=negative_percentage_second,
                           video_name_second=video_name_second)

def process_video(video_id):
    # Configura a API do YouTube
    api_key = 'AIzaSyDpTNlBKWJ2RWe7O47EzVkBlnXNkR8GNAg'  # Substitua pela sua própria API Key
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        # Faz a chamada da API para obter os comentários do vídeo
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        ).execute()

        # Processa a resposta da API
        comments = response['items']

        # Ordena os comentários por relevância (número de gostos)
        comments.sort(key=lambda x: x['snippet']['topLevelComment']['snippet']['likeCount'], reverse=True)

        # Seleciona apenas os 10 melhores comentários
        top_comments = comments[:10]

        analyzed_comments = []
        total_score = 0

        for comment in top_comments:
            snippet = comment['snippet']
            author = snippet['topLevelComment']['snippet']['authorDisplayName']
            text = snippet['topLevelComment']['snippet']['textDisplay']

            # Calcula o sentimento do comentário
            sentiment, score = calculate_sentiment(text)

            # Adiciona o comentário e o sentimento à lista
            analyzed_comments.append({'author': author, 'text': text, 'sentiment': sentiment})

            # Soma o score para calcular a média
            total_score += score

        # Calcula a média de sentimentos
        average_score = total_score / len(top_comments)
        average_score_formatted = '{:.2f}'.format(average_score * 100)

        # Calcula o percentual de comentários positivos e negativos
        positive_percentage = sum(comment['sentiment'] == 'POSITIVE' for comment in analyzed_comments) / len(
            analyzed_comments) * 100
        negative_percentage = 100 - positive_percentage

        # Obtém o nome do vídeo usando a API do YouTube
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        video_name = video_response['items'][0]['snippet']['title']

        return analyzed_comments, average_score_formatted, positive_percentage, negative_percentage, video_name

    except HttpError as e:
        error_message = e.content.decode('utf-8')
        return [], None, None, None, None

@app.route('/feedPalavras', methods=['GET', 'POST'])
def feed_palavras():
    if request.method == 'POST':
        palavra = request.form['palavras_frequentes']
        
        # Configurar a API do YouTube
        api_key = 'AIzaSyDpTNlBKWJ2RWe7O47EzVkBlnXNkR8GNAg'
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Realizar a busca dos vídeos com base na palavra-chave
        search_request = youtube.search().list(
            q=palavra,
            part='snippet',
            type='video',
            order='viewCount',
            maxResults=10
        )
        response = search_request.execute()
        
        videos = []
        
        # Extrair informações relevantes dos vídeos
        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            
            videos.append({
                'titulo': video_title,
                'url': video_url
            })
        
        return render_template('feedPalavras.html', palavra=palavra, videos=videos)
    
    return render_template('feedPalavras.html')

if __name__ == '__main__':
    app.run(debug=True)