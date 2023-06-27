from views.WelcomeView import WelcomeView
from views.ChartView import ChartView
from views.MusicView import MusicView
import tkinter.messagebox as messagebox
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter import Toplevel, Label, PhotoImage
import pandas as pd
from random import choice
from model import *
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import statistics
import os
from reportlab.lib.pagesizes import A4

class UserController:
    def __init__(self, master):
        self.master = master

        # Data variables:
        self.df = pd.DataFrame()
        self.bar_x_label = StringVar()
        self.bar_y_label = StringVar()
        self.scatter_x_name = StringVar()
        self.scatter_y_name = StringVar()
        self.pie_value_name = StringVar()
        self.pie_group_name = StringVar()
        self.line_name = StringVar()
        self.currentMusic = ""
        self.all_songs = {}
        self.default_save_path = os.path.join(os.getcwd(), "assets", "summary")



        # Bar box Label
        self.bar_box_xlabels =[]
        self.bar_box_ylabels =[]
        # Scatter box Label
        self.scatter_box_xlabels =[]
        self.scatter_box_ylabels =[]
        # Line box Label
        self.line_box_labels =[]
        # Pie box Label
        self.pie_box_xlabels =[]
        self.pie_box_ylabels =[]

        
        # Setting Views
        self.welcome_view = WelcomeView(self.master, self)
        self.chart_view = ChartView(self.master, self)
        self.music_view = MusicView(self.master, self)


    # ================================ Page manager ============================= #
    def popup(self, title, message):
        messagebox.showinfo(title, message)

    def decidePopup(self, title, message):
        confirmed = messagebox.askokcancel(title, message)
        return confirmed

    def show_welcome_view(self):
        self.chart_view.frame.pack_forget()
        self.music_view.frame.pack_forget()
        self.welcome_view.frame.pack()

    def show_chart_view(self):
        self.welcome_view.frame.pack_forget()
        self.fill_bar_box()
        self.fill_line_box()
        self.fill_pie_box()
        self.fill_scatter_box()
        self.chart_view.setComponent()

        self.chart_view.frame.pack()
        
    def show_music_view(self):
        self.welcome_view.frame.pack_forget()
        self.chart_view.frame.pack_forget()
        self.music_view.show_song_view(self.currentMusic)
        self.music_view.frame.pack()
    # ================================ Load Csv ============================= #
    def file_open(self):
        file_name = filedialog.askopenfilename(
            initialdir=FILE_LOCATION,
            title="Open A File",
            filetypes=(("csv files", "*.csv"), ("All Files", "*.*"))
        )
        if file_name:
            try:
                file_name = f"{file_name}"
                self.df = pd.read_csv(file_name)
                self.welcome_view.enableBtn()

                # Create a dictionary of Song objects with the title as the key
                self.all_songs = {}
                for index, row in self.df.iterrows():
                    song = Song(
                        title=row["title"],
                        artist=row["artist"],
                        top_genre=row["top genre"],
                        year=row["year"],
                        bpm=row["beats.per.minute"],
                        energy=row["energy"],
                        danceability=row["danceability"],
                        loudness=row["loudness.dB"],
                        liveness=row["liveness"],
                        valence=row["valance"],
                        length=row["length"],
                        acousticness=row["acousticness"],
                        speechiness=row["speechiness"],
                        popularity=row["popularity"],
                        url=row["url"]
                    )
                    self.all_songs[song.title] = song

            except ValueError:
                self.error_info.config(text="file can not be opened!")
            except FileNotFoundError:
                self.error_info.config(text="file can not be found!")

        self.clear_table_data()
        # from csv into dataframe:
        self.my_table["column"] = list(self.df.columns)
        self.my_table["show"] = "headings"
        for column in self.my_table["column"]:
            self.my_table.heading(column, text=column)
        # resize columns:
        for column_name in self.my_table["column"]:
            self.my_table.column(column_name, width=60)
        # fill rows with data:
        df_rows_old = self.df.to_numpy()
        df_rows_refreshed = [list(item) for item in df_rows_old]
        for row in df_rows_refreshed:
            self.my_table.insert("", "end", values=row)
        
        self.my_table.place(x=5, y=5, width=1200, height=600)



    def clear_table_data(self):
        self.my_table.delete(*self.my_table.get_children())

    # ================================ Bar Box ============================= #
    def fill_bar_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'object':
                x_labels.append(column)
            elif self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                y_labels.append(column)
        self.bar_box_xlabels = (x_labels)
        self.bar_box_ylabels = (y_labels)


     # ================================ Scatter ============================= #
    def fill_scatter_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                x_labels.append(column)
                y_labels.append(column)
        self.scatter_box_xlabels = (x_labels)
        self.scatter_box_ylabels = (y_labels)
     # ================================ pie ============================= #
    def fill_pie_box(self):
        columns = [item for item in self.df]
        x_labels = []
        y_labels = []
        for column in columns:
            if self.df[column].dtype == 'object':
                x_labels.append(column)
            elif self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                y_labels.append(column)
        self.pie_box_xlabels = (x_labels)
        self.pie_box_ylabels = (y_labels)
     # ================================ line ============================= #
    def fill_line_box(self):
        columns = [item for item in self.df]
        x_labels = []
        for column in columns:
            if self.df[column].dtype == 'int64' or self.df[column].dtype == 'float64':
                x_labels.append(column)
        self.line_box_labels = (x_labels)


    def getRecommendMusicByName(self, musicTitle):
        # Define the features to use for similarity calculation
        features = ['beats.per.minute', 'energy', 'danceability', 'loudness.dB',
                     'liveness', 'valance', 'length', 'acousticness', 'speechiness']
        # Normalize the features
        self.df[features] = self.df[features].apply(lambda x: (x - x.mean()) / x.std(), axis=0)
        # Compute the pairwise similarity matrix using cosine similarity
        sim_matrix = cosine_similarity(self.df[features])
        # Define a function to get recommendations based on a song
        def get_recommendations(title, data=self.df, sim_matrix=sim_matrix, top_n=5):
            # Get the index of the song that matches the title
            idx = data[data['title'] == title].index[0]
            # Get the similarity scores of all songs with respect to the input song
            sim_scores = list(enumerate(sim_matrix[idx]))
            # Sort the songs based on the similarity scores
            sorted_sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            # Get the top n most similar songs
            song_indices = [i[0] for i in sorted_sim_scores[1:top_n+1]]
            # Return the titles of the top n songs
            return data['title'].iloc[song_indices].tolist()
        # Example usage
        return get_recommendations(musicTitle)


    
    def show_loading_popup(self):
        self.loading_popup = Toplevel(self.master)
        self.loading_popup.geometry("200x200")
        self.loading_label = Label(self.loading_popup, text="Loading...")
        self.loading_label.pack(pady=10)
        self.loading_animation_gif = PhotoImage(file="assets/loading-gif.gif")
        self.loading_animation = Label(self.loading_popup, image=self.loading_animation_gif)
        self.loading_animation.pack(pady=10)

    def hide_loading_popup(self):
        if self.loading_popup:
            self.loading_popup.destroy()
            self.loading_popup = None
            self.loading_label = None
            self.loading_animation = None

    def summarize_df_to_pdf(self, pdf_path=None):
        if not self.decidePopup("Caution", "Print Report to PDF!"):
            return
        summary = self.df.describe()
        if pdf_path is None:
            pdf_path = os.path.join(self.default_save_path, 'summary.pdf')
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setFont('Helvetica-Bold', 18)
        c.drawString(50, 750, 'Summary of DataFrame')
        c.setFont('Helvetica', 12)
        x, y = 50, 700
        c.drawString(x, y, 'Attribute')
        c.drawString(x + 100, y, 'Count')
        c.drawString(x + 200, y, 'Mean')
        c.drawString(x + 300, y, 'Std')
        c.drawString(x + 400, y, 'Min')
        c.drawString(x + 500, y, '25%')
        c.drawString(x + 600, y, '50%')
        c.drawString(x + 700, y, '75%')
        c.drawString(x + 800, y, 'Max')
        y -= 20
        for col in summary.columns:
            x=50
            c.drawString(x, y, col)
            for val in summary[col]:
                c.drawString(x + 100, y, '{:,.2f}'.format(val))
                x+=100
            top_songs = self.get_top_songs(col)
            if not top_songs.empty:
                y -= 20
                c.drawString(50, y, 'Top 5 Songs:')
                y -= 20
                for _, row in top_songs.iterrows():
                    c.drawString(50, y, row['title'])
                    c.drawString(x + 100, y, '{:,.2f}'.format(row[col]))
                    y -= 20
            y -= 20
            
            # add a new page if the current page is filled with data
            if y <= 50:
                c.showPage()
                y = 700
        
        c.save()

        self.popup("Success", "File has saved!")
        os.startfile(os.path.dirname(os.path.abspath(pdf_path)))

    def get_top_songs(self, attribute):
        top_songs = self.df.nlargest(5, attribute)
        return top_songs[['title', attribute]]

    # def getRecommendMusicByName(self, musicTitle):
    #     # Define the features to use for similarity calculation
    #     features = ['beats.per.minute', 'energy', 'danceability', 'loudness.dB', 'liveness', 'valance', 'length', 'acousticness', 'speechiness']
    #     # Normalize the features
    #     self.df[features] = self.df[features].apply(lambda x: (x - x.mean()) / x.std(), axis=0)
    #     # Compute the pairwise similarity matrix using cosine similarity
    #     sim_matrix = np.zeros((len(self.df), len(self.df)))
    #     for i in range(len(self.df)):
    #         for j in range(len(self.df)):
    #             if i != j:
    #                 vec1 = self.df.loc[i, features].values
    #                 vec2 = self.df.loc[j, features].values
    #                 sim_matrix[i, j] = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    #     # Define a function to compute the shortest paths between two nodes in a graph
    #     def shortest_paths(matrix):
    #         n = matrix.shape[0]
    #         for k in range(n):
    #             for i in range(n):
    #                 for j in range(n):
    #                     if matrix[i, k] + matrix[k, j] < matrix[i, j]:
    #                         matrix[i, j] = matrix[i, k] + matrix[k, j]
    #         return matrix
    #     # Compute the shortest paths between all pairs of songs
    #     dist_matrix = shortest_paths(1 - sim_matrix)
    #     # Define a function to get recommendations based on a song
    #     def get_recommendations(title, data=self.df, dist_matrix=dist_matrix, top_n=5):
    #         # Get the index of the song that matches the title
    #         idx = data[data['title'] == title].index[0]
    #         # Get the shortest distances to all other songs
    #         distances = dist_matrix[idx, :]
    #         # Sort the songs based on the shortest distances
    #         sorted_distances = sorted(enumerate(distances), key=lambda x: x[1])
    #         # Get the top n most similar songs
    #         song_indices = [i[0] for i in sorted_distances[1:top_n+1]]
    #         # Return the titles of the top n songs
    #         return data['title'].iloc[song_indices].tolist()
    #     # Example usage
    #     return get_recommendations(musicTitle)