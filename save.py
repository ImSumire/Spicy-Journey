from tkinter import filedialog
from datetime import datetime
import os


# Global varibals for the different parameters
mapName = ""
timeCreated = ""
mapHeight = ""
mapTemperature = ""
mapRainfall = ""


# Function to save the map
def save(mapName, Map):
    if not os.path.exists(os.getcwd() + '/savedMaps'):
        os.makedirs(os.getcwd() + '/savedMaps')
    
    now = str(datetime.now()).replace(":", "_")
    heightString = ""
    for y in range(len(Map)):
        for x in range(len(Map[y])):
            heightString += str(Map[y][x]["height"]) + " "
        heightString += "\n"
    heightString = heightString[:-1]
    temperatureString = ""
    for y in range(len(Map)):
        for x in range(len(Map[y])):
            temperatureString += str(Map[y][x]["temperature"]) + " "
        temperatureString += "\n"
    temperatureString = temperatureString[:-1]
    rainfallString = ""
    for y in range(len(Map)):
        for x in range(len(Map[y])):
            rainfallString += str(Map[y][x]["rainfall"]) + " "
        rainfallString += "\n"
    rainfallString = rainfallString[:-1]

    filePath = os.getcwd() + "/savedMaps/" + mapName + " (" + now[:10] + "-" + now[11:] + ").txt"
    with open(file = filePath, mode = "x", encoding = "utf-8") as f:
        f.write('### Map Name :\n' +
                mapName +
                '\n### Created on :\n' +
                now +
                '\n### Height map :\n' +
                heightString +
                '\n### Temperature map :\n' +
                temperatureString +
                '\n### Rainfall map :\n' +
                rainfallString)

# Function to open a map file and read it
def openFile():
    global mapName, timeCreated, mapHeight, mapTemperature, mapRainfall

    openedMap = filedialog.askopenfile(title = "Open a map", initialdir = os.getcwd() + "/savedMaps/")
    if openedMap == None:
        mapName = ""
        timeCreated = ""
        mapHeight = ""
        return
    
    openedMap.readline()
    mapName = openedMap.readline()
    openedMap.readline()
    timeCreated = openedMap.readline()
    openedMap.readline()
    line = openedMap.readline()
    while line != "### Temperature map :":
        mapHeight += line
        line = openedMap.readline()
    while line != "### Rainfall map :":
        mapTemperature += line
        line = openedMap.readline()
    while line:
        mapRainfall += line
        line = openedMap.readline()
