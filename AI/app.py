import csv
import os

import classification.classification
import processing
from genre_prediction.genre_prediction import predict_genre, get_album_genre
from clustering.cluster import recommend_songs

CSV_FILE_PATH = 'expanded_details.csv'

MIN_RECOMMENDATIONS = 10
INITIAL_SONGS_REQUESTED = 50


def process_song(song_name, artist):
    track_name = song_name
    artist_name = artist

    print("Song Name: ", song_name)
    print("Artist: ", artist_name)
    print()

    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)

        song_row = next((row for row in data if row['Song Name'] == song_name and row['Artist'] == artist_name), None)

        if song_row:
            track_id = song_row['Track ID']
            song_features = eval(song_row['Song Features'])
            cluster_number = song_row['Cluster Number']
            emotion = song_row['Emotion']
            predicted_genre = song_row['Predicted Genre']
            album_genre = song_row['Album Genre']
        else:
            track_id = processing.get_track_id(track_name, artist_name)
            song_features = processing.get_song_features(track_id)
            cluster_number = processing.get_cluster(track_name, artist)
            emotion = classification.classification.run_lyric_analysis(song_name, artist)
            predicted_genre = predict_genre(track_name, artist_name)
            album_genre = get_album_genre(track_name, artist_name)

            update_csv(song_name, artist_name, track_id, song_features, cluster_number, emotion, predicted_genre, album_genre)

        cluster_songs = recommend_songs(song_features)
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

        return similar_songs


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

            song_name, artist_name = processing.get_track_details(song)
            song_row = next((row for row in data if row['Song Name'] == song_name and row['Artist'] == artist_name), None)

            if song_row:
                track_id = song_row['Track ID']
                song_features = eval(song_row['Song Features'])
                cluster_number = song_row['Cluster Number']
                emotion = song_row['Emotion']
                predicted_genre = song_row['Predicted Genre']
                album_genre = song_row['Album Genre']
            else:
                track_id = processing.get_track_id(song_name, artist_name)
                song_features = processing.get_song_features(track_id)
                cluster_number = processing.get_cluster(song_name, artist_name)
                emotion = classification.classification.run_lyric_analysis(song_name, artist_name)
                predicted_genre = predict_genre(song_name, artist_name)
                album_genre = get_album_genre(song_name, artist_name)

                update_csv(song_name, artist_name, track_id, song_features, cluster_number, emotion, predicted_genre, album_genre)

            if not track_id:
                continue

            if artist_name == song_artist:
                similar_songs.append("spotify:track:" + track_id)
                processed_songs.add(song)
                print(song_name + " by " + artist_name + " added")
            else:
                if emotion and song_emotion:
                    emotion, song_emotion = emotion.lower(), song_emotion.lower()
                if predicted_genre and song_predicted_genre:
                    predicted_genre, song_predicted_genre = predicted_genre.lower(), song_predicted_genre.lower()
                if album_genre and song_album_genre:
                    album_genre, song_album_genre = processing.map_deezer_genre_to_model_genre(album_genre), processing.map_deezer_genre_to_model_genre(song_album_genre)

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
                    distance = processing.emotional_similarity[emotion][song_emotion]
                    if distance >= 7:
                        similar_song_emotion = True

                if (similar_predicted_genre or similar_album_genre or similar_genre_1 or similar_genre_2) and similar_song_emotion:
                    similar_songs.append("spotify:track:" + track_id)
                    processed_songs.add(song)
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


process_song("Another Life", "Motionless In White")
