import csv
import os

import classification.classification
import processing
from genre_prediction.genre_prediction import predict_genre, get_album_genre
from clustering.cluster import recommend_songs

CSV_FILE_PATH = 'expanded_details.csv'


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
            print("Song found in CSV")
            track_id = song_row['Track ID'].values[0]
            song_features = eval(song_row['Song Features'].values[0])
            cluster_number = song_row['Cluster Number'].values[0]
            emotion = song_row['Emotion'].values[0]
            predicted_genre = song_row['Predicted Genre'].values[0]
            album_genre = song_row['Album Genre'].values[0]
        else:
            print("Song not found in CSV")
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


# def process_similar_songs(songs):
#     for song in songs:
#         if os.path.exists(CSV_FILE_PATH):
#             with open(CSV_FILE_PATH, mode='r', newline='') as csvfile:
#                 reader = csv.DictReader(csvfile)
#                 data = list(reader)



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
            print(f"Added new song to CSV: {song_name} by {artist_name}")
    else:
        print(f"Song already in CSV: {song_name} by {artist_name}")


process_song("Welcome to Paradise", "Green Day")
