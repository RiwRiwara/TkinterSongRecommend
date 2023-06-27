# Import necessary modules from tkinter
from tkinter import font
from tkinter import *
from tkinter import ttk
# Import the UserController class from controller module
from controller import UserController
# Define the App class that initializes the main window and sets its properties
class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1360x770")  # Set the size of the window
        self.master.resizable(False, False)  # Disable resizing the window
        self.master.title("Recommend Music")  # Set the title of the window
        # Create a ttk style object to customize the appearance of the widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Set the style to 'clam'
        # Create an instance of the UserController class to handle user interaction
        self.controller = UserController(self.master)
        # Show a pop-up message to ask the user to upload a file to start the program
        self.controller.popup("Caution", "Upload File in require to start program!")
        # Show the welcome view that displays the program's title and instructions
        self.controller.show_welcome_view()
# If this module is executed as a script (not imported), create a new instance of the App class and start the main event loop
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
