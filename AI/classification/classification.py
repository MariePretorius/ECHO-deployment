import re
import os
import requests
from transformers import pipeline
from bs4 import BeautifulSoup

CLIENT_ID = os.environ.get('DEEZER_CLIENT_ID')
CLIENT_SECRET = os.environ.get('DEEZER_CLIENT_SECRET')
ACCESS_TOKEN = os.environ.get('DEEZER_ACCESS_TOKEN')

classifier_path = 'classifier_model'


def save_classifier(classifier, path):
    classifier.model.save_pretrained(path)
    classifier.tokenizer.save_pretrained(path)


def load_classifier():
    if os.path.exists(classifier_path):
        classifier = pipeline(task="text-classification", model=classifier_path, tokenizer=classifier_path, top_k=None)
    else:
        classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
        save_classifier(classifier, classifier_path)
    return classifier


def process_lyrics(text):
    text = text.replace('\\', '\n')
    text = re.sub(r'\[.*?\]', '\n', text)

    lines = []
    current_line = []

    words = text.split()
    for word in words:
        if word and word[0].isupper() and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    if current_line:
        lines.append(' '.join(current_line))

    processed_text = ' '.join(lines)
    return processed_text


def get_highest_score_label(model_outputs):
    highest_score = -1
    highest_label = None

    for output in model_outputs:
        if output['score'] > highest_score:
            highest_score = output['score']
            highest_label = output['label']

    return highest_label


def get_lyrics_url(song_name, artist_name):
    base_url = "https://api.genius.com"
    headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
    search_url = base_url + "/search"
    data = {'q': song_name + ' ' + artist_name}
    response = requests.get(search_url, headers=headers, data=data)
    response_data = response.json()

    path = response_data['response']['hits'][0]['result']['path']
    lyrics_url = "https://genius.com" + path

    return lyrics_url


def get_lyrics(song_name, artist_name):
    song_api_path = get_lyrics_url(song_name, artist_name)

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    song_url = song_api_path
    print("Song URL: ", song_url)

    response = requests.get(song_url, headers=headers)
    # print("Response: ", response.text)

    if response.status_code != 200:
        print(f"Failed to retrieve lyrics. Status code: {response.status_code}")
        return None

    html = BeautifulSoup(response.content, "html.parser")
    [h.extract() for h in html('script')]

    lyric_containers = html.find_all("div", attrs={"data-lyrics-container": "true"})

    lyrics_list = []
    for container in lyric_containers:
        lyrics_list.append(container.get_text().strip())

    return lyrics_list


def run_lyric_analysis(song_name, artist):
    classifier = load_classifier()

    lyrics = get_lyrics(song_name, artist)

    for lyric in lyrics:
        lyric = process_lyrics(lyric)
        print(lyric)
        print()

    # model_outputs = classifier(lyrics)
    # scores = model_outputs[0]
    # print(scores)
    # label = get_highest_score_label(scores)
    # print("Emotion: " + label)
    # return label


run_lyric_analysis("Style", "Taylor Swift")
