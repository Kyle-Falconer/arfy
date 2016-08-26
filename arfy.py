

# small
# adult
# housebroken
# preferably shih tzu


import requests, bs4
from datetime import datetime
import json

BASE_URL = 'https://www.arflife.org/'
PETS_FILE = 'pets.json'

def getNewDogs(current_dogs):
    new_adoptables = {}
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
            if dog_id not in current_dogs:
                dog = {}
                dog['id'] = adoptableElems[index].find('a')['href'].split('/')[1]
                dog['age'] = item["data-age"]
                dog['name'] = item['data-alph']
                dog['url'] = BASE_URL+dog['id']
                dog['img'] = adoptableElems[index].find('div', {"class":"iadopt_img"}).find('img')['src']
                dog['breed'] = adoptableElems[index].find('div', {"class":"txt_12"}).text.split('  ')[0]
                dog["date_added"] = str(datetime.now())
                new_adoptables[dog['id']] = dog
    # todo: use dogs_seen_today to add the "last_seen_on field"
    return new_adoptables


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

def getNewGetPetsList(old_a, new_a):
    newly_added = []
    for p in new_a:
        if p not in old_a:
            newly_added.append(new_a[p])
    return newly_added

def notify(new_dogs):
    print("found some new dogs:")
    print(new_dogs)

def readPetsFromDisk():
    with open(PETS_FILE) as data_file:    
        data = json.load(data_file)
        return data

def writePetsToDisk(pets_list):
    with open(PETS_FILE, 'w') as outfile:
        json.dump(pets_list, outfile)


def main():
    dogs_a = { '16258942' : {'name': 'Lucetta', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/5/1/8/220332046.jpg', 'url': 'https://www.arflife.org/dogs/16258942', 'age': 'Young', 'breed': 'Chihuahua Mix'}, '16454181' : {'name': 'Aliena', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/7/f/224593911.jpg', 'url': 'https://www.arflife.org/dogs/16454181', 'age':'Young', 'breed': 'Pointer / Shar Pei'}, '16470768' : {'name': 'Bambi', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/4/5/224960982.jpg', 'url': 'https://www.arflife.org/dogs/16470768', 'age':'Adult', 'breed': 'Rat Terrier Mix'}, '16470769' : {'name': 'Husker Du', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/4/2/3/224961016.jpg', 'url': 'https://www.arflife.org/dogs/16470769', 'age':'Puppy', 'breed': 'Plott Hound / Terrier (Unknown Type, Medium)'},'16426567' : {'name': 'Koffi', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/7/7/8/223952148.jpg', 'url': 'https://www.arflife.org/dogs/16426567', 'age':'Young', 'breed': 'Labrador Retriever / Shepherd (Unknown Type)'},'16376675' : {'name': 'Luke', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/7/7/3/223129430.jpg', 'url': 'https://www.arflife.org/dogs/16376675', 'age':'Adult', 'breed': 'Chihuahua / Terrier (Unknown Type, Small)'},'16418665' : {'name': 'Milhiser', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/d/1/223780987.jpg', 'url': 'https://www.arflife.org/dogs/16418665', 'age':'Adult', 'breed': 'Labrador Retriever Mix'}, '16391099' : {'name': 'Oz', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/1/2/223781002.jpg', 'url': 'https://www.arflife.org/dogs/16391099', 'age':'Adult', 'breed': 'Chihuahua Mix'}, '16269011' : {'name': 'Palamon', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/2/2/222431716.jpg', 'url': 'https://www.arflife.org/dogs/16269011', 'age':'Adult', 'breed': 'Border Collie Mix'},' 16461796' : {'name': 'Phoenix', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/4/0/6/224767914.jpg', 'url': 'https://www.arflife.org/dogs/16461796', 'age':'Senior', 'breed': 'Beagle Mix'}, '16434485' : {'name': 'Winston Zeddemore', 'img': '/images/NoPetImage.jpg', 'url': 'https://www.arflife.org/dogs/16434485', 'age': 'Young', 'breed': 'Dachshund Mix'}, '16368562' : {'name': 'Yahtzee', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/d/e/222643719.jpg', 'url': 'https://www.arflife.org/dogs/16368562', 'age': 'Adult', 'breed': 'Hound (Unknown Type) Mix'}}
    dogs_b = { '16478473' : {'name': 'Clementine', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/9/4/5/225125246.jpg', 'breed': 'Poodle (Toy or Tea Cup) / Cocker Spaniel', 'id': '16478473', 'age': 'Adult', 'url': 'https://www.arflife.org/16478473'}, '16478478': {'name': 'Sprinkle', 'img': '/images/NoPetImage.jpg', 'breed': 'Rhodesian Ridgeback Mix', 'id': '16478478', 'age': 'Puppy', 'url': 'https://www.arflife.org/16478478'}, '16478477': {'name': 'Sugar', 'img': '/images/NoPetImage.jpg', 'breed': 'Rhodesian Ridgeback Mix', 'id': '16478477', 'age': 'Puppy', 'url': 'https://www.arflife.org/16478477'}, '16454181': {'name': 'Aliena', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/7/f/224593911.jpg', 'breed': 'Pointer / Shar Pei', 'id': '16454181', 'age': 'Young', 'url': 'https://www.arflife.org/16454181'}, '16391099': {'name': 'Oz', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/1/2/223781002.jpg', 'breed': 'Chihuahua Mix', 'id': '16391099', 'age': 'Adult', 'url': 'https://www.arflife.org/16391099'}, '16478481': {'name': 'Long John', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/1/4/225125364.jpg', 'breed': 'Dachshund / Chihuahua', 'id': '16478481', 'age': 'Puppy', 'url': 'https://www.arflife.org/16478481'}, '16478476': {'name': 'Maple', 'img': '/images/NoPetImage.jpg', 'breed': 'Rhodesian Ridgeback Mix', 'id': '16478476', 'age': 'Puppy', 'url': 'https://www.arflife.org/16478476'}, '16426567': {'name': 'Koffi', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/7/7/8/223952148.jpg', 'breed': 'Labrador Retriever / Shepherd (Unknown Type)', 'id': '16426567', 'age': 'Young', 'url': 'https://www.arflife.org/16426567'}, '16478480': {'name': 'Cronut', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/8/6/7/225125337.jpg', 'breed': 'Jack Russell Terrier Mix', 'id': '16478480', 'age': 'Adult', 'url': 'https://www.arflife.org/16478480'}, '16258942': {'name': 'Lucetta', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/5/1/8/220332046.jpg', 'breed': 'Chihuahua Mix', 'id': '16258942', 'age': 'Young', 'url': 'https://www.arflife.org/16258942'}, '16269011': {'name': 'Palamon', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/2/2/222431716.jpg', 'breed': 'Border Collie Mix', 'id': '16269011', 'age': 'Adult', 'url': 'https://www.arflife.org/16269011'}, '16470769': {'name': 'Husker Du', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/4/2/3/224961016.jpg', 'breed': 'Plott Hound / Terrier (Unknown Type, Medium)', 'id': '16470769', 'age': 'Puppy', 'url': 'https://www.arflife.org/16470769'}, '16368562': {'name': 'Yahtzee', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/d/e/222643719.jpg', 'breed': 'Hound (Unknown Type) Mix', 'id': '16368562', 'age': 'Adult', 'url': 'https://www.arflife.org/16368562'}, '16418665': {'name': 'Milhiser', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/d/1/223780987.jpg', 'breed': 'Labrador Retriever Mix', 'id': '16418665', 'age': 'Adult', 'url': 'https://www.arflife.org/16418665'}, '16478479': {'name': 'Spudnut', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/5/1/6/225125316.jpg', 'breed': 'Rat Terrier Mix', 'id': '16478479', 'age': 'Adult', 'url': 'https://www.arflife.org/16478479'}, '16470768': {'name': 'Bambi', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/4/5/224960982.jpg', 'breed': 'Rat Terrier Mix', 'id': '16470768', 'age': 'Adult', 'url': 'https://www.arflife.org/16470768'}, '16478475': {'name': 'Fritter', 'img': '/images/NoPetImage.jpg', 'breed': 'Rhodesian Ridgeback Mix', 'id': '16478475', 'age': 'Puppy', 'url': 'https://www.arflife.org/16478475'}, '16376675': {'name': 'Luke', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/7/7/3/223129430.jpg', 'breed': 'Chihuahua / Terrier (Unknown Type, Small)', 'id': '16376675', 'age': 'Adult', 'url': 'https://www.arflife.org/16376675'}, '16478474': {'name': 'Johnny Castle', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/3/b/7/225125301.jpg', 'breed': 'Poodle (Toy or Tea Cup) Mix', 'id': '16478474', 'age': 'Adult', 'url': 'https://www.arflife.org/16478474'}, '16434485': {'name': 'Winston Zeddemore', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/1/c/225125279.jpg', 'breed': 'Dachshund Mix', 'id': '16434485', 'age': 'Young', 'url': 'https://www.arflife.org/16434485'}}
    #print(formatAdoptableAsHtml(dogs[0]))
    #print(dogs[0])
    #print(getDogs())
    #print(getNewGetPetsList(dogs_a, dogs_b))

    pets = readPetsFromDisk()
    new_dogs = getNewDogs(pets)
    updated_pets = pets.copy()
    updated_pets.update(new_dogs)
    notify(new_dogs)
    writePetsToDisk(updated_pets)

if __name__ == '__main__':
    main()