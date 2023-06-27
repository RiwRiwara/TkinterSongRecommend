# Define constants for file location, fonts, colors
FILE_LOCATION = "./assets"
BUTTON_FONT = ("Arial", 13, "bold")
LABEL_FONT = ("Arial", 20, "bold")
LABEL_FONT_H1 = ("Arial", 36, "bold")
LABEL_FONT_H2 = ("Arial", 30, "bold")
USER_FONT = ("Arial", 14, "bold")
INFO_FONT = ("Arial", 12, "bold")
SMALL_FONT = ("Arial", 12, "normal")
COLORS = ['green', 'red', 'purple', 'brown', 'blue']
MT_FONT = ("Arial", 20, "bold")
AT_FONT = ("Arial", 16, "bold")
# Import the pandas library to manipulate CSV files
import pandas as pd
# Define a Song class that represents a song object
class Song:
    def __init__(self, title, artist, top_genre, year, bpm, energy, danceability, loudness, liveness, valence, length, acousticness, speechiness, popularity, url):
        self.title = title
        self.artist = artist
        self.top_genre = top_genre
        self.year = year
        self.bpm = bpm
        self.energy = energy
        self.danceability = danceability
        self.loudness = loudness
        self.liveness = liveness
        self.valence = valence
        self.length = length
        self.acousticness = acousticness
        self.speechiness = speechiness
        self.popularity = popularity
        self.url = url
    def __str__(self):
        return f"{self.title} - {self.artist} ({self.year})"
    def __repr__(self):
        return self.__str__()



#    def getRecommendMusicByName(self, musicTitle):
#         # Define the features to use for similarity calculation
#         features = ['beats.per.minute', 'energy', 'danceability', 'loudness.dB', 'liveness', 'valance', 'length', 'acousticness', 'speechiness']
#         # Normalize the features
#         self.df[features] = self.df[features].apply(lambda x: (x - x.mean()) / x.std(), axis=0)
#         # Compute the pairwise similarity matrix using cosine similarity
#         sim_matrix = np.zeros((len(self.df), len(self.df)))
#         for i in range(len(self.df)):
#             for j in range(len(self.df)):
#                 if i != j:
#                     vec1 = self.df.loc[i, features].values
#                     vec2 = self.df.loc[j, features].values
#                     sim_matrix[i, j] = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
#         # Define a function to compute the shortest paths between two nodes in a graph
#         def shortest_paths(matrix):
#             n = matrix.shape[0]
#             for k in range(n):
#                 for i in range(n):
#                     for j in range(n):
#                         if matrix[i, k] + matrix[k, j] < matrix[i, j]:
#                             matrix[i, j] = matrix[i, k] + matrix[k, j]
#             return matrix
#         # Compute the shortest paths between all pairs of songs
#         dist_matrix = shortest_paths(1 - sim_matrix)
#         # Define a function to get recommendations based on a song
#         def get_recommendations(title, data=self.df, dist_matrix=dist_matrix, top_n=5):
#             # Get the index of the song that matches the title
#             idx = data[data['title'] == title].index[0]
#             # Get the shortest distances to all other songs
#             distances = dist_matrix[idx, :]
#             # Sort the songs based on the shortest distances
#             sorted_distances = sorted(enumerate(distances), key=lambda x: x[1])
#             # Get the top n most similar songs
#             song_indices = [i[0] for i in sorted_distances[1:top_n+1]]
#             # Return the titles of the top n songs
#             return data['title'].iloc[song_indices].tolist()
#         # Example usage
#         return get_recommendations(musicTitle)