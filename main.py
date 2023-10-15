import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import hashlib


def get_spotify_keys():
    client_id = input("Enter Spotify client ID: ")
    client_secret = input("Enter Spotify client secret: ")

    credentials = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    with open("spotify_credentials.json", "w") as json_file:
        json.dump(credentials, json_file)
    return credentials


def get_track_ids(username, sp):
    # Get a user's playlists
    playlists = sp.user_playlists(username)

    # print the playlists and allow the user to choose one
    print("Your Playlists:")
    for i, playlist in enumerate(playlists['items'], start=1):
        print(f"{i}. {playlist['name']}")

    while True:
        try:
            choice = int(input("Enter the number of the playlist you want to use for recommendations: "))
            if 1 <= choice <= len(playlists['items']):  # checks if choice is in range
                selected_playlist = playlists['items'][choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid playlist number.")
        except ValueError:
            print("Invalid input. Please enter a valid playlist number.")

    # requests the URI of the selected playlist
    selected_playlist_uri = selected_playlist['uri']

    sp_res = sp.playlist_items(selected_playlist_uri)
    track_ids = []

    # Iterate through the items in the response and collect track IDs
    for item in sp_res['items']:
        track_id = item['track']['id']
        track_ids.append(track_id)

    return track_ids


def signup():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    encode = password.encode()  # using hashlib python library to encode password
    hash_pass = hashlib.md5(encode).hexdigest()

    with open("account_credentials.txt", "w") as f:
        f.write(username + "/n")
        f.write(hash_pass)
    f.close()
    print("Registered Successfully")


def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter you password: ")

        auth_pass = password.encode()
        hash_pass = hashlib.md5(auth_pass).hexdigest()
        with open("account_credentials.txt", "r") as f:
            stored_user, stored_pass = f.read().split("/n")
        f.close()

        if username == stored_user and hash_pass == stored_pass:
            print("Logged In")
            break
        else:
            print("Login Failed")


def main():
    print("Welcome to MusicTinker's Song Recommender")
    print("1) Signup")
    print("2) Login")
    print("3) Exit")

    while True:
        try:
            select = int(input("Enter selection: "))
            if select == 1:
                signup()
                break
            elif select == 2:
                login()
                break
            elif select == 3:
                exit()
        except ValueError:
            print("Invalid input. Please enter an option.")

    try:
        with open("spotify_credentials.json", 'r') as json_file:
            credentials = json.load(json_file)
    except FileNotFoundError:
        print("Spotify credentials not found. Please input credentials.")
        credentials = get_spotify_keys()

    auth_manager = SpotifyClientCredentials(client_id=credentials["client_id"], client_secret=credentials["client_secret"])
    sp = spotipy.Spotify(auth_manager=auth_manager)

    spotusername = input("Please enter your Spotify username: ")

    # Load the spreadsheet data
    tracks = pd.read_csv('result.csv')

    # code from Kuvam Bhardwaj on dev.to
    favorites = tracks[tracks['id'].isin(get_track_ids(spotusername, sp))]

    # find the most occurring cluster number in user's track
    cluster_numbers = list(favorites['type'])
    clusters = {}
    for num in cluster_numbers:
        clusters[num] = cluster_numbers.count(num)

    # select the user favorite cluster by sorting
    user_favorite_cluster = [(k, v) for k, v in sorted(clusters.items(), key=lambda z: z[1])][0][0]

    print('\nFavorite cluster:', user_favorite_cluster, '\n')

    tracks = tracks[tracks.popularity > 70]
    # get suggestion songs from that cluster
    suggestions = tracks[tracks['type'] == user_favorite_cluster]

    print("Recommended Songs:")
    for index, row in suggestions.head(10).iterrows():
        print(f"Song Name: {row['name']}")
        print(f"Song Preview: {row['preview_url']}")


if __name__ == '__main__':
    main()
