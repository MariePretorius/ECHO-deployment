import requests
from pydub import AudioSegment
import os
import librosa
import numpy as np
from transformers import pipeline


def get_deezer_preview_url(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    url = f"https://api.deezer.com/search?q={query}"
    response = requests.get(url)
    data = response.json()

    if data['total'] > 0:
        preview_url = data['data'][0]['preview']
        return preview_url
    else:
        raise Exception("No results found on Deezer for the given song and artist.")


def download_and_convert_to_wav(audio_url, output_path):
    response = requests.get(audio_url)
    with open('temp.mp3', 'wb') as file:
        file.write(response.content)

    audio = AudioSegment.from_file('temp.mp3', format='mp3')
    audio.export(output_path, format='wav')
    os.remove('temp.mp3')


def predict_genre(song_name, artist_name):
    preview_url = get_deezer_preview_url(song_name, artist_name)
    output_path = 'song.wav'
    download_and_convert_to_wav(preview_url, output_path)

    audio_classification = pipeline("audio-classification", model="dima806/music_genres_classification")
    genre_prediction = audio_classification(output_path)

    os.remove(output_path)

    return genre_prediction[0]['label']
