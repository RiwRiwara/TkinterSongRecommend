from tkinter import *
from tkinter import ttk
from model import *


class WelcomeView:
    def __init__(self, master, controller):

        # Init variable
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.master = master
        self.controller = controller
        # GUI
        self.frame = Frame(self.master, width=1300, height=750)
        self.frame.pack()


    
        # ================================ TOP FRAME ================================ #
        self.top_frame = Frame(self.frame, bg="light sea green", relief=RIDGE)
        self.top_frame.place(x=2, y=0, width=1363, height=60)

        self.build_chart = Label(self.top_frame, text="Music Recommend", font=LABEL_FONT,
                                 fg="khaki", bg="light sea green")
        self.build_chart.place(x=10, y=10)

        # =================================== SEARCH BAR ================================ #
        self.search_label = Label(self.frame, text="Name:", font=USER_FONT, bg="white smoke")
        self.search_label.place(x=20, y=65)

        self.search_entry = Entry(self.frame, font=USER_FONT, width=95)
        self.search_entry.place(x=120, y=65)
        self.search_entry.bind('<KeyRelease>', self.search_table)
        self.search_entry.configure(state="disabled")

        self.searchList = Label(self.frame, text="List of search:", font=USER_FONT, bg="white smoke")
        self.searchList.place(x=20, y=100)

        self.slist = []
        self.combo = ttk.Combobox(self.frame, values=self.slist, width=80, height=35, font=USER_FONT, state="readonly")
        self.combo.place(x=180, y=100)
        self.buttonS = Button(self.frame, text="Select", font=BUTTON_FONT, command=lambda: self.print_title(event=None, title=self.combo.get()))
        self.buttonS.place(x=1190, y=100)
        self.buttonS.configure(state='disabled')

        # =================================== TABLE ================================ #
        self.left_frame = Frame(self.frame, bg="white smoke", relief=RIDGE, bd=1)
        self.left_frame.place(x=10, y=150, width=1250, height=550)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", backgroung="silver", foreground="black", rowheight=25, fieldbackground="silver")
        style.map("Treeview", background=[("selected", "medium sea green")])
        style.configure("Treeview.Heading", background="light steel blue", font=("Arial", 10, "bold"))
        self.controller.my_table = ttk.Treeview(self.left_frame)
        self.controller.my_table.bind("<ButtonRelease-1>", self.print_title)

        scroll_x_label = ttk.Scrollbar(self.left_frame, orient=HORIZONTAL, command=self.controller.my_table .xview)
        scroll_y_label = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.controller.my_table .yview)
        scroll_x_label.pack(side=BOTTOM, fill=X)
        scroll_y_label.pack(side=RIGHT, fill=Y)

        self.button0 = Button(self.frame, text="Upload File(CSV)", font=BUTTON_FONT, command=self.controller.file_open)
        self.button0.place(x=500, y=300, width=300, height=50)

        # ================================== BUTTONS ================================ #
        self.button_frame = Frame(self.frame, bg="white smoke", relief=RIDGE, bd=1)
        self.button_frame.place(x=10, y=700, width=1250, height=50)

        self.button1 = Button(self.button_frame, text="Chart", font=BUTTON_FONT , command=self.controller.show_chart_view)
        self.button1.pack(side=LEFT, padx=10)
        self.button1.configure(state="disabled")
        
        self.button2 = Button(self.button_frame, text="Report", font=BUTTON_FONT, command=self.controller.summarize_df_to_pdf)
        self.button2.pack(side=LEFT, padx=10)
        self.button2.configure(state="disabled")

        self.button3 = Button(self.button_frame, text="Get recommend music", font=BUTTON_FONT)
        # self.button3.pack(side=LEFT, padx=10)
        self.button3.configure(state="disabled")

        self.button4 = Button(self.button_frame, text="Exit", font=BUTTON_FONT, command=self.exitp)
        self.button4.pack(side=RIGHT, padx=10)

    def enableBtn(self):
        self.buttonS.configure(state='normal')
        self.button1.configure(state="normal")
        self.button2.configure(state="normal")
        self.button3.configure(state="normal")
        self.search_entry.configure(state="normal")
        self.button0.place_forget()

        
    def print_title(self,event, title=None):
        if not title==None:
            pass
        else:
            item = self.controller.my_table.selection()[0]
            title = self.controller.my_table.item(item, "values")[0]
            
        self.controller. currentMusic = title      
        if self.controller.decidePopup('Confirm', f'See Detail of {title}?'):      
            self.controller.show_music_view()
        # if self.controller.decidePopup('Confirm', f'Get reccomend music with "{title}"'):
        #     self.controller. show_loading_popup()
        #     self.master.update()
        #     recommended_songs = self.controller.getRecommendMusicByName(title)
        #     self.controller.hide_loading_popup()
        #     self.controller.popup("Recommended Songs", "\n".join(recommended_songs))



    def search_table(self, event):
        # create a list of items from the table
        items = self.controller.my_table.get_children()
        # create a list of values for each item
        values = [self.controller.my_table.item(item, 'values')[0] for item in items]
        
        # filter the values based on the search query
        search_query = self.search_entry.get().lower()
        filtered_values = [value for value in values if search_query in value.lower()]
        
        # update the values in the Combobox widget
        self.combo['values'] = filtered_values
        
        # select the first item in the filtered list (if any)
        if filtered_values:
            self.combo.current(0)
    def exitp(self):
        exit(0)