

# small
# adult
# housebroken
# preferably shih tzu


import requests, bs4

BASE_URL = 'https://www.arflife.org/'

def getDogs():
    adoptables = []
    res = requests.get(BASE_URL+'/dogs', headers={'User-Agent':'Arfy/1.0 (https://github.com/Kyle-Falconer/arfy; kfalconer@gmail.com)'})
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    adoptableElems = soup.select(".iadopt")
    if adoptableElems == []:
        print('Could not find any adoptables.')
    else:
        for index, item in enumerate(adoptableElems):
            dog = {}
            dog['age'] = item["data-age"]
            dog['name'] = item['data-alph']
            dog['url'] = BASE_URL+adoptableElems[index].find('a')['href']
            dog['img'] = adoptableElems[index].find('div', {"class":"iadopt_img"}).find('img')['src']
            dog['breed'] = adoptableElems[index].find('div', {"class":"txt_12"}).text.split('  ')[0]
            adoptables.append(dog)
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



def main():
    #dogs = [{'breed': 'Chihuahua Mix', 'age': 'Young', 'name': 'Lucetta', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/5/1/8/220332046.jpg', 'url': 'https://www.arflife.org/dogs/16258942'}, {'breed': 'Pointer / Shar Pei', 'age': 'Young', 'name': 'Aliena', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/7/f/224593911.jpg', 'url': 'https://www.arflife.org/dogs/16454181'}, {'breed': 'Rat Terrier Mix', 'age': 'Adult', 'name': 'Bambi', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/4/5/224960982.jpg', 'url': 'https://www.arflife.org/dogs/16470768'}, {'breed': 'Plott Hound / Terrier (Unknown Type, Medium)', 'age': 'Puppy', 'name': 'Husker Du', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/4/2/3/224961016.jpg', 'url': 'https://www.arflife.org/dogs/16470769'}, {'breed': 'Labrador Retriever / Shepherd (Unknown Type)', 'age': 'Young', 'name': 'Koffi', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/7/7/8/223952148.jpg', 'url': 'https://www.arflife.org/dogs/16426567'}, {'breed': 'Chihuahua / Terrier (Unknown Type, Small)', 'age': 'Adult', 'name': 'Luke', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/7/7/3/223129430.jpg', 'url': 'https://www.arflife.org/dogs/16376675'}, {'breed': 'Labrador Retriever Mix', 'age': 'Adult', 'name': 'Milhiser', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/d/1/223780987.jpg', 'url': 'https://www.arflife.org/dogs/16418665'}, {'breed': 'Chihuahua Mix', 'age': 'Adult', 'name': 'Oz', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/1/2/223781002.jpg', 'url': 'https://www.arflife.org/dogs/16391099'}, {'breed': 'Border Collie Mix', 'age': 'Adult', 'name': 'Palamon', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/1/2/2/222431716.jpg', 'url': 'https://www.arflife.org/dogs/16269011'}, {'breed': 'Beagle Mix', 'age': 'Senior', 'name': 'Phoenix', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/4/0/6/224767914.jpg', 'url': 'https://www.arflife.org/dogs/16461796'}, {'breed': 'Dachshund Mix', 'age': 'Young', 'name': 'Winston Zeddemore', 'img': '/images/NoPetImage.jpg', 'url': 'https://www.arflife.org/dogs/16434485'}, {'breed': 'Hound (Unknown Type) Mix', 'age': 'Adult', 'name': 'Yahtzee', 'img': 'https://s3.amazonaws.com/pet-uploads.adoptapet.com/b/d/e/222643719.jpg', 'url': 'https://www.arflife.org/dogs/16368562'}]
    #print(formatAdoptableAsHtml(dogs[0]))
    #print(dogs[0])
    print(getDogs())

if __name__ == '__main__':
    main()