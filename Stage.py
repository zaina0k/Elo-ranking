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