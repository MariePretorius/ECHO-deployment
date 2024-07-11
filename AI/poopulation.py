import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from classification.classification import run_lyric_analysis
from clustering.cluster import get_cluster_number
from genre_prediction.genre_prediction import predict_genre, get_album_genre

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)


def extract_uris(file_path):
    uris = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uris.append(row)
    return uris


def load_data():
    file_path = 'clustered_music_data.csv'
    uris = extract_uris(file_path)
    return uris


def get_track_details(uri):
    if uri:
        track_id = uri.split(':')[-1]
        track_info = sp.track(track_id)
        track_name = track_info['name']
        artist_name = track_info['album']['artists'][0]['name'] if track_info['album']['artists'] else 'Unknown Artist'
        print("Track Name: " + track_name)
        print("Artist: " + artist_name)
        return track_name, artist_name


def get_song_features(track_id):
    if track_id:
        features = sp.audio_features(track_id)
        if features:
            print(features[0])
            return features[0]
        else:
            return None


def get_track_id(track_name, artist_name):
    results = sp.search(q=f'track:{track_name} artist:{artist_name}', type='track')
    items = results['tracks']['items']

    if items:
        return items[0]['id']
    else:
        return None


def process_all_lyrics(uris):
    if uris:
        moods = []
        for uri in uris:
            song_name, artist = get_track_details(uri)
            mood = run_lyric_analysis(song_name, artist)
            moods.append(mood)
            print("Mood: " + mood)
        return moods


def get_song_clusters(uri):
    if uri:
        song_name, artist = get_track_details(uri)
        song_id = get_track_id(song_name, artist)
        song_features = get_song_features(song_id)
        if song_features:
            cluster = get_cluster_number(song_features)
            print(song_id + " processed")
            return cluster


def predict_all_genres(uris):
    if uris:
        predicted_genres = []
        for uri in uris:
            song_name, artist = get_track_details(uri)
            predicted_genre = predict_genre(song_name, artist)
            predicted_genres.append(predicted_genre)
            print("Predicted Genre: " + predicted_genre)
        return predicted_genres


def get_album_genres(uris):
    if uris:
        album_genres = []
        for uri in uris:
            song_name, artist = get_track_details(uri)
            album_genre = get_album_genre(song_name, artist)
            album_genres.append(album_genre)
            print("Album Genre: " + album_genre)
        return album_genres


def process_batch(uris, cluster_num, batch_num):
    output_file = f'expanded_music_data_cluster_{cluster_num}_batch_{batch_num}.csv'
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['uri', 'track_name', 'artist_name', 'mood', 'predicted_genre', 'album_genre']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for uri in uris:
            track_name, artist_name = get_track_details(uri)
            mood = run_lyric_analysis(track_name, artist_name)
            print("Mood: " + mood)
            predicted_genre = predict_genre(track_name, artist_name)
            print("Predicted Genre: " + predicted_genre)
            album_genre = get_album_genre(track_name, artist_name)
            print("Album Genre: " + album_genre)

            writer.writerow({
                'uri': uri,
                'track_name': track_name,
                'artist_name': artist_name,
                'mood': mood,
                'predicted_genre': predicted_genre,
                'album_genre': album_genre
            })
            print(f"{uri} for cluster {cluster_num} batch {batch_num} done")


def populate_dataset():
    full_dataset = load_data()

    batch_size = 500

    uris = [row['uri'] for row in full_dataset if int(float(row['Cluster'])) == 1]

    for i in range(0, len(uris), batch_size):
        batch_uris = uris[i:i + batch_size]
        batch_num = i // batch_size + 1
        process_batch(batch_uris, 1, batch_num)
        print(f"Batch {batch_num} for cluster {1} done")
