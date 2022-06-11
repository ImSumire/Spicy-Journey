from random import choice
from tkinter import *
import biome, generation, save, map_name


# Global pixel size varibals on the canvas
scale = 2
hp, wp = 256, 256
h, w = hp * scale, wp * scale

# Color palette for the window
background = '#262626'
primaryColor = '#2e2e2e'

white = '#ffffff'


# Main function of the window
def start_window():
    global map, mapName

    # Window initialization
    fenetre = Tk()
    fenetre.title('Map Generator')
    fenetre.geometry(str(h+50)+"x"+str(w+150))
    fenetre.resizable(False, False)

    # Function to create a new random map
    def newMap():
        global map, mapName

        map = [[{} for i in range(wp)] for j in range(hp)]

        fenetre.title('Loading')
        map = generation.mapNoise(map)
        fenetre.title('Current Display')

        drawMap(map)
        mapName = choice(map_name.mapNames)
        fenetre.title(mapName)
    
    # Function to open a saved map
    def openMap():
        global map, mapName

        save.openFile()

        mapName = save.mapName
        map = [[]]
        line = 0
        num = ""
        for i in range(len(save.mapHeight)):
            if save.mapHeight[i] == "\n":
                map.append([])
                line += 1
            elif save.mapHeight[i] != " ":
                num += save.mapHeight[i]
            elif save.mapHeight[i] == " ":
                map[line]["height"] = int(num)
                num = ""
        line = 0
        num = ""
        for i in range(len(save.mapTemperature)):
            if save.mapTemperature[i] == "\n":
                line += 1
            elif save.mapTemperature[i] != " ":
                num += save.mapTemperature[i]
            elif save.mapTemperature[i] == " ":
                map[line]["temperature"] = int(num)
                num = ""
        line = 0
        num = ""
        for i in range(len(save.mapRainfall)):
            if save.mapRainfall[i] == "\n":
                line += 1
            elif save.mapRainfall[i] != " ":
                num += save.mapRainfall[i]
            elif save.mapRainfall[i] == " ":
                map[line]["rainfall"] = int(num)
                num = ""
        
        fenetre.title("Current Display")
        drawMap(map)
        fenetre.title(mapName)

    # Function to display some things when you click on the map (𝗪𝗜𝗣)
    def click(event):
        height = (event.x // scale)
        temperature = (event.x // scale)
        rainfall = (event.x // scale)
        infos_text = 'Height :' + height + '\nTemperature :' + temperature + '\nRainfall :' + rainfall + '\nx :' + str(event.x // scale) + '     y :' + str(event.y // scale)
        infos.set(infos_text)
        label.update()
    
    # Function to display the map on the canvas
    def drawMap(map):
        for y in range(h//scale):
            for x in range(w//scale):
                canvas.create_rectangle(y * scale + 1, x * scale + 1, y * scale + scale + 1, x * scale + scale + 1, fill = biome.height(int(map[y][x]['height'])), outline = '')

    # Creation of the widget to put under the canva
    infos = StringVar()

    label = Label(fenetre, textvariable = infos, bg = background, fg = white)
    infos.set('Height :\nTemperature :\nRainfall :\nx :     y :')
    label.pack(side=BOTTOM, padx=5, pady=5)
    
    # Menu
    menubar = Menu(fenetre)
    menu1 = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label = " ☰ ", menu = menu1)
    menu1.add_command(label = "New Map", command = newMap)
    menu1.add_command(label = "Save", command = lambda : save.save(mapName, map))
    menu1.add_command(label = "Open", command = openMap)
    menu1.add_separator()
    menu1.add_command(label = "Exit", command = fenetre.quit)
    fenetre.config(menu = menubar)

    # Setting up the window colors
    fenetre['bg'] = background

    menubar['bg'] = primaryColor
    menubar['fg'] = white
    menubar['border'] = 0

    menu1['bg'] = primaryColor
    menu1['fg'] = white
    menu1['bd'] = 0

    # Creation of the canvas
    canvas = Canvas(fenetre, width = w, height = h, bg = primaryColor, bd = 0, highlightthickness=0, relief='ridge')
    canvas.pack(padx = 50, pady = 50)
    canvas.bind("<Button-1>", click)

    # Launching the window loop
    fenetre.mainloop()


# Program launch
start_window()
