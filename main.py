# from guizero import App
from os import walk,rename

PATH = "photos/"
filenames = next(walk(PATH), (None, None, []))[2]  # [] if no file
population = []

class Item:
    def __init__(self,name):
        self.name = name
        self.rating = 1500
        self.ratingHistory = []
    def resetRating(self):
        self.rating = 1500
    def resetHistory(self):
        self.ratingHistory.clear()
    def __str__(self):
        print_str = ""
        print_str += "Name: " + str(self.name) + "\n"
        print_str += "Rating: " + str(self.rating) + "\n"
        print_str += "Rating history: " + str(self.ratingHistory) + "\n"
        return(print_str)

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


initialisePopulation()
input(len(population))
for i in range(len(population)):
    print(population[i])






