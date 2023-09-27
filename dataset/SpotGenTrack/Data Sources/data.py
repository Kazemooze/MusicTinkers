import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# read the data into tracks data frame
tracks_df = pd.read_csv("spotify_tracks.csv")

# creates the clustering model
model = KMeans(n_clusters=15)

# divide the data into 5 clusters
model.fit(tracks_df[['danceability', 'instrumentalness', 'energy', 'tempo', 'valence', 'liveness']])

tracks_df['type'] = model.labels_
tracks_df.head(10)
tracks_df.to_csv("result.csv")

# reduced_df = tracks_df[:1000]

# pd.plotting.scatter_matrix(reduced_df[['danceability', 'instrumentalness', 'energy', 'tempo', 'valence']],
# figsize=(30, 15))

# plt.show()
