# Import necessary libraries
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import hashlib
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import requests
from io import BytesIO
import os
import tempfile
import pygame
import threading
import csv
from sklearn.cluster import KMeans


# Base class for screens
class BaseScreen(tk.Frame):
    def __init__(self, master, entry_widgets, current_user=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg='#fff')
        program_name = Label(text="MusicTinkers", fg='#57a1f8', bg='white',
                             font=('Microsoft YaHei UI Light', 30, 'bold'))
        program_name.place(x=0, y=0)
        self.entry_widgets = entry_widgets
        self.current_user = current_user

    def set_current_user(self, spotusername):
        self.current_user = spotusername

    def show_signup_screen(self):
        RegistrationScreen(self.master)

    def show_login_screen(self):
        LoginScreen(self.master)

    def show_spotifykeys_screen(self):
        SpotifyKeysScreen(self.master)

    def show_recommendations_screen(self, current_user=None):
        RecommendationsScreen(self.master, current_user=self.current_user)


# Entry widget for placeholder text
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        self.config(fg='grey')

        self.bind("<FocusIn>", self.on_enter)
        self.bind("<FocusOut>", self.on_leave)

    def on_enter(self, event):
        if self.get() == self.placeholder:
            self.delete("0", "end")
            self.config(fg='black')  # Change text color when user starts typing

    def on_leave(self, event):
        if not self.get():
            self.insert("0", self.placeholder)
            self.config(fg='grey')  # Change text color back to placeholder color


# Login Screen
class LoginScreen(BaseScreen):
    def __init__(self, master, current_user=None):
        # Initialize entry widgets
        self.image_label = None
        self.frame = None
        self.username_entry = None
        self.password_entry = None
        entry_widgets = [
            {"widget": self.username_entry, "placeholder": "Username"},
            {"widget": self.password_entry, "placeholder": "Password"},
        ]
        super().__init__(master, entry_widgets)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg='#fff')
        self.create_widgets()

    def login(self):
        # Get username and password from entry widgets
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hash the entered password using sha224
        auth_pass = hashlib.sha224(password.encode()).hexdigest()

        # Check user credentials from the stored account credentials file
        with open("account_credentials.txt", "r") as f:
            for line in f:
                try:
                    # Load account data from JSON
                    account_data = json.loads(line)
                    stored_user = account_data.get("username", "")
                    stored_pass = account_data.get("password", "")
                except json.JSONDecodeError:
                    print("Error decoding JSON:", repr(line))  # Debug print
                    continue  # Skip lines with invalid JSON

                # Authenticate user
                if username == stored_user and auth_pass == stored_pass:
                    print("Logged In")
                    # Set the current user and handle Spotify credentials
                    self.set_current_user(account_data.get("spotusername", ""))
                    try:
                        with open("spotify_credentials.json", 'r') as json_file:
                            json.load(json_file)
                            self.image_label.destroy()
                            self.frame.destroy()
                            self.show_recommendations_screen(current_user=self.current_user)
                    except FileNotFoundError:
                        print("Spotify credentials not found. Please input credentials.")
                        self.show_spotifykeys_screen()
                        self.image_label.destroy()
                        self.frame.destroy()
                    return
                else:
                    print("Login Failed")

    def signup_transition(self):
        self.image_label.destroy()
        self.frame.destroy()
        self.show_signup_screen()

    def create_widgets(self):
        # Create GUI components for login screen
        self.frame = Frame(width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        img = Image.open('musiclogo.png')
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)

        # Create a label to display the image
        self.image_label = Label(image=img, bg='white')
        self.image_label.image = img  # Keep a reference to avoid garbage collection
        self.image_label.place(x=90, y=95)

        heading = Label(self.frame, text="Sign in", fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.username_entry = PlaceholderEntry(self.frame, placeholder="Username", width=25, fg='black', bg="white",
                                               border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.username_entry.place(x=30, y=80)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.password_entry = PlaceholderEntry(self.frame, placeholder="Password", width=25, show='*', fg='black',
                                               bg="white", border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.password_entry.place(x=30, y=150)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        login_button = tk.Button(self.frame, text="Login", command=self.login, bg='#57a1f8', fg='white', width='39',
                                 border=0)
        login_button.place(x=35, y=204)

        label = Label(self.frame, text="Create an account", fg='black', bg='white',
                      font=('Microsoft YaHei UI Light', 9))
        label.place(x=75, y=270)

        signup_button = tk.Button(self.frame, text="Sign up", command=self.signup_transition, fg='#57a1f8', bg='white',
                                  width='6', cursor='hand2',
                                  border=0)
        signup_button.place(x=180, y=270)


# Registration Screen
class RegistrationScreen(BaseScreen):
    def __init__(self, master, current_user=None):
        # Initialize entry widgets
        self.spotusername_entry = None
        self.image_label = None
        self.frame = None
        self.username_entry = None
        self.password_entry = None
        entry_widgets = [
            {"widget": self.username_entry, "placeholder": "Username"},
            {"widget": self.password_entry, "placeholder": "Password"},
        ]
        super().__init__(master, entry_widgets)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg='#fff')
        self.create_widgets()

    def signup(self):
        # Get user registration details from entry widgets
        username = self.username_entry.get()
        password = self.password_entry.get()
        spotusername = self.spotusername_entry.get()

        # Encode and hash the password using sha224
        encode = password.encode()
        hash_pass = hashlib.sha224(encode).hexdigest()

        # Create a dictionary with user account data
        account_data = {"username": username, "password": hash_pass, "spotusername": spotusername}

        # Write the account data to the account credentials file
        with open("account_credentials.txt", "a") as f:
            f.write(json.dumps(account_data) + "\n")
        f.close()
        print("Registered Successfully")

        # Destroy the signup screen components and show the login screen
        self.image_label.destroy()
        self.frame.destroy()
        self.show_login_screen()

    def login_transition(self):
        self.image_label.destroy()
        self.frame.destroy()
        self.show_login_screen()

    def create_widgets(self):
        # Create GUI components for registration screen
        self.frame = Frame(width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        img = Image.open('musiclogo.png')
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)

        # Create a label to display the image
        self.image_label = Label(image=img, bg='white')
        self.image_label.place(x=90, y=95)

        heading = Label(self.frame, text="Sign Up", fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.username_entry = PlaceholderEntry(self.frame, placeholder="Username", width=25, fg='black', bg="white",
                                               border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.username_entry.place(x=30, y=80)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.password_entry = PlaceholderEntry(self.frame, placeholder="Password", width=25, show='*', fg='black',
                                               bg="white", border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.password_entry.place(x=30, y=150)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        self.spotusername_entry = PlaceholderEntry(self.frame, placeholder="Spotify Username", width=25, fg='black',
                                                   bg="white", border=0,
                                                   font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.spotusername_entry.place(x=30, y=220)

        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=247)

        signup_button = tk.Button(self.frame, text="Sign up", command=self.signup, bg='#57a1f8', fg='white', width='39',
                                  border=0)
        signup_button.place(x=35, y=274)

        label = Label(self.frame, text="Back to", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=120, y=320)

        login_button = tk.Button(self.frame, text="Login", command=self.login_transition, fg='#57a1f8', bg='white',
                                 width='6', cursor='hand2',
                                 border=0)

        login_button.place(x=180, y=320)


# Spotify Keys Screen
class SpotifyKeysScreen(BaseScreen):
    def __init__(self, master, current_user=None):
        # Initialize entry widgets
        self.frame = None
        self.clientid_entry = None
        self.clientsecret_entry = None
        entry_widgets = [
            {"widget": self.clientid_entry, "placeholder": "Spotify Client ID"},
            {"widget": self.clientsecret_entry, "placeholder": "Spotify Client Secret"},
        ]
        super().__init__(master, entry_widgets)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg='#fff')
        self.create_widgets()

    def get_spotify_keys(self):
        # Get Spotify client ID and client secret
        client_id = self.clientid_entry.get()
        client_secret = self.clientsecret_entry.get()

        # Check if both client ID and client secret are provided
        if client_id and client_secret:
            credentials = {
                "client_id": client_id,
                "client_secret": client_secret
            }

            with open("spotify_credentials.json", "w") as json_file:
                json.dump(credentials, json_file)
            print("Spotify keys saved successfully.")

            with open("account_credentials.txt", "r") as f:
                for line in f:
                    account_data = json.loads(line)
                    self.set_current_user(account_data.get("spotusername", ""))
            self.frame.destroy()
            RecommendationsScreen(self.master, current_user=self.current_user)
        else:
            print("Please enter both Spotify Client ID and Spotify Client Secret.")

    def create_widgets(self):
        # Create GUI components for Spotify Keys screen
        self.frame = Frame(width=350, height=350, bg="white")
        self.frame.place(relwidth=1, relheight=1, relx=0, rely=0, anchor='nw')

        heading = Label(self.frame, text="Enter Spotify Keys", fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=325, y=5)

        self.clientid_entry = PlaceholderEntry(self.frame, placeholder="Spotify Client ID", width=25, fg='black',
                                               bg="white",
                                               border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.clientid_entry.place(x=325, y=110)

        Frame(self.frame, width=295, height=2, bg='black').place(x=325, y=137)

        self.clientsecret_entry = PlaceholderEntry(self.frame, placeholder="Spotify Client Secret", width=25,
                                                   fg='black',
                                                   bg="white", border=0, show='*',
                                                   font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.clientsecret_entry.place(x=325, y=180)

        Frame(self.frame, width=295, height=2, bg='black').place(x=325, y=207)

        save_button = tk.Button(self.frame, text="Save Keys", command=self.get_spotify_keys, bg='#57a1f8', fg='white',
                                width='39', border=0)
        save_button.place(x=325, y=240)


# Recommendations Screen
class RecommendationsScreen(BaseScreen):
    def __init__(self, master, current_user=None):
        # Initialize attributes
        self.spotusername = None
        self.str_out = None
        self.playlist_value = None
        self.recommendations_frame = None  # Frame to display recommendations

        with open("spotify_credentials.json", 'r') as json_file:
            credentials = json.load(json_file)
        auth_manager = SpotifyClientCredentials(client_id=credentials["client_id"],
                                                client_secret=credentials["client_secret"])
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

        pygame.mixer.init()
        entry_widgets = [
            {"widget": self.spotusername, "placeholder": "Username"},
        ]

        super().__init__(master, entry_widgets, current_user=current_user)
        self.master.geometry("1440x720+150+100")
        self.playlist_value = tk.StringVar(self)  # Create StringVar for each playlist

        self.pack(fill=tk.BOTH, expand=True)
        self.current_user = current_user
        self.configure(bg='#fff')
        self.create_widgets()

    def get_playlist_data(self, sp):
        # get the current user spotify name
        username = self.current_user
        # use spotify API to get users playlits
        playlists = sp.user_playlists(username)
        # get the name and uri of the playlist
        playlist_data = [{'name': playlist['name'], 'uri': playlist['uri']} for playlist in playlists['items']]
        return playlist_data

    def perform_kmeans(self):
        # read the data into tracks data frame
        tracks_df = pd.read_csv("result.csv")

        # creates the clustering model
        model = KMeans(n_clusters=15)

        # divide the data into 5 clusters
        model.fit(tracks_df[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                             'speechiness', 'tempo', 'valence']])
        tracks_df['type'] = model.labels_

        tracks_df.to_csv("result.csv", index=False)

        return tracks_df

    def get_song_features(self, track_id):
        try:
            track_features = self.sp.audio_features(track_id)[0]
            features_list = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                             'speechiness', 'tempo', 'valence']
            # filter out only the needed data
            features = {feature: track_features[feature] for feature in features_list}

            # Specify the order of columns in the CSV file
            columns = ["Unnamed: 0", "acousticness", "danceability", "energy", "id", "instrumentalness", "liveness",
                       "loudness",
                       "name", "popularity", "preview_url", "speechiness", "tempo", "valence", "type"]

            # write the new data in the correct order with the dict
            with open("result.csv", 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writerow({"id": track_id, **features})

        except Exception as e:
            print(f"Error fetching features for track {track_id}: {e}")

    def get_recommendations(self):
        # Get the selected playlist name from the dropdown menu
        selected_playlist = self.playlist_value.get()

        # Retrieve all playlist data
        playlist_data = self.get_playlist_data(self.sp)

        # Find the data for the selected playlist of selected playlist
        selected_playlist_data = next((playlist for playlist in playlist_data if playlist['name'] == selected_playlist),
                                      None)

        selected_playlist_uri = None

        # Check if the selected playlist data exists
        if selected_playlist_data:
            # Retrieve the URI of the selected playlist
            selected_playlist_uri = selected_playlist_data['uri']
        else:
            print(f"Playlist '{selected_playlist}' not found in the data.")

        track_ids = []
        tracks = pd.read_csv('result.csv')

        # Check if a valid playlist URI exists
        if selected_playlist_uri is not None:
            # Use Spotify API to get the items (tracks) in the selected playlist
            sp_res = self.sp.playlist_items(selected_playlist_uri)

            # Extract track IDs from the items in the playlist
            for item in sp_res['items']:
                track_id = item['track']['id']

                if track_id not in tracks['id'].values:
                    self.get_song_features(track_id)

                track_ids.append(track_id)

        # update csv dataframe for new potential songs
        tracks = pd.read_csv('result.csv')

        # perform kmeans calculations on the new songs
        thread = threading.Thread(target=self.perform_kmeans)
        thread.start()
        thread.join()
        # update dataframe with the new kmeans numbers
        tracks = pd.read_csv('result.csv')

        # code from Kuvam Bhardwaj on dev.to
        favorites = tracks[tracks['id'].isin(track_ids)]

        # find the most occurring cluster number in user's track
        cluster_numbers = list(favorites['type'])
        clusters = {}
        for num in cluster_numbers:
            clusters[num] = cluster_numbers.count(num)

        user_favorite_cluster = [(k, v) for k, v in sorted(clusters.items(), key=lambda z: z[1])][0][0]

        tracks = tracks[tracks.popularity > 70]

        # get suggestion songs from that cluster
        suggestions = tracks[tracks['type'] == user_favorite_cluster].head(35).tail(8)
        # Retrieve detailed information for each track using Spotify API in a separate thread

        thread = threading.Thread(target=self.fetch_detailed_info, args=(suggestions,))
        thread.start()

    def fetch_detailed_info(self, suggestions):

        # Retrieve detailed information for each track using Spotify API
        detailed_track_info = []
        for track_id in suggestions['id']:
            track_info = self.sp.track(track_id)
            detailed_track_info.append({
                'name': track_info['name'],
                'artists': [artist['name'] for artist in track_info['artists']],
                'preview_url': track_info['preview_url'],
                'image_url': track_info['album']['images'][0]['url'] if track_info['album']['images'] else None
            })

        # Display recommendations in the GUI
        self.display_recommendations(detailed_track_info)

    def play_preview(self, preview_url):
        try:
            # Download the audio preview and save it to a temporary file
            response = requests.get(preview_url)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            # Set an event to be triggered when music playback is finished
            pygame.mixer.music.set_endevent(pygame.USEREVENT)

            # Play the audio preview using pygame.mixer
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()

            # Wait for the playback to finish
            pygame.event.wait()

            # Remove the temporary file
            os.remove(temp_file_path)

        except Exception as e:
            print(f"Error playing preview: {e}")

    def stop_preview(self):
        pygame.mixer.music.stop()

    def display_recommendations(self, detailed_track_info):

        # Clear previous recommendations
        if self.recommendations_frame:
            self.recommendations_frame.destroy()

        # Create a new frame for recommendations
        self.recommendations_frame = Frame(root, width=500, height=300, bg="white")
        self.recommendations_frame.place(x=325, y=250)

        # Display detailed information about each track
        for index, track_info in enumerate(detailed_track_info, start=1):
            song_name = track_info['name']
            artists = (track_info['artists'][0])
            preview_url = track_info['preview_url']
            image_url = track_info['image_url']

            # Display song details using Label widgets
            song_label = Label(self.recommendations_frame, text=f"{index}. {song_name} by {artists}", bg='white',
                               font=('Arial', 12))
            song_label.grid(row=index, column=0, sticky=tk.W, pady=2)

            if image_url:
                # Download the image and display it
                image_data = requests.get(image_url).content
                image = Image.open(BytesIO(image_data))
                image = image.resize((50, 50))
                image = ImageTk.PhotoImage(image)

                image_label = Label(self.recommendations_frame, image=image, bg='white')
                image_label.image = image  # Keep a reference to the image
                image_label.grid(row=index, column=1, sticky=tk.W, padx=10)

            if preview_url:
                play_button = tk.Button(self.recommendations_frame, text="Play Preview",
                                        command=lambda url=preview_url: self.play_preview(url), bg='#57a1f8',
                                        fg='white',
                                        width='15', border=0)
                play_button.grid(row=index, column=2, sticky=tk.W, padx=10)

                stop_button = tk.Button(self.recommendations_frame, text="Stop Preview",
                                        command=self.stop_preview, bg='#ff5733', fg='white', width='15', border=0)
                stop_button.grid(row=index, column=3, sticky=tk.W, padx=10)

    def create_widgets(self):
        # create the screen widgets
        frame = Frame(width=350, height=450, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=50)

        caret_img = Image.open("caret_down.png")
        caret_img = caret_img.resize((15, 15))
        caret_img = ImageTk.PhotoImage(caret_img)
        caret_img.image = caret_img

        heading = Label(frame, text="Recommendations", fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=300, y=0)

        # retieve playlist name from method and get playlist names from data
        playlist_data = self.get_playlist_data(self.sp)
        playlist_names = [playlist['name'] for playlist in playlist_data]

        # create Tk stringvar to hold playlist names
        self.playlist_value = tk.StringVar(root)
        self.playlist_value.set("Select a Playlist")
        # option menu with the playlist names
        self.select_menu = tk.OptionMenu(frame, self.playlist_value, *playlist_names)

        self.select_menu.config(
            bg="#57a1f8",
            fg="White",
            activebackground="#bcd7f7",
            activeforeground="Black",
            font=('Arial', 16),
            border=0,
            highlightthickness=1,
            highlightbackground="#bcd7f7",
            pady=10,
            indicatoron=False,
            image=caret_img,
            compound=tk.RIGHT,
            width=180
        )

        self.select_menu['menu'].config(
            bg='#57a1f8',
            fg="White",
            activebackground="#bcd7f7",
            activeforeground="Black",
            font=('Arial', 16),
            border=0,
        )

        self.select_menu.place(x=50, y=50)

        submit_button = tk.Button(frame, text="Get Recommendations", command=lambda: self.get_recommendations(),
                                  bg='#57a1f8', fg='white', width='20', border=0, pady=10, font=('Arial', 10))
        submit_button.place(x=50, y=150)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('MusicTinkers')
    root.geometry('925x500+300+200')
    root.configure(bg='white')
    root.iconbitmap("collection.ico")
    pygame.init()

    main_screen = BaseScreen(root, entry_widgets=[])
    main_screen.show_login_screen()

    root.mainloop()
