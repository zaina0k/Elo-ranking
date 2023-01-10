from guizero import App,PushButton,Text,Box,Picture
from os import walk,rename
from random import shuffle
import matplotlib. pyplot as plt
from operator import itemgetter

PATH = "temp/"
filenames = next(walk(PATH), (None, None, []))[2]  # [] if no file
try:
    filenames.remove(".DS_Store")
except:
    pass
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
        self.item1 = None#first item
        self.item2 = None#second item
        self.item1ExScore = 0#item expected score according to ranking
        self.item2ExScore = 0#item expected score according to ranking
        self.previousItem = None#previous item 1. used to ensure two rounds arent the same in a row
    def setStage(self,comp1,comp2):
        self.item1 = comp1
        self.item2 = comp2
        rat1 = self.item1.rating
        rat2 = self.item2.rating
        self.item1ExScore = 1/(1+10**((rat2-rat1)/400))
        self.item2ExScore = 1/(1+10**((rat1-rat2)/400))
    def resetStage(self):
        self.previousItem=self.item1
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
        if self.fullStage():
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

def chooseCompetitors(stage=None):
    global population
    options = []
    final_options = []
    dif = []
    average_element_pool = 3 #number of elements used to create the average
    #shuffling the list so that they are in random positions
    shuffle(population)
    #makes sure that the previous item1 and new item1 are not the same
    #both items do not need to be checked. only 1 needs to be different between rounds.
    if stage != None:
        if stage.previousItem == population[0]:
            final_options.append(population[-1])
        else:
            final_options.append(population[0])#first element becomes reference item
    else:
        final_options.append(population[0])#first element becomes reference item
    #loop creates a set of randomly chosen items
    for i in range(len(population)):
        if i>average_element_pool:
            break
        elif i == 0:
            pass
        else:
            options.append(population[i])
    baseline = final_options[0]
    #compare each of the randomly chosen items to the reference item
    #this allows for random selection but also allowing some rating based matchmaking
    for i in range(len(options)):
        comparitor = options[i]
        dif.append(abs(baseline.rating - comparitor.rating))
    chosen_index = dif.index(min(dif))
    if options[chosen_index] == baseline:
        final_options.append(options[chosen_index+1])
    final_options.append(options[chosen_index])
    return final_options

def totalRankingsGraph():
    """looks for the top 5 ratings
    pairs item names as key with their rating as value in a dictionary"""
    global population
    for i in range(len(population)):
        population[i].rating = i
    rankDict = {}
    for item in population:
        rankDict[item.name] = item.rating
    top5Dict = dict(sorted(rankDict.items(), key = itemgetter(1), reverse = True)[:5])
    return top5Dict

#GUIZERO functions
def item1Winner():
    mainStage.stageItem1Winner()
    nextComp()

def item2Winner():
    mainStage.stageItem2Winner()
    nextComp()

def resetPhotos():
    picture1.image=PATH+mainStage.item1.name
    picture2.image=PATH+mainStage.item2.name

def nextComp():
    newPics = chooseCompetitors(mainStage)
    mainStage.resetStage()
    mainStage.setStage(newPics[0],newPics[1])
    resetPhotos()

def displayTop5Ratings():
    global top5_rated_text_list
    top5Dict = totalRankingsGraph()
    counter = 0
    for item in top5Dict:
        counter += 1
        if counter >5:
            break
        else:
            top5_rated_text_list[counter-1].value = str(counter) + ". " + str(item) + ": " + str(top5Dict[item])
    settings_box.hide()
    top5_ratings_box.show()
    
#GUI changing page function
def home_to_settings():
    home_box.hide()
    settings_box.show()

def settings_to_home():
    settings_box.hide()
    home_box.show()

def home_to_comp():
    home_box.hide()
    comp_box.show()

def comp_to_home():
    comp_box.hide()
    home_box.show()

def quit_app():
    app.destroy()

def top5_to_settings():
    top5_ratings_box.hide()
    settings_box.show()

def settings_to_rank_history():
    settings_box.hide()
    rank_history_box.show()

def rank_history_to_settings():
    rank_history_box.hide()
    settings_box.show() 

##START##
initialisePopulation()
mainStage = Stage()
initialItems = chooseCompetitors()
mainStage.setStage(initialItems[0],initialItems[1])

totalRankingsGraph()

app = App(title="Elo ranking",bg="light grey",height=1000,width=1500)
home_box = Box(master=app,layout="grid",visible=True)
home_title = Text(master=home_box,text="Welcome to Elo Ranking",grid=[5,0],size=30,font="courier new")
home_start_btn = PushButton(master=home_box,text="Start",grid=[10,10],padx=10,pady=10,command=home_to_comp)
home_settings_btn = PushButton(master=home_box,text="Settings",grid=[5,10],command=home_to_settings,padx=10,pady=10)
home_quit_btn = PushButton(master=home_box,text="Quit",grid=[0,10],command=quit_app,padx=10,pady=10)

settings_box = Box(master=app,layout="grid",visible=False)
settings_title = Text(master=settings_box,text="Settings",grid=[5,0],size=30,font="courier new")
settings_home_btn = PushButton(master=settings_box,text="Home",grid=[0,10],command=settings_to_home,padx=10,pady=10)
settings_top5_btn = PushButton(master=settings_box,text="Display top 5 rated",grid=[5,5],command=displayTop5Ratings,padx=10,pady=10)
settings_rank_history_btn = PushButton(master=settings_box,text="Individual item rank history",grid=[6,5],command=settings_to_rank_history,padx=10,pady=10)

top5_ratings_box = Box(master=app,layout="grid",visible=False)
top5_rating_title = Text(master=top5_ratings_box,text="Top 5 Rated Items",grid=[0,0],size=30,font="courier new")
top5_rated_1 = Text(master=top5_ratings_box,text="1.",grid=[0,2],size=30,font="courier new",align="left")
top5_rated_2 = Text(master=top5_ratings_box,text="2.",grid=[0,3],size=30,font="courier new",align="left")
top5_rated_3 = Text(master=top5_ratings_box,text="3.",grid=[0,4],size=30,font="courier new",align="left")
top5_rated_4 = Text(master=top5_ratings_box,text="4.",grid=[0,5],size=30,font="courier new",align="left")
top5_rated_5 = Text(master=top5_ratings_box,text="5.",grid=[0,6],size=30,font="courier new",align="left")
top5_rated_text_list = [top5_rated_1,top5_rated_2,top5_rated_3,top5_rated_4,top5_rated_5]
top5_rat_to_settings = PushButton(master=top5_ratings_box,text="Back",grid=[0,10],command=top5_to_settings,padx=10,pady=10)

rank_history_box = Box(master=app,layout="grid",visible=False)
rank_history_title = Text(master=rank_history_box,text="Rank history",grid=[0,0],size=30,font="courier new",align="left")
rank_his_to_settings = PushButton(master=rank_history_box,text="Back",grid=[0,10],command=rank_history_to_settings,padx=10,pady=10)



comp_box = Box(master=app,layout="grid",visible=False)
comp_home_button = PushButton(master=comp_box,text="Home",grid=[0,10],command=comp_to_home,padx=10,pady=10)
comp_title = Text(master=settings_box,text="Competitive",grid=[5,0],size=30,font="courier new")
picture1 = Picture(master=comp_box,grid=[2,2],image=PATH+mainStage.item1.name,width=480,height=854)
picture2 = Picture(master=comp_box,grid=[4,2],image=PATH+mainStage.item2.name,width=480,height=854)
comp1_btn = PushButton(master=comp_box,text="OPTION 1",grid=[1,2],command=item1Winner,padx=10,pady=10)
comp2_btn = PushButton(master=comp_box,text="OPTION 2",grid=[5,2],command=item2Winner,padx=10,pady=10)

app.display()