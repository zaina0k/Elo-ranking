# from guizero import App
from os import walk,rename

PATH = "photos/"
filenames = next(walk(PATH), (None, None, []))[2]  # [] if no file
population = []

class Item:
    """item class encapsulates each rated item carrying its current rating
    as well as carrying its rating history as an 1d array"""
    def __init__(self,name):
        self.name = name
        self.rating = 1500
        self.ratingHistory = []
    def resetRating(self):
        self.rating = 1500
    def resetHistory(self):
        self.ratingHistory.clear()
    def updateStats(self,newRating):
        self.ratingHistory.append(self.rating)
        self.rating = newRating
    def __str__(self):
        print_str = ""
        print_str += "Name: " + str(self.name) + "\n"
        print_str += "Rating: " + str(self.rating) + "\n"
        print_str += "Rating history: " + str(self.ratingHistory) + "\n"
        return(print_str)

class Stage:
    """stage class allows for 2 objects to be set up for comparison"""
    def __init__(self):
        self.item1 = None
        self.item2 = None
    def setStage(self,comp1,comp2):
        self.item1 = comp1
        self.item2 = comp2
    def resetStage(self):
        self.item1 = None
        self.item2 = None
    def fullStage(self):
        if self.item1 == None or self.item2 == None:
            return False
        else:
            return True
    def __str__(self):
        print_str = ""
        if self.fullStage():
            print_str += "First Item: " + self.item1.name + "\n"
            print_str += "Second Item: " + self.item2.name + "\n"
        return print_str

def changeFileName(originalname,newname,path,fileEnding):
    filenames = next(walk(path), (None, None, []))[2]  # [] if no file
    for i in range(len(filenames)):
        p1 = originalname
        p2 = newname + str(i) + fileEnding
        rename(p1,p2)

def fullReset():
    for element in population:
        element.resetRating()
        element.resetHistory()

def initialisePopulation():
    global filenames
    global population
    for i in range(len(filenames)):
        population.append(Item(filenames[i]))

mainStage = Stage()

item1 = Item("hello")
item2 = Item("world")

mainStage.setStage(item1,item2)

print(mainStage)






