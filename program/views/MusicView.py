from tkinter import *
from tkinter import ttk
from model import *
import webbrowser
from tksheet import Sheet
from tkinter import Toplevel, Label, PhotoImage

class MusicView:
    def __init__(self, master, controller):

        # Init variable
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.master = master
        self.controller = controller
        self.frame = Frame(self.master, width=1300, height=700)
        self.frame.pack()

        self.buttonEx = Button(self.frame, text="Back", font=BUTTON_FONT, command=self.controller.show_welcome_view)
        self.buttonEx.place(x=5, y=10)

        # Create a label to display the attributes of a Song
        my = 60
        self.song_label = Label(self.frame, font=MT_FONT, anchor="w")
        self.song_label.place(x=60, y=my+50)

        self.artist = Label(self.frame, font=AT_FONT, anchor="w")
        self.artist.place(x=60, y=my+50*2)

        self.top_genre = Label(self.frame, font=AT_FONT, anchor="w")
        self.top_genre.place(x=60, y=my+50*2)


        self.detail = Label(self.frame, font=AT_FONT, anchor="w", justify='left')
        self.detail.place(x=60, y=my+50*3, width=500)

        self.buttonLink = Button(self.frame, text="Open In youtube", font=BUTTON_FONT, width=20,command=self.openWeb)
        self.buttonLink.place(x=60, y=my+510)

        self.buttonR = Button(self.frame, text="Recommend Songs", font=BUTTON_FONT, width=20,command=self.reccommend)
        self.buttonR.place(x=60, y=my+550)



    def show_song_view(self, song_title):
        # Get the Song object with the given title from the all_songs dictionary
        song = self.controller.all_songs.get(song_title)

        if song:
            # Set the text of the song_label to display all the attributes of the Song object
            self.song_label.config(text=f"Title: {song.title} [{song.year}]")
            self.artist.config(text=f"Artist: {song.artist}")
            self.top_genre.config(text=f"Genre: {song.top_genre}")
            self.detail.config(text=f"Detail\n"
                                         f"BPM: {song.bpm}\n"
                                         f"Energy: {song.energy}\n"
                                         f"Danceability: {song.danceability}\n"
                                         f"Loudness: {song.loudness}\n"
                                         f"Liveness: {song.liveness}\n"
                                         f"Valence: {song.valence}\n"
                                         f"Length: {song.length}\n"
                                         f"Acousticness: {song.acousticness}\n"
                                         f"Speechiness: {song.speechiness}\n"
                                         f"Popularity: {song.popularity}\n"
                                         f"URL: {song.url}")
            try:
                self.image = PhotoImage(file=f"assets/thumnail/{song.title}.gif")
                self.imageShow  = Label(self.frame, image=self.image, width=800, height=700)
                self.imageShow .place(x=500, y=80)
            except:
                self.controller.popup("Warning", "This song don't have Image")
                self.image = PhotoImage(file=f"assets/thumnail/none.gif")
                self.imageShow  = Label(self.frame, image=self.image, width=800, height=700)
                self.imageShow .place(x=500, y=80)
        else:
            self.song_label.config(text="Song not found!")

    def openWeb(self):
        self.sheet = Sheet(self.frame, width=800, height=400)
        self.sheet.enable_bindings()
        try:
            self.sheet.set_sheet_data([[webbrowser.open(self.controller.all_songs.get(self.controller.currentMusic).url)]])
        except:
            self.controller.popup("Warning", "This song don't URL")

    def reccommend(self):
        if self.controller.decidePopup('Confirm', f'Get reccomend music?'):
            self.controller. show_loading_popup()
            self.master.update()
            recommended_songs = self.controller.getRecommendMusicByName(self.controller.currentMusic)
            self.controller.hide_loading_popup()
            self.controller.popup("Top 5 Recommended Songs", "\n".join(recommended_songs))
