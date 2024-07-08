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


def split_lyrics(text):
    verse_sections = re.split(r'\[\s*Verse\s*\d*\s*\]', text)
    pre_chorus_sections = re.split(r'\[\s*Pre-Chorus\s*\]', ' '.join(verse_sections))
    chorus_sections = re.split(r'\[\s*Chorus\s*\]', ' '.join(pre_chorus_sections))

    all_sections = []
    for section in chorus_sections:
        if section.strip():
            all_sections.append(section.strip())

    return all_sections


def process_lyrics(text):
    text = text.replace('\\', '\n')
    text = text.replace('[Chorus]', '\n')
    text = text.replace('[Pre-Chorus]', '\n')
    text = re.sub(r'\[Verse.*?\]', '\n', text)

    lines = []
    current_line = []

    i = 0
    while i < len(text):
        while i < len(text) and text[i].isspace():
            i += 1

        word_start = i
        while i < len(text) and not text[i].isspace():
            current_line.append(text[i])
            i += 1

        if len(current_line) > 1:
            for j in range(1, len(current_line)):
                if current_line[j].isupper():
                    current_line.insert(j, ' ')
                    break

        if current_line:
            lines.append(''.join(current_line))
            current_line = []

    if current_line:
        lines.append(''.join(current_line))

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
