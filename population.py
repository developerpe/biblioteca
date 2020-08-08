import os
import time
import django,random as rd
from random import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE","biblioteca.settings")

django.setup()

from apps.libro.models import Autor

vocals = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z',
              'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z']


def generate_string(length):
    if length <= 0:
        return False
    
    random_string = ''

    for i in range(length):
        decision = rd.choice(('vocals','consonants'))

        if random_string[-1:].lower() in vocals:
            decision = 'consonants'
        if random_string[-1:].lower() in consonants:
            decision = 'vocals'
        
        if decision == 'consonants':
            character = rd.choice(consonants)
        else:
            character = rd.choice(vocals)
        
        random_string += character
    
    return random_string


def generate_number():
    return int(random()*10+1)

def generate_autor(count):
    length = generate_number()
    for j in range(count):
        random_name = generate_string(length)
        random_last_name = generate_string((length+10))
        random_country = generate_string(length)
        random_description = generate_string((length*2))

        Autor.objects.create(
            nombre = random_name,
            apellidos=random_last_name,
            nacionalidad=random_country,
            descripcion=random_description
        )

if __name__=='__main__':    
    print("Inicio de creación de población")
    print("Por favor, espere. . . ")
    start = time.strftime("%c")
    print(f'Fecha y hora de inicio: {start}')
    generate_autor(2000)
    end = time.strftime("%c")
    print(f'Fecha y hora de finalización: {end}')
    print("Creación automática de datos finalizada!")

