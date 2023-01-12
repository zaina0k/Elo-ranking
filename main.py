from guizero import App,PushButton,Text,Box,Picture,TextBox,Combo,Slider
from os import walk,rename
import os
from random import shuffle
import matplotlib. pyplot as plt
from operator import itemgetter
import json
from Item import Item
from Stage import Stage

PATH = "temp/"
filenames = next(walk(PATH), (None, None, []))[2]  # [] if no file
try:
    filenames.remove(".DS_Store")
except:
    pass
population = []

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
    if os.path.exists("db.json"):
        os.remove("db.json")

def initialisePopulation():
    global filenames
    global population
    if os.path.exists("db.json"):#if existing file save
        with open('db.json', 'r') as openfile:
            json_object = json.load(openfile)
            openfile.close()
        for item in json_object:
            population.append(Item(name=item["name"],rating=item["rating"],ratingHistory=item["ratingHistory"]))
        print("file successfully loaded")
    else:#if no save data
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

def totalRankingsGraph(num):
    """looks for the top 5 ratings
    pairs item names as key with their rating as value in a dictionary"""
    global population
    if num > len(population):
        return None
    rankDict = {}
    for item in population:
        rankDict[item.name] = item.rating
    top5Dict = dict(sorted(rankDict.items(), key = itemgetter(1), reverse = True)[:num])
    return top5Dict

def simulateRankedPlay(num):
    for i in range(num):
        item1Winner()

def populationSort():
    global population
    newlist = sorted(population, key=lambda x: x.rating, reverse=True)
    return newlist

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
    pic_name1.value = mainStage.item1.name
    pic_name2.value = mainStage.item2.name

def nextComp():
    newPics = chooseCompetitors(mainStage)
    mainStage.resetStage()
    mainStage.setStage(newPics[0],newPics[1])
    resetPhotos()

def displayTop5Ratings():
    global top5_rated_text_list
    top5Dict = totalRankingsGraph(5)
    counter = 0
    for item in top5Dict:
        counter += 1
        if counter >5:
            break
        else:
            top5_rated_text_list[counter-1].value = str(counter) + ". " + str(item) + ": " + str(top5Dict[item])
    settings_box.hide()
    top5_ratings_box.show()

def plotHistory(object=None):
    for item in population:
        if item.name == rank_his_dropdown.value:
            rank_his_picture.image=PATH+item.name
            rank_his_cur_rank.value = "Current Rank: " + str(item.rating)
            object = item
    if object==None:
        return None
    else:
        rankHistory = object.ratingHistory
        plt.title("Interesting ranking graph")
        plt.plot(rankHistory,label=object.name)
        plt.legend()
        plt.grid(visible=True)
        plt.show()

def dev_simulate_button():
    user_input = dev_sim_input.value
    if user_input.isdigit():
        if int(user_input) <= 100:
            print("simulating " + str(user_input) + " times")
            simulateRankedPlay(int(user_input))
        else:
            print("only simulate 100 or less at a time")
    else:
        print("enter a number into the text box")

def save_progress():
    settings_to_home()
    results = [obj.toDict() for obj in population]
    jsdata = json.dumps(results,indent=4)
    with open("db.json", "w") as outfile:
        outfile.write(jsdata)
        outfile.close()

def current_most_frequent_voted():
    mx = 0
    pr = None
    for item in population:
        if len(item.ratingHistory) > mx:
            pr = item
            mx = len(item.ratingHistory)
    print(pr)

def total_recall():
    global population
    population = populationSort()
    total_graph = [obj.toDict() for obj in population]
    total_graph = total_graph[:int(dev_total_recall_slider.value)]
    for item in total_graph:
        plt.plot(item["ratingHistory"],label=item["name"])
    plt.legend()
    plt.grid(visible=True)
    plt.title(label="Top " + str(dev_total_recall_slider.value) + " rated items")
    plt.show()

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
    pic_name1.value = mainStage.item1.name
    pic_name2.value = mainStage.item2.name

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

def settings_to_dev():
    settings_box.hide()
    dev_box.show()

def dev_to_settings():
    dev_box.hide()
    settings_box.show()

##START##
initialisePopulation()
mainStage = Stage()
initialItems = chooseCompetitors()
mainStage.setStage(initialItems[0],initialItems[1])

#Home Page
app = App(title="Elo ranking",bg="dark grey",height=1000,width=1500)
home_box = Box(master=app,layout="grid",visible=True)
home_title = Text(master=home_box,text="Welcome to Elo Ranking",grid=[5,0],size=30,font="courier new")
home_start_btn = PushButton(master=home_box,text="Start",grid=[10,10],padx=10,pady=10,command=home_to_comp)
home_settings_btn = PushButton(master=home_box,text="Settings",grid=[5,10],command=home_to_settings,padx=10,pady=10)
home_quit_btn = PushButton(master=home_box,text="Quit",grid=[0,10],command=quit_app,padx=10,pady=10)

#Settings page
settings_box = Box(master=app,layout="grid",visible=False)
settings_title = Text(master=settings_box,text="Settings",grid=[5,0],size=30,font="courier new")
settings_home_btn = PushButton(master=settings_box,text="Home",grid=[4,6],command=settings_to_home,padx=10,pady=10,align="right")
settings_top5_btn = PushButton(master=settings_box,text="Display top 5 rated",grid=[6,5],command=displayTop5Ratings,padx=10,pady=10,align="left")
settings_rank_history_btn = PushButton(master=settings_box,text="Individual item rank history",grid=[6,6],command=settings_to_rank_history,padx=10,pady=10,align="left")
settings_dev_btn = PushButton(master=settings_box,text="DEV",grid=[4,5],command=settings_to_dev,padx=10,pady=10,align="right")
settings_save_btn = PushButton(master=settings_box,text="SAVE",grid=[5,5],command=save_progress,padx=10,pady=10)

#Top 5 ratings page
top5_ratings_box = Box(master=app,layout="grid",visible=False)
top5_rating_title = Text(master=top5_ratings_box,text="Top 5 Rated Items",grid=[0,0],size=30,font="courier new")
top5_rated_1 = Text(master=top5_ratings_box,text="1.",grid=[0,2],size=30,font="courier new",align="left")
top5_rated_2 = Text(master=top5_ratings_box,text="2.",grid=[0,3],size=30,font="courier new",align="left")
top5_rated_3 = Text(master=top5_ratings_box,text="3.",grid=[0,4],size=30,font="courier new",align="left")
top5_rated_4 = Text(master=top5_ratings_box,text="4.",grid=[0,5],size=30,font="courier new",align="left")
top5_rated_5 = Text(master=top5_ratings_box,text="5.",grid=[0,6],size=30,font="courier new",align="left")
top5_rated_text_list = [top5_rated_1,top5_rated_2,top5_rated_3,top5_rated_4,top5_rated_5]
top5_rat_to_settings = PushButton(master=top5_ratings_box,text="Back",grid=[0,10],command=top5_to_settings,padx=10,pady=10)

#Rank history page
rank_history_box = Box(master=app,layout="grid",visible=False)
rank_history_title = Text(master=rank_history_box,text="Rank history",grid=[0,0],size=30,font="courier new",align="left")
rank_his_to_settings = PushButton(master=rank_history_box,text="Back",grid=[0,10],command=rank_history_to_settings,padx=10,pady=10)
rank_his_show_btn = PushButton(master=rank_history_box,text="Show",grid=[5,5],command=plotHistory,padx=10,pady=10)
rank_his_dropdown = Combo(master=rank_history_box,options=filenames,grid=[4,5])
rank_his_picture = Picture(master=rank_history_box,grid=[10,5],width=480,height=854)
rank_his_cur_rank = Text(master=rank_history_box,text="",grid=[10,6],size=30,font="courier new",align="left")

#Developer page
dev_box = Box(master=app,layout="grid",visible=False)
dev_title = Text(master=dev_box,text="Dev options",grid=[5,0],size=30,font="courier new")
dev_sim_input = TextBox(master=dev_box,grid=[6,5],align="left")
dev_simulate = PushButton(master=dev_box,text="Simulate",grid=[7,5],command=dev_simulate_button,padx=10,pady=10,align="left")
dev_to_settings_btn = PushButton(master=dev_box,text="Back",grid=[0,10],command=dev_to_settings,padx=10,pady=10,align="left")
dev_reset_btn = PushButton(master=dev_box,text="FULL RESET",grid=[0,6],command=fullReset,padx=10,pady=10,align="left")
dev_most_history_btn = PushButton(master=dev_box,text="History",grid=[0,7],command=current_most_frequent_voted,padx=10,pady=10,align="left")
dev_total_recall_btn = PushButton(master=dev_box,text="Full graph",grid=[7,6],command=total_recall,padx=10,pady=10,align="left")##
dev_total_recall_slider = Slider(master=dev_box,start=0,end=len(population),grid=[6,6])

#Comparing items page
comp_box = Box(master=app,layout="grid",visible=False)
comp_home_button = PushButton(master=comp_box,text="Home",grid=[0,10],command=comp_to_home,padx=10,pady=10)
comp_title = Text(master=comp_box,text="Competitive",grid=[1,0],size=30,font="courier new")
picture1 = Picture(master=comp_box,grid=[2,2],image=PATH+mainStage.item1.name,width=480,height=854,align="right")
picture2 = Picture(master=comp_box,grid=[4,2],image=PATH+mainStage.item2.name,width=480,height=854,align="left")
pic_name1 = Text(master=comp_box,text="Picture 1",grid=[2,3],size=30,font="courier new")
pic_name2 = Text(master=comp_box,text="Picture 2",grid=[4,3],size=30,font="courier new")

comp1_btn = PushButton(master=comp_box,text="OPTION 1",grid=[1,2],command=item1Winner,padx=10,pady=10,align="right")
comp2_btn = PushButton(master=comp_box,text="OPTION 2",grid=[5,2],command=item2Winner,padx=10,pady=10)

app.display()