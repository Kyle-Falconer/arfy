

# small
# adult
# housebroken
# preferably shih tzu


import requests, bs4
from datetime import datetime
import json
import emailer
import config
import threading

BASE_URL = 'https://www.arflife.org/'
PETS_FILE = 'pets.json'

def getCurrentDogs():
    adoptables = {}
    dogs_seen_today = []
    res = requests.get(BASE_URL+'/dogs', headers={'User-Agent':'Arfy/1.0 (https://github.com/Kyle-Falconer/arfy; kfalconer@gmail.com)'})
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    adoptableElems = soup.select(".iadopt")
    if adoptableElems == []:
        print('Could not find any new adoptables.')
    else:
        for index, item in enumerate(adoptableElems):
            dog_id = adoptableElems[index].find('a')['href'].split('/')[1]
            dogs_seen_today.append(dog_id)
            dog = {}
            dog['id'] = adoptableElems[index].find('a')['href'].split('/')[1]
            dog['age'] = item["data-age"]
            dog['name'] = item['data-alph']
            dog['url'] = BASE_URL+dog['id']
            dog['img'] = adoptableElems[index].find('div', {"class":"iadopt_img"}).find('img')['src']
            if dog['img'] == '/images/NoPetImage.jpg':
                dog['img'] = BASE_URL + '/images/NoPetImage.jpg'
            dog['breed'] = adoptableElems[index].find('div', {"class":"txt_12"}).text.split('  ')[0]
            dog["date_added"] = str(datetime.now())
            adoptables[dog['id']] = dog
    # todo: use dogs_seen_today to add the "last_seen_on field"
    return adoptables


def formatAdoptableAsHtml(adoptable):
    _pet = dict(adoptable)
    _pet['url'] = '<a href="{0}">{0}</a>'.format(_pet['url'])
    img = '<img src="{0}"/>'.format(_pet['img'])
    _pet.pop('img', None)
    html = ["<table width=100%>"]
    html.append("<tr><td colspan=2>{0}</td></tr>".format(img))
    for key, value in _pet.items():
        html.append("<tr>")
        html.append("<td>{0}</td>".format(key))
        html.append("<td>{0}</td>".format(value))
        html.append("</tr>")
    html.append("</table>")
    return ''.join(html)


def getNewPetsList(previous, current):
    new_pets = []
    for dog in current:
        if dog not in previous:
            new_pets.append(current[dog])
    return new_pets


def updatePetsList(previous, current):
    updated_pets = previous.copy()
    updated_pets.update(current)
    for dog in previous:
        if dog not in current:
            updated_pets[dog]['date_removed'] = str(datetime.now())
    return updated_pets


def notify(new_dogs):    
    new_dogs_names = []
    message = []
    for d in new_dogs:
        dog = new_dogs[d]
        new_dogs_names.append(dog['name'])
        message.append(formatAdoptableAsHtml(dog))
    subject = "Arfy found new dogs: {0}".format(", ".join(new_dogs_names))
    
    emailer.sendMail(subject = subject, content="".join(message))

def readPetsFromDisk():
    with open(PETS_FILE) as data_file:    
        data = json.load(data_file)
        return data

def writePetsToDisk(pets_list):
    with open(PETS_FILE, 'w') as outfile:
        json.dump(pets_list, outfile)

def run():
    previous = readPetsFromDisk()
    current_dogs = getCurrentDogs()
    new_pets = getNewPetsList(previous, current_dogs)
    updated_pets = updatePetsList(previous, current_dogs)
    notify(current_dogs)
    writePetsToDisk(updated_pets)
    threading.Timer(config.delay, run).start()

def main():
    run()

if __name__ == '__main__':
    main()