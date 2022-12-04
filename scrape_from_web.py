from bs4 import BeautifulSoup
import requests
import json
import gzip
import unidecode

canadian_franchies_url = "https://en.wikipedia.org/wiki/List_of_Canadian_restaurant_chains#The_Works"
us_franchies_url = "https://www.fsdbco.com/top-250-restaurant-chains-us-2019/"

restaurants_names = []

body = requests.get(canadian_franchies_url)
body_text = body.content  

soup = BeautifulSoup(body_text, 'lxml')
names = soup.find_all('span', class_='toctext')
for name in names: 
    text = name.text
    text = unidecode.unidecode(text)
    restaurants_names.append({
        'name': text
    })

body = requests.get(us_franchies_url)
body_text = body.content  

soup = BeautifulSoup(body_text, 'lxml')
trs = soup.find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    text = tds[1].text
    text = unidecode.unidecode(text)
    restaurants_names.append({
        'name': text
    })

json_object = json.dumps(restaurants_names, indent=4)
 

filename = "franchise_restaurants.json.gz"
# with open("franchise_restaurants.json", "w") as outfile:
#     outfile.write(json_object)

with gzip.open(filename, 'wt', encoding='UTF-8') as zipfile:
    json.dump(json_object, zipfile)