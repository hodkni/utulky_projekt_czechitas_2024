import os

line_no = 0

with open('data_dogs.csv', mode='w', encoding='utf-8') as new_file:
    new_file.write('id;name;status;gender;age;size;breed;cross_breed;childrenFriend;catFriend;dogFriend;begginerFriend;gardenFriend;flatFriend;activeFriend;color;tattoo;neutered;handicap;find_location;region;find_date;actual_location;detailed_description\n')
    
    with open('projekt_utulky/data_shelter_dogs.csv', encoding='utf-8') as f:
        for line in f:
            if line_no != 0:
                parts = line.split(';')
                
                first_part = ';'.join(parts[:24])
                remaining = ''.join(parts[24:])
                
                new_file.write(first_part + remaining)
            
            line_no += 1
