class Item:
    """item class encapsulates each rated item carrying its current rating
    as well as carrying its rating history as an 1d array"""
    def __init__(self,name,rating=1500,ratingHistory=[1500]):
        self.name = name
        self.rating = rating
        self.ratingHistory = ratingHistory.copy()
    def resetRating(self):
        self.rating = 1500
    def resetHistory(self):
        self.ratingHistory.clear()
        self.ratingHistory = [1500]
    def updateStats(self,newRating):
        self.ratingHistory.append(round(newRating))
        if newRating <= 0:
            self.rating = 0
        else:
            self.rating = round(newRating)
    def toDict(self):
        return {"name":self.name,"rating":self.rating,"ratingHistory":self.ratingHistory}

    def __str__(self):
        print_str = ""
        print_str += "Name: " + str(self.name) + "\n"
        print_str += "Rating: " + str(self.rating) + "\n"
        print_str += "Rating history: " + str(self.ratingHistory) + "\n"
        return(print_str)