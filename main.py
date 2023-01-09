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
        if newRating <= 0:
            self.rating = 0
        else:
            self.rating = round(newRating)
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
        self.item1ExScore = 0
        self.item2ExScore = 0
    def setStage(self,comp1,comp2):
        self.item1 = comp1
        self.item2 = comp2
        rat1 = self.item1.rating
        rat2 = self.item2.rating
        self.item1ExScore = 1/(1+10**((rat2-rat1)/400))
        self.item2ExScore = 1/(1+10**((rat1-rat2)/400))
    def resetStage(self):
        self.item1 = None
        self.item2 = None
        self.item1ExScore = 0
        self.item2ExScore = 0
    def stageItem1Winner(self):
        if self.fullStage():
            newRating1 = self.item1.rating + 32*(1-self.item1ExScore)
            self.item1.updateStats(newRating1)
            newRating2 = self.item2.rating + 32*(0-self.item2ExScore)
            self.item2.updateStats(newRating2)

    def stageItem2Winner(self):
        if self.fullstage():
            newRating2 = self.item2.rating + 32*(1-self.item2ExScore)
            self.item2.updateStats(newRating2)
            newRating1 = self.item1.rating + 32*(0-self.item1ExScore)
            self.item1.updateStats(newRating1)

    def fullStage(self):
        if self.item1 == None or self.item2 == None:
            return False
        else:
            return True
    def __str__(self):
        print_str = ""
        if self.fullStage():
            print_str += "First Item: " + self.item1.name + "\n"
            print_str += "First Item win probability: " + str(round(self.item1ExScore,2))+ "\n"
            print_str += "Second Item: " + self.item2.name + "\n"
            print_str += "Second Item win probability: " + str(round(self.item2ExScore,2)) + "\n"
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

def item1Winner():
    mainStage.stageItem1Winner()

def item2Winner():
    mainStage.stageItem2Winner()

mainStage = Stage()

item1 = Item("hello")
item2 = Item("world")
item1.rating= 1656
item2.rating= 1763

mainStage.setStage(item1,item2)

print(item1)
print(item2)

print(mainStage)

item1Winner()

print(item1)
print(item2)








