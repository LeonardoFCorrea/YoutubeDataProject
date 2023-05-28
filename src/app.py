from flask import Flask, render_template, request
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from transformers import pipeline

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

    # Extrai o ID do vídeo a partir do link
    video_id = extract_video_id(video_link)

    if video_id:
        # Configura a API do YouTube
        api_key = 'AIzaSyAjABpgnQ6QLsLss7EDF9iRNz2kD0QT8Y8'  # Substitua pelo seu próprio API Key
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
            positive_percentage = sum(comment['sentiment'] == 'POSITIVE' for comment in analyzed_comments) / len(analyzed_comments) * 100
            negative_percentage = 100 - positive_percentage

            return render_template('index.html', comments=analyzed_comments, average_score=average_score_formatted,
                                   positive_percentage=positive_percentage, negative_percentage=negative_percentage)

        except HttpError as e:
            error_message = e.content.decode('utf-8')
            return render_template('index.html', error_message=error_message)
    else:
        error_message = 'O link do vídeo é inválido'
        return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run()
