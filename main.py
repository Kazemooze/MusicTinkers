import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import hashlib
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image


class BaseScreen(tk.Frame):
    def __init__(self, master, entry_widgets):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg='#fff')
        program_name = Label(text="MusicTinkers", fg='#57a1f8', bg='white',
                             font=('Microsoft YaHei UI Light', 30, 'bold'))
        program_name.place(x=0, y=0)
        self.entry_widgets = entry_widgets


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


class LoginScreen(BaseScreen):
    def __init__(self, master):
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        encode = password.encode()
        hash_pass = hashlib.md5(encode).hexdigest()

        account_data = {"username": username, "password": hash_pass}

        with open("account_credentials.txt", "a") as f:
            f.write(json.dumps(account_data) + "\n")
        f.close()
        print("Registered Successfully")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        auth_pass = hashlib.md5(password.encode()).hexdigest()

        with open("account_credentials.txt", "r") as f:
            for line in f:
                try:
                    account_data = json.loads(line)
                    stored_user = account_data.get("username", "")
                    stored_pass = account_data.get("password", "")
                except json.JSONDecodeError:
                    print("Error decoding JSON:", repr(line))  # Debug print
                    continue  # Skip lines with invalid JSON

                if username == stored_user and auth_pass == stored_pass:
                    print("Logged In")
                    self.show_spotifykeys_screen()
                    return
                else:
                    print("Login Failed")

    def create_widgets(self):
        frame = Frame(width=350, height=350, bg="white")
        frame.place(x=480, y=70)

        img = Image.open('musiclogo.png')
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)

        # Create a label to display the image
        image_label = Label(image=img, bg='white')
        image_label.image = img  # Keep a reference to avoid garbage collection
        image_label.place(x=90, y=95)

        heading = Label(frame, text="Sign in", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.username_entry = PlaceholderEntry(frame, placeholder="Username", width=25, fg='black', bg="white",
                                               border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.username_entry.place(x=30, y=80)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.password_entry = PlaceholderEntry(frame, placeholder="Password", width=25, show='*', fg='black',
                                               bg="white", border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.password_entry.place(x=30, y=150)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        login_button = tk.Button(frame, text="Login", command=self.login, bg='#57a1f8', fg='white', width='39',
                                 border=0)
        login_button.place(x=35, y=204)

        signup_button = tk.Button(frame, text="Sign up", command=self.signup, bg='#57a1f8', fg='white', width='39',
                                  border=0)
        signup_button.place(x=35, y=240)

    def show_spotifykeys_screen(self):
        # Hide the current frame
        self.pack_forget()
        # Create a new frame for recommendations
        SpotifyKeysScreen(self.master)

    # def show_recommendations_screen(self):
    #         self.pack_forget()
    #         RecommendationsScreen(self.master)


class SpotifyKeysScreen(BaseScreen):
    def __init__(self, master):
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
        else:
            print("Please enter both Spotify Client ID and Spotify Client Secret.")

    def create_widgets(self):
        frame = Frame(width=350, height=350, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        heading = Label(frame, text="Enter Spotify Keys", fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=325, y=5)

        self.clientid_entry = PlaceholderEntry(frame, placeholder="Spotify Client ID", width=25, fg='black', bg="white",
                                               border=0,
                                               font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.clientid_entry.place(x=325, y=110)

        Frame(frame, width=295, height=2, bg='black').place(x=325, y=137)

        self.clientsecret_entry = PlaceholderEntry(frame, placeholder="Spotify Client Secret", width=25, fg='black',
                                                   bg="white", border=0,
                                                   font=('Microsoft YaHei UI Light', 11, 'bold'))
        self.clientsecret_entry.place(x=325, y=180)

        Frame(frame, width=295, height=2, bg='black').place(x=325, y=207)

        save_button = tk.Button(frame, text="Save Keys", command=self.get_spotify_keys, bg='#57a1f8', fg='white',
                                width='39', border=0)
        save_button.place(x=325, y=240)


class RecommendationsScreen(BaseScreen):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(bg='#fff')
        # You can add widgets specific to the recommendations screen here
        self.create_widgets()

    def create_widgets(self):
        return


# create another frame after login
# implement spotify stuff here, lookup, selection,recommendation
# create another frame for signup
# make sure theres a way to probably fix and not random characters enter into data

# image_path=PhotoImage(file="C:\Files\Background.png")
# background_label = tk.Label(self, image=image_path)
# background_label.place(relheight=1,relwidth=1)


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


def main():
    print("Welcome to MusicTinker's Song Recommender")
    print("1) Signup")
    print("2) Login")
    print("3) Exit")

    while True:
        try:
            select = int(input("Enter selection: "))
            if select == 1:
                # signup()
                break
            elif select == 2:
                # login()
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
        # credentials = get_spotify_keys()

    auth_manager = SpotifyClientCredentials(client_id=credentials["client_id"],
                                            client_secret=credentials["client_secret"])
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
    if __name__ == '__main__':
        root = tk.Tk()
        root.title('MusicTinkers')
        root.geometry('925x500+300+200')
        root.configure(bg='white')
        root.iconbitmap("collection.ico")

        main_screen = LoginScreen(root)
        root.mainloop()
