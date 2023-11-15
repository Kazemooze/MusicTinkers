import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import hashlib
import tkinter as tk
from tkinter import ttk, PhotoImage
# from PIL import ImageTk, Image

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


class Starter(tk.Tk):
    def __init__(self, title, size):
        # main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.iconbitmap('collection.ico')
        # widgets
        self.mainscreen = MainScreen(self)
        # run
        self.mainloop()


class MainScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.place(x=0, y=0, relwidth=0.3, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # create a label and entry for username
        username = ttk.Label(self, text="Username:")
        user_entry = ttk.Entry(self)
        # create a label and entry for password
        password = ttk.Label(self, text="Password:")
        pass_entry = ttk.Entry(self, show="*")
        # create a button to submit the form
        login_button = ttk.Button(self, text="Login")
        signup_button = ttk.Button(self, text="Sign Up")

        entry = ttk.Entry(self)
        # create grid rework
        self.columnconfigure((0, 1, 2, 3, 4), uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4), uniform='a')
        # place widgets
        username.grid(row=1, column=0, sticky='nswe')
        user_entry.grid(row=1, column=1, sticky='nswe')
        password.grid(row=2, column=0, sticky='nswe')
        pass_entry.grid(row=2, column=1, sticky='nswe')
        login_button.grid(row=3, column=0, )  # command=check login
        signup_button.grid(row=3, column=1, )  # command= sign up page


# create another frame after login
# implement spotify stuff here, lookup, selection,recommendation
# create another frame for signup
# make sure theres a way to probably fix and not random characters enter into data

# image_path=PhotoImage(file="C:\Files\Background.png")
# background_label = tk.Label(self, image=image_path)
# background_label.place(relheight=1,relwidth=1)


# start the event loop
Starter("Music Tinkerers", (600, 600))
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
