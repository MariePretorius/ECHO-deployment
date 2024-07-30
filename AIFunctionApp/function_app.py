import csv
import os
import json

import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import classification
import utils
from genre_prediction import predict_genre, get_album_genre
from cluster import recommend_songs

CSV_FILE_PATH = 'expanded_details.csv'

MIN_RECOMMENDATIONS = 10
INITIAL_SONGS_REQUESTED = 50

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_songs")
def get_songs(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    provided_key = req_body.get('access_key')

    if ACCESS_KEY != provided_key:
        return func.HttpResponse(
            json.dumps({"error": "Unauthorized access. Invalid access key."}),
            mimetype="application/json",
            status_code=401
        )
    
    try:
        song_name = req_body.get("song_name")
        artist = req_body.get("artist")

        if not song_name or not artist:
            return func.HttpResponse(
                json.dumps({"error": "Please provide both song_name and artist."}),
                mimetype="application/json",
                status_code=400
            )
        
        track_name = song_name
        artist_name = artist

        if os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

            song_row = next((row for row in data if row['Song Name'] == track_name and row['Artist'] == artist_name), None)

            if song_row:
                track_id = song_row['Track ID']
                song_features = eval(song_row['Song Features'])
                cluster_number = song_row['Cluster Number']
                emotion = song_row['Emotion']
                predicted_genre = song_row['Predicted Genre']
                album_genre = song_row['Album Genre']
            else:
                track_id = utils.get_track_id(track_name, artist_name)
                song_features = utils.get_song_features(track_id)
                cluster_number = utils.get_cluster(track_name, artist_name)
                emotion = classification.run_lyric_analysis(song_name, artist_name)
                predicted_genre = predict_genre(track_name, artist_name)
                album_genre = get_album_genre(track_name, artist_name)

                update_csv(track_name, artist_name, track_id, song_features, cluster_number, emotion, predicted_genre, album_genre)

            cluster_songs = recommend_songs(song_features)
            print("cluster songs found")
            print("Cluster Number: ", cluster_number)
            print("Emotion: ", emotion)
            print("Predicted Genre: ", predicted_genre)
            print("Album Genre: ", album_genre)

            similar_songs = process_similar_songs(cluster_songs, artist_name, emotion, predicted_genre, album_genre)

            i = 2
            while len(similar_songs) < MIN_RECOMMENDATIONS:
                additional_songs_needed = MIN_RECOMMENDATIONS - len(similar_songs)

                if additional_songs_needed > 0:
                    more_cluster_songs = recommend_songs(song_features, n_recommendations=INITIAL_SONGS_REQUESTED * i)
                    print("More recommendations needed, pulling " + str(INITIAL_SONGS_REQUESTED * i) + " more songs")
                    i = i + 1

                    more_similar_songs = process_similar_songs(more_cluster_songs, artist_name, emotion, predicted_genre, album_genre)
                    similar_songs.extend(more_similar_songs[:additional_songs_needed])

            return func.HttpResponse(
            json.dumps({"recommended_tracks": similar_songs}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )


processed_songs = set()


def process_similar_songs(songs, song_artist, song_emotion, song_predicted_genre, song_album_genre):
    similar_songs = []

    for song in songs:
        if len(processed_songs) >= MIN_RECOMMENDATIONS:
            break

        if song in processed_songs:
            continue

        if os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

            song_name, artist_name = utils.get_track_details(song)
            if not song_name or not artist_name:
                continue

            song_row = next((row for row in data if row['Song Name'] == song_name and row['Artist'] == artist_name), None)

            print("processing " + song_name + " by " + artist_name)

            if song_row:
                track_id = song_row.get('Track ID')
                song_features = eval(song_row['Song Features']) if 'Song Features' in song_row else None
                cluster_number = song_row.get('Cluster Number')
                emotion = song_row.get('Emotion')
                predicted_genre = song_row.get('Predicted Genre')
                album_genre = song_row.get('Album Genre')
            else:
                track_id = utils.get_track_id(song_name, artist_name)
                song_features = utils.get_song_features(track_id)
                cluster_number = utils.get_cluster(song_name, artist_name)
                emotion = classification.run_lyric_analysis(song_name, artist_name)
                predicted_genre = predict_genre(song_name, artist_name)
                print("predicted genre found")
                album_genre = get_album_genre(song_name, artist_name)

                update_csv(song_name, artist_name, track_id, song_features, cluster_number, emotion, predicted_genre, album_genre)

            if track_id is None:
                continue

            if artist_name == song_artist:
                if track_id:
                    similar_songs.append("spotify:track:" + track_id)
                    processed_songs.add(song)
                    if song_name and artist_name:
                        print(song_name + " by " + artist_name + " added")
            else:
                if emotion and song_emotion:
                    emotion, song_emotion = emotion.lower(), song_emotion.lower()
                if predicted_genre and song_predicted_genre:
                    predicted_genre, song_predicted_genre = predicted_genre.lower(), song_predicted_genre.lower()
                if album_genre and song_album_genre:
                    album_genre, song_album_genre = utils.map_deezer_genre_to_model_genre(album_genre), utils.map_deezer_genre_to_model_genre(song_album_genre)

                similar_predicted_genre = False
                similar_song_emotion = False
                similar_album_genre = False
                similar_genre_1 = False
                similar_genre_2 = False

                if predicted_genre and song_predicted_genre:
                    similar_predicted_genre = (predicted_genre == song_predicted_genre)
                if album_genre and song_album_genre:
                    similar_album_genre = (album_genre == song_album_genre)
                if predicted_genre and song_album_genre:
                    similar_genre_1 = (predicted_genre == song_album_genre)
                if album_genre and song_predicted_genre:
                    similar_genre_2 = (album_genre == song_predicted_genre)

                if emotion and song_emotion:
                    distance = utils.emotional_similarity[emotion][song_emotion]
                    if distance >= 7:
                        similar_song_emotion = True

                if (similar_predicted_genre or similar_album_genre or similar_genre_1 or similar_genre_2) and similar_song_emotion:
                    if track_id:
                        similar_songs.append("spotify:track:" + track_id)
                        processed_songs.add(song)
                        if song_name and artist_name:
                            print(song_name + " by " + artist_name + " added")

    return similar_songs


def update_csv(song_name, artist_name, track_id, song_features, cluster_number, emotion, predicted_genre, album_genre):
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    else:
        data = []

    if not any(row['Song Name'] == song_name and row['Artist'] == artist_name for row in data):
        with open(CSV_FILE_PATH, mode='a', newline='') as csvfile:
            fieldnames = ['Song Name', 'Artist', 'Track ID', 'Song Features', 'Cluster Number', 'Emotion',
                          'Predicted Genre', 'Album Genre']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if os.stat(CSV_FILE_PATH).st_size == 0:
                writer.writeheader()

            writer.writerow({
                'Song Name': song_name,
                'Artist': artist_name,
                'Track ID': track_id,
                'Song Features': str(song_features),
                'Cluster Number': cluster_number,
                'Emotion': emotion,
                'Predicted Genre': predicted_genre,
                'Album Genre': album_genre
            })
