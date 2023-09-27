import pandas as pd

# Load the spreadsheet data
tracks = pd.read_csv('result.csv')

# Take user input for favorite song names
favorite_song_names = input('Enter comma-separated names of your favorite songs\n> ').strip().split(',')

# Initialize an empty list to store matching song IDs
matching_ids = []

# Search for the song names in the dataset
for song_name in favorite_song_names:
    matching_ids.extend(tracks[tracks['name'].str.contains(song_name, case=False)]['id'].tolist())

# Remove duplicate IDs by converting the list to a set and then back to a list
matching_ids = list(set(matching_ids))

# Check if any matching song IDs were found
if not matching_ids:
    print("No matching songs found.")
else:
    # Get the tracks corresponding to the matching song IDs
    favorites = tracks[tracks['id'].isin(matching_ids)]

    # Code to find the most occurring cluster number among user's favorite track types
    cluster_numbers = list(favorites['type'])
    clusters = {}
    for num in cluster_numbers:
        clusters[num] = cluster_numbers.count(num)

    # Sort the cluster numbers and find out the number which occurs the most
    user_favorite_cluster = [(k, v) for k, v in sorted(clusters.items(), key=lambda item: item[1])][0][0]

    print('\nFavorite cluster:', user_favorite_cluster, '\n')

    tracks = tracks[tracks.popularity > 70]
    # Finally, get the tracks of that cluster
    suggestions = tracks[tracks['type'] == user_favorite_cluster]

    print("Recommended Songs:")
    for index, row in suggestions.head().iterrows():
        print(f"Song Name: {row['name']}")
        print(f"Song Preview: {row['preview_url']}")
