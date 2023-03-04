from random import choice
from tkinter import *
from time import time
from snoise import *

__inspiration__ = "https://azgaar.github.io/Fantasy-Map-Generator/"

#    _____          ____
#   / ___/__  ___  / _(_)__ _
#  / /__/ _ \/ _ \/ _/ / _ `/
#  \___/\___/_//_/_//_/\_, /
#                     /___/

# Getting variables from the `config.json` file
import json

# Open the configuration file
with open("config.json") as f:
    config = json.load(f)

# Title
title = config["title"]

# Global pixel size varibals on the canvas
scale = config["software"]["dimensions"]["scale"]
hp = config["software"]["dimensions"]["hp"]
wp = config["software"]["dimensions"]["wp"]
h, w = hp * scale, wp * scale

# Color palette for the window
background = config["software"]["colors"]["background"]
primaryColor = config["software"]["colors"]["primaryColor"]

white = config["software"]["colors"]["white"]


### Function to apply colors to the different regions of the map
def height(h):  # Sand [156, 145, 93]
    return brighten(
        [
            [19, 20, 87],  # Sea
            [19, 20, 87],  # Sea
            [19, 20, 87],  # Sea
            [17, 54, 5],  # Grass
            [17, 54, 5],  # Grass
            [42, 42, 42],  # Mountain
            [181, 181, 181],
        ][  # Snow on the moutains
            h // 14
        ],
        h // 2,
    )


### Function to adjust color shades    r                g                b
def brighten(color, rate):
    return "#%02x%02x%02x" % (color[0] + rate, color[1] + rate, color[2] + rate)


#     ___             ___          __  _
#    / _ | ___  ___  / (_)______ _/ /_(_)__  ___
#   / __ |/ _ \/ _ \/ / / __/ _ `/ __/ / _ \/ _ \
#  /_/ |_/ .__/ .__/_/_/\__/\_,_/\__/_/\___/_//_/
#       /_/  /_/


class App:
    def __init__(self):
        self.app = Tk()
        self.app.title(title)
        self.app.geometry(str(h + 50) + "x" + str(w + 150))
        self.app.resizable(False, False)

        self.displayed = False

        self.debug = False

    def open(self):
        # Creation of the widget to put under the canva
        self.infos = StringVar()
        self.label = Label(self.app, textvariable=self.infos, bg=background, fg=white)
        self.infos.set("Height :\nx :     y :")
        self.label.pack(side=BOTTOM, padx=5, pady=5)

        menubar = Menu(self.app)

        creation_menu = Menu(menubar, tearoff=0)
        save_menu = Menu(menubar, tearoff=0)
        style_menu = Menu(menubar, tearoff=0)
        tools_menu = Menu(menubar, tearoff=0)

        for cascade in [
            (creation_menu, " Creation "),
            (save_menu, " Save "),
            (style_menu, " Style "),
            (tools_menu, " Tools "),
        ]:
            menubar.add_cascade(menu=cascade[0], label=cascade[1])

        # Add command with parameters : command = lambda : function(n)
        # Add command without parameters : command = function

        creation_menu.add_command(label="Create a new world", command=self.generate)

        save_menu.add_command(label="Save")
        save_menu.add_command(label="Open")

        # default | ancient | clean | atlas
        style_menu.add_command(label="Style Preset")
        # grayscale | sepia | dingy | tint
        style_menu.add_command(label="Global Filter")
        # heightmap | religions | rivers | temperature | population
        style_menu.add_command(label="Layers")

        tools_menu.add_command(label="Switch debug mode", command=self.debug_mode)

        self.app.config(menu=menubar)

        # 🎨 Setting up the app colors
        for menu in [creation_menu, save_menu, style_menu, tools_menu]:
            menu["bg"] = primaryColor
            menu["fg"] = white
            menu["bd"] = 0

        self.app["bg"] = background
        menubar["bg"] = primaryColor
        menubar["fg"] = white
        menubar["border"] = 0

        # 🖌 Creation of the canvas
        self.canvas = Canvas(
            self.app,
            width=w,
            height=h,
            bg=primaryColor,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.pack(padx=50, pady=50)
        self.canvas.bind("<Button-1>", self.click)

        # 🚀 Launching the app loop
        self.app.mainloop()

    def generate(self):
        """
        Todos :
        Canvas size
        Map seed
        Map name

        Year
        Cultures number
        Growth rate
        """

        self.app.title(title + "  |  Generation...")

        if self.debug:
            start = time()

        new_seed()
        self.map = [
            [
                ((noise(x / 100, y / 100) + noise(x / 33, y / 33) / 3 + 1) * 50)
                for x in range(256)
            ]
            for y in range(256)
        ]

        self.rivers = [
            [
                (
                    abs(noise(x * 0.02, y * 0.02) - noise(x * 0.08, y * 0.08) * 0.25)
                    < 0.05
                )
                for x in range(256)
            ]
            for y in range(256)
        ]

        if self.debug:
            print(
                "\n[ i ] Seed :",
                get_seed(),
                "\n[ ⌛] Generation time :",
                str(round((time() - start), 3)) + "s",
            )

        self.display(self.map)

    def display(self, map_data):
        self.app.title(title + "  |  Loading...")  # Atlas  |  Loading...
        self.canvas.delete("all")  # Canvas reset
        if self.debug:
            start = time()  # Timer
        for y, row in enumerate(self.map):  # Display
            for x, tile in enumerate(row):
                if self.rivers[y][x] and tile > 42 and tile < 70:
                    self.canvas.create_rectangle(
                        y * scale + 1,
                        x * scale + 1,  # ┌
                        y * scale + scale + 1,
                        x * scale + scale + 1,  # ┘
                        fill=height(int(tile * 0.15)),
                        outline="",
                    )

                else:
                    self.canvas.create_rectangle(
                        y * scale + 1,
                        x * scale + 1,  # ┌
                        y * scale + scale + 1,
                        x * scale + scale + 1,  # ┘
                        fill=height(int(tile)),
                        outline="",
                    )
        if self.debug:
            print("[ ⌛] Display time :", str(round((time() - start), 3)) + "s")
        self.displayed = True
        self.app.title(title + "  |  Seed : " + str(get_seed()))

    def click(self, event):
        if self.displayed:
            height = str(self.map[event.x // scale][event.y // scale])
            self.infos.set(
                "Height :"
                + height
                + "\nx :"
                + str(event.x // scale)
                + "     y :"
                + str(event.y // scale)
            )
            self.label.update()

    def debug_mode(self):
        self.debug = not self.debug
        print("[ ✓ ] Debug mode {}".format("on" if self.debug else "off"))


atlas = App()
atlas.open()
