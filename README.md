# Elo-ranking
Elo ranking

Description:
Elo ranking is a python project that showcases the elo ranking system commonly used in chess in the context of comparing photos.

Elo Ranking (https://en.wikipedia.org/wiki/Elo_rating_system)
The elo ranking system is a system devised to compare to players (in this case photos) and add or subtract (whether they win or lose) from their rating based on how likely they were to win.
For example, all items start with the same rating (1500) and are therefore all equally likely to win or lose but an item with 400 elo more than its competition will be 10x more likely to win

GUIZERO (https://lawsie.github.io/guizero/about/) 
A tkinter based library to provide a GUI for the user.
GUIZERO allows for the program to display the photos to be compared and contains a menu system that allows the user to view the current stats of individual photos.

Matplotlib (https://matplotlib.org)
A graphing library that allows the project to showcase 1 or more pictures' history as a line chart.
This allows the user to see the progress of individual pictures in terms of their rating.

JSON (https://docs.python.org/3/library/json.html)
A library that allows the picture item objects to be serialised and saved into a file that is stored in the current directory.
The JSON file acts as a local database to save and load the rating and progress of the photo item objects.



![image](https://user-images.githubusercontent.com/70727546/212143466-9f73c320-77d6-41e1-a9fb-089af60216a6.jpeg)
Figure 1:
Showcasing the photo comparison GUI. There are 2 photos with a button either side for the user to choose a "winner"


![image](https://user-images.githubusercontent.com/70727546/212144929-02f00922-77dc-4ed1-b7ba-56949357f8c1.jpeg)
Figure 2:
Showcasing the individual rank feature. A drop down box allows the user to select a photo item to showcase. The specific image is shown alongside the rank as well as a graph of the rating history.


![image](https://user-images.githubusercontent.com/70727546/212143839-b99143ff-d743-4034-b4a7-c21365f28369.jpeg)
Figure 3:
Showcasing the group rank feature. Using a slider the user can choose a set amount of picture item graphs to plot. This overlay allows the user to view the progression over time. (slider organises by the best currently rated photos. i.e. 5 on the slider will plot the top 5 ranked photos)
