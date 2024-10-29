import requests
import xml.etree.ElementTree as ET
import pandas as pd # type: ignore
import numpy as np
import matplotlib.pyplot as plt # type: ignore

url = "https://api.geekdo.com/xmlapi/collection/megtrinity"
response = requests.get(url)

# Voir doc https://docs.python.org/fr/3/library/xml.etree.elementtree.html
if response.status_code == 200:
    root = ET.fromstring(response.content)
    
    data = []
    for item in root.findall('item'):
        mydata = {
            'name': item.find('name').text,
            'year_published': item.find('yearpublished').text,
            'num_plays': item.find('numplays').text,
            'minplayers': item.find('stats').get('minplayers') ,
            'maxplayers': item.find('stats').get('maxplayers') ,
            'playingtime': item.find('stats').get('playingtime'),
            'usersrated': item.find('stats/rating/usersrated').get('value'), 
            'own': item.find('status').get('own'),
            'want': item.find('status').get('want'),
            'wishlist': item.find('status').get('wishlist')
        }
        data.append(mydata)
#print(data)

dataframe = pd.DataFrame(data)
dataframe['own'] = dataframe['own'].astype(int)
sommejeuxown = dataframe['own'].sum()
print('La somme des jeux détenus  est de :', sommejeuxown)

#Moyenne
dataframe['playingtime'] = dataframe['playingtime'].astype(int)
moyenne = np.mean(dataframe['playingtime'])
print('La moyenne de temps de jeu est:', moyenne)

#Exporter le dataframe pandas en CSV
dataframe.to_csv('dataframe_eval', index=False)

#Histogramme, repris de : https://fr.moonbooks.org/Articles/Simple-histogramme-avec-matplotlib/
plt.hist(dataframe['year_published'])
plt.title('Histogramme des années de sorties des jeux')
plt.savefig('Histogramme')
#plt.show() # PLT show ne marche pas sur Linux ? 

#Graphiques en barres comparant nombre moyen de joueurs mini et maxi requis
moyminijoueurs = np.mean(dataframe['minplayers'])
moymaxjoueurs = np.mean(dataframe['maxplayers'])
fig, ax = plt.subplot
ax.plot(moyminijoueurs, moymaxjoueurs)
plt.savefig('moyennejoueurs')
