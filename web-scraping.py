import requests
import os
from bs4 import BeautifulSoup

from dataclasses import dataclass

@dataclass
class Dog:
    id: int
    name: str
    status: str
    gender: str
    age: str
    size: str 
    breed: str
    cross_breed: str
    childrenFriend: str
    catFriend: str
    dogFriend: str
    begginerFriend: str
    gardenFriend: str
    flatFriend: str
    activeFriend: str
    color: str
    tattoo: str
    neutered: str
    handicap: str
    find_location: str
    region: str
    find_date: str
    actual_location: str
    detailed_description: str

    def __str__(self):
        return f'Pes se jménem {self.name}, status: {self.status}, pohlaví: {self.gender}, jeho plemeno je {self.breed} a jeho velikost je {self.size}. Kříženec: {self.cross_breed}.'

def get_from_tbl(document, width_percent: str):
    element = document.find('td', {'width': width_percent})
    
    if element:
        for tag in element(['h3']):
            tag.decompose()
        
        return element.get_text().strip()
        
    return 'N/A'


def get_table_data(document, header_string):
    th = document.find('th', string=header_string)
    return th.find_next_sibling('td').get_text().strip() if th else None


def suitable_data(document, suitable: str):
    ul = document.find('ul', class_ = 'suitable')
    classes = ul.find('li', string=suitable).get('class')

    return classes[0].strip() if len(classes) > 0 else 'Unknown'

def get_detailed_descr(document: BeautifulSoup):
    header = document.find('h2', string='Podrobný popis')
    if header is None:
        return 'N/A'
    sibling = header.find_next_sibling('p')
    if sibling is None:
        if len(header.find_next_sibling().get_text()) > 0:
            return header.findNextSibling().get_text().strip().replace('\n', ' EOL ')
    
    detailed_description_output = []
    while sibling is not None:
        detailed_description_output.append(sibling.get_text().strip() + ' EOL ')
        sibling = sibling.find_next_sibling('p')
    return ''.join(detailed_description_output)


objid = 1

maxCount_notFound = 10000
counter_notFound = 0

file_path = 'projekt_utulky/data_shelter_dogs.csv'

if not os.path.exists(file_path):
    with open(file_path, mode='w') as file:
        attributes = Dog.__annotations__.keys()
        file.write(';'.join(attributes) + '\n')

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
while counter_notFound < maxCount_notFound:

    try:
        objid += 1

        data = requests.get(url=f'https://www.pesweb.cz/cz/psi-k-adopci?objid={objid}', headers=headers).text.replace('&nbsp;', ' ')
        document = BeautifulSoup(data, 'html.parser')

        print(f'Parsuji stránku pro psa s id {objid}')

        name = document.find('h1', {'class': 'nadpis'}).get_text().strip()

        if name == 'Psi k adopci':
            print(f'Pes s id {objid} neexistuje')
            counter_notFound += 1
            continue
        
        if name.startswith('- '):
            status = name.split('- ')[1]
            name = 'N/A'
        elif '-' in name:
            name_split = name.rsplit('-', 1)
            name = name_split[0].strip()
            status = name_split[1].strip()
        else:
            status = 'N/A'

        gender = get_from_tbl(document, '27%')
        
        age = get_from_tbl(document, '28%')
    
        size = get_from_tbl(document, '55%')
        
        breed_div = document.find('div', {'id': 'breed'})
        
        if len(list(breed_div.children)) > 1:
            breed = breed_div.find('a').get_text().strip()
            cross_breed = breed_div.get_text().replace(breed, '').strip()
        else:
            if breed_div.get_text().strip() == 'Kříženec':
                breed = 'N/A'
                cross_breed = breed_div.get_text().strip()
            else:
                breed = breed_div.get_text().strip()
                cross_breed = 'N/A'

        
        childrenFriend = suitable_data(document, 'Hodí se k dětem')

        catFriend = suitable_data(document, 'Kočičí kamarád')
        
        dogFriend = suitable_data(document, 'K jiným psům')
        
        begginerFriend = suitable_data(document, 'Pro začátečníky')
        
        gardenFriend = suitable_data(document, 'Na zahradu')
    
        flatFriend = suitable_data(document, 'Do bytu')
        
        activeFriend = suitable_data(document, 'Pro aktivní majitele')

        color = get_table_data(document, 'Barva:')
        
        tattoo = get_table_data(document, 'Tetování:')
        
        neutered = get_table_data(document, 'Kastrovaný:')
        
        handicap = get_table_data(document, 'Handicapovaný:')
        
        find_location = get_table_data(document, 'Místo nálezu:')
        
        region = get_table_data(document, 'Region:')
        
        find_date = get_table_data(document, 'Datum nálezu:')
        
        actual_location = document.find('th', string='Akt. umístění:').find_next('td').find('a').get_text().strip()

        detailed_description = get_detailed_descr(document)
        
        dog = Dog(id=objid,name=name, status=status, gender=gender, age=age, size=size, breed=breed, cross_breed=cross_breed, childrenFriend=childrenFriend, catFriend=catFriend,
                dogFriend=dogFriend,begginerFriend=begginerFriend, gardenFriend=gardenFriend, flatFriend=flatFriend, activeFriend=activeFriend, color=color,
                tattoo=tattoo, neutered=neutered, handicap=handicap, find_location=find_location, region=region, find_date=find_date, actual_location=actual_location, detailed_description=detailed_description)

        print(dog)

        counter_notFound = 0

        with open(file_path, mode='a', encoding='utf-8') as file:
            attributes = vars(dog)
            file.write(';'.join(str(value) for value in attributes.values()) + '\n')


    except KeyboardInterrupt:
        raise

    except Exception as e:
        print(f'Error. Incomplete data. {e}')
        counter_notFound = 0
