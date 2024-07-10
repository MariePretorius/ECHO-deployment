import classification.classification
import processing
from genre_prediction.genre_prediction import predict_genre, get_album_genre


def process_song(song_name, artist):
    track_name = song_name
    artist_name = artist

    print("Song Name: ", song_name)
    print("Artist: ", artist_name)
    print()

    track_id = processing.get_track_id(track_name, artist_name)
    song_features = processing.get_song_features(track_id)

    cluster_number = processing.get_cluster(track_name, artist)
    print("Cluster Number: ", cluster_number)
    print()

    emotion = classification.classification.run_lyric_analysis(song_name, artist)
    print("Emotion: ", emotion)
    print()

    predicted_genre = predict_genre(track_name, artist_name)
    print("Predicted Genre: ", predicted_genre)
    album_genre = get_album_genre(track_name, artist_name)
    print("Album Genre: ", album_genre)


process_song("Radio", "Lana Del Rey")
