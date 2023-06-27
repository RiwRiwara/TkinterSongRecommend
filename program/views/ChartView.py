from tkinter import *
from tkinter import ttk
from model import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import choice
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

class ChartView:
    def __init__(self, master, controller):

        # Init variable
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.master = master
        self.controller = controller
        self.frame = Frame(self.master, width=1300, height=900)
        self.frame.pack()
        # ================================ TOP FRAME ================================ #
        self.top_frame = Frame(self.frame, bg="light sea green", relief=RIDGE)
        self.top_frame.place(x=2, y=0, width=1363, height=60)
        self.bar_heading = Label(self.top_frame, text="Chart", font=LABEL_FONT,
                                 fg="khaki", bg="light sea green")
        self.bar_heading.place(x=10, y=5)


        # ================================ Button ================================ #
        btnY = 200
        btnW = 15
        self.buttonEx = Button(self.frame, text="Back", font=BUTTON_FONT , width=btnW, command=self.controller.show_welcome_view)
        self.buttonEx.place(x=5, y=btnY-100)

        self.buttonC1 = Button(self.frame, text="BAR CHART", font=BUTTON_FONT , width=btnW, command=lambda: self.setComponent(0))
        self.buttonC1.place(x=5, y=btnY+100)

        self.buttonC2 = Button(self.frame, text="SCATTER CHART", font=BUTTON_FONT , width=btnW, command=lambda: self.setComponent(1))
        self.buttonC2.place(x=5, y=btnY+180)

        self.buttonC3 = Button(self.frame, text="PIE CHART", font=BUTTON_FONT , width=btnW, command=lambda: self.setComponent(2))
        self.buttonC3.place(x=5, y=btnY+260)

        self.buttonC4 = Button(self.frame, text="LINE CHART", font=BUTTON_FONT , width=btnW, command=lambda: self.setComponent(3))
        self.buttonC4.place(x=5, y=btnY+340)
        
        self.buttonC4 = Button(self.frame, text="NETWORk GRAPH", font=BUTTON_FONT , width=btnW, command=lambda: self.setComponent(4))
        self.buttonC4.place(x=5, y=btnY+420)
        


    def setComponent(self, ac=0):
        # ================================ Bar Chart ================================ #
        bx = 200
        by = 50
        bwidth = 1000
        bheight = 800

        # Init Chart component
        self.bar_info = Frame(self.frame)
        self.x_label = Label(self.bar_info, text="XLabel", font=SMALL_FONT, bd=1)
        self.y_label = Label(self.bar_info, text="YLabel", font=SMALL_FONT, bd=1)
        self.x_box = ttk.Combobox(self.bar_info, font=SMALL_FONT, justify="center", state="readonly",
                                  textvariable=self.controller.bar_x_label)
        self.y_box = ttk.Combobox(self.bar_info, font=SMALL_FONT, justify="center", state="readonly",
                                  textvariable=self.controller.bar_y_label)
        self.bar_draw_button = Button(self.bar_info, text="draw", justify="center", font=INFO_FONT, relief=RIDGE, bd=2,
                                      bg="ivory", cursor="hand2", width=5, command=self.draw_bar_chart)

        self.x_box["values"] = self.controller.bar_box_xlabels
        self.y_box["values"] = self.controller.bar_box_ylabels
        if ac==0:
            pass
        elif ac==1:
            self.bar_heading.configure(text="Scatter Chart")
            self.x_box.configure(textvariable=self.controller.scatter_x_name)
            self.y_box.configure(textvariable=self.controller.scatter_y_name)
            self.bar_draw_button.configure(command=self.draw_scatter_chart)
            self.x_box["values"] = self.controller.scatter_box_xlabels
            self.y_box["values"] = self.controller.scatter_box_ylabels
        elif ac ==2:
            self.bar_heading.configure(text="Pie Chart")
            self.x_label.configure(text="Values")
            self.y_label.configure(text="Group By")
            self.x_box.configure(textvariable=self.controller.pie_value_name)
            self.y_box.configure(textvariable=self.controller.pie_group_name)
            self.bar_draw_button.configure(command=self.draw_pie_chart)
            self.x_box["values"] = self.controller.pie_box_ylabels
            self.y_box["values"] = self.controller.pie_box_xlabels
        elif ac ==3:
            self.bar_heading.configure(text="Line Chart")
            self.x_box.configure(textvariable=self.controller.line_name)
            self.bar_draw_button.configure(command=self.draw_line_chart)
            self.x_box["values"] = self.controller.line_box_labels
        elif ac ==4:
            self.bar_heading.configure(text="NETWORK GRAPH")
            self.bar_draw_button.configure(command=self.draw_network_chart)
            
        # Place component
        self.bar_info.place(x=bx+300, y=by+20, width=bwidth, height=90)
        self.x_label.grid(row=0, column=0, padx=10)
        self.x_box.grid(row=0, column=1)
        self.y_label.grid(row=1, column=0, padx=10)
        self.y_box.grid(row=1, column=1)
        if ac ==2:
            self.x_label.grid_forget()
            self.x_box.grid_forget()
        if ac ==3:
            self.y_label.grid_forget()
            self.y_box.grid_forget()
        if ac ==4:
            self.y_label.grid_forget()
            self.y_box.grid_forget()
            self.x_label.grid_forget()
            self.x_box.grid_forget()
            
        self.bar_draw_button.grid(row=0, column=2, padx=10)

        self.bar_clear_button = Button(self.bar_info, text="clean", justify="center", font=INFO_FONT, relief=RIDGE,
                                       bg="ivory", cursor="hand2", bd=2, width=5, command=self.clear_bar)
        self.bar_clear_button.grid(row=1, column=2, padx=10)

        # bar diagram replacement:
        self.top_left = Frame(self.frame)
        self.top_left.place(x=bx, y=by+110, width=bwidth, height=900)
        self.canvas_1 = Canvas(self.top_left, width=bwidth, height=800, relief=RIDGE)
        self.canvas_1.pack()
        self.fig_1 = None
        self.output_1 = None


        self.x_box.current(0)
        self.y_box.current(0)

            # Draw and clean Bar Chart
    
    def draw_bar_chart(self):
        self.clear_bar()
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(12, 4), dpi=100)
        xl = self.controller.bar_x_label.get()
        yl = self.controller.bar_y_label.get()
        year_counts = self.controller.df.groupby([yl])[xl].nunique()
        ax.bar(year_counts.index, year_counts.values, color=choice(COLORS))
        ax.set_xticklabels(year_counts.index, rotation=45)
        ax.set_ylabel(F'Number of {xl}', fontsize=12)
        ax.set_xlabel(yl, fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.spines['left'].set_color('#DDDDDD')
        ax.tick_params(axis='x', colors='#AAAAAA')
        ax.tick_params(axis='y', colors='#AAAAAA')
        ax.grid(axis='both', linestyle='--', alpha=0.7)
        ax.yaxis.set_label_coords(-0.1, 0.5)  # adjust y-axis label position
        self.output_1 = FigureCanvasTkAgg(fig, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()



    def draw_scatter_chart(self):
        self.clear_bar()
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(12, 4), dpi=110)
        ax.scatter(self.controller.df[f"{self.controller.scatter_x_name.get()}"],
                self.controller.df[f"{self.controller.scatter_y_name.get()}"],
                c=choice(COLORS))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_xlabel(self.controller.scatter_x_name.get(), fontsize=12)
        ax.set_ylabel(self.controller.scatter_y_name.get(), fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.spines['left'].set_color('#DDDDDD')
        ax.tick_params(axis='x', colors='#AAAAAA')
        ax.tick_params(axis='y', colors='#AAAAAA')
        ax.grid(axis='both', linestyle='--', alpha=0.7)
        self.output_1 = FigureCanvasTkAgg(fig, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()


    def draw_pie_chart(self):
        self.clear_bar()
        plt.style.use('seaborn')
        # prepare values:
        group_col = self.controller.pie_group_name.get()
        display = self.controller.df.groupby([group_col])[group_col].count()
        labels = display.index.tolist()
        values = display.values

        # combine categories with less than 3% into "Other"
        total = np.sum(values)
        threshold = 0.02 * total
        other_labels = []
        other_count = 0
        for i, value in enumerate(values):
            if value < threshold:
                other_count += value
                other_labels.append(labels[i])
        if other_count > 0:
            values = np.append(values[values >= threshold], other_count)
            labels = [l for l in labels if l not in other_labels] + ["Other"]

        # visualize:
        fig, ax = plt.subplots(figsize=(12, 4), dpi=110)
        ax.pie(values, labels=labels, shadow=True, autopct='%1.1f%%')
        ax.set_title(f"Ratio of {group_col}", fontsize=12)
        self.output_1 = FigureCanvasTkAgg(fig, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()


    def draw_line_chart(self):
        self.clear_bar()
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(12, 4), dpi=110)
        ax.plot(self.controller.df[f"{self.controller.line_name.get()}"], c=choice(COLORS))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_ylabel(self.controller.line_name.get(), fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.spines['left'].set_color('#DDDDDD')
        ax.tick_params(axis='x', colors='#AAAAAA')
        ax.tick_params(axis='y', colors='#AAAAAA')
        ax.grid(axis='both', linestyle='--', alpha=0.7)
        self.output_1 = FigureCanvasTkAgg(fig, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()

    def draw_network_chart(self):
        self.clear_bar()
        plt.style.use('seaborn')
        fig, ax = plt.subplots(figsize=(12, 4), dpi=110)

        df = self.controller.df
        G = nx.from_pandas_edgelist(df, source='artist', target='top genre')
        pos = nx.spring_layout(G, k=0.6)  # layout the graph using the spring layout algorithm
        nx.draw(G, pos=pos, with_labels=True, font_size=8) 
        plt.title('Artist-Genre Network Graph')

        self.output_1 = FigureCanvasTkAgg(fig, master=self.canvas_1)
        self.output_1.draw()
        self.output_1.get_tk_widget().pack()
        
    def clear_bar(self):
        if self.output_1:
            for child in self.canvas_1.winfo_children():
                child.destroy()
        self.output_1 = None